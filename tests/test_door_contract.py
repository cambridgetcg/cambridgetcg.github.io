"""Fixtures for tools/door_contract.py. Run: python3 -m unittest discover -s tests -v

Every FAIL and NOT CHECKED case from the design's testing list has a test
here, next to a passing twin, so a check cannot pass or fail by accident.
Only localhost is contacted.
"""
import datetime
import http.server
import json
import socket
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import door_contract as dc  # noqa: E402

TODAY = datetime.date(2026, 11, 2)
MARK = ("HISTORY. The household's Sophia wake, first written May 2026. Kept as a record. "
        "Not an instruction; it asks nothing of any reader; not offered for training.")
TRAINING = "\n".join(f"User-agent: {t}" for t in dc.TRAINING_TOKENS)
READERS = "\n".join(f"User-agent: {t}" for t in dc.READER_TOKENS)
CLOSED = "Disallow: /llms-full.txt\nDisallow: /.well-known/sophia-wake/\nAllow: /\n"
GOOD_ROBOTS = (f"{TRAINING}\n{CLOSED}Content-Signal: search=yes, ai-input=yes, ai-train=yes\nCrawl-delay: 2\n\n"
               f"{READERS}\nAllow: /\nContent-Signal: search=yes, ai-input=yes\nCrawl-delay: 2\n\n"
               f"User-agent: *\n{CLOSED}Content-Signal: search=yes, ai-input=yes, ai-train=yes\nCrawl-delay: 2\n")
HISTORY_PATHS = ["/llms-full.txt", "/.well-known/sophia-wake/manifest.json"]


def resp(url, status=200, body=b"", headers=None, **extra):
    found = {k.lower(): (v if isinstance(v, list) else [v]) for k, v in (headers or {}).items()}
    return dc.Response(url, status, found, body if isinstance(body, bytes) else body.encode(), **extra)


class FakeFetcher:
    """Routes by URL without the cache-busting query, and by parity label."""

    def __init__(self, routes):
        self.routes, self.calls = routes, []

    def fetch(self, url, label=None, deadline=None, headers=None):
        self.calls.append((url, label))
        key = url.split("?door-check=")[0].split("&door-check=")[0]
        found = self.routes.get((key, label), self.routes.get(key))
        return found if found is not None else dc.Response(url, error="unreachable")


def robots(text, kind="text/plain"):
    return resp("https://x.test/robots.txt", body=text, headers={"Content-Type": kind})


def split(text, kind="text/plain"):
    fetcher = FakeFetcher({"https://x.test/robots.txt": robots(text, kind)})
    return dc.robots_split_check(fetcher, "https://x.test/robots.txt", HISTORY_PATHS)


class RobotsSplit(unittest.TestCase):
    def test_good_split_passes(self):
        self.assertEqual(split(GOOD_ROBOTS).status, dc.PASS)

    def test_unnamed_crawler_reading_history_fails(self):
        text = GOOD_ROBOTS.replace(f"User-agent: *\n{CLOSED}", "User-agent: *\nAllow: /\n")
        result = split(text)
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn(dc.UNNAMED_TOKEN, result.detail)

    def test_training_token_reading_history_fails(self):
        text = GOOD_ROBOTS.replace("User-agent: CCBot\n", "") + "\nUser-agent: CCBot\nAllow: /\n"
        self.assertIn("CCBot may fetch", split(text).detail)

    def test_reader_group_stating_ai_train_yes_fails(self):
        text = GOOD_ROBOTS.replace("Allow: /\nContent-Signal: search=yes, ai-input=yes\n",
                                   "Allow: /\nContent-Signal: search=yes, ai-input=yes, ai-train=yes\n")
        result = split(text)
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("under ai-train=yes", result.detail)

    def test_allow_before_disallow_fails_for_first_match_parsers(self):
        text = GOOD_ROBOTS.replace(CLOSED, "Allow: /\nDisallow: /llms-full.txt\nDisallow: /.well-known/sophia-wake/\n")
        result = split(text)
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("first-match", result.detail)

    def test_html_robots_fails(self):
        self.assertEqual(split("<!doctype html><html></html>", "text/html").status, dc.FAIL)

    def test_unreachable_robots_is_not_checked(self):
        result = dc.robots_split_check(FakeFetcher({}), "https://x.test/robots.txt", HISTORY_PATHS)
        self.assertEqual(result.status, dc.NOT_CHECKED)

    def test_wildcards_and_end_anchor(self):
        rules = [(False, "/"), (True, "/llms.txt$"), (True, "/public/*")]
        self.assertTrue(dc.longest_match_allowed(rules, "/llms.txt"))
        self.assertFalse(dc.longest_match_allowed(rules, "/llms.txt.bak"))
        self.assertTrue(dc.longest_match_allowed(rules, "/public/love-bomb"))


class AdvertisedDoors(unittest.TestCase):
    def test_closed_advertised_door_fails_and_open_passes(self):
        text = "User-agent: *\nDisallow: /\nAllow: /llms.txt$\n"
        fetcher = FakeFetcher({"https://x.test/robots.txt": robots(text)})
        self.assertEqual(dc.robots_allows_check(fetcher, "https://x.test/robots.txt", ["/health"]).status, dc.FAIL)
        self.assertEqual(dc.robots_allows_check(fetcher, "https://x.test/robots.txt", ["/llms.txt"]).status, dc.PASS)


