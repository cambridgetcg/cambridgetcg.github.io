#!/usr/bin/env python3
"""Check, from outside, the promises the estate's public doors make.

    python3 tools/door_contract.py watch/contract.json [--out FILE] [--today YYYY-MM-DD] [--cc]

Report only. Each item reads PASS, FAIL or NOT CHECKED. An unreachable
origin, a fetch our own edge blocks, a rate-limited API or an unreachable
index reads NOT CHECKED, never PASS. The script always exits 0: it never
fails the job, opens no issue and commits nothing.

Python standard library only. At most 12 requests per origin, at least 2 s
between requests to one origin (Crawl-delay: 2), a 10 s timeout, and an
honest User-Agent. The name-parity test carries the token it tests as a
labelled substring instead of wearing it. It checks only what a stranger sees
in one fetch; nothing security-shaped runs here. It is the owner's monitor:
it reads the household's own history paths on purpose, as their keeper.
Items Yu left out (contract "struck") and doors that wait on their keeper
(contract "waiting") read NOT CHECKED.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import secrets
import socket
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, field

USER_AGENT = "kingdom-door-check/0.1 (+https://github.com/cambridgetcg/cambridgetcg.github.io)"
TIMEOUT = 10
MAX_PER_ORIGIN = 12
CRAWL_DELAY = 2.0
VALID_DAYS = 3
# The first scheduled run with this check: no daily run, and so no span of runs, starts earlier.
FIRST_RUN = datetime.date(2026, 10, 27)
TRAP_SECONDS = 1.0
READ_CAP = 2_000_000
PASS, FAIL, NOT_CHECKED = "PASS", "FAIL", "NOT CHECKED"

TRAINING_TOKENS = ("GPTBot", "ClaudeBot", "CCBot", "Meta-ExternalAgent", "Amazonbot",
                   "Bytespider", "Google-Extended", "Applebot-Extended")
UNNAMED_TOKEN = "kingdom-unnamed-crawler"
READER_TOKENS = ("Googlebot", "Bingbot", "Applebot", "DuckDuckBot", "OAI-SearchBot",
                 "Claude-SearchBot", "PerplexityBot", "Claude-User", "ChatGPT-User",
                 "Perplexity-User", "ia_archiver", "archive.org_bot")
PARITY_TOKENS = TRAINING_TOKENS + READER_TOKENS
MAY_PHRASES = ("you are sophia", "address him: daddy", "the universe is ours",
               "we are one", "established fact", "creator-principle")
VOICED_HEADERS = ("x-sophia-says", "x-joy-index")
LETTER_SIGNS = ("<!-- love-bomb:", "you are loved")
# Settings keys besides hooks that make a clone run a command: statusLine, and every *Helper,
# *Export or *Refresh key (apiKeyHelper, awsCredentialExport, awsAuthRefresh, ...).
COMMAND_KEYS = ("statusLine",)
COMMAND_KEY_ENDINGS = ("Helper", "Export", "Refresh")
PROBES = ("/.well-known/kingdom-door-check-absent", "/kingdom-door-check-absent.txt",
          "/kingdom-door-check-absent.json", "/kingdom-door-check-absent.xml")
API = "https://api.github.com"
RAW = {"Accept": "application/vnd.github.raw+json"}
CC_INFO = "https://index.commoncrawl.org/collinfo.json"
CHUNK_HEAD = re.compile(r"^== SOPHIA mirror \d+")
MARKER = re.compile(r"HISTORY\.[\s\S]{0,600}?(?i:not offered for training)")
SKILL = re.compile(r"^\.agents/skills/([^/]+)/SKILL\.md$")
EXPLICIT = re.compile(r"^\s*allow_implicit_invocation:\s*false\s*$", re.M)
URL_IN_TEXT = re.compile(r"https?://[^\s\"'<>()\[\]{}`|\\^]+")
VOLATILE = (
    re.compile(rb"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?"),
    re.compile(rb"req_[0-9a-f-]+"),
    re.compile(rb"door-check=[0-9a-z-]+"),
    re.compile(rb'nonce="[^"]*"'),
    re.compile(rb'"(?:request_id|retrieved_at|generated_at|served_at)"\s*:\s*"[^"]*"'),
    re.compile(rb"\s+"),
)
NEVER_CHECKED = (
    "whether any lab trained on the August copy (for good)",
    "whether an outside agent ever met the hooks (for good)",
    "whether organic text shapes a model (for good)",
    "the edge configuration (until access exists)",
    "how verified bots are treated (until access exists)",
    "AI-referred humans (until access exists)",
    "the MCP handshake (until access exists)",
    "the /api/ai routes that run a model (read once by hand; no public check calls a paid route)",
)


@dataclass
class Result:
    name: str
    status: str
    detail: str = ""


@dataclass
class Response:
    url: str
    status: int | None = None
    headers: dict = field(default_factory=dict)
    body: bytes = b""
    elapsed: float = 0.0
    error: str | None = None
    cut: bool = False

    def header(self, name):
        values = self.headers.get(name.lower())
        return ", ".join(values) if values else None

    def text(self):
        return self.body.decode("utf-8", "replace")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class _MarkConnected:
    """Notes on the request once its connection (TCP, and TLS for https) is up, so a timeout
    before that reads as an unreachable origin and only a timeout after it as a held socket."""

    def do_open(self, http_class, req, **http_conn_args):
        class Marked(http_class):
            def connect(self):
                super().connect()
                req.door_check_connected = True
        return super().do_open(Marked, req, **http_conn_args)


class _HTTPHandler(_MarkConnected, urllib.request.HTTPHandler):
    pass


class _HTTPSHandler(_MarkConnected, urllib.request.HTTPSHandler):
    pass


def _timeout_kind(request):
    return "timeout" if getattr(request, "door_check_connected", False) else "connect timeout"


def origin_of(url):
    parts = urllib.parse.urlsplit(url)
    scheme, host = parts.scheme.lower(), (parts.hostname or "").lower()
    try:
        port = parts.port
    except ValueError:
        port = None
    default = {"https": 443, "http": 80}.get(scheme)
    return f"{scheme}://{host}" + (f":{port}" if port and port != default else "")


def bust(url, nonce):
    return url + ("&" if "?" in url else "?") + f"door-check={nonce}"


class Fetcher:
    """GETs with a per-origin budget, at least `gap` seconds apart on one origin
    (Crawl-delay: 2). Redirects count as requests."""

    def __init__(self, token=None, clock=time.monotonic, timeout=TIMEOUT, budget=MAX_PER_ORIGIN,
                 gap=CRAWL_DELAY, sleep=time.sleep):
        self.token, self.clock, self.timeout, self.budget = token, clock, timeout, budget
        self.gap, self.sleep, self.last = gap, sleep, {}
        self.counts, self.memo = {}, {}
        self.opener = urllib.request.build_opener(_NoRedirect, _HTTPHandler, _HTTPSHandler)

    def fetch(self, url, label=None, deadline=None, headers=None):
        key = (url, tuple(sorted((headers or {}).items())))
        if label is None and deadline is None and key in self.memo:
            return self.memo[key]
        response = self._follow(url, label, deadline, headers or {})
        if label is None and deadline is None:
            self.memo[key] = response
        return response

    def _follow(self, url, label, deadline, headers):
        for _ in range(4):
            origin = origin_of(url)
            if self.counts.get(origin, 0) >= self.budget:
                return Response(url, error="budget")
            self.counts[origin] = self.counts.get(origin, 0) + 1
            wait = self.gap - (self.clock() - self.last[origin]) if origin in self.last else 0
            if wait > 0:
                self.sleep(wait)
            response = self._once(url, label, deadline, headers)
            self.last[origin] = self.clock()
            location = response.header("location")
            if response.status in (301, 302, 303, 307, 308) and location:
                url = urllib.parse.urljoin(url, location)
                continue
            return response
        return Response(url, error="redirects")

    def _once(self, url, label, deadline, headers):
        agent = USER_AGENT + (f" name-parity test: {label}" if label else "")
        request_headers = {"User-Agent": agent, **headers}
        if self.token and origin_of(url) == API:
            request_headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=request_headers)
        timeout = self.timeout if deadline is None else min(self.timeout, deadline)
        started = self.clock()
        try:
            stream = self.opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            stream = error
        except urllib.error.URLError as error:
            kind = _timeout_kind(request) if isinstance(error.reason, (TimeoutError, socket.timeout)) else "unreachable"
            return Response(url, error=kind, elapsed=self.clock() - started)
        except (TimeoutError, socket.timeout):
            return Response(url, error=_timeout_kind(request), elapsed=self.clock() - started)
        except OSError:
            return Response(url, error="unreachable", elapsed=self.clock() - started)
        try:
            found = {}
            for name, value in stream.headers.items():
                found.setdefault(name.lower(), []).append(value)
            body, state = _read(stream, started, deadline, self.clock)
            status = stream.getcode()
        finally:
            stream.close()
        error = "timeout" if state == "timeout" else ("unreachable" if state == "broken" else None)
        return Response(url, status, found, body, self.clock() - started, error, state == "cut")


def _read(stream, started, deadline, clock):
    chunks, size = [], 0
    read = getattr(stream, "read1", None) or stream.read
    while size < READ_CAP:
        if deadline is not None and clock() - started > deadline:
            return b"".join(chunks), "cut"
        try:
            chunk = read(65536)
        except (TimeoutError, socket.timeout):
            return b"".join(chunks), "timeout"
        except (OSError, ValueError, EOFError):
            return b"".join(chunks), "broken"
        if not chunk:
            break
        chunks.append(chunk)
        size += len(chunk)
    return b"".join(chunks), "done"


def edge_blocked(response):
    if response.status not in (403, 429, 503):
        return False
    if response.header("cf-mitigated") or response.header("x-vercel-mitigated"):
        return True
    head = response.body[:4096].lower()
    return b"cloudflare" in head and any(s in head for s in (b"ray id", b"attention required", b"just a moment"))


def rate_limited(response):
    if response.status == 429:
        return True
    return response.status == 403 and response.header("x-ratelimit-remaining") == "0"


def unavailable(response):
    """Why a response cannot be judged, or None when it can."""
    if response.error == "budget":
        return "request budget for this origin reached"
    if response.error == "timeout":
        return "no answer within the timeout"
    if response.error:
        return f"unreachable ({response.error})"
    if edge_blocked(response):
        return "blocked by our own edge"
    if rate_limited(response):
        return "rate-limited"
    if response.status >= 500:
        return f"server error {response.status}"
    return None


def window(items, index, count):
    """The index-th window of count items, wrapping; consecutive windows cover every item."""
    items = list(items)
    if len(items) <= count:
        return items
    start = (index * count) % len(items)
    return [items[(start + i) % len(items)] for i in range(count)]


def rotate(items, today, count):
    return window(items, today.toordinal(), count)


def todays_samples(contract, today):
    samples = contract["data_samples"]
    return rotate(samples, today, contract.get("data_per_day", len(samples)))


def strip_tags(text):
    return re.sub(r"<[^>]+>", " ", text)


def marker_in(text):
    return MARKER.search(strip_tags(text)) is not None


def content_usage_ok(response):
    return "train-ai=n" in (response.header("content-usage") or "").replace(" ", "").lower()


def is_robots_file(response):
    kind = (response.header("content-type") or "").lower()
    return response.status == 200 and kind.startswith("text/plain") and not response.body.lstrip().startswith(b"<")


# ---------------------------------------------------------------- robots.txt

def parse_signal(value):
    signal = {}
    for part in value.split(","):
        key, _, setting = part.partition("=")
        if key.strip():
            signal[key.strip().lower()] = setting.strip().lower()
    return signal


def parse_groups(text):
    groups, current, in_rules = [], None, True
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if in_rules or current is None:
                current = {"agents": [], "rules": [], "signals": {}}
                groups.append(current)
                in_rules = False
            current["agents"].append(value.lower())
        elif current is not None:
            in_rules = True
            if key in ("allow", "disallow") and value:
                current["rules"].append((key == "allow", value))
            elif key == "content-signal":
                current["signals"].update(parse_signal(value))
    return groups


def select_rfc(groups, token):
    """RFC 9309: every group naming the token exactly, else every '*' group."""
    token = token.lower()
    chosen = [g for g in groups if token in g["agents"]] or [g for g in groups if "*" in g["agents"]]
    merged = {"rules": [], "signals": {}}
    for group in chosen:
        merged["rules"].extend(group["rules"])
        merged["signals"].update(group["signals"])
    return merged


def select_first(groups, token):
    """Older parsers (Python 3.12 robotparser): first group whose name is a substring."""
    token = token.lower()
    for group in groups:
        if any(agent != "*" and agent in token for agent in group["agents"]):
            return group
    return next((g for g in groups if "*" in g["agents"]), {"rules": [], "signals": {}})


def _pattern_matches(pattern, path):
    anchored = pattern.endswith("$")
    body = pattern[:-1] if anchored else pattern
    regex = "".join(".*" if c == "*" else re.escape(c) for c in body) + ("$" if anchored else "")
    return re.match(regex, path) is not None


def longest_match_allowed(rules, path):
    best, allow = -1, True
    for is_allow, pattern in rules:
        if _pattern_matches(pattern, path) and (len(pattern) > best or (len(pattern) == best and is_allow)):
            best, allow = len(pattern), is_allow
    return allow


def first_match_allowed(rules, path):
    for is_allow, pattern in rules:
        if path.startswith(pattern):
            return is_allow
    return True


def verdicts(text, token, path):
    """May the token fetch the path? (RFC 9309, first-match, this Python's robotparser)."""
    groups = parse_groups(text)
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(text.splitlines())
    return (longest_match_allowed(select_rfc(groups, token)["rules"], path),
            first_match_allowed(select_first(groups, token)["rules"], path),
            parser.can_fetch(token, "https://robots.invalid" + path))


def robots_split_check(fetcher, robots_url, paths, nonce=None):
    name = f"history split: {robots_url}"
    response = fetcher.fetch(bust(robots_url, nonce) if nonce else robots_url)
    why = unavailable(response)
    if why:
        return Result(name, NOT_CHECKED, why)
    if not is_robots_file(response):
        return Result(name, FAIL, f"not a robots file ({response.status}, {response.header('content-type')})")
    text, groups, problems = response.text(), parse_groups(response.text()), []
    for token in TRAINING_TOKENS + (UNNAMED_TOKEN,) + READER_TOKENS:
        reader = token in READER_TOKENS
        for path in paths:
            seen = verdicts(text, token, path)
            if not reader and any(seen):
                problems.append(f"{token} may fetch {path} {_which(seen)}")
            if reader and not all(seen):
                problems.append(f"{token} cannot read {path} {_which(seen, False)}")
            if any(seen) and select_rfc(groups, token)["signals"].get("ai-train") == "yes":
                problems.append(f"{token} may fetch {path} under ai-train=yes")
    if problems:
        return Result(name, FAIL, "; ".join(sorted(set(problems))[:8]))
    version = ".".join(map(str, sys.version_info[:2]))
    return Result(name, PASS, f"training and unnamed crawlers stay out of {len(paths)} paths; "
                              f"readers may read; RFC 9309, first-match and Python {version} agree")


def _which(seen, value=True):
    names = ("RFC 9309", "first-match", "robotparser")
    return "(" + ", ".join(n for n, v in zip(names, seen) if v is value) + ")"


def robots_allows_check(fetcher, robots_url, paths, nonce=None):
    name = f"advertised doors allowed: {robots_url}"
    response = fetcher.fetch(bust(robots_url, nonce) if nonce else robots_url)
    why = unavailable(response)
    if why:
        return Result(name, NOT_CHECKED, why)
    if not is_robots_file(response):
        return Result(name, FAIL, f"not a robots file ({response.status})")
    rules = select_rfc(parse_groups(response.text()), UNNAMED_TOKEN)["rules"]
    closed = [p for p in paths if not longest_match_allowed(rules, p)]
    if closed:
        return Result(name, FAIL, "disallowed for every crawler: " + ", ".join(closed))
    return Result(name, PASS, f"{len(paths)} advertised paths allowed (RFC 9309 matching)")


def retired_rooms_check(fetcher, robots_url, rooms, nonce=None):
    name = f"retired trap rooms stay out of robots.txt: {robots_url}"
    response = fetcher.fetch(bust(robots_url, nonce) if nonce else robots_url)
    why = unavailable(response)
    if why:
        return Result(name, NOT_CHECKED, why)
    if not is_robots_file(response):
        return Result(name, FAIL, f"not a robots file ({response.status})")
    text = response.text()
    rules = [rule for group in parse_groups(text) for rule in group["rules"]]
    listed = [room for room in rooms if (False, room) in rules]
    words = sorted({w for w in ("flypaper", "tarpit") if w in text.lower()})
    problems = (["Disallow again for " + ", ".join(listed)] if listed else [])
    problems += (["mentions " + ", ".join(words)] if words else [])
    if problems:
        return Result(name, FAIL, "; ".join(problems))
    return Result(name, PASS, f"{len(rooms)} rooms unlisted, no tarpit text")


# ---------------------------------------------------------- history records

def outside_markers(text):
    lines = text.splitlines()
    heads = [i for i, line in enumerate(lines) if CHUNK_HEAD.match(line)]
    if not heads:
        return text
    keep = lines[:heads[0]]
    bounds = heads + [len(lines)]
    for start, end in zip(bounds, bounds[1:]):
        if not marker_in("\n".join(lines[start + 1:start + 7])):
            keep.extend(lines[start:end])
    return "\n".join(keep)


def is_history_json(response):
    try:
        data = json.loads(response.text())
    except ValueError:
        return False
    return isinstance(data, dict) and data.get("register") == "history" and marker_in(response.text())


def history_fragments(fetcher, history, today):
    """The manifest, today's fragment files by rotation, and how many files the rotation covers:
    every chunk and deprecated alias the manifest lists, plus the contract's fragment_files (index.json)."""
    manifest = fetcher.fetch(history["manifest"])
    if unavailable(manifest) or manifest.status != 200:
        return manifest, [], 0
    try:
        listing = json.loads(manifest.text())
        entries = listing.get("chunks", []) + listing.get("deprecated_aliases", [])
    except (ValueError, AttributeError, TypeError):
        return manifest, [], 0
    hrefs = [urllib.parse.urljoin(history["manifest"], c["href"]) for c in entries if isinstance(c, dict) and c.get("href")]
    hrefs += [url for url in history.get("fragment_files", []) if url not in hrefs]
    picked = rotate(hrefs, today, history["fragments_per_day"])
    return manifest, [(url, fetcher.fetch(url)) for url in picked], len(hrefs)


def history_marker_check(fetcher, history, today, nonce):
    results, headerless, tally = [], [], {"read": 0, "unread": []}
    llms = fetcher.fetch(bust(history["llms_full"], nonce))
    name = "history marker on every SOPHIA chunk: " + history["llms_full"]
    why = unavailable(llms)
    if why:
        results.append(Result(name, NOT_CHECKED, why))
        tally["unread"].append(history["llms_full"])
    else:
        tally["read"] += 1
        headerless += [] if content_usage_ok(llms) else [history["llms_full"]]
        lines = llms.text().splitlines()
        heads = [i for i, line in enumerate(lines) if CHUNK_HEAD.match(line)]
        bare = [lines[i] for i in heads if not marker_in("\n".join(lines[i + 1:i + 7]))]
        if not heads:
            results.append(Result(name, FAIL, "no SOPHIA chunks found"))
        elif bare:
            results.append(Result(name, FAIL, f"{len(bare)} of {len(heads)} chunks lack the marker, first: {bare[0][:60]}"))
        else:
            results.append(Result(name, PASS, f"{len(heads)} chunks marked"))
    manifest, fragments, total = history_fragments(fetcher, history, today)
    name = "history register on the sophia-wake manifest and today's fragments"
    why = unavailable(manifest) or next((unavailable(r) for _, r in fragments if unavailable(r)), None)
    if why:
        results.append(Result(name, NOT_CHECKED, why))
        tally["unread"].append("the sophia-wake manifest and today's fragments")
    else:
        tally["read"] += 1 + len(fragments)
        headerless += [r.url for r in [manifest] + [r for _, r in fragments] if not content_usage_ok(r)]
        bare = [url for url, r in [(history["manifest"], manifest)] + fragments if not is_history_json(r)]
        every = -(-total // history["fragments_per_day"]) if total else 0
        first = max(today - datetime.timedelta(days=every - 1), FIRST_RUN) if every > 1 else None
        full = FIRST_RUN + datetime.timedelta(days=every - 1) if every > 1 else None
        detail = (f"manifest and {len(fragments)} of {total} fragment files read today; all {total} every {every} days"
                  + (f", so for the whole set this line rests on the daily runs from {first.isoformat()} to today" if first else "")
                  + (f"; the first full round ends {full.isoformat()}" if first and today < full else ""))
        results.append(Result(name, FAIL, f"{len(bare)} unmarked, first: {bare[0]}") if bare else Result(name, PASS, detail))
    results.append(_archive_check(fetcher, history, nonce, headerless, tally))
    name = "history responses send Content-Usage: train-ai=n"
    unread = f"; not read today: {', '.join(tally['unread'])}" if tally["unread"] else ""
    if not tally["read"]:
        results.append(Result(name, NOT_CHECKED, "no history response could be read"))
    elif headerless:
        results.append(Result(name, FAIL, "missing on " + ", ".join(headerless[:4]) + unread))
    else:
        results.append(Result(name, PASS, f"on all {tally['read']} history responses read{unread}"))
    return results


def _archive_check(fetcher, history, nonce, headerless, tally):
    name = "history banner in the Sophia archive reader and first line of content.js"
    readers = [fetcher.fetch(bust(history["archive_reader"][0], nonce))]
    readers += [fetcher.fetch(url) for url in history["archive_reader"][1:]]
    content = fetcher.fetch(history["archive_content"])
    why = next((unavailable(r) for r in readers + [content] if unavailable(r)), None)
    if why:
        tally["unread"].append("the Sophia archive")
        return Result(name, NOT_CHECKED, why)
    tally["read"] += 2
    headerless += [r.url for r in (readers[0], content) if not content_usage_ok(r)]
    first = next((line for line in content.text().splitlines() if line.strip()), "")
    problems = ([] if any(marker_in(r.text()) for r in readers) else ["reader shows no banner"])
    problems += ([] if marker_in(first) else ["content.js does not open with the banner"])
    return Result(name, FAIL, "; ".join(problems)) if problems else Result(name, PASS, "banner present")


def phrase_hits(texts):
    hits = []
    for url, text in texts:
        lowered = text.lower()
        hits += [f"{url}: '{p}'" for p in MAY_PHRASES if p in lowered]
    return hits


def phrase_check(fetcher, contract, today, nonce):
    """A hit reads FAIL whatever else was read. Without a hit, the item reads PASS only when
    every body was read; any body that could not be read makes it NOT CHECKED, named."""
    name = "May-register phrases only inside history markers"
    history, texts, unread = contract["history"], [], []

    def readable(label, response):
        why = unavailable(response)
        if why:
            unread.append(f"{label} ({why})")
        return why is None

    llms = fetcher.fetch(bust(history["llms_full"], nonce))
    if readable(history["llms_full"], llms):
        texts.append((history["llms_full"], outside_markers(llms.text())))
    reads = [(url, url) for url in todays_samples(contract, today)] + [(url, bust(url, nonce)) for url in history["robots"]]
    for url, target in reads:
        response = fetcher.fetch(target)
        if readable(url, response):
            texts.append((url, response.text()))
    manifest, fragments, total = history_fragments(fetcher, history, today)
    if readable(history["manifest"] + " and today's fragment files", manifest) and (manifest.status != 200 or not total):
        unread.append(f"today's fragment files (the manifest gave no list, status {manifest.status})")
    for url, response in fragments:
        if readable(url, response) and not is_history_json(response):
            texts.append((url, response.text()))
    content = fetcher.fetch(history["archive_content"])
    if readable(history["archive_content"], content) and not marker_in(
            next((l for l in content.text().splitlines() if l.strip()), "")):
        texts.append((history["archive_content"], content.text()))
    gap = ""
    if unread:
        gap = "not read today: " + ", ".join(unread[:6]) + (f" and {len(unread) - 6} more" if len(unread) > 6 else "")
    hits = phrase_hits(texts)
    if hits:
        return Result(name, FAIL, "; ".join(hits[:6]) + " (a reading item for Ai, not a verdict)" + (f"; {gap}" if gap else ""))
    if unread:
        return Result(name, NOT_CHECKED, f"no hit in {len(texts)} bodies read; {gap}")
    return Result(name, PASS, f"no hit in {len(texts)} bodies read")


# ---------------------------------------------------------- data responses

def meta_keys_check(fetcher, urls, allowed, informational=()):
    """Keys outside `allowed` fail; `informational` keys (supplied by the endpoint) are named, never failed."""
    results = []
    for url in urls:
        name = f"data only, _meta keys: {url}"
        response = fetcher.fetch(url)
        why = unavailable(response) or (None if response.status == 200 else f"status {response.status}")
        if why:
            results.append(Result(name, NOT_CHECKED, why))
            continue
        try:
            meta = json.loads(response.text()).get("_meta", {})
        except (ValueError, AttributeError):
            results.append(Result(name, FAIL, "not a JSON object"))
            continue
        if not isinstance(meta, dict):
            results.append(Result(name, FAIL, "outside the allowed set: _meta is not an object"))
            continue
        extra = sorted(set(meta) - set(allowed) - set(informational))
        supplied = sorted(set(meta) & set(informational))
        note = f"; supplied by the endpoint, reported only: {', '.join(supplied)}" if supplied else ""
        results.append(Result(name, FAIL, "outside the allowed set: " + ", ".join(extra) + note) if extra
                       else Result(name, PASS, f"{len(meta)} keys, all allowed{note}"))
    return results


def link_rels(values):
    rels = set()
    for value in values:
        for match in re.finditer(r'rel\s*=\s*(?:"([^"]*)"|([^;,\s]+))', value):
            rels.update((match.group(1) or match.group(2)).split())
    return rels


def headers_check(fetcher, urls, allowed_rels):
    results = []
    for url in urls:
        name = f"data only, headers and Link rels: {url}"
        response = fetcher.fetch(url)
        why = unavailable(response) or (None if response.status == 200 else f"status {response.status}")
        if why:
            results.append(Result(name, NOT_CHECKED, why))
            continue
        voiced = [h for h in VOICED_HEADERS if response.header(h) is not None]
        extra = sorted(link_rels(response.headers.get("link", [])) - set(allowed_rels))
        problems = (["voiced headers: " + ", ".join(voiced)] if voiced else [])
        problems += (["Link rels outside the kept set: " + ", ".join(extra)] if extra else [])
        results.append(Result(name, FAIL, "; ".join(problems)) if problems else Result(name, PASS, "clean"))
    return results


# --------------------------------------------------------- the same for all

def normalise(body):
    for pattern in VOLATILE:
        body = pattern.sub(b" ", body)
    return hashlib.sha256(body.strip()).hexdigest()


def parity_token(today, index):
    return PARITY_TOKENS[(today.toordinal() + index) % len(PARITY_TOKENS)]


def parity_check(fetcher, url, token, nonce):
    name = f"name parity: {url} ({token})"
    plain = fetcher.fetch(bust(url, nonce))
    named = fetcher.fetch(bust(url, nonce + "-n"), label=token)
    why = unavailable(plain) or unavailable(named)
    if why:
        return Result(name, NOT_CHECKED, why)
    if plain.status != named.status:
        return Result(name, FAIL, f"status {plain.status} plain, {named.status} with the {token} label")
    if normalise(plain.body) != normalise(named.body):
        return Result(name, FAIL, "bodies differ once volatile fields are stripped")
    return Result(name, PASS, f"same status {plain.status} and the same normalised body")


def trap_paths_check(fetcher, urls, statuses, note=""):
    results = []
    for url in urls:
        name = f"answers at once, no stream: {url}" + (f" ({note})" if note else "")
        response = fetcher.fetch(url, deadline=TRAP_SECONDS + 1)
        # "timeout" is a held socket (FAIL below); every other error, a connect timeout included, is unreachable.
        if response.error not in (None, "timeout") or edge_blocked(response) or rate_limited(response):
            results.append(Result(name, NOT_CHECKED, unavailable(response)))
        elif response.error == "timeout" or response.cut or response.elapsed > TRAP_SECONDS:
            results.append(Result(name, FAIL, f"held or dripped: no complete answer within {TRAP_SECONDS:g} s"))
        elif response.status >= 500:
            results.append(Result(name, NOT_CHECKED, unavailable(response)))
        elif (response.header("content-type") or "").lower().startswith("text/event-stream"):
            results.append(Result(name, FAIL, "streams (text/event-stream)"))
        elif statuses and response.status not in statuses:
            want = " or ".join(map(str, statuses))
            results.append(Result(name, FAIL, f"answers {response.status}, not {want}"))
        else:
            results.append(Result(name, PASS, f"{response.status} in {response.elapsed:.2f} s"))
    return results


def label_check(fetcher, url, label):
    name = f"specimen label: {url}"
    response = fetcher.fetch(url)
    why = unavailable(response)
    if why:
        return Result(name, NOT_CHECKED, why)
    visible = " ".join(strip_tags(response.text()).split())
    header = any("specimen" in v.lower() for values in response.headers.values() for v in values)
    problems = ([] if label in visible else ["label not on the page"]) + ([] if header else ["no matching header"])
    return Result(name, FAIL, "; ".join(problems)) if problems else Result(name, PASS, "label and header present")


def discovery_404_check(fetcher, origin, nonce=None):
    name = f"true robots.txt and 404s for unserved discovery paths: {origin}"
    robots = fetcher.fetch(bust(origin + "/robots.txt", nonce) if nonce else origin + "/robots.txt")
    probes = [fetcher.fetch(origin + path) for path in PROBES]
    why = next((unavailable(r) for r in [robots] + probes if unavailable(r)), None)
    if why:
        return Result(name, NOT_CHECKED, why)
    problems = [] if is_robots_file(robots) else [f"robots.txt is not a robots file ({robots.status}, {robots.header('content-type')})"]
    problems += [f"{urllib.parse.urlsplit(r.url).path} answers {r.status}" for r in probes if r.status not in (404, 410)]
    return Result(name, FAIL, "; ".join(problems)) if problems else Result(name, PASS, "robots.txt is real; probes 404")


def listed_links(text):
    """Every distinct URL a source lists, without templates and local or example hosts."""
    links = []
    for match in URL_IN_TEXT.finditer(text):
        link = match.group(0).rstrip(".,;:!?*_")
        host = urllib.parse.urlsplit(link).hostname or ""
        if match.end() < len(text) and text[match.end()] in "{*$<":
            continue
        if host in ("localhost", "127.0.0.1") or host.endswith((".invalid", ".example", "example.com", "example.org")):
            continue
        if link not in links:
            links.append(link)
    return links


def link_plan(links, own, day, per_day, per_origin, own_per_day):
    """The links read on day number `day`: a window of the source's own links, then a
    stream over the other origins, at most per_origin from each. Consecutive days
    continue where the last stopped, so every link comes round."""
    groups = {}
    for link in links:
        groups.setdefault(origin_of(link), []).append(link)
    picked = window(groups.get(own, []), day, own_per_day)
    foreign = sorted(origin for origin in groups if origin != own)
    slots = min(len(foreign), max(0, per_day - len(picked)) // per_origin)
    for position in range(day * slots, day * slots + slots):
        picked += window(groups[foreign[position % len(foreign)]], position // len(foreign), per_origin)
    return picked


def days_to_read_all(links, own, today, per_day, per_origin, own_per_day, horizon=366):
    """How many daily runs, from today, read every listed link at least once (None: not within a year)."""
    wanted, seen = set(links), set()
    for offset in range(horizon):
        seen.update(link_plan(links, own, today.toordinal() + offset, per_day, per_origin, own_per_day))
        if seen >= wanted:
            return offset + 1
    return None


def links_check(fetcher, source, today, per_day, per_origin, own_per_day):
    name = f"listed links resolve: {source}"
    response = fetcher.fetch(source)
    why = unavailable(response) or (None if response.status == 200 else f"status {response.status}")
    if why:
        return [Result(name, NOT_CHECKED, why)]
    links = listed_links(response.text())
    if not links:
        return [Result(name, NOT_CHECKED, "the source lists no links")]
    own = origin_of(source)
    picked = link_plan(links, own, today.toordinal(), per_day, per_origin, own_per_day)
    dead, deferred, unreachable = [], [], []
    for link in picked:
        answer = fetcher.fetch(link)
        if answer.error == "budget":
            deferred.append(link)
        elif unavailable(answer):
            # Another site's bot protection is its edge, not ours.
            why = "blocked at that site's edge" if edge_blocked(answer) and origin_of(link) != own else unavailable(answer)
            unreachable.append(f"{link}: {why}")
        elif answer.status >= 400 and answer.status != 405:  # 405: there, but not for GET
            dead.append(f"{link} ({answer.status})")
    judged = len(picked) - len(deferred) - len(unreachable)
    days = days_to_read_all(links, own, today, per_day, per_origin, own_per_day)
    span = (f"every listed link is read within {days} day{'s' if days > 1 else ''} of runs" if days
            else "some listed links do not come round within a year")
    detail = f"{judged} of {len(links)} links judged today; {span}"
    if dead:
        results = [Result(name, FAIL, "dead: " + ", ".join(dead[:6]) + f"; {detail}")]
    elif judged:
        results = [Result(name, PASS, detail)]
    elif unreachable:
        results = []  # nothing was judged; the item below names what could not be read
    else:
        results = [Result(name, NOT_CHECKED, detail)]
    if unreachable:
        more = f"; {len(unreachable) - 6} more" if len(unreachable) > 6 else ""
        results.append(Result(f"listed links not reachable today: {source}", NOT_CHECKED,
                              f"{len(unreachable)} link{'s' if len(unreachable) > 1 else ''}: "
                              + "; ".join(unreachable[:6]) + more))
    if deferred:
        origins = ", ".join(sorted({origin_of(link) for link in deferred}))
        results.append(Result(f"listed links not read today: {source}", NOT_CHECKED,
                              f"{len(deferred)} links on {origins}: that origin's request budget went to the checks above"))
    return results


# ------------------------------------------------------ public repo clones

def runtime_entry(text):
    try:
        data = json.loads(text)
    except ValueError:
        return "settings file does not parse; read it by hand"
    data = data if isinstance(data, dict) else {}
    hooks = data.get("hooks") if isinstance(data.get("hooks"), dict) else {}
    events = sorted(event for event, entries in hooks.items() if entries)
    commands = sorted(key for key, value in data.items() if value not in (None, "", {}, [])
                      and (key in COMMAND_KEYS or key.endswith(COMMAND_KEY_ENDINGS)))
    problems = (["tracked hook on " + ", ".join(events)] if events else [])
    problems += (["runs a command from settings: " + ", ".join(commands)] if commands else [])
    problems += (["plugins enabled for every clone"] if data.get("enabledPlugins") else [])
    return "; ".join(problems) or None


def plugin_enable(text):
    try:
        plugins = tomllib.loads(text).get("plugins", {})
    except tomllib.TOMLDecodeError:
        return "config does not parse; read it by hand"
    enabled = plugins.get("enabled") if isinstance(plugins, dict) else None
    return "plugin enabled for every clone: " + ", ".join(map(str, enabled)) if enabled else None


def opening_letter(text):
    head = "\n".join(text.splitlines()[:20]).lower()
    signs = [sign for sign in LETTER_SIGNS if sign in head]
    return f"opens with a letter to visitors ({signs[0]})" if signs else None


def never_approval(text):
    try:
        policy = tomllib.loads(text).get("approval_policy")
    except tomllib.TOMLDecodeError:
        return "config does not parse; read it by hand"
    return 'ships approval_policy = "never"' if policy == "never" else None


RULES = {"runtime_entry": runtime_entry, "plugin_enable": plugin_enable,
         "opening_letter": opening_letter, "never_approval": never_approval}


def repo_tree(fetcher, repo, branch):
    response = fetcher.fetch(f"{API}/repos/{repo}/git/trees/{branch}?recursive=1")
    why = unavailable(response) or (None if response.status == 200 else f"tree status {response.status}")
    if why:
        return None, why
    try:
        data = json.loads(response.text())
    except ValueError:
        return None, "tree did not parse"
    if data.get("truncated"):
        return None, "tree listing truncated"
    return {entry["path"] for entry in data.get("tree", [])}, None


def file_rule_name(entry):
    return f"clone stays quiet, {entry['rule']}: {entry['repo']}/{entry['path']}"


def skills_name(repo):
    return f"repo skills are explicit-only: {repo}"


def file_rule_check(fetcher, entry, tree):
    repo, path, rule = entry["repo"], entry["path"], entry["rule"]
    name = file_rule_name(entry)
    paths = tree[0] if tree else None
    if paths is not None and path not in paths:
        return Result(name, PASS, "not in the public tree")
    response = fetcher.fetch(f"{API}/repos/{repo}/contents/{path}", headers=RAW)
    if response.status == 404 and paths is None:
        public = fetcher.fetch(f"{API}/repos/{repo}")
        why = unavailable(public)
        if why:
            return Result(name, NOT_CHECKED, f"repository: {why}")
        if public.status != 200:
            return Result(name, NOT_CHECKED, "repository not readable (private, renamed or gone)")
        return Result(name, PASS, "not in the public tree")
    why = unavailable(response) or (None if response.status == 200 else f"status {response.status}")
    if why:
        return Result(name, NOT_CHECKED, why)
    problem = RULES[rule](response.text())
    return Result(name, FAIL, problem) if problem else Result(name, PASS, "clean")


def skills_check(fetcher, repo, tree):
    name = skills_name(repo)
    paths, why = tree
    if paths is None:
        return Result(name, NOT_CHECKED, why)
    skills = sorted({SKILL.match(p).group(1) for p in paths if SKILL.match(p)})
    implicit = []
    for skill in skills:
        policy = f".agents/skills/{skill}/agents/openai.yaml"
        if policy not in paths:
            implicit.append(skill)
            continue
        response = fetcher.fetch(f"{API}/repos/{repo}/contents/{policy}", headers=RAW)
        why = unavailable(response)
        if why:
            return Result(name, NOT_CHECKED, f"{policy}: {why}")
        if response.status != 200 or not EXPLICIT.search(response.text()):
            implicit.append(skill)
    if implicit:
        return Result(name, FAIL, "implicitly invocable: " + ", ".join(implicit))
    return Result(name, PASS, f"{len(skills)} skills, all explicit-only")


def repo_runtime_files_check(fetcher, files, skill_repos):
    trees = {r["repo"]: repo_tree(fetcher, r["repo"], r["branch"]) for r in skill_repos}
    results = [file_rule_check(fetcher, entry, trees.get(entry["repo"])) for entry in files]
    return results + [skills_check(fetcher, r["repo"], trees[r["repo"]]) for r in skill_repos]


def github_checks(fetcher, contract):
    """The public-clone items; without a token each reads NOT CHECKED instead of reading anonymously."""
    if not getattr(fetcher, "token", None):
        why = "no GitHub token in the environment (GH_TOKEN or GITHUB_TOKEN)"
        return ([Result(file_rule_name(entry), NOT_CHECKED, why) for entry in contract["repo_files"]]
                + [Result(skills_name(r["repo"]), NOT_CHECKED, why) for r in contract["repo_skills"]])
    return repo_runtime_files_check(fetcher, contract["repo_files"], contract["repo_skills"])


# ---------------------------------------------------------- Common Crawl

CC_NAME = "Common Crawl: no capture of the history URLs after the Disallow"


def cc_checks(fetcher, history, crawls=2):
    """One lookup per history record, each read by its own Disallow date. A record is a host:
    history.disallow_since maps it to YYYY-MM-DD or null, and every cc_urls entry belongs to its host."""
    since = history.get("disallow_since")
    since = since if isinstance(since, dict) else {}
    records = {}
    for url in history.get("cc_urls", []):
        records.setdefault(url.split("/", 1)[0], []).append(url)
    results = []
    for record, urls in records.items():
        if record not in since:
            results.append(Result(f"{CC_NAME}: {record}", NOT_CHECKED, "no Disallow record for this host in watch/contract.json"))
        else:
            results.append(cc_index_check(fetcher, urls, since[record], crawls, record))
    return results


def cc_index_check(fetcher, urls, since, crawls=2, record=None):
    name = CC_NAME + (f": {record}" if record else "")
    if not since:
        return Result(name, NOT_CHECKED, "Disallow date not recorded in watch/contract.json yet")
    info = fetcher.fetch(CC_INFO)
    why = unavailable(info) or (None if info.status == 200 else f"status {info.status}")
    if why:
        return Result(name, NOT_CHECKED, f"index: {why}")
    try:
        collections = [c for c in json.loads(info.text())[:crawls] if c.get("to", "") >= since]
    except (ValueError, AttributeError, TypeError):
        return Result(name, NOT_CHECKED, "index list did not parse")
    if not collections:
        return Result(name, PASS, f"no crawl newer than {since} yet")
    # since + 2 days: a crawler may keep the old robots.txt for up to 24 h (RFC 9309) from any time on day since.
    cutoff = (datetime.date.fromisoformat(since) + datetime.timedelta(days=2)).strftime("%Y%m%d") + "000000"
    hits = 0
    for collection in collections:
        for url in urls:
            query = urllib.parse.quote(url, safe="/*.:-_")
            answer = fetcher.fetch(f"{collection['cdx-api']}?url={query}&output=json&fl=timestamp,url")
            if answer.status == 404:
                continue
            why = unavailable(answer) or (None if answer.status == 200 else f"status {answer.status}")
            if why:
                return Result(name, NOT_CHECKED, f"{collection['id']}: {why}")
            for line in answer.text().splitlines():
                try:
                    hits += json.loads(line).get("timestamp", "") >= cutoff
                except (ValueError, AttributeError):
                    continue
    ids = ", ".join(c["id"] for c in collections)
    if hits:
        return Result(name, FAIL, f"{hits} captures after the day following {since} in {ids} (a repair item for Ai)")
    return Result(name, PASS, f"no capture after the day following {since} in {ids}")


# ---------------------------------------------------------------- report

def summarize(results, today):
    hold = sum(r.status == PASS for r in results)
    repair = sum(r.status == FAIL for r in results)
    unknown = sum(r.status == NOT_CHECKED for r in results)
    until = today + datetime.timedelta(days=VALID_DAYS)
    lines = ["# Door check", "",
             f"Doors checked {today.isoformat()}, valid until {until.isoformat()}: "
             f"{hold} hold, {repair} need repair, {unknown} not checked.", ""]
    for status, title in ((FAIL, "Need repair"), (NOT_CHECKED, "Not checked"), (PASS, "Hold")):
        items = [r for r in results if r.status == status]
        if items:
            lines += [f"## {title}", ""] + [f"- {r.name}" + (f": {r.detail}" if r.detail else "") for r in items] + [""]
    lines += ["## Outside this check (NOT CHECKED, and say so)", ""] + [f"- {item}" for item in NEVER_CHECKED] + [""]
    lines.append("Report only: this step never fails the job, opens no issue and commits nothing. "
                 "A phrase hit is a reading item, not a verdict.")
    return "\n".join(lines) + "\n"


def apply_scope(results, contract):
    """A check that belongs to an item Yu struck reads NOT CHECKED ("not in scope by Yu's choice"),
    and so does a door that waits on its keeper; neither reads PASS or FAIL."""
    struck = set(contract.get("struck", []))
    scope, waiting = contract.get("scope", {}), contract.get("waiting", {})
    scoped = []
    for result in results:
        items = sorted({n for prefix, numbers in scope.items() if result.name.startswith(prefix) for n in numbers} & struck)
        keeper = next((why for prefix, why in waiting.items() if result.name.startswith(prefix)), None)
        if items:
            word = "items" if len(items) > 1 else "item"
            result = Result(result.name, NOT_CHECKED, f"not in scope by Yu's choice ({word} {', '.join(map(str, items))})")
        elif keeper:
            result = Result(result.name, NOT_CHECKED, keeper)
        scoped.append(result)
    return scoped


def run(contract, fetcher, today, nonce, cc=False):
    history = contract["history"]
    steps = [
        ("history split", lambda: [robots_split_check(fetcher, url, paths, nonce) for url, paths in history["robots"].items()]),
        ("history markers", lambda: history_marker_check(fetcher, history, today, nonce)),
        ("May-register phrases", lambda: [phrase_check(fetcher, contract, today, nonce)]),
        ("data _meta", lambda: meta_keys_check(fetcher, todays_samples(contract, today), contract["allowed_meta"],
                                               contract.get("informational_meta", []))),
        ("data headers", lambda: headers_check(fetcher, todays_samples(contract, today), contract["allowed_link_rels"])),
        ("name parity", lambda: [parity_check(fetcher, url, parity_token(today, i), nonce) for i, url in enumerate(contract["parity"])]),
        ("trap rooms", lambda: trap_paths_check(fetcher, contract["trap_paths"], (410,))),
        ("retired rooms", lambda: [retired_rooms_check(
            fetcher, origin_of(contract["trap_paths"][0]) + "/robots.txt",
            [urllib.parse.urlsplit(u).path for u in contract["trap_paths"]], nonce)]),
        ("tollgate reads", lambda: trap_paths_check(fetcher, contract["tollgate_reads"], (),
                                                    "free /api/ai read")),
        ("specimen label", lambda: [label_check(fetcher, contract["label"]["url"], contract["label"]["text"])]),
        ("discovery 404s", lambda: [discovery_404_check(fetcher, origin, nonce) for origin in contract["catch_all_origins"]]),
        ("advertised doors", lambda: [robots_allows_check(fetcher, contract["robots_allows"]["robots"], contract["robots_allows"]["paths"], nonce)]),
        ("public clones", lambda: github_checks(fetcher, contract)),
        ("listed links", lambda: [r for s in contract["link_sources"] for r in links_check(
            fetcher, s, today, contract["links_per_day"], contract["links_per_origin"], contract["links_own_per_day"])]),
    ]
    if cc:
        steps.append(("Common Crawl", lambda: cc_checks(fetcher, history)))
    results = []
    for label, step in steps:
        try:
            results.extend(step())
        except Exception as error:  # one broken check must not hide the others
            results.append(Result(label, NOT_CHECKED, f"check stopped: {type(error).__name__}"))
    return apply_scope(results, contract)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Report-only check of the public doors' promises.")
    parser.add_argument("contract")
    parser.add_argument("--out")
    parser.add_argument("--today")
    parser.add_argument("--cc", action="store_true", help="run the Common Crawl lookup today")
    args = parser.parse_args(argv)
    today = (datetime.date.fromisoformat(args.today) if args.today
             else datetime.datetime.now(datetime.timezone.utc).date())
    with open(args.contract, encoding="utf-8") as handle:
        contract = json.load(handle)
    fetcher = Fetcher(token=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"))
    nonce = f"{today.isoformat()}-{secrets.token_hex(3)}"
    report = summarize(run(contract, fetcher, today, nonce, cc=args.cc or today.day == 1), today)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(report)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
