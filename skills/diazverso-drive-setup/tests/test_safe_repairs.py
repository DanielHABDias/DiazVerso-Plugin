"""E03/E04: synthetic readback fixtures; absolutely no connected writes."""
import importlib.util
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]/"scripts"

def load(filename,name):
    spec=importlib.util.spec_from_file_location(name, BASE/filename)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

drive=load("discover_structure.py","safe_drive")
sheets=load("validate_sheet_schema.py","safe_sheets")

def action():
    return {"operation":"CREATE_FOLDER_IF_STILL_MISSING",
            "path":"Roteiros/Shorts","name":"Shorts",
            "parent_id":"roteiros-verified","requires_authorization":True,
            "requires_readback":True}

def parent():
    return {"parent_id":"roteiros-verified","parent_mime":drive.FOLDER,
            "complete":True,"new_read":True,"pages":[{"results":[]}]}

def schema():
    return {"sheets":[{"properties":{"title":name,"sheetId":idx+1,
                      "gridProperties":{"frozenRowCount":1},"hidden":name=="Config"}}
                      for idx,name in enumerate(sheets.HEADERS)],
            "headers":{k:list(v) for k,v in sheets.HEADERS.items()}}

class DriveSafeRepairTests(unittest.TestCase):
    def test_valid_fresh_parent_still_waits_for_authorization(self):
        r=drive.preflight_folder_create(action(),fresh_parent=parent())
        self.assertEqual(r["status"],"AWAITING_EXPLICIT_AUTHORIZATION")
        self.assertFalse(r["writes_performed"])
    def test_fresh_parent_and_approval_only_allow_attempt(self):
        r=drive.preflight_folder_create(action(),fresh_parent=parent(),authorized=True)
        self.assertEqual(r["status"],"SAFE_TO_ATTEMPT_CREATE_NOW")
        self.assertFalse(r["writes_performed"])
        self.assertIn("readback",r["mandatory_after_action"])
    def test_concurrent_existing_folder_prevents_duplicate(self):
        p=parent()
        p["pages"][0]["results"]=[{"id":"already","name":"Shorts",
                                   "mimeType":drive.FOLDER,"parents":["roteiros-verified"]}]
        self.assertEqual(drive.preflight_folder_create(action(),fresh_parent=p,authorized=True)["status"],
                         "BLOCKED_ALREADY_EXISTS_OR_CONFLICT")
    def test_same_name_wrong_mime_prevents_duplicate(self):
        p=parent()
        p["pages"][0]["results"]=[{"id":"conflict","name":"Shorts",
                                   "mimeType":"text/plain","parents":["roteiros-verified"]}]
        self.assertEqual(drive.preflight_folder_create(action(),fresh_parent=p,authorized=True)["status"],
                         "BLOCKED_ALREADY_EXISTS_OR_CONFLICT")
    def test_stale_or_wrong_parent_blocked(self):
        p=parent();p["new_read"]=False
        self.assertEqual(drive.preflight_folder_create(action(),fresh_parent=p,authorized=True)["status"],
                         "BLOCKED_PARENT_NOT_VERIFIED")
    def test_incomplete_pagination_blocked(self):
        p=parent();p["complete"]=False
        with self.assertRaises(ValueError):
            drive.preflight_folder_create(action(),fresh_parent=p,authorized=True)
    def test_wrong_path_rejected(self):
        a=action();a["path"]="Roteiros/Longos"
        with self.assertRaises(ValueError):drive.preflight_folder_create(a,fresh_parent=parent())

class SheetSafeRepairTests(unittest.TestCase):
    def test_clean_sheet_no_repair(self):
        result=sheets.plan_safe_metadata_repairs(schema())
        self.assertEqual(result["status"],"NO_SAFE_REPAIR_NEEDED")
        self.assertFalse(result["writes_performed"])
    def test_single_header_freeze_request_is_field_scoped(self):
        data=schema()
        data["sheets"][0]["properties"]["gridProperties"]["frozenRowCount"]=0
        result=sheets.plan_safe_metadata_repairs(data)
        self.assertEqual(len(result["requests"]),1)
        request=result["requests"][0]["updateSheetProperties"]
        self.assertEqual(request["fields"],"gridProperties.frozenRowCount")
        self.assertEqual(request["properties"]["sheetId"],1)
    def test_config_hide_request_is_field_scoped(self):
        data=schema()
        data["sheets"][3]["properties"]["hidden"]=False
        result=sheets.plan_safe_metadata_repairs(data)
        self.assertEqual(result["requests"][0]["updateSheetProperties"]["fields"],"hidden")
    def test_header_mismatch_blocks_all_repairs(self):
        data=schema()
        data["headers"]["Ideias"][0]="WRONG"
        data["sheets"][3]["properties"]["hidden"]=False
        result=sheets.plan_safe_metadata_repairs(data)
        self.assertEqual(result["status"],"BLOCKED_UNSAFE_SCHEMA")
        self.assertEqual(result["requests"],[])
    def test_missing_sheet_id_invalid(self):
        data=schema()
        del data["sheets"][1]["properties"]["sheetId"]
        with self.assertRaises(ValueError):sheets.plan_safe_metadata_repairs(data)
    def test_does_not_claim_dropdown_filter_or_style_audited(self):
        result=sheets.plan_safe_metadata_repairs(schema())
        self.assertEqual(result["validation_not_performed"],
                         ["dropdowns","filters","cell_formatting"])

if __name__=="__main__":unittest.main()