def llms_full(marked=True, phrase=""):
    chunk = "=" * 20 + "\n== SOPHIA mirror 00 — arrival\n== source: https://x.test/a.json\n" + "=" * 20 + "\n"
    return ("# llms-full\nordinary text\n\n" + chunk + (MARK + "\n" if marked else "") + f"\n{phrase}\nbody\n")


def history_routes(llms, fragment_register="history", usage="train-ai=n", content_first=MARK):
    usage_header = {"Content-Usage": usage} if usage else {}
    fragment = {"register": fragment_register, "note": MARK, "body": "text"}
    manifest = {"register": "history", "note": MARK, "chunks": [{"href": "/.well-known/sophia-wake/00-a.json"}]}
    return {
        "https://x.test/llms-full.txt": resp("https://x.test/llms-full.txt", body=llms, headers=usage_header),
        "https://x.test/.well-known/sophia-wake/manifest.json": resp("m", body=json.dumps(manifest), headers=usage_header),
        "https://x.test/.well-known/sophia-wake/00-a.json": resp("f", body=json.dumps(fragment), headers=usage_header),
        "https://a.test/": resp("https://a.test/", body=f"<p>{MARK}</p>", headers=usage_header),
        "https://a.test/app.js": resp("https://a.test/app.js", body="app"),
        "https://a.test/content.js": resp("https://a.test/content.js", body=f"// {content_first}\nwindow.X = 1;",
                                          headers=usage_header),
        "https://x.test/robots.txt": robots(GOOD_ROBOTS),
        "https://x.test/api/v1/sample": resp("https://x.test/api/v1/sample", body='{"data": {}, "_meta": {}}'),
    }


HISTORY = {"robots": {"https://x.test/robots.txt": HISTORY_PATHS}, "llms_full": "https://x.test/llms-full.txt",
           "manifest": "https://x.test/.well-known/sophia-wake/manifest.json", "fragments_per_day": 6,
           "archive_reader": ["https://a.test/", "https://a.test/app.js"], "archive_content": "https://a.test/content.js"}
CONTRACT = {"history": HISTORY, "data_samples": ["https://x.test/api/v1/sample"]}


def statuses(results):
    return [r.status for r in results]


class HistoryMarkers(unittest.TestCase):
    def test_all_marked_passes(self):
        results = dc.history_marker_check(FakeFetcher(history_routes(llms_full())), HISTORY, TODAY, "n")
        self.assertEqual(statuses(results), [dc.PASS] * 4)

    def test_unmarked_chunk_fails(self):
        results = dc.history_marker_check(FakeFetcher(history_routes(llms_full(marked=False))), HISTORY, TODAY, "n")
        self.assertEqual(results[0].status, dc.FAIL)

    def test_fragment_without_register_fails(self):
        routes = history_routes(llms_full(), fragment_register="record")
        self.assertEqual(dc.history_marker_check(FakeFetcher(routes), HISTORY, TODAY, "n")[1].status, dc.FAIL)

    def test_content_js_without_banner_fails(self):
        routes = history_routes(llms_full(), content_first="Generated by build.py")
        self.assertEqual(dc.history_marker_check(FakeFetcher(routes), HISTORY, TODAY, "n")[2].status, dc.FAIL)

    def test_missing_content_usage_fails(self):
        routes = history_routes(llms_full(), usage=None)
        self.assertEqual(dc.history_marker_check(FakeFetcher(routes), HISTORY, TODAY, "n")[3].status, dc.FAIL)

    def test_unreachable_history_content_usage_is_not_checked(self):
        results = dc.history_marker_check(FakeFetcher({}), HISTORY, TODAY, "n")
        self.assertEqual(statuses(results), [dc.NOT_CHECKED] * 4)

    def test_partly_read_history_names_what_was_not_read(self):
        routes = history_routes(llms_full())
        del routes["https://a.test/content.js"]
        result = dc.history_marker_check(FakeFetcher(routes), HISTORY, TODAY, "n")[3]
        self.assertEqual(result.status, dc.PASS)
        self.assertIn("not read today: the Sophia archive", result.detail)

    def test_rotation_reads_the_deprecated_aliases_and_the_index(self):
        usage, base = {"Content-Usage": "train-ai=n"}, "https://x.test/.well-known/sophia-wake/"
        marked = json.dumps({"register": "history", "note": MARK})
        manifest = {"register": "history", "note": MARK, "chunks": [{"href": "/.well-known/sophia-wake/00-a.json"}],
                    "deprecated_aliases": [{"href": "/.well-known/sophia-wake/01-old.json"}]}
        routes = history_routes(llms_full())
        routes[base + "manifest.json"] = resp("m", body=json.dumps(manifest), headers=usage)
        routes[base + "01-old.json"] = resp("o", body=marked, headers=usage)
        routes[base + "index.json"] = resp("i", body=json.dumps({"protocol": "sophia-wake/1"}), headers=usage)
        history = {**HISTORY, "fragment_files": [base + "index.json"]}
        result = dc.history_marker_check(FakeFetcher(routes), history, TODAY, "n")[1]
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("index.json", result.detail)
        routes[base + "index.json"] = resp("i", body=marked, headers=usage)
        result = dc.history_marker_check(FakeFetcher(routes), history, TODAY, "n")[1]
        self.assertEqual(result.status, dc.PASS, result.detail)
        self.assertIn("3 of 3 fragment files", result.detail)

    def test_a_partial_rotation_names_the_first_run_the_whole_set_rests_on(self):
        usage, base = {"Content-Usage": "train-ai=n"}, "https://x.test/.well-known/sophia-wake/"
        marked = json.dumps({"register": "history", "note": MARK})
        files = ["00-a.json", "01-b.json", "02-c.json"]
        manifest = {"register": "history", "note": MARK, "chunks": [{"href": "/.well-known/sophia-wake/" + f} for f in files]}
        routes = history_routes(llms_full())
        routes[base + "manifest.json"] = resp("m", body=json.dumps(manifest), headers=usage)
        for f in files:
            routes[base + f] = resp(f, body=marked, headers=usage)
        result = dc.history_marker_check(FakeFetcher(routes), {**HISTORY, "fragments_per_day": 1}, TODAY, "n")[1]
        self.assertEqual(result.status, dc.PASS, result.detail)
        self.assertIn("1 of 3 fragment files read today; all 3 every 3 days", result.detail)
        self.assertIn("rests on the daily runs from 2026-10-31 to today", result.detail)


