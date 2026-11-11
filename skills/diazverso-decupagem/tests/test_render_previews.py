"""H08: unit/integration-with-fake-CLI tests; never render a real video."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "diazverso_render_previews", ROOT / "scripts" / "render_previews.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return json.loads((ROOT / "examples" / "short-remotion-props.example.json").read_text("utf-8"))


class RenderPreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.props = self.base / "props.json"
        self.props.write_text(json.dumps(sample()), encoding="utf-8")
        self.entry = self.base / "src" / "index.tsx"
        self.entry.parent.mkdir()
        self.entry.write_text("// independent runtime placeholder", encoding="utf-8")
        self.out = self.base / "output"

    def plan(self, data=None):
        if data is not None:
            self.props.write_text(json.dumps(data), encoding="utf-8")
        return mod.build_plan(data or sample(), self.props, self.entry, "DiazversoShort", self.out)

    def test_two_scenes_get_two_clips_six_frames(self):
        p = self.plan()
        self.assertEqual(p["scene_count"], 2)
        self.assertEqual(sum(len(s["steps"]) for s in p["scenes"]), 8)
        self.assertEqual([x["range"] for x in p["scenes"]], [[0, 89], [90, 179]])
        self.assertFalse(p["writes_performed"])
        self.assertFalse(self.out.exists())

    def test_commands_use_absolute_entry_props_and_frame_flags(self):
        p = self.plan()
        clip = p["scenes"][0]["steps"][0]["command"]
        still = p["scenes"][0]["steps"][1]["command"]
        self.assertEqual(clip[:4], ["npx", "--no-install", "remotion", "render"])
        self.assertIn("--frames=0-89", clip)
        self.assertIn("--overwrite=false", clip)
        self.assertIn("--frame=0", still)
        self.assertIn(f"--props={self.props.resolve()}", still)

    def test_untrusted_composition_id_rejected(self):
        with self.assertRaises(ValueError):
            mod.build_plan(sample(), self.props, self.entry, "Comp;rm -rf /", self.out)

    def test_invalid_schema_blocks_plan(self):
        data = sample()
        data["scenes"][1]["start_frame"] = 200
        with self.assertRaises(ValueError):
            self.plan(data)

    def test_fake_cli_writes_expected_files_and_records_evidence(self):
        p = self.plan()
        def fake_run(cmd, **kwargs):
            # Uses the expected output argument from our CLI shape.
            target = Path(cmd[6])
            target.write_bytes(b"synthetic-pretend-render")
            return SimpleNamespace(returncode=0, stderr="")
        with patch.object(mod.shutil, "which", return_value="/usr/bin/npx"), patch.object(
                mod.subprocess, "run", side_effect=fake_run) as call:
            result = mod.execute_plan(p)
        self.assertEqual(call.call_count, 8)
        self.assertEqual(len(result["outputs"]), 8)
        self.assertTrue(result["render_verified"])
        self.assertFalse(result["visual_qa_verified"])
        self.assertFalse(result["final_render_performed"])
        self.assertFalse(result["publishing_performed"])

    def test_refuses_to_overwrite_prior_outputs(self):
        p = self.plan()
        f = Path(p["scenes"][0]["steps"][0]["output"])
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b"previous")
        with patch.object(mod.shutil, "which", return_value="/usr/bin/npx"), self.assertRaises(FileExistsError):
            mod.execute_plan(p)
        self.assertEqual(f.read_bytes(), b"previous")

    def test_missing_npx_fails_before_writing(self):
        with patch.object(mod.shutil, "which", return_value=None), self.assertRaises(RuntimeError):
            mod.execute_plan(self.plan())
        self.assertFalse(self.out.exists())

    def test_failure_stops_and_does_not_claim_success(self):
        with patch.object(mod.shutil, "which", return_value="/usr/bin/npx"), patch.object(
                mod.subprocess, "run", return_value=SimpleNamespace(returncode=1, stderr="No Remotion")) as call:
            with self.assertRaises(RuntimeError):
                mod.execute_plan(self.plan())
        self.assertEqual(call.call_count, 1)

    def test_timeout_rejected(self):
        with self.assertRaises(ValueError):
            mod.execute_plan(self.plan(), timeout_s=0)

    def test_execution_uses_independent_project_cwd(self):
        p = self.plan()
        expected_cwd = str(self.entry.parent.resolve())
        def fake_run(cmd, **kwargs):
            self.assertEqual(kwargs["cwd"], expected_cwd)
            Path(cmd[6]).write_bytes(b"synthetic-render-output")
            return SimpleNamespace(returncode=0, stderr="")
        with patch.object(mod.shutil, "which", return_value="/usr/bin/npx"), patch.object(
                mod.subprocess, "run", side_effect=fake_run):
            result = mod.execute_plan(p)
        self.assertEqual(len(result["outputs"]), 8)

    def test_no_shell_execution(self):
        p = self.plan()
        self.assertTrue(all(isinstance(x["command"], list)
                            for s in p["scenes"] for x in s["steps"]))


if __name__ == "__main__":
    unittest.main()
