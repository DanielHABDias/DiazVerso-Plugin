"""Atomic request construction and recovery from an unknown write outcome."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sheets_batch as mod


def snapshot():
    out = {"spreadsheet_id": "qa-isolated-sheet", "complete_fresh_read": True, "history_verified_complete": True,
            "sheets": {name: {"sheet_id": i, "grid_rows": 100,
                               "rows": [list(mod.HEADERS[name])]}
                       for i, name in enumerate(("Ideias", "Produções", "Config"))}}
    out["sheets"]["Config"]["rows"].append(["CURRENT_SPREADSHEET_ID", "qa-isolated-sheet"])
    return out


def apply(snap, requests):
    out = copy.deepcopy(snap)
    for request in requests:
        if "updateCells" not in request:
            continue
        value = request["updateCells"]
        rng = value["range"]
        sheet = next(s for s in out["sheets"].values() if s["sheet_id"] == rng["sheetId"])
        while len(sheet["rows"]) <= rng["startRowIndex"]:
            sheet["rows"].append([])
        row = sheet["rows"][rng["startRowIndex"]]
        while len(row) < rng["endColumnIndex"]:
            row.append("")
        row[rng["startColumnIndex"]:rng["endColumnIndex"]] = [
            v["userEnteredValue"]["stringValue"] for v in value["rows"][0]["values"]]
    return out


class NativeBatchTests(unittest.TestCase):
    def test_copied_config_cannot_write_into_foreign_installation(self):
        snap=snapshot();snap["sheets"]["Config"]["rows"][1][1]="another-sheet"
        with self.assertRaises(ValueError): self.plan(snap)

    def plan(self, snap=None, operation="idea-test-001", fields=None):
        return mod.reserve_insert(snap or snapshot(), "TF", operation,
             fields or {"TEMA": "Teste isolado", "TESE / CONTEXTO": "Tese de teste"},
             historical_ids=["TF_0017"], single_writer=True)

    def test_retry_after_lost_response_is_noop(self):
        snap = snapshot(); first = self.plan(snap)
        self.assertEqual(first["id"], "TF_0018")
        committed = apply(snap, first["requests"])
        repeated = self.plan(committed)
        self.assertEqual(repeated["status"], "ALREADY_COMMITTED")
        self.assertEqual(repeated["requests"], [])

    def test_same_operation_changed_payload_blocks(self):
        snap = apply(snapshot(), self.plan()["requests"])
        with self.assertRaises(ValueError):
            self.plan(snap, fields={"TEMA": "Outro", "TESE / CONTEXTO": "Tese"})

    def test_removed_idea_never_reissued(self):
        snap = apply(snapshot(), self.plan()["requests"])
        snap["sheets"]["Ideias"]["rows"] = [mod.HEADERS["Ideias"]]
        self.assertEqual(self.plan(snap)["status"], "REQUIRES_RECONCILIATION")
        new = self.plan(snap, operation="idea-test-002",
                        fields={"TEMA": "Nova", "TESE / CONTEXTO": "Tese"})
        self.assertEqual(new["id"], "TF_0019")

    def test_incomplete_history_or_unserialized_writer_blocks(self):
        snap = snapshot(); snap["history_verified_complete"] = False
        with self.assertRaises(ValueError): self.plan(snap)
        with self.assertRaises(ValueError):
            mod.reserve_insert(snapshot(), "TF", "idea-test-001", {}, historical_ids=[])

    def test_full_config_cannot_leave_partial_reservation(self):
        snap=snapshot(); snap["sheets"]["Config"]["grid_rows"]=2
        with self.assertRaises(ValueError): self.plan(snap)
        self.assertEqual(len(snap["sheets"]["Ideias"]["rows"]), 1)

    def test_conflicting_ledger_keys_block(self):
        snap=snapshot(); snap["sheets"]["Config"]["rows"] += [["KEY", "1"], ["KEY", "2"]]
        with self.assertRaises(ValueError): self.plan(snap)

    def test_promote_and_retry_keeps_source_and_origin(self):
        snap=apply(snapshot(), self.plan()["requests"])
        result=mod.reserve_insert(snap,"VD","promote-test-001",{"idea_id":"TF_0018"},
                                  historical_ids=["VD_0008"],single_writer=True)
        committed=apply(snap,result["requests"])
        self.assertEqual(committed["sheets"]["Ideias"]["rows"][1][0],"TF_0018")
        self.assertIn("IDEIA_ORIGEM_ID=TF_0018",committed["sheets"]["Produções"]["rows"][1])
        again=mod.reserve_insert(committed,"VD","promote-test-001",{"idea_id":"TF_0018"},
                                 historical_ids=[],single_writer=True)
        self.assertEqual(again["status"],"ALREADY_COMMITTED")
        committed["sheets"]["Produções"]["rows"][1][15]="IDEIA_ORIGEM_ID=TF_9999"
        changed=mod.reserve_insert(committed,"VD","promote-test-001",{"idea_id":"TF_0018"},
                                   historical_ids=[],single_writer=True)
        self.assertEqual(changed["status"],"REQUIRES_RECONCILIATION")

    def test_only_structure_is_copied_and_values_are_literal(self):
        plan=self.plan()
        copies=[r["copyPaste"]["pasteType"] for r in plan["requests"] if "copyPaste" in r]
        self.assertEqual(copies,["PASTE_FORMAT","PASTE_DATA_VALIDATION"])
        self.assertNotIn("formulaValue",str(plan["requests"]))


if __name__ == "__main__": unittest.main()
