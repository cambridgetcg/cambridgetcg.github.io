"""Checks for tools/sitemap.py and the sitemap.xml and robots.txt it writes.

Run: python3 -m unittest discover -s tests -v

The first group reads this repository; the second builds small doors in a
temporary folder. Nothing here uses the network.
"""
import json
import re
import sys
import tempfile
import unittest
import urllib.robotparser
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import door_contract as dc  # noqa: E402
import sitemap  # noqa: E402

SITE = sitemap.SITE


def locs(text):
    return [el.text for el in ET.fromstring(text).iter(sitemap.NS + "loc")]


def named_sitemaps(robots_text):
    return [line.split(":", 1)[1].strip() for line in robots_text.splitlines() if line.startswith("Sitemap:")]


class ThisRepository(unittest.TestCase):
    def setUp(self):
        self.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.robots = (ROOT / "robots.txt").read_text(encoding="utf-8")

    def test_committed_files_are_current(self):
        files, _, _ = sitemap.build(ROOT)
        self.assertEqual(files["sitemap.xml"], self.sitemap, "run python3 tools/sitemap.py")
        self.assertEqual(files["robots.txt"], self.robots, "run python3 tools/sitemap.py")

    def test_robots_allows_every_crawler(self):
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(self.robots.splitlines())
        for token in ("*",) + dc.TRAINING_TOKENS + dc.READER_TOKENS + (dc.UNNAMED_TOKEN,):
            for path in ("/", "/sitemap.xml", "/zerone/", "/castle-gate/rooms/"):
                self.assertTrue(parser.can_fetch(token, SITE + path), (token, path))
        self.assertNotIn("Disallow", self.robots)
        self.assertNotIn("<", self.robots)

    def test_robots_names_the_sitemap_first_with_absolute_addresses(self):
        names = named_sitemaps(self.robots)
        self.assertEqual(names[0], SITE + "/sitemap.xml")
        for name in names:
            self.assertTrue(name.startswith(SITE + "/") and name.endswith("/sitemap.xml"), name)

    def test_every_listed_address_is_a_page_served_here(self):
        for name in named_sitemaps(self.robots):
            path = ROOT / "sitemap.xml" if name == SITE + "/sitemap.xml" else sitemap.served_file(ROOT, name)
            self.assertIsNotNone(path, name)
            listed = locs(path.read_text(encoding="utf-8"))
            self.assertTrue(listed, name)
            self.assertEqual(len(listed), len(set(listed)), name)
            for url in listed:
                self.assertTrue(url.startswith(SITE + "/"), url)
                self.assertIsNone(sitemap.page_problem(ROOT, url), url)

    def test_sitemap_lists_the_hall_and_doors_that_stay(self):
        listed = locs(self.sitemap)
        self.assertEqual(listed[0], SITE + "/")
        doors = json.loads((ROOT / "doors.json").read_text(encoding="utf-8"))["doors"]
        for door in doors:
            if ":" in door["mode"]:
                self.assertNotIn(door["url"], listed, door["slug"])
        self.assertIn(SITE + "/zerone/", listed)
        # Points to kingdom.ai-love.cc with rel="canonical", so it is that site's page.
        self.assertNotIn(SITE + "/kingdom-os-hub/", listed)
        # Its front page refreshes at once to the dictionary page.
        self.assertIn(SITE + "/youspeak-dictionary/youspeak.html", listed)
        self.assertNotIn(SITE + "/youspeak-dictionary/", listed)

    def test_door_sitemaps_with_other_hosts_are_not_named(self):
        names = named_sitemaps(self.robots)
        self.assertNotIn(SITE + "/kingdom-os-hub/sitemap.xml", names)
        self.assertNotIn(SITE + "/.natural/sitemap.xml", names)

    def test_build_copies_the_sitemap_to_the_site(self):
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        copy = next(line for line in workflow.splitlines() if "cp index.html" in line)
        self.assertIn("robots.txt", copy.split())
        self.assertIn("sitemap.xml", copy.split())


