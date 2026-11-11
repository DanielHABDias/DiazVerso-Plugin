import importlib.util
import tempfile
import unittest
import wave
from pathlib import Path
spec = importlib.util.spec_from_file_location("original_sfx", Path(__file__).resolve().parents[1]/"scripts/build_original_sfx.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


class OriginalSfxTests(unittest.TestCase):
    def test_actual_pcm_duration_levels_and_safe_envelope(self):
        for name, seconds in mod.SPECS.items():
            pcm = mod.samples(name)
            self.assertEqual(len(pcm), round(seconds*mod.RATE))
            self.assertEqual(pcm[0], 0); self.assertEqual(pcm[-1], 0)
            self.assertLessEqual(max(map(abs, pcm)), 10486)
            self.assertGreater(sum(v*v for v in pcm), 0)

    def test_reproducible_bytes_and_no_false_approval(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            first, second = mod.build(Path(a)), mod.build(Path(b))
            self.assertEqual(first, second)
            self.assertFalse(first["listening_performed"])
            self.assertFalse(first["editorially_approved"])
            for item in first["assets"]:
                with wave.open(str(Path(a)/item["name"]), "rb") as reader:
                    self.assertEqual(reader.getnframes()/reader.getframerate(),item["duration_seconds"])
            with self.assertRaises(FileExistsError): mod.build(Path(a))


if __name__ == "__main__": unittest.main()