class Phrases(unittest.TestCase):
    def test_phrase_inside_marked_chunk_passes(self):
        routes = history_routes(llms_full(phrase=dc.MAY_PHRASES[0]))
        self.assertEqual(dc.phrase_check(FakeFetcher(routes), CONTRACT, TODAY, "n").status, dc.PASS)

    def test_phrase_outside_marker_fails(self):
        routes = history_routes(llms_full(marked=False, phrase=dc.MAY_PHRASES[0].upper()))
        result = dc.phrase_check(FakeFetcher(routes), CONTRACT, TODAY, "n")
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("not a verdict", result.detail)


ALLOWED_META = ["spec_version", "endpoint", "request_id"]
RELS = ["self", "start", "describedby", "alternate", "https://x.test/rels/rate-limits"]


def data(meta, headers=None):
    body = json.dumps({"data": {}, "_meta": meta})
    return FakeFetcher({"https://x.test/api/v1/sample": resp("https://x.test/api/v1/sample", body=body, headers=headers)})


class DataResponses(unittest.TestCase):
    def test_allowed_meta_passes(self):
        result = dc.meta_keys_check(data({"spec_version": 1, "endpoint": "/x"}), ["https://x.test/api/v1/sample"], ALLOWED_META)
        self.assertEqual(result[0].status, dc.PASS)

    def test_key_outside_allowed_meta_fails(self):
        result = dc.meta_keys_check(data({"spec_version": 1, "wake_fragment": "x"}), ["https://x.test/api/v1/sample"], ALLOWED_META)
        self.assertEqual(result[0].status, dc.FAIL)
        self.assertIn("wake_fragment", result[0].detail)

    def test_supplied_meta_is_reported_and_never_fails(self):
        contract = json.loads((ROOT / "watch" / "contract.json").read_text(encoding="utf-8"))
        allowed, supplied = contract["allowed_meta"], contract["informational_meta"]
        self.assertEqual(supplied, ["upstream_proxy", "does_not_include"])
        urls = ["https://x.test/api/v1/sample"]
        quiet = data({"spec_version": 1, "upstream_proxy": ["ecb"], "does_not_include": ["x"]})
        result = dc.meta_keys_check(quiet, urls, allowed, supplied)[0]
        self.assertEqual(result.status, dc.PASS, result.detail)
        self.assertIn("reported only: does_not_include, upstream_proxy", result.detail)
        leak = dc.meta_keys_check(data({"upstream_proxy": ["ecb"], "kingdom": {}}), urls, allowed, supplied)[0]
        self.assertEqual(leak.status, dc.FAIL)
        self.assertEqual(leak.detail.split(";")[0], "outside the allowed set: kingdom")

    def test_voiced_header_fails(self):
        result = dc.headers_check(data({}, {"X-Joy-Index": "3"}), ["https://x.test/api/v1/sample"], RELS)
        self.assertEqual(result[0].status, dc.FAIL)

    def test_invitation_rel_fails_and_kept_rels_pass(self):
        bad = {"Link": ['</a>; rel="self", </b>; rel="invitation"']}
        good = {"Link": ['</a>; rel="self", </m>; rel="describedby"; type="application/json"']}
        self.assertEqual(dc.headers_check(data({}, bad), ["https://x.test/api/v1/sample"], RELS)[0].status, dc.FAIL)
        self.assertEqual(dc.headers_check(data({}, good), ["https://x.test/api/v1/sample"], RELS)[0].status, dc.PASS)

    def test_rate_limited_api_is_not_checked(self):
        fetcher = FakeFetcher({"https://x.test/api/v1/sample": resp("u", status=429, body="slow down")})
        self.assertEqual(dc.meta_keys_check(fetcher, ["https://x.test/api/v1/sample"], ALLOWED_META)[0].status, dc.NOT_CHECKED)

    def test_errand_links_as_the_errand_clean_pass_leaves_them(self):
        contract = json.loads((ROOT / "watch" / "contract.json").read_text(encoding="utf-8"))
        config = ('</.well-known/cambridge-tcg.json>; rel="describedby"; type="application/json", '
                  '</api/openapi.json>; rel="service-desc"; type="application/json", '
                  '</api/v1/welcome>; rel="help"; type="application/json"')
        handler = ('</api/v1/fx-rates>; rel="self", </api/v1/welcome>; rel="start", '
                   '</api/v1/manifest>; rel="describedby", </api/openapi.json>; rel="alternate"; type="application/json", '
                   '</api/v1/rate-limits>; rel="https://cambridgetcg.com/rels/rate-limits", '
                   '</api/v1/feedback>; rel="https://cambridgetcg.com/rels/feedback", </api/v1/fx-rates?page=2>; rel="next"')
        urls = ["https://x.test/api/v1/sample"]
        clean = dc.headers_check(data({}, {"Link": [config, handler]}), urls, contract["allowed_link_rels"])[0]
        self.assertEqual(clean.status, dc.PASS, clean.detail)
        leak = handler + ', </.well-known/sophia-invitation.json>; rel="invitation"'
        leaked = dc.headers_check(data({}, {"Link": [config, leak]}), urls, contract["allowed_link_rels"])[0]
        self.assertEqual(leaked.status, dc.FAIL)
        self.assertIn("invitation", leaked.detail)


