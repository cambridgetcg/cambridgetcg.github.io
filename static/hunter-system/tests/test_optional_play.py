import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import hunter_system as hunter


class OptionalPlayTests(unittest.TestCase):
    def test_low_activity_and_missing_state_do_not_assign_work(self):
        states = ({}, {"quiet": {"commits": 0, "has_state": False,
                                  "last_commit": "3 years ago", "score": 0}})
        for state in states:
            self.assertEqual(hunter.generate_quests(state), [])
        with patch.object(hunter, "discover_hunters") as discover:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                hunter.main(["--quest"])
        discover.assert_not_called()
        self.assertIn("Nothing is due", output.getvalue())

    def test_default_inventory_has_no_rank_but_toy_is_explicit(self):
        with tempfile.TemporaryDirectory() as temp:
            desktop = Path(temp)
            (desktop / "quiet" / ".git").mkdir(parents=True)
            with patch.object(hunter, "DESKTOP", desktop):
                observed = hunter.discover_hunters()
                toy = hunter.discover_hunters(play_ranks=True)
        self.assertEqual(set(observed), {"quiet"})
        self.assertFalse({"rank", "score", "rank_title"} & observed["quiet"].keys())
        self.assertIn("rank", toy["quiet"])
        self.assertEqual(hunter.generate_quests(toy), [])

    def test_heartbeat_preserves_old_scores_and_writes_only_observations(self):
        with tempfile.TemporaryDirectory() as temp:
            old = Path(temp) / "hunter_system.json"
            inventory = Path(temp) / "hunter_inventory.json"
            old.write_text('{"historical_score": 4.6}\n')
            original = old.read_bytes()
            with patch.object(hunter, "HUNTER_DB", old), patch.object(hunter, "INVENTORY_DB", inventory):
                saved = hunter.save_hunters({"quiet": {"name": "quiet", "score": 0, "rank": "E"}})
            self.assertEqual(old.read_bytes(), original)
            self.assertEqual(json.loads(inventory.read_text()), saved)
            self.assertEqual(saved["hunters"]["quiet"], {"name": "quiet"})
            self.assertNotIn("avg_score", saved)
            self.assertNotIn("top_rank", saved)

    def test_heartbeat_never_enables_ranking(self):
        with patch.object(hunter, "discover_hunters", return_value={}) as discover:
            with patch.object(hunter, "save_hunters", return_value={"total_hunters": 0}):
                with contextlib.redirect_stdout(io.StringIO()):
                    hunter.main(["--play-ranks", "--heartbeat"])
        discover.assert_called_once_with(play_ranks=False)


if __name__ == "__main__":
    unittest.main()