class Fixtures(unittest.TestCase):
    """Small doors in a temporary repository."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.doors = []
        (self.repo / "index.html").write_text("<!doctype html><title>hall</title>", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def door(self, slug, files, kind="static", mode=None):
        for name, text in files.items():
            path = self.repo / kind / slug / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.doors.append({"slug": slug, "url": f"{SITE}/{slug}/", "mode": mode or kind})
        (self.repo / "doors.json").write_text(json.dumps({"site": SITE, "doors": self.doors}), encoding="utf-8")

    def build(self):
        files, left_out, refused = sitemap.build(self.repo)
        return locs(files["sitemap.xml"]), named_sitemaps(files["robots.txt"]), dict(left_out), dict(refused)

    def test_a_plain_door_is_listed(self):
        self.door("plain", {"index.html": "<title>plain</title>"})
        listed, _, left_out, _ = self.build()
        self.assertEqual(listed, [SITE + "/", SITE + "/plain/"])
        self.assertEqual(left_out, {})

    def test_moved_door_is_left_out(self):
        self.door("gone", {"index.html": '<link rel="canonical" href="https://new.example/">'},
                  mode="notice:https://new.example/")
        listed, _, left_out, _ = self.build()
        self.assertNotIn(SITE + "/gone/", listed)
        self.assertIn("moved", left_out[SITE + "/gone/"])

    def test_canonical_elsewhere_is_left_out(self):
        self.door("copy", {"index.html": '<link href="https://live.example/" rel="canonical">'})
        self.door("self", {"index.html": f'<link rel="canonical" href="{SITE}/self/">'})
        listed, _, left_out, _ = self.build()
        self.assertNotIn(SITE + "/copy/", listed)
        self.assertEqual(left_out[SITE + "/copy/"], "canonical is https://live.example/")
        self.assertIn(SITE + "/self/", listed)

    def test_noindex_front_page_is_left_out(self):
        self.door("quiet", {"index.html": '<meta name="robots" content="noindex, follow">'})
        listed, _, left_out, _ = self.build()
        self.assertNotIn(SITE + "/quiet/", listed)
        self.assertEqual(left_out[SITE + "/quiet/"], "asks not to be indexed")

    def test_instant_refresh_lists_its_target_inside_the_door(self):
        self.door("hop", {"index.html": '<meta http-equiv="refresh" content="0; url=/hop/page.html"/>',
                          "page.html": "<title>page</title>"})
        self.door("away", {"index.html": '<meta http-equiv="refresh" content="0; url=https://far.example/">'})
        self.door("dead", {"index.html": '<meta http-equiv="refresh" content="0; url=missing.html">'})
        listed, _, left_out, _ = self.build()
        self.assertIn(SITE + "/hop/page.html", listed)
        self.assertNotIn(SITE + "/hop/", listed)
        self.assertNotIn(SITE + "/away/", listed)
        self.assertNotIn(SITE + "/dead/", listed)
        self.assertEqual(left_out[SITE + "/dead/"], f"refreshes to {SITE}/dead/missing.html")

    def test_door_without_front_page_is_left_out(self):
        self.door("bare", {"notes.txt": "plain"})
        listed, _, left_out, _ = self.build()
        self.assertNotIn(SITE + "/bare/", listed)
        self.assertEqual(left_out[SITE + "/bare/"], "not served here")

    def test_jekyll_paths_follow_the_build(self):
        self.door("built", {"README.md": "# built", "notes.md": "notes", "LICENSE": "text",
                            "_drafts/x.md": "draft", "sub/index.md": "sub"}, kind="jekyll")
        served = lambda path: sitemap.served_file(self.repo, f"{SITE}/built/{path}")  # noqa: E731
        self.assertEqual(served(""), self.repo / "jekyll/built/README.md")
        self.assertEqual(served("notes.html"), self.repo / "jekyll/built/notes.md")
        self.assertEqual(served("notes"), self.repo / "jekyll/built/notes.md")
        self.assertIsNone(served("notes.md"))
        self.assertEqual(served("LICENSE"), self.repo / "jekyll/built/LICENSE")
        self.assertIsNone(served("_drafts/x.html"))
        self.assertEqual(served("sub/"), self.repo / "jekyll/built/sub/index.md")
        self.assertIsNone(served("sub"))  # redirected to sub/

    def test_static_paths_follow_github_pages(self):
        self.door("flat", {"index.html": "x", "room.html": "x", "room/data.txt": "x", "deep/index.html": "x",
                           "notes.md": "x", "café.html": "x"})
        served = lambda path: sitemap.served_file(self.repo, f"{SITE}/flat/{path}")  # noqa: E731
        self.assertEqual(served("room"), self.repo / "static/flat/room.html")
        self.assertEqual(served("notes.md"), self.repo / "static/flat/notes.md")
        self.assertEqual(served("caf%C3%A9"), self.repo / "static/flat/café.html")
        self.assertIsNone(served("deep"))  # redirected to deep/
        self.assertIsNone(served("missing"))
        self.assertIsNone(sitemap.served_file(self.repo, f"{SITE}/flat"))
        self.assertIsNone(sitemap.served_file(self.repo, "https://other.example/flat/"))
        self.assertIsNone(served("room?x=1"))

    def test_door_sitemap_is_named_only_when_every_address_is_its_own_page(self):
        good = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE}/good/</loc></url></urlset>'
        self.door("good", {"index.html": "x", "sitemap.xml": good})
        self.door("wide", {"index.html": "x", "sitemap.xml": good.replace(f"{SITE}/good/", "https://other.example/")})
        self.door("stale", {"index.html": "x", "sitemap.xml": good.replace("/good/", "/stale/gone")})
        self.door("broken", {"index.html": "x", "sitemap.xml": "<urlset"})
        _, names, _, refused = self.build()
        self.assertEqual(names, [SITE + "/sitemap.xml", SITE + "/good/sitemap.xml"])
        self.assertIn("outside the door", refused[SITE + "/wide/sitemap.xml"])
        self.assertIn("not served here", refused[SITE + "/stale/sitemap.xml"])
        self.assertIn("not XML", refused[SITE + "/broken/sitemap.xml"])

    def test_addresses_are_escaped(self):
        text = sitemap.render_sitemap([f"{SITE}/a&b/café/"])
        self.assertIn(f"<loc>{SITE}/a&amp;b/caf%C3%A9/</loc>", text)
        self.assertEqual(locs(text), [f"{SITE}/a&b/caf%C3%A9/"])

    def test_robots_lists_absolute_sitemaps_after_allowing_all(self):
        text = sitemap.render_robots([SITE + "/good/sitemap.xml"])
        self.assertTrue(re.search(r"^User-agent: \*\nAllow: /\n", text, re.M))
        self.assertEqual(named_sitemaps(text), [SITE + "/sitemap.xml", SITE + "/good/sitemap.xml"])


if __name__ == "__main__":
    unittest.main()