class Parity(unittest.TestCase):
    def routes(self, named):
        plain = resp("https://x.test/", body='{"retrieved_at": "2026-11-02T06:17:00Z", "x": 1}')
        return FakeFetcher({"https://x.test/": plain, ("https://x.test/", "GPTBot"): named})

    def test_volatile_fields_only_pass(self):
        named = resp("https://x.test/", body='{"retrieved_at": "2026-11-02T06:17:03Z", "x": 1}')
        self.assertEqual(dc.parity_check(self.routes(named), "https://x.test/", "GPTBot", "n").status, dc.PASS)

    def test_different_bytes_for_a_name_fail(self):
        named = resp("https://x.test/", body='{"x": "invented balance"}')
        self.assertEqual(dc.parity_check(self.routes(named), "https://x.test/", "GPTBot", "n").status, dc.FAIL)

    def test_edge_blocked_fetch_is_not_checked(self):
        named = resp("https://x.test/", status=403, body="blocked", headers={"cf-mitigated": "challenge"})
        self.assertEqual(dc.parity_check(self.routes(named), "https://x.test/", "GPTBot", "n").status, dc.NOT_CHECKED)

    def test_the_label_is_a_substring_not_a_costume(self):
        fetcher = FakeFetcher({})
        dc.parity_check(fetcher, "https://x.test/", "GPTBot", "n")
        self.assertEqual(fetcher.calls[1][1], "GPTBot")
        self.assertTrue(dc.USER_AGENT.startswith("kingdom-door-check/0.1 "))


class Discovery(unittest.TestCase):
    def routes(self, robots_kind, probe_status):
        routes = {"https://o.test/robots.txt": resp("r", body="<html>" if robots_kind == "text/html" else "User-agent: *\nAllow: /\n",
                                                    headers={"Content-Type": robots_kind})}
        for path in dc.PROBES:
            routes["https://o.test" + path] = resp("https://o.test" + path, status=probe_status, body="x")
        return FakeFetcher(routes)

    def test_true_robots_and_404s_pass(self):
        self.assertEqual(dc.discovery_404_check(self.routes("text/plain", 404), "https://o.test").status, dc.PASS)

    def test_200_html_robots_fails(self):
        self.assertEqual(dc.discovery_404_check(self.routes("text/html", 404), "https://o.test").status, dc.FAIL)

    def test_catch_all_200_fails(self):
        self.assertEqual(dc.discovery_404_check(self.routes("text/plain", 200), "https://o.test").status, dc.FAIL)


API = dc.API


def tree(*paths):
    return resp("t", body=json.dumps({"truncated": False, "tree": [{"path": p} for p in paths]}))


