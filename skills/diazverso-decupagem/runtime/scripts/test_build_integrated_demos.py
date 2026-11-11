"""Focused integration builder tests using generated WAV fixtures, not fake CI renders."""
from __future__ import annotations
import importlib.util
import json
import struct
import tempfile
import unittest
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("integrated", HERE/"build_integrated_demos.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def synth_fixture(_text: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(struct.pack("<h", 200) * 16000)


class IntegratedDemosTests(unittest.TestCase):
    def test_both_formats_generate_h01_contract_and_measured_caption_cues(self):
        fixture = builder.read_fixture(builder.RUNTIME/"fixtures/integrated-demos.json")
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for kind,prefix in [("LONGO","l02"),("SHORT","l03")]:
                result=builder.build_one(kind,fixture[kind],public=root/"public",out=root/"out",
                                         synth=synth_fixture)
                contract=json.loads((root/"out"/f"{prefix}-h01.json").read_text())
                plan=json.loads((root/"out"/f"{prefix}-input.json").read_text())["plan"]
                evidence=json.loads((root/"out"/f"{prefix}-timing-evidence.json").read_text())
                self.assertEqual(result["validated"],"VALID_CONTRACT")
                self.assertTrue(plan["demo_only"])
                self.assertFalse(plan["editorial_approved"])
                self.assertEqual(contract["duration_frames"],plan["duration_frames"])
                self.assertEqual(len(evidence["audio_evidence"]),len(plan["scenes"]))
                for scene in plan["scenes"]:
                    self.assertEqual(scene["caption"]["duration_frames"],30)
                    self.assertEqual(scene["voice_duration_frames"],30)
                    self.assertEqual(scene["caption"]["start_frame"],scene["voice_start_frame"])
                srt=(root/"out"/f"{prefix}-captions.srt").read_text()
                self.assertIn("00:00:",srt)
                self.assertIn(plan["scenes"][0]["narration"],srt)
            self.assertTrue(plan["scenes"][-1]["cta"])

    def test_fails_if_voice_longer_than_scene(self):
        fixture=builder.read_fixture(builder.RUNTIME/"fixtures/integrated-demos.json")
        entry=dict(fixture["LONGO"],frames_per_scene=75)
        def long_voice(_text, path):
            with wave.open(str(path),"wb") as wav:
                wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(16000)
                wav.writeframes(b"\x00\x00"*(16000*3))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"overflows scene"):
                builder.build_one("LONGO",entry,public=Path(tmp)/"public",
                                  out=Path(tmp)/"out",synth=long_voice)

    def test_short_without_contextual_cta_is_rejected(self):
        fixture=builder.read_fixture(builder.RUNTIME/"fixtures/integrated-demos.json")
        bad={**fixture["SHORT"],"scenes":[dict(s) for s in fixture["SHORT"]["scenes"]]}
        bad["scenes"][-1]["cta"]=False
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"CTA"):
                builder.build_one("SHORT",bad,public=Path(tmp)/"public",
                                  out=Path(tmp)/"out",synth=synth_fixture)

    def test_srt_time_rounds_from_frames_not_guessed_word_times(self):
        self.assertEqual(builder.srt_timestamp(15,30),"00:00:00,500")
        self.assertEqual(builder.srt_timestamp(45,30),"00:00:01,500")


if __name__ == "__main__":
    unittest.main()
