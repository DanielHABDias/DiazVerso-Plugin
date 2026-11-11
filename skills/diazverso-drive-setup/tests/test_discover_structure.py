"""Unit tests for E02. No Google account/network required."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "discover_structure.py"
spec = importlib.util.spec_from_file_location("diazverso_discover", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

F = module.FOLDER
S = module.SHEET


def entry(id, name, mime=F, parent=None):
    return {"id": id, "title": name, "mime_type": mime,
            "parent_ids": [parent] if parent else []}


def sample():
    root = entry("root", "Diazverso")
    root_files = [entry("scripts", "Roteiros", parent="root"),
                  entry("thumbs", "Thumbnails", parent="root"),
                  entry("sheet", "Canal do YT — V1.0 (Diazverso)", S, "root")]
    root_files.extend(entry(f"lib{i}", n, parent="root") for i, n in enumerate(sorted(module.OPTIONAL)))
    return {
        "root_pages": [{"results": [root]}],
        "children": {
            "root": [{"results": root_files}],
            "scripts": [{"results": [entry("l", "Longos", parent="scripts"),
                                     entry("s", "Shorts", parent="scripts")]}],
            "thumbs": [{"results": [entry("tl", "Longos", parent="thumbs"),
                                    entry("ts", "Shorts", parent="thumbs")]}],
        },
        "complete": {"roots": True, "root": True, "scripts": True, "thumbs": True},
    }


class DiscoveryTests(unittest.TestCase):
    def test_complete_no_writes(self):
        snap = sample()
        a = module.discover(snap)
        b = module.discover(snap)
        self.assertEqual(a, b)
        self.assertEqual(a["status"], "COMPLETE")
        self.assertFalse(a["writes_performed"])
        self.assertEqual(a["folders"]["Roteiros/Shorts"]["id"], "s")

    def test_missing_item_reported_no_creation(self):
        snap = sample()
        snap["children"]["thumbs"][0]["results"].pop()
        result = module.discover(snap)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["missing"], ["Thumbnails/Shorts"])

    def test_same_name_different_parent_is_ignored(self):
        snap = sample()
        snap["children"]["root"][0]["results"].append(entry("wrong", "Roteiros", parent="other"))
        self.assertEqual(module.discover(snap)["status"], "COMPLETE")

    def test_duplicate_exact_folder_blocks(self):
        snap = sample()
        snap["children"]["root"][0]["results"].append(entry("dup", "Roteiros", parent="root"))
        result = module.discover(snap)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("Roteiros", result["ambiguous"])

    def test_preferred_id_must_match_parent_name_type(self):
        snap = sample()
        snap["preferred_ids"] = {"Roteiros": "sheet"}
        self.assertEqual(module.discover(snap)["folders"]["Roteiros"]["status"], "CONFIG_ID_INVALID")

    def test_root_ambiguous(self):
        snap = sample()
        snap["root_pages"][0]["results"].append(entry("other", "Diazverso"))
        self.assertEqual(module.discover(snap)["root"]["status"], "AMBIGUOUS")

    def test_unfinished_page_rejected(self):
        snap = sample()
        snap["children"]["root"][0]["next_page_token"] = "more"
        with self.assertRaises(ValueError):
            module.discover(snap)

    def test_missing_list_is_unknown_not_missing(self):
        snap = sample()
        snap["children"].pop("thumbs")
        with self.assertRaises(ValueError):
            module.discover(snap)

    def test_wrong_mime_not_accepted(self):
        snap = sample()
        snap["children"]["root"][0]["results"][0]["mime_type"] = S
        result = module.discover(snap)
        self.assertEqual(result["folders"]["Roteiros"]["status"], "MISSING")

    def test_preferred_unique_root(self):
        snap = sample()
        snap["root_pages"][0]["results"].append(entry("other", "Diazverso"))
        snap["preferred_root_id"] = "root"
        self.assertEqual(module.discover(snap)["status"], "COMPLETE")


if __name__ == "__main__":
    unittest.main()