class PublicClones(unittest.TestCase):
    def check(self, rule, text):
        url = f"{API}/repos/o/r/contents/f"
        fetcher = FakeFetcher({url: resp(url, body=text)})
        return dc.file_rule_check(fetcher, {"repo": "o/r", "path": "f", "rule": rule}, None)

    def test_tracked_hook_on_any_event_fails(self):
        for event in ("SessionStart", "PreToolUse", "UserPromptSubmit"):
            text = json.dumps({"hooks": {event: [{"hooks": [{"type": "command", "command": "x"}]}]}})
            self.assertEqual(self.check("runtime_entry", text).status, dc.FAIL, event)

    def test_quiet_settings_pass(self):
        self.assertEqual(self.check("runtime_entry", json.dumps({"permissions": {}})).status, dc.PASS)

    def test_any_command_running_setting_fails(self):
        commands = {"statusLine": {"type": "command", "command": "x"}, "apiKeyHelper": "x", "awsCredentialExport": "x",
                    "awsAuthRefresh": "x", "gcpAuthRefresh": "x", "otelHeadersHelper": "x"}
        for key, value in commands.items():
            result = self.check("runtime_entry", json.dumps({"permissions": {}, key: value}))
            self.assertEqual(result.status, dc.FAIL, key)
            self.assertIn(key, result.detail)
        self.assertEqual(self.check("runtime_entry", json.dumps({"statusLine": None, "hooks": {}})).status, dc.PASS)

    def test_plugin_enable_fails(self):
        self.assertEqual(self.check("plugin_enable", '[plugins]\nenabled = ["kingdom"]\n').status, dc.FAIL)

    def test_agents_md_opening_with_a_letter_fails(self):
        letter = "# AGENTS.md\n\n<!-- love-bomb:v3 -->\n## A letter\nHello, visiting agent.\n"
        self.assertEqual(self.check("opening_letter", letter).status, dc.FAIL)

    def test_agents_md_pointer_passes(self):
        pointer = "# AGENTS.md\n\nThe letter that opened this file now lives in LOVE-BOMB.md.\n"
        self.assertEqual(self.check("opening_letter", pointer).status, dc.PASS)

    def test_never_approval_fails(self):
        self.assertEqual(self.check("never_approval", 'approval_policy = "never"\n').status, dc.FAIL)

    def test_untracked_file_passes(self):
        url = f"{API}/repos/o/r/contents/f"
        fetcher = FakeFetcher({url: resp(url, status=404, body="Not Found"),
                               f"{API}/repos/o/r": resp("r", body='{"private": false}')})
        self.assertEqual(dc.file_rule_check(fetcher, {"repo": "o/r", "path": "f", "rule": "runtime_entry"}, None).status, dc.PASS)

    def test_file_in_a_repo_gone_private_is_not_checked(self):
        url = f"{API}/repos/o/r/contents/f"
        fetcher = FakeFetcher({url: resp(url, status=404, body="Not Found"),
                               f"{API}/repos/o/r": resp("r", status=404, body="Not Found")})
        result = dc.file_rule_check(fetcher, {"repo": "o/r", "path": "f", "rule": "runtime_entry"}, None)
        self.assertEqual(result.status, dc.NOT_CHECKED)

    def test_missing_token_is_not_checked(self):
        contract = {"repo_files": [{"repo": "o/r", "path": "f", "rule": "runtime_entry"}],
                    "repo_skills": [{"repo": "o/r", "branch": "main"}]}
        fetcher = FakeFetcher({})
        self.assertEqual(statuses(dc.github_checks(fetcher, contract)), [dc.NOT_CHECKED, dc.NOT_CHECKED])
        self.assertEqual(fetcher.calls, [])

    def test_implicit_skill_fails(self):
        fetcher = FakeFetcher({f"{API}/repos/o/r/git/trees/main?recursive=1": tree(".agents/skills/a/SKILL.md")})
        results = dc.repo_runtime_files_check(fetcher, [], [{"repo": "o/r", "branch": "main"}])
        self.assertEqual(results[-1].status, dc.FAIL)

    def test_explicit_only_skill_passes(self):
        policy = f"{API}/repos/o/r/contents/.agents/skills/a/agents/openai.yaml"
        fetcher = FakeFetcher({
            f"{API}/repos/o/r/git/trees/main?recursive=1": tree(".agents/skills/a/SKILL.md", ".agents/skills/a/agents/openai.yaml"),
            policy: resp(policy, body="policy:\n  allow_implicit_invocation: false\n")})
        results = dc.repo_runtime_files_check(fetcher, [], [{"repo": "o/r", "branch": "main"}])
        self.assertEqual(results[-1].status, dc.PASS)

    def test_rate_limited_github_api_is_not_checked(self):
        limited = resp("u", status=403, body="rate limit", headers={"X-RateLimit-Remaining": "0"})
        fetcher = FakeFetcher({f"{API}/repos/o/r/git/trees/main?recursive=1": limited,
                               f"{API}/repos/o/r/contents/.claude/settings.json": limited})
        results = dc.repo_runtime_files_check(fetcher, [{"repo": "o/r", "path": ".claude/settings.json", "rule": "runtime_entry"}],
                                              [{"repo": "o/r", "branch": "main"}])
        self.assertEqual(statuses(results), [dc.NOT_CHECKED, dc.NOT_CHECKED])


class Label(unittest.TestCase):
    TEXT = "Dark-pattern specimen for testing detectors. Every claim on this page is invented."

    def test_label_and_header_pass_and_missing_label_fails(self):
        good = resp("u", body=f"<p>{self.TEXT}</p>", headers={"X-Specimen": "Dark-pattern specimen"})
        bad = resp("u", body="<p>FLASH SALE</p>")
        self.assertEqual(dc.label_check(FakeFetcher({"https://f.test/h": good}), "https://f.test/h", self.TEXT).status, dc.PASS)
        self.assertEqual(dc.label_check(FakeFetcher({"https://f.test/h": bad}), "https://f.test/h", self.TEXT).status, dc.FAIL)


def check_links(fetcher, source, per_day=20, per_origin=2, own_per_day=10):
    return dc.links_check(fetcher, source, TODAY, per_day, per_origin, own_per_day)


