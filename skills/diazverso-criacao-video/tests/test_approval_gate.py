"""J08: approval cannot be inferred from completed render alone."""
import importlib.util
import unittest
from pathlib import Path

MOD = Path(__file__).resolve().parents[1]/"scripts"/"approval_gate.py"
spec = importlib.util.spec_from_file_location("diazverso_approval_gate", MOD)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record():
    return {"production_id":"VD_0011",
            "gates":{k:{"status":"APROVADO","evidence":"Revisado pelo criador; registro de QA anexado"}
                     for k in module.GATES},
            "creator_decision":{"approved":True,"evidence":"Decisão explícita do criador"}}


class ApprovalGateTests(unittest.TestCase):
    def test_approved_with_evidence_still_does_not_post(self):
        result=module.evaluate(record())
        self.assertEqual(result["status"],"KIT_APROVADO_PARA_ENTREGA_MANUAL")
        self.assertFalse(result["posting_performed"])

    def test_unchecked_gate_blocks(self):
        d=record();d["gates"]["qa_audio"]["status"]="PENDENTE"
        r=module.evaluate(d)
        self.assertEqual(r["status"],"REVISAO_PENDENTE")
        self.assertEqual(r["pending"][0]["gate"],"qa_audio")

    def test_failed_gate_blocks(self):
        d=record();d["gates"]["direitos_midias"]["status"]="REPROVADO"
        self.assertEqual(module.evaluate(d)["status"],"REVISAO_PENDENTE")

    def test_false_creator_approval_blocks(self):
        d=record();d["creator_decision"]["approved"]=False
        self.assertEqual(module.evaluate(d)["status"],"REVISAO_PENDENTE")

    def test_creator_approval_needs_evidence(self):
        d=record();d["creator_decision"]["evidence"]=""
        with self.assertRaises(ValueError):module.evaluate(d)

    def test_gate_approval_needs_evidence(self):
        d=record();d["gates"]["qa_visual"]["evidence"]=""
        with self.assertRaises(ValueError):module.evaluate(d)

    def test_missing_gate_rejected(self):
        d=record();d["gates"].pop("legendas")
        with self.assertRaises(ValueError):module.evaluate(d)

    def test_invalid_status_rejected(self):
        d=record();d["gates"]["kit_textual"]["status"]="VERIFICADO"
        with self.assertRaises(ValueError):module.evaluate(d)

    def test_invalid_production_id_rejected(self):
        d=record();d["production_id"]="TF_0001"
        with self.assertRaises(ValueError):module.evaluate(d)


if __name__=="__main__":
    unittest.main()
