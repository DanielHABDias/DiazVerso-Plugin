import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SOURCE=Path(__file__).resolve().parents[1]/"scripts"/"correction_loop.py"
spec=importlib.util.spec_from_file_location("diazverso_correction_loop",SOURCE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BASE="a"*64
NEW_SRC="b"*64
NEW_RENDER="c"*64

def reports():
    return [
        {"source":"J03","evidence_ref":"frames/review-v1.json","findings":[
            {"code":"LOW_TONAL_VARIATION","scene":"S01","severity":"REVIEW"},
            {"code":"ABRUPT_VISUAL_CHANGE","scene":"S02","severity":"BLOCKER"}]},
        {"source":"J04","evidence_ref":"audio/review-v1.json","findings":[
            {"code":"PCM_SAMPLE_CLIPPING","scene":"S02","severity":"BLOCKER"}]},
    ]

def state():
    return mod.collect("VD_0007",reports(),BASE)

def fix():
    return {"change_ref":"commit:abc","description":"Corrigiu um único corte identificado",
            "new_source_sha256":NEW_SRC}

def render():
    return {"render_ref":"output/scene-S02-v2.mp4","render_sha256":NEW_RENDER,
            "source_sha256":NEW_SRC,"scope":"SCENE","verified_file":True}

def recheck(task,passed=True):
    return {"review_ref":"reviews/J03-v2.json","render_sha256":NEW_RENDER,
            "reviewed_source":task["source"],"reviewed_code":task["code"],
            "reviewed_scene":task["scene"],"result":"PASSED" if passed else "FAILED",
            "review_evidence":"Inspeção da revisão da nova renderização, com evidência anexada"}

class CorrectionLoopTests(unittest.TestCase):
    def test_priority_and_single_next(self):
        s=state()
        self.assertEqual(len(s["tasks"]),3)
        self.assertEqual(s["tasks"][0]["severity"],"BLOCKER")
        self.assertEqual(mod.next_task(s)["task_id"],"FIX_0001")
        self.assertFalse(s["render_performed"])

    def test_collect_deduplicates_same_source_code_scene(self):
        rs=reports()
        rs[0]["findings"].append(rs[0]["findings"][0].copy())
        self.assertEqual(len(mod.collect("VD_0007",rs,BASE)["tasks"]),3)

    def test_full_happy_path_closes_first_only(self):
        s=state()
        first=mod.next_task(s)
        ident=first["task_id"]
        s=mod.advance(s,ident,"record_fix",fix())
        self.assertEqual(mod.next_task(s)["stage"],"FIX_APPLIED")
        s=mod.advance(s,ident,"record_rerender",render())
        s=mod.advance(s,ident,"record_recheck",recheck(first))
        s=mod.advance(s,ident,"close",{})
        self.assertEqual(s["tasks"][0]["stage"],"CLOSED")
        self.assertEqual(s["tasks"][1]["stage"],"OPEN")
        self.assertEqual(mod.summary(s)["closed"],1)
        self.assertFalse(mod.summary(s)["ready_for_creator_approval"])
        self.assertEqual(s["event_index"],4)

    def test_no_second_issue_while_first_unresolved(self):
        s=state()
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0002","record_fix",fix())

    def test_cannot_render_before_fix(self):
        s=state()
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_rerender",render())

    def test_fix_requires_change_and_source_digest(self):
        s=state()
        bad=fix();bad["new_source_sha256"]="invalid"
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_fix",bad)

    def test_rerender_must_use_fixed_source(self):
        s=mod.advance(state(),"FIX_0001","record_fix",fix())
        bad=render();bad["source_sha256"]="f"*64
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_rerender",bad)

    def test_rerender_digest_must_differ(self):
        s=mod.advance(state(),"FIX_0001","record_fix",fix())
        bad=render();bad["render_sha256"]=BASE
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_rerender",bad)

    def test_rerender_requires_file_receipt(self):
        s=mod.advance(state(),"FIX_0001","record_fix",fix())
        bad=render();bad["verified_file"]=False
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_rerender",bad)

    def test_recheck_must_reference_new_render(self):
        initial=state()
        first=mod.next_task(initial)
        s=mod.advance(initial,"FIX_0001","record_fix",fix())
        s=mod.advance(s,"FIX_0001","record_rerender",render())
        bad=recheck(first);bad["render_sha256"]=BASE
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_recheck",bad)

    def test_recheck_must_match_original_finding(self):
        first=mod.next_task(state())
        s=mod.advance(state(),"FIX_0001","record_fix",fix())
        s=mod.advance(s,"FIX_0001","record_rerender",render())
        bad=recheck(first);bad["reviewed_code"]="NOT_THE_FINDING"
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","record_recheck",bad)

    def test_failed_review_cannot_close_and_can_retry(self):
        first=mod.next_task(state())
        s=mod.advance(state(),"FIX_0001","record_fix",fix())
        s=mod.advance(s,"FIX_0001","record_rerender",render())
        s=mod.advance(s,"FIX_0001","record_recheck",recheck(first,False))
        with self.assertRaises(ValueError):
            mod.advance(s,"FIX_0001","close",{})
        s=mod.advance(s,"FIX_0001","retry",{})
        self.assertEqual(mod.next_task(s)["stage"],"OPEN")
        self.assertIsNone(s["tasks"][0]["rerender"])

    def test_pure_transition_does_not_mutate_input(self):
        s=state()
        original=json.dumps(s,sort_keys=True)
        mod.advance(s,"FIX_0001","record_fix",fix())
        self.assertEqual(original,json.dumps(s,sort_keys=True))

    def test_unsupported_transition_rejected(self):
        with self.assertRaises(ValueError):
            mod.advance(state(),"FIX_0001","close",{})

    def test_no_findings_is_ready_for_review_not_approved(self):
        s=mod.collect("SH_0010",[{"source":"J03","evidence_ref":"review.json","findings":[]}],BASE)
        out=mod.summary(s)
        self.assertEqual(out["status"],"ALL_ISSUES_CLOSED")
        self.assertFalse(out["creator_approved"])
        self.assertFalse(out["publishing_performed"])

    def test_invalid_original_report_rejected(self):
        with self.assertRaises(ValueError):
            mod.collect("VD_0007",[{"source":"OTHER","evidence_ref":"foo","findings":[]}],BASE)


if __name__=="__main__":
    unittest.main()
