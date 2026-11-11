"""E04 smoke tests, no Google credentials required."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "validate_sheet_schema.py"
spec = importlib.util.spec_from_file_location("diazverso_sheet_validate", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def snapshot():
    props = [
        {"properties": {"title": name, "gridProperties": {"frozenRowCount": 1},
                        "hidden": name == "Config"}}
        for name in mod.HEADERS
    ]
    return {"sheets": props, "headers": {k: list(v) for k, v in mod.HEADERS.items()}}


class SchemaTests(unittest.TestCase):
    def test_valid_and_read_only(self):
        result = mod.validate(snapshot())
        self.assertEqual(result["status"], "VALID")
        self.assertFalse(result["writes_performed"])

    def test_missing_tab_blocks(self):
        data = snapshot()
        data["sheets"].pop(0)
        self.assertEqual(mod.validate(data)["issues"][0]["issue"], "MISSING_TAB")

    def test_wrong_header_not_overwritten(self):
        data = snapshot()
        data["headers"]["Ideias"][1] = "TEMA ERRADO"
        result = mod.validate(data)
        self.assertEqual(result["status"], "NEEDS_ATTENTION")
        self.assertIn("HEADER_MISMATCH", [x["issue"] for x in result["issues"]])

    def test_missing_header_read_not_treated_as_empty(self):
        data = snapshot()
        del data["headers"]["Afiliados"]
        self.assertIn("HEADER_NOT_READ", [x["issue"] for x in mod.validate(data)["issues"]])

    def test_config_visibility_and_freeze(self):
        data = snapshot()
        data["sheets"][3]["properties"]["hidden"] = False
        data["sheets"][2]["properties"]["gridProperties"]["frozenRowCount"] = 0
        kinds = {x["issue"] for x in mod.validate(data)["issues"]}
        self.assertEqual(kinds, {"CONFIG_VISIBLE", "HEADER_NOT_FROZEN"})

    def test_preserves_legacy_tabs(self):
        data = snapshot()
        data["sheets"].append({"properties": {"title": "LEGADO — Shorts", "hidden": True}})
        self.assertEqual(mod.validate(data)["status"], "VALID")


if __name__ == "__main__":
    unittest.main()
