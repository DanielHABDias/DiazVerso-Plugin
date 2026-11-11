"""J04: actual PCM synthesis in temp files; never claims listening to a video."""
import importlib.util
import json
import math
import struct
import tempfile
import unittest
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("diazverso_audio_review",ROOT/"scripts"/"review_audio.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class AudioReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.wav=Path(self.tmp.name)/"test.wav"

    def make_wav(self,samples,rate=8000,channels=1):
        with wave.open(str(self.wav),"wb") as writer:
            writer.setnchannels(channels)
            writer.setsampwidth(2)
            writer.setframerate(rate)
            writer.writeframes(struct.pack("<"+"h"*len(samples),*samples))

    def test_normal_signal_metrics_no_fake_listening(self):
        self.make_wav([int(10000*math.sin(i*2*math.pi*220/8000)) for i in range(8000)])
        r=mod.review(self.wav)
        self.assertEqual(r["sample_rate"],8000)
        self.assertEqual(r["duration_seconds"],1.0)
        self.assertEqual(r["clipped_samples"],0)
        self.assertFalse(r["audio_listened"])
        self.assertFalse(r["voice_sync_verified"])
        self.assertFalse(r["publishing_performed"])

    def test_fullscale_samples_signal_clipping(self):
        self.make_wav([32767,-32768]*4000)
        r=mod.review(self.wav)
        self.assertEqual(r["status"],"REVIEW_REQUIRED")
        self.assertIn("PCM_SAMPLE_CLIPPING",[x["code"] for x in r["issues"]])

    def test_silence_detected_in_real_waveform(self):
        self.make_wav([0]*8000)
        r=mod.review(self.wav)
        self.assertTrue(any(x["start_s"]==0 for x in r["low_energy_intervals"]))
        self.assertLessEqual(r["rms_dbfs"],-100)

    def test_low_energy_overlaps_planned_voice(self):
        self.make_wav([0]*8000)
        r=mod.review(self.wav,voice=[{"start_s":0.2,"end_s":0.8}])
        self.assertIn("LOW_ENERGY_DURING_PLANNED_VOICE",[x["code"] for x in r["issues"]])

    def test_voice_schedule_cannot_prove_sync(self):
        self.make_wav([1000]*8000)
        r=mod.review(self.wav,voice=[{"start_s":0,"end_s":1}])
        self.assertEqual(r["voice_intervals_checked"],1)
        self.assertFalse(r["voice_sync_verified"])

    def test_music_without_voice_marks_ducking_review(self):
        self.make_wav([500]*8000)
        r=mod.review(self.wav,music=[{"start_s":0,"end_s":0.9}])
        self.assertIn("NO_VOICE_TIMELINE_FOR_MUSIC",[x["code"] for x in r["issues"]])

    def test_overlapping_sfx_cues_rejected(self):
        self.make_wav([100]*8000)
        with self.assertRaises(ValueError):
            mod.review(self.wav,sfx=[
                {"start_s":0.1,"end_s":0.5},{"start_s":0.4,"end_s":0.8}])

    def test_stereo_supported(self):
        self.make_wav([1000,-1000]*8000,channels=2)
        r=mod.review(self.wav)
        self.assertEqual(r["channels"],2)
        self.assertEqual(r["duration_seconds"],1)

    def test_8bit_pcm_explicitly_unsupported(self):
        with wave.open(str(self.wav),"wb") as w:
            w.setnchannels(1);w.setsampwidth(1);w.setframerate(8000)
            w.writeframes(bytes([128]*8000))
        with self.assertRaises(ValueError):
            mod.review(self.wav)

    def test_empty_and_invalid_wav_rejected(self):
        self.wav.write_bytes(b"not a wave")
        with self.assertRaises(ValueError):
            mod.review(self.wav)

    def test_out_of_bounds_voice_rejected(self):
        self.make_wav([0]*8000)
        with self.assertRaises(ValueError):
            mod.review(self.wav,voice=[{"start_s":0.5,"end_s":2}])

    def test_invalid_threshold_rejected(self):
        self.make_wav([0]*8000)
        with self.assertRaises(ValueError):
            mod.review(self.wav,silence_dbfs=0)

    def test_silent_expected_sfx_is_flagged(self):
        self.make_wav([0]*8000)
        result=mod.review(self.wav,sfx=[{"start_s":0.2,"end_s":0.4}])
        self.assertIn("LOW_ENERGY_DURING_PLANNED_SFX",
                      [x["code"] for x in result["issues"]])

    def test_silent_expected_music_is_flagged(self):
        self.make_wav([0]*8000)
        result=mod.review(self.wav,music=[{"start_s":0.1,"end_s":0.9}])
        self.assertIn("LOW_ENERGY_DURING_PLANNED_MUSIC",
                      [x["code"] for x in result["issues"]])

    def test_wrong_timeline_container_rejected(self):
        self.make_wav([0]*8000)
        with self.assertRaises(ValueError):
            mod.review(self.wav,voice={})

    def test_still_no_write_to_original(self):
        self.make_wav([250]*8000)
        before=self.wav.read_bytes()
        mod.review(self.wav)
        self.assertEqual(before,self.wav.read_bytes())


if __name__=="__main__":
    unittest.main()
