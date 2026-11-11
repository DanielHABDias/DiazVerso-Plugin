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


    def test_plan_new_idea_unique_sequential(self):
        rows = [list(mod.HEADERS["Ideias"]),
                ["TF_0002", "Outra ideia"], ["TF_0004", "Tema anterior"]]
        idea = mod.plan_new_idea(rows, {"TEMA": "Novo herói", "TESE / CONTEXTO": "Uma tese concreta"}, previously_issued_ids=["TF_0003"])
        self.assertEqual(idea["id"], "TF_0005")
        self.assertEqual(idea["values"][1:3], ["Novo herói", "Uma tese concreta"])
        self.assertFalse(idea["writes_performed"])
        self.assertEqual(idea["values"][9], "IDEIA")

    def test_invalid_dropdown_values_block_before_write(self):
        for patch in ({"STATUS": "A AVALIAR"}, {"PRIORIDADE": "URGENTE"}):
            with self.assertRaises(ValueError):
                mod.plan_new_idea([list(mod.HEADERS["Ideias"])],
                    {"TEMA": "Nova", "TESE / CONTEXTO": "Tese", **patch},
                    previously_issued_ids=[])

    def test_existing_theme_not_inserted(self):
        rows = [list(mod.HEADERS["Ideias"]), ["TF_0001", "A origem do herói"]]
        result = mod.plan_new_idea(rows, {"TEMA": "  a ORIGEM do HEROI  ", "TESE / CONTEXTO": "Nova análise"}, previously_issued_ids=[])
        self.assertEqual(result["status"], "EXISTS")

    def test_bad_header_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_new_idea([["ID", "WRONG"]], {"TEMA": "Nova", "TESE / CONTEXTO": "Tese"}, previously_issued_ids=[])

    def test_formula_is_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_new_idea([list(mod.HEADERS["Ideias"])],
                              {"TEMA": "=IMPORTXML(...)", "TESE / CONTEXTO": "Tese"}, previously_issued_ids=[])

    def test_existing_duplicate_id_rejected(self):
        rows = [list(mod.HEADERS["Ideias"]), ["TF_0001", "A"], ["TF_0001", "B"]]
        with self.assertRaises(ValueError):
            mod.plan_new_idea(rows, {"TEMA": "Nova", "TESE / CONTEXTO": "Tese"}, previously_issued_ids=[])

    def test_historical_id_is_not_reused(self):
        rows = [list(mod.HEADERS["Ideias"]), ["TF_0002", "Existing"]]
        planned = mod.plan_new_idea(rows, {"TEMA": "Other", "TESE / CONTEXTO": "Tese"}, previously_issued_ids=["TF_0098"])
        self.assertEqual(planned["id"], "TF_0099")

    def test_historical_ledger_is_required(self):
        with self.assertRaises(TypeError):
            mod.plan_new_idea([list(mod.HEADERS["Ideias"])], {"TEMA": "Other", "TESE / CONTEXTO": "Tese"})

    def test_missing_tese_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_new_idea([list(mod.HEADERS["Ideias"])], {"TEMA": "Nova"}, previously_issued_ids=[])



if __name__ == "__main__":
    unittest.main()
