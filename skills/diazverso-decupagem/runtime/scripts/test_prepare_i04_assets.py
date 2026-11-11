"""Focused I04 tests, no Remotion install or external audio involved."""
import importlib.util
import struct
import tempfile
import unittest
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prepare_i04_assets", HERE / "prepare_i04_assets.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
REPO = HERE.parents[3]


class PrepareI04Tests(unittest.TestCase):
    def test_can_verify_real_canonical_asset(self):
        nox = module.verify_nox(REPO)
        self.assertEqual(nox.name, "Nox.png")
        self.assertEqual(nox.stat().st_size, 415179)

    def test_whoosh_is_deterministic_mono_pcm_and_not_clipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.wav", Path(tmp) / "b.wav"
            module.build_original_whoosh(a)
            module.build_original_whoosh(b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with wave.open(str(a), "rb") as wav:
                self.assertEqual((wav.getnchannels(), wav.getsampwidth(), wav.getframerate()), (1, 2, 48000))
                self.assertEqual(wav.getnframes(), 57600)
                values = struct.unpack("<" + "h" * wav.getnframes(), wav.readframes(wav.getnframes()))
            self.assertGreater(max(abs(v) for v in values), 700)
            self.assertLess(max(abs(v) for v in values), 32000)
            self.assertLess(max(abs(v) for v in values[:100]), 5)
            self.assertLess(max(abs(v) for v in values[-100:]), 5)

    def test_prepare_copies_byte_identical_nox(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = module.prepare(REPO, out)
            self.assertEqual((out / "i04-nox-canonical.png").read_bytes(),
                             (REPO / "assets/brand/nox/Nox.png").read_bytes())
            self.assertTrue((out / "i04-whoosh-original.wav").is_file())
            self.assertEqual(result["source_blob_sha1"], "776d1b26983e6f9095178881c83b44f114a40336")


if __name__ == "__main__":
    unittest.main()
