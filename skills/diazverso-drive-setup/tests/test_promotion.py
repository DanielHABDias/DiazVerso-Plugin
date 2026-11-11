"""E06/E07 state transitions: test without accessing or altering Google Sheets."""
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "promotion.py"
spec = importlib.util.spec_from_file_location("diazverso_promotion", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def idea(link=""):
    return list(mod.IDEAS), ["TF_0002", "Pauta", "Tese original", "Título provisório",
                             "Thumb", "Motivo", "ALTA", "", "", "APROVADA", link, ""]


def prod(ident="VD_0008", linked=True, url=""):
    note = "IDEIA_ORIGEM_ID=TF_0002" if linked else ""
    d = {"ID": ident, "TIPO": "LONGO", "TEMA / CONTEXTO": "Pauta — Tese original",
         "ROTEIRO": url, "OBSERVAÇÕES": note}
    return [d.get(k, "") for k in mod.PRODUCTIONS]


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.ideas = [list(mod.IDEAS), idea()[1]]
        self.productions = [list(mod.PRODUCTIONS)]

    def run_plan(self, doc_verified=False):
        return mod.plan_promotion(self.ideas, self.productions, "TF_0002", "LONGO",
                                  historical_production_ids=["VD_0007"], doc_verified=doc_verified)

    def test_first_step_creates_only_proposal(self):
        result = self.run_plan()
        self.assertEqual(result["status"], "CREATE_PRODUCTION")
        self.assertEqual(result["id"], "VD_0008")
        self.assertEqual(result["row"][0:2], ["VD_0008", "LONGO"])
        self.assertIn("IDEIA_ORIGEM_ID=TF_0002", result["row"][15])
        self.assertFalse(result["writes_performed"])

    def test_historical_ids_respected(self):
        result = mod.plan_promotion(self.ideas, self.productions, "TF_0002", "SHORT",
                                    historical_production_ids=["SH_0032"])
        self.assertEqual(result["id"], "SH_0033")

    def test_repeated_after_creation_does_not_duplicate(self):
        self.productions.append(prod())
        self.assertEqual(self.run_plan()["status"], "LINK_SOURCE_IDEA")

    def test_failure_after_link_resumes_at_doc(self):
        self.productions.append(prod())
        self.ideas[1][10] = "VD_0008"
        self.assertEqual(self.run_plan()["status"], "WAIT_FOR_VERIFIED_DOC")

    def test_doc_url_alone_does_not_authorize_removal(self):
        self.productions.append(prod(url="https://docs.google.com/document/d/realDoc/edit"))
        self.ideas[1][10] = "VD_0008"
        self.assertEqual(self.run_plan()["status"], "WAIT_FOR_VERIFIED_DOC")

    def test_verified_doc_and_link_allow_only_removal_proposal(self):
        self.productions.append(prod(url="https://docs.google.com/document/d/realDoc/edit"))
        self.ideas[1][10] = "VD_0008"
        result = self.run_plan(doc_verified=True)
        self.assertEqual(result["status"], "READY_FOR_AUTHORIZED_REMOVAL")
        self.assertFalse(result["writes_performed"])

    def test_after_removal_is_idempotent(self):
        self.productions.append(prod(url="https://docs.google.com/document/d/realDoc/edit"))
        self.ideas.pop()
        self.assertEqual(self.run_plan(doc_verified=True)["status"], "ALREADY_PROMOTED")

    def test_duplicate_productions_block(self):
        self.productions.extend([prod(), prod("VD_0009")])
        self.assertEqual(self.run_plan()["status"], "BLOCKED_DUPLICATE_PRODUCTION")

    def test_conflicting_link_blocks(self):
        self.productions.append(prod())
        self.ideas[1][10] = "VD_9999"
        self.assertEqual(self.run_plan()["status"], "BLOCKED_CONFLICTING_LINK")

    def test_reuse_existing_id_without_origin_not_allowed(self):
        self.productions.append(prod(linked=False))
        self.assertEqual(self.run_plan()["id"], "VD_0009")

    def test_same_idea_wrong_type_blocks(self):
        self.productions.append(prod())
        result = mod.plan_promotion(self.ideas, self.productions, "TF_0002", "SHORT",
                                    historical_production_ids=[])
        self.assertEqual(result["status"], "BLOCKED_TYPE_MISMATCH")

    def test_incomplete_headers_refuse_operation(self):
        with self.assertRaises(ValueError):
            mod.plan_promotion([["ID"], self.ideas[1]], self.productions, "TF_0002", "LONGO",
                               historical_production_ids=[])

    def test_no_source_does_not_create(self):
        self.ideas.pop()
        self.assertEqual(self.run_plan()["status"], "BLOCKED_IDEA_NOT_FOUND")

    def test_missing_ledger_rejected(self):
        with self.assertRaises(TypeError):
            mod.plan_promotion(self.ideas, self.productions, "TF_0002", "LONGO")

    def test_invalid_type_rejected(self):
        with self.assertRaises(ValueError):
            mod.plan_promotion(self.ideas, self.productions, "TF_0002", "MUSIC",
                               historical_production_ids=[])


if __name__ == "__main__":
    unittest.main()
