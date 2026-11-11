"""E08: focused pure logic tests; no Google access or writes."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "upsert_production.py"
spec = importlib.util.spec_from_file_location("diazverso_upsert", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def data():
    row = [""] * len(mod.HEADERS)
    for key, val in {"ID": "VD_0008", "TIPO": "LONGO",
                     "TEMA / CONTEXTO": "Pauta", "STATUS": "ROTEIRO",
                     "TÍTULO A": "Título original"}.items():
        row[mod.HEADERS.index(key)] = val
    return [list(mod.HEADERS), row]


class UpsertTests(unittest.TestCase):
    def test_one_cell_only_and_no_write(self):
        result = mod.plan_upsert(data(), "VD_0008", {"TÍTULO B": "Alternativa"})
        self.assertEqual(result["status"], "READY_TO_WRITE")
        self.assertEqual(result["updates"][0]["a1"], "G2")
        self.assertFalse(result["writes_performed"])

    def test_repeated_change_is_noop(self):
        self.assertEqual(mod.plan_upsert(data(), "VD_0008",
                          {"TÍTULO A": "Título original"})["status"], "NO_CHANGE")

    def test_existing_value_not_overwritten_silently(self):
        self.assertEqual(mod.plan_upsert(data(), "VD_0008",
                          {"TÍTULO A": "Outro"})["status"], "CONFLICT")

    def test_explicit_replace_allowed(self):
        self.assertEqual(mod.plan_upsert(data(), "VD_0008",
                          {"TÍTULO A": "Outro"}, allow_replace=True)["status"], "READY_TO_WRITE")

    def test_stale_expected_blocks(self):
        self.assertEqual(mod.plan_upsert(data(), "VD_0008", {"TÍTULO B": "Nova"},
                          expected={"STATUS": "PLANEJADO"})["status"], "CONFLICT")

    def test_duplicate_id_blocks(self):
        rows = data()
        rows.append(rows[1][:])
        with self.assertRaises(ValueError):
            mod.plan_upsert(rows, "VD_0008", {"TÍTULO B": "Nova"})

    def test_invalid_rota_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_upsert(data(), "VD_0008",
                            {"ROTEIRO": "https://drive.google.com/drive/folders/abcd"})

    def test_direct_doc_accepted(self):
        doc = "https://docs.google.com/document/d/abcDEF_123/edit"
        self.assertEqual(mod.plan_upsert(data(), "VD_0008",
                          {"ROTEIRO": doc})["status"], "READY_TO_WRITE")

    def test_thumb_folder_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_upsert(data(), "VD_0008",
                            {"THUMBNAIL A": "https://drive.google.com/drive/folders/abc"})

    def test_publication_requires_verified_link_and_date(self):
        with self.assertRaises(ValueError):
            mod.plan_upsert(data(), "VD_0008", {"STATUS": "PUBLICADO"},
                            publication_verified=True)

    def test_publication_success_only_with_verification(self):
        result = mod.plan_upsert(data(), "VD_0008",
                  {"STATUS": "PUBLICADO", "PUBLICADO EM": "2026-11-11",
                   "LINK YOUTUBE": "https://www.youtube.com/watch?v=abc123DEF45"},
                   publication_verified=True)
        self.assertEqual(result["status"], "READY_TO_WRITE")
        self.assertEqual(len(result["updates"]), 3)

    def test_review_approval_not_inferred(self):
        with self.assertRaises(ValueError):
            mod.plan_upsert(data(), "VD_0008", {"REVISÃO": "APROVADO"})

    def test_unexpected_column_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_upsert(data(), "VD_0008", {"ID": "VD_0999"})

    def test_formula_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_upsert(data(), "VD_0008", {"TÍTULO B": "=IMPORTDATA(...)"})

    def test_wrong_kind_rejected(self):
        rows = data()
        rows[1][1] = "SHORT"
        with self.assertRaises(ValueError):
            mod.plan_upsert(rows, "VD_0008", {"TÍTULO B": "Nova"})


if __name__ == "__main__":
    unittest.main()
