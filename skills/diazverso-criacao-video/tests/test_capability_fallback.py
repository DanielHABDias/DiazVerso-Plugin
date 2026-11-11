"""L05: no-capability and partial capability matrices, no external actions."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"capability_fallback.py"
spec=importlib.util.spec_from_file_location("fallback",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def snapshot(**changes):
    caps={name: False for name in mod.CAPABILITIES}
    caps.update(changes)
    return {"session_id":"test-session","verified_at":"2026-11-11T09:00:00-03:00",
            "capabilities":caps}


class FallbackTests(unittest.TestCase):
    def test_no_services_still_allows_local_editorial_planning(self):
        r=mod.evaluate(snapshot(),["ideation","draft_script_local","draft_thumbnail_brief"])
        self.assertEqual(r["status"],"CAPABILITY_PLAN_ONLY")
        self.assertEqual(len(r["available"]),3)
        self.assertFalse(r["host_actions_performed"])

    def test_all_external_work_fails_closed_without_connectors(self):
        external=["discover_drive","read_sheet","create_native_doc","write_production_row",
                  "render_preview","extract_frames","analyze_with_earshot"]
        r=mod.evaluate(snapshot(),external)
        self.assertEqual(r["status"],"DEGRADED")
        self.assertEqual(r["blocked"],external)
        self.assertTrue(all(not x["performed"] for x in r["actions"]))

    def test_drive_read_does_not_imply_write(self):
        r=mod.evaluate(snapshot(drive_read=True),
                       ["discover_drive","create_native_doc"])
        self.assertEqual(r["available"],["discover_drive"])
        self.assertEqual(r["blocked"],["create_native_doc"])

    def test_write_production_needs_read_and_write(self):
        r=mod.evaluate(snapshot(sheets_write=True),["write_production_row"])
        self.assertEqual(r["actions"][0]["missing"],["sheets_read"])
        self.assertEqual(r["actions"][0]["evidence_required"],"SHEET_WRITE_AND_READBACK")

    def test_render_without_ffmpeg_still_allows_preview_not_extraction(self):
        r=mod.evaluate(snapshot(render_runtime=True),
                       ["plan_render_commands","render_preview","extract_frames"])
        self.assertEqual(r["available"],["plan_render_commands","render_preview"])
        self.assertIn("extract_frames",r["blocked"])
        self.assertFalse(r["actions"][1]["completed"])

    def test_ffmpeg_does_not_imply_remotion(self):
        r=mod.evaluate(snapshot(ffmpeg=True),["render_preview","extract_frames"])
        self.assertEqual(r["available"],["extract_frames"])
        self.assertEqual(r["blocked"],["render_preview"])

    def test_earshot_absence_does_not_block_local_wav_inspection(self):
        r=mod.evaluate(snapshot(),["inspect_local_wav_pcm16","analyze_with_earshot"])
        self.assertEqual(r["available"],["inspect_local_wav_pcm16"])
        self.assertEqual(r["blocked"],["analyze_with_earshot"])

    def test_earshot_presence_requires_real_run_and_consent(self):
        r=mod.evaluate(snapshot(earshot=True),["analyze_with_earshot"])
        a=r["actions"][0]
        self.assertEqual(a["status"],"AVAILABLE_FOR_ATTEMPT")
        self.assertEqual(a["evidence_required"],"EARSHOT_ACTUAL_RUN_AND_USER_AUTHORIZATION")
        self.assertFalse(a["performed"])

    def test_connector_presence_never_claims_doc_written(self):
        r=mod.evaluate(snapshot(drive_write=True,docs_write=True),["create_native_doc"])
        self.assertEqual(r["available"],["create_native_doc"])
        self.assertFalse(r["actions"][0]["completed"])
        self.assertFalse(r["actions"][0]["performed"])

    def test_unknown_or_posting_action_rejected(self):
        with self.assertRaises(ValueError):
            mod.evaluate(snapshot(),["post_video"])

    def test_incomplete_capabilities_rejected(self):
        s=snapshot()
        del s["capabilities"]["ffmpeg"]
        with self.assertRaises(ValueError):
            mod.evaluate(s,["ideation"])

    def test_string_approval_capability_rejected(self):
        s=snapshot()
        s["capabilities"]["drive_read"]="true"
        with self.assertRaises(ValueError):
            mod.evaluate(s,["discover_drive"])

    def test_duplicate_requests_deduplicated_in_order(self):
        r=mod.evaluate(snapshot(),["ideation","ideation","render_preview"])
        self.assertEqual([x["action"] for x in r["actions"]],
                         ["ideation","render_preview"])

    def test_no_capability_inference_from_other_tools(self):
        r=mod.evaluate(snapshot(drive_read=True,sheets_read=False),["read_sheet"])
        self.assertEqual(r["blocked"],["read_sheet"])

    def test_no_video_publication_even_all_true(self):
        full=snapshot(**{name:True for name in mod.CAPABILITIES})
        r=mod.evaluate(full,["write_production_row","render_preview",
                             "analyze_with_earshot"])
        self.assertFalse(r["publishing_performed"])
        self.assertTrue(r["creator_approval_required"])
        self.assertEqual(r["status"],"CAPABILITY_PLAN_ONLY")


if __name__=="__main__":
    unittest.main()