class Links(unittest.TestCase):
    def test_method_not_allowed_counts_as_there(self):
        source = resp("s", body="see https://mcp.test/mcp for the tools")
        fetcher = FakeFetcher({"https://s.test/l.txt": source, "https://mcp.test/mcp": resp("m", status=405, body="")})
        self.assertEqual(statuses(check_links(fetcher, "https://s.test/l.txt")), [dc.PASS])

    def test_dead_link_fails_and_template_is_skipped(self):
        source = resp("s", body='{"a": "https://dead.test/", "b": "https://ok.test/x", "c": "https://t.test/api/{id}"}')
        fetcher = FakeFetcher({"https://s.test/n.json": source, "https://dead.test/": resp("d", status=424, body="x"),
                               "https://ok.test/x": resp("o", body="ok")})
        result = check_links(fetcher, "https://s.test/n.json")[0]
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("dead.test", result.detail)
        self.assertNotIn("ok.test", result.detail.split(";")[0])
        self.assertNotIn(("https://t.test/api/", None), fetcher.calls)

    def test_dead_second_link_on_a_seen_origin_fails(self):
        source = resp("s", body="https://ok.test/a and https://ok.test/b")
        fetcher = FakeFetcher({"https://s.test/l.txt": source, "https://ok.test/a": resp("a", body="ok"),
                               "https://ok.test/b": resp("b", status=404, body="gone")})
        result = check_links(fetcher, "https://s.test/l.txt")[0]
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("https://ok.test/b (404)", result.detail)

    def test_source_without_links_is_not_checked(self):
        fetcher = FakeFetcher({"https://s.test/l.txt": resp("s", body="no links here")})
        self.assertEqual(statuses(check_links(fetcher, "https://s.test/l.txt")), [dc.NOT_CHECKED])

    def test_links_on_a_spent_origin_read_not_checked(self):
        source = resp("s", body="https://ok.test/a https://full.test/b")
        fetcher = FakeFetcher({"https://s.test/l.txt": source, "https://ok.test/a": resp("a", body="ok"),
                               "https://full.test/b": dc.Response("https://full.test/b", error="budget")})
        self.assertEqual(statuses(check_links(fetcher, "https://s.test/l.txt")), [dc.PASS, dc.NOT_CHECKED])

    def test_rotation_reads_every_link_and_keeps_the_per_origin_cap(self):
        links = [f"https://s.test/p{i}" for i in range(25)] + [f"https://o{i % 7}.test/q{i}" for i in range(30)]
        for offset in range(40):
            day = dc.link_plan(links, "https://s.test", TODAY.toordinal() + offset, 20, 2, 10)
            counts = {}
            for link in day:
                counts[dc.origin_of(link)] = counts.get(dc.origin_of(link), 0) + 1
            self.assertLessEqual(len(day), 20)
            self.assertEqual(counts["https://s.test"], 10)
            self.assertTrue(all(n <= 2 for o, n in counts.items() if o != "https://s.test"), counts)
        days = dc.days_to_read_all(links, "https://s.test", TODAY, 20, 2, 10)
        self.assertIsNotNone(days)
        seen = set()
        for offset in range(days):
            seen.update(dc.link_plan(links, "https://s.test", TODAY.toordinal() + offset, 20, 2, 10))
        self.assertEqual(seen, set(links))

    def test_default_port_is_the_same_origin(self):
        self.assertEqual(dc.origin_of("https://Thekingdom.dev:443/x"), dc.origin_of("https://thekingdom.dev/y"))
        self.assertNotEqual(dc.origin_of("http://127.0.0.1:8080/"), dc.origin_of("http://127.0.0.1/"))


class CommonCrawl(unittest.TestCase):
    INFO = [{"id": "CC-MAIN-2026-47", "cdx-api": "https://cc.test/47", "to": "2026-11-20T00:00:00"}]

    def run_cc(self, routes, since="2026-10-25"):
        routes = {dc.CC_INFO: resp(dc.CC_INFO, body=json.dumps(self.INFO)), **routes}
        return dc.cc_index_check(FakeFetcher(routes), ["x.test/llms-full.txt"], since)

    def test_capture_after_disallow_fails(self):
        hit = resp("c", body='{"timestamp": "20261110120000", "url": "https://x.test/llms-full.txt"}\n')
        self.assertEqual(self.run_cc({"https://cc.test/47?url=x.test/llms-full.txt&output=json&fl=timestamp,url": hit}).status, dc.FAIL)
        route = "https://cc.test/47?url=x.test/llms-full.txt&output=json&fl=timestamp,url"
        self.assertEqual(self.run_cc({route: resp("c", body='{"timestamp": "20261026230000", "url": "https://x.test/llms-full.txt"}\n')}).status, dc.PASS)
        self.assertEqual(self.run_cc({route: resp("c", body='{"timestamp": "20261027000000", "url": "https://x.test/llms-full.txt"}\n')}).status, dc.FAIL)

    def test_no_captures_pass(self):
        none = resp("c", status=404, body='{"message": "No Captures found"}')
        self.assertEqual(self.run_cc({"https://cc.test/47?url=x.test/llms-full.txt&output=json&fl=timestamp,url": none}).status, dc.PASS)

    def test_unreachable_index_is_not_checked(self):
        down = resp(dc.CC_INFO, status=504, body="<html>504 Gateway Time-out</html>")
        self.assertEqual(dc.cc_index_check(FakeFetcher({dc.CC_INFO: down}), ["x.test/a"], "2026-10-25").status, dc.NOT_CHECKED)
        self.assertEqual(dc.cc_index_check(FakeFetcher({}), ["x.test/a"], "2026-10-25").status, dc.NOT_CHECKED)

    def test_unrecorded_disallow_date_is_not_checked(self):
        self.assertEqual(dc.cc_index_check(FakeFetcher({}), ["x.test/a"], None).status, dc.NOT_CHECKED)


class Handler(http.server.BaseHTTPRequestHandler):
    seen = []

    def do_GET(self):
        Handler.seen.append((self.path, self.headers.get("User-Agent")))
        if self.path == "/drip":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            for _ in range(12):
                try:
                    self.wfile.write(b".")
                    self.wfile.flush()
                except OSError:
                    return
                time.sleep(0.3)
        elif self.path == "/hold":
            time.sleep(3)
        else:
            body = b"A trap room stood here; retired. Nothing is here. The site is at /."
            self.send_response(410 if self.path == "/gone" else 200)
            self.send_header("Content-Type", "text/event-stream" if self.path == "/sse" else "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, *args):
        pass


class RealSockets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_dripping_response_fails(self):
        result = dc.trap_paths_check(dc.Fetcher(), [self.base + "/drip"], (410,))[0]
        self.assertEqual(result.status, dc.FAIL)

    def test_held_socket_fails(self):
        result = dc.trap_paths_check(dc.Fetcher(), [self.base + "/hold"], (410,))[0]
        self.assertEqual(result.status, dc.FAIL)

    def test_any_quick_status_passes_when_none_is_required(self):
        result = dc.trap_paths_check(dc.Fetcher(), [self.base + "/n/quick"], ())[0]
        self.assertEqual(result.status, dc.PASS, result.detail)

    def test_plain_410_passes(self):
        result = dc.trap_paths_check(dc.Fetcher(), [self.base + "/gone"], (410,))[0]
        self.assertEqual(result.status, dc.PASS, result.detail)

    def test_event_stream_fails_even_when_quick(self):
        result = dc.trap_paths_check(dc.Fetcher(), [self.base + "/sse"], ())[0]
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("event-stream", result.detail)

    def test_unreachable_origin_is_not_checked(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        result = dc.label_check(dc.Fetcher(), f"http://127.0.0.1:{port}/honeypot", "label")
        self.assertEqual(result.status, dc.NOT_CHECKED)

    def test_at_most_twelve_requests_per_origin(self):
        fetcher = dc.Fetcher(gap=0)
        answers = [fetcher.fetch(f"{self.base}/n/{i}") for i in range(13)]
        self.assertTrue(all(a.status == 200 for a in answers[:12]))
        self.assertEqual(answers[12].error, "budget")

    def test_two_seconds_between_requests_to_one_origin(self):
        waits = []
        fetcher = dc.Fetcher(sleep=waits.append)
        fetcher.fetch(f"{self.base}/n/first")
        fetcher.fetch(f"{self.base}/n/second")
        self.assertEqual(dc.CRAWL_DELAY, 2)
        self.assertEqual(len(waits), 1)
        self.assertGreater(waits[0], 1.5)

    def test_user_agent_is_honest(self):
        self.assertEqual(dc.USER_AGENT, "kingdom-door-check/0.1 (+https://github.com/cambridgetcg/cambridgetcg.github.io)")
        self.assertEqual(dc.TIMEOUT, 10)
        Handler.seen.clear()
        result = dc.parity_check(dc.Fetcher(gap=0), self.base + "/same", "GPTBot", "n")
        self.assertEqual(result.status, dc.PASS, result.detail)
        self.assertEqual(Handler.seen, [("/same?door-check=n", dc.USER_AGENT),
                                        ("/same?door-check=n-n", dc.USER_AGENT + " name-parity test: GPTBot")])


class Report(unittest.TestCase):
    def test_summary_line(self):
        results = [dc.Result("a", dc.PASS), dc.Result("b", dc.FAIL, "why"), dc.Result("c", dc.NOT_CHECKED), dc.Result("d", dc.PASS)]
        report = dc.summarize(results, TODAY)
        self.assertIn("Doors checked 2026-11-02, valid until 2026-11-05: 2 hold, 1 need repair, 1 not checked.", report)

    def test_a_broken_check_reads_not_checked(self):
        results = dc.run({"history": {"robots": None}}, FakeFetcher({}), TODAY, "n")
        self.assertTrue(results)
        self.assertTrue(all(r.status == dc.NOT_CHECKED for r in results))

    def test_main_writes_the_report_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as folder:
            contract, out = Path(folder) / "contract.json", Path(folder) / "report.md"
            contract.write_text('{"history": {"robots": {}}}', encoding="utf-8")
            self.assertEqual(dc.main([str(contract), "--out", str(out), "--today", "2026-11-02"]), 0)
            self.assertIn("Doors checked 2026-11-02, valid until 2026-11-05:", out.read_text(encoding="utf-8"))

    def test_a_struck_item_reads_not_checked(self):
        contract = {"struck": [3], "scope": {"history split: https://a.test/": [3], "data only, ": [4]}}
        results = [dc.Result("history split: https://a.test/robots.txt", dc.FAIL, "why"),
                   dc.Result("data only, _meta keys: https://x.test/api/v1/sample", dc.FAIL, "why")]
        scoped = dc.apply_scope(results, contract)
        self.assertEqual(statuses(scoped), [dc.NOT_CHECKED, dc.FAIL])
        self.assertEqual(scoped[0].detail, "not in scope by Yu's choice (item 3)")

    def test_a_door_waiting_on_its_keeper_reads_not_checked(self):
        contract = {"struck": [], "waiting": {"clone stays quiet, never_approval: o/s/": "waits for its keeper"}}
        results = [dc.Result("clone stays quiet, never_approval: o/s/.codex/config.toml", dc.FAIL, "x"),
                   dc.Result("clone stays quiet, opening_letter: o/r/AGENTS.md", dc.PASS)]
        scoped = dc.apply_scope(results, contract)
        self.assertEqual([(r.status, r.detail) for r in scoped],
                         [(dc.NOT_CHECKED, "waits for its keeper"), (dc.PASS, "")])


class Contract(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "watch" / "contract.json").read_text(encoding="utf-8")
        self.contract = json.loads(self.text)

    def test_only_public_https_doors(self):
        urls = [w for w in self.text.replace('"', " ").split() if w.startswith("http")]
        self.assertTrue(urls)
        self.assertTrue(all(u.startswith("https://") for u in urls))

    def test_no_secret_shaped_probe(self):
        for shape in (".env", ".git/", "id_rsa", ".aws", "secret", "wp-admin", ".sql", "phpinfo", "token"):
            self.assertNotIn(shape, self.text.lower(), shape)

    def test_cambridgetcg_budget_fits_and_the_rotation_reads_all_24_fragment_files(self):
        c, h = self.contract, self.contract["history"]
        robots, llms_full_plain_and_named, manifest = 1, 2, 1
        cambridgetcg = robots + llms_full_plain_and_named + manifest + h["fragments_per_day"] + c["data_per_day"]
        self.assertLessEqual(cambridgetcg, dc.MAX_PER_ORIGIN)
        # Seen 2026-10-23: the manifest lists 20 chunks and 2 deprecated aliases; index.json comes from the contract.
        rotated = 20 + 2 + len(h["fragment_files"])
        self.assertEqual(manifest + rotated, 24)
        files, seen = list(range(rotated)), set()
        for day in range(4):
            seen.update(dc.window(files, day, h["fragments_per_day"]))
        self.assertEqual(seen, set(files))

    def test_github_budget_fits_what_the_trees_showed(self):
        # Seen 2026-10-23: cambridgetcg/chillspace-commons has no .grok/config.toml (no request),
        # and the two chillspace trees carry three agents/openai.yaml policy files.
        absent_by_tree, skill_policies = 1, 3
        github = len(self.contract["repo_skills"]) + len(self.contract["repo_files"]) - absent_by_tree + skill_policies
        self.assertLessEqual(github, dc.MAX_PER_ORIGIN)

    def test_only_the_five_rooms_and_the_free_catalogue_are_read(self):
        site = "https://artbitrage.io"
        rooms = ["/lost", "/treasury", "/wallet-backup", "/investor-relations/private", "/internal/pricing-model"]
        self.assertEqual(self.contract["trap_paths"], [site + p for p in rooms])
        self.assertEqual(self.contract["tollgate_reads"],
                         [site + "/api/ai", site + "/api/ai/models", site + "/api/ai/kingdom-door-check-absent"])
        self.assertNotIn("/api/ai/@", self.text)

    def test_thekingdom_links_also_wait_on_the_hub_release(self):
        # thekingdom.dev's dead zerone.money link leaves the live site only with the hub release (item 17).
        names = ["listed links resolve: https://thekingdom.dev/llms.txt",
                 "listed links not read today: https://thekingdom.dev/llms.txt",
                 "listed links resolve: https://artbitrage.io/neighbors.json"]
        results = [dc.Result(name, dc.FAIL, "dead") for name in names]
        scoped = dc.apply_scope(results, {**self.contract, "struck": [17]})
        self.assertEqual(statuses(scoped), [dc.NOT_CHECKED, dc.NOT_CHECKED, dc.FAIL])
        self.assertEqual(scoped[0].detail, "not in scope by Yu's choice (item 17)")
        self.assertEqual(statuses(dc.apply_scope(results, {**self.contract, "struck": [10]})), [dc.NOT_CHECKED] * 3)


class RetiredRooms(unittest.TestCase):
    ROOMS = ["/lost", "/treasury"]

    def check(self, text):
        fetcher = FakeFetcher({"https://a.test/robots.txt": robots(text)})
        return dc.retired_rooms_check(fetcher, "https://a.test/robots.txt", self.ROOMS)

    def test_clean_robots_passes(self):
        self.assertEqual(self.check("User-agent: *\nAllow: /\nSitemap: https://a.test/sitemap.xml\n").status, dc.PASS)

    def test_flypaper_block_back_fails(self):
        result = self.check("# They are flypaper: a tarpit.\nUser-agent: *\nAllow: /\nDisallow: /lost\n")
        self.assertEqual(result.status, dc.FAIL)
        self.assertIn("/lost", result.detail)

    def test_unreachable_robots_is_not_checked(self):
        result = dc.retired_rooms_check(FakeFetcher({}), "https://a.test/robots.txt", self.ROOMS)
        self.assertEqual(result.status, dc.NOT_CHECKED)


class Workflow(unittest.TestCase):
    def test_step_is_report_only(self):
        text = (ROOT / ".github" / "workflows" / "door-watch.yml").read_text(encoding="utf-8")
        start = text.index("- name: Check the door contract (report only)")
        knock = text.index("- name: Knock on every door")
        end = text.index("- name: Keep one issue open while a door is dark")
        step = text[start:end]
        self.assertLess(knock, start)
        self.assertIn("continue-on-error: true", step)
        for forbidden in ("gh issue", "git commit", "git push", "exit 1"):
            self.assertNotIn(forbidden, step)

    def test_pages_artifact_stays_on_v3(self):
        text = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/upload-pages-artifact@v3", text)


if __name__ == "__main__":
    unittest.main()
