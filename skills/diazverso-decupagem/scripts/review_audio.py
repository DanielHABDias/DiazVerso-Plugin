#!/usr/bin/env python3
"""J04 - real PCM WAV technical inspection, plus cue-plan consistency checks.

Input: locally supplied 16-bit PCM WAV, with optional verified voice/music/SFX
timelines. Computes sample peak, RMS, clipping and low-energy intervals;
does NOT transcribe, listen, infer intent, certify sync, or publish media.
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import sys
import wave
from pathlib import Path

PCM16_MAX = 32768.0
CLIP_THRESHOLD = 32760


def _finite(value: object) -> bool:
    return type(value) in (float, int) and math.isfinite(value)


def _intervals(items: list, duration: float, label: str) -> list[dict]:
    if not isinstance(items, list):
        raise ValueError(f"{label} must be a list")
    result = []
    for item in items:
        if not isinstance(item, dict) or set(item) != {"start_s", "end_s"}:
            raise ValueError(f"Invalid {label} interval")
        start, end = item["start_s"], item["end_s"]
        if not _finite(start) or not _finite(end) or start < 0 or end <= start or end > duration + 0.001:
            raise ValueError(f"{label} interval is out of range")
        if result and start < result[-1]["end_s"]:
            raise ValueError(f"{label} intervals must be sorted and nonoverlapping")
        result.append({"start_s": float(start), "end_s": float(end)})
    return result


def review(wav_path: Path, *, voice: list | None = None,
           music: list | None = None, sfx: list | None = None,
           silence_dbfs: float = -48.0, pause_seconds: float = 0.50) -> dict:
    if not _finite(silence_dbfs) or not -90 <= silence_dbfs <= -12:
        raise ValueError("silence_dbfs must be -90..-12")
    if not _finite(pause_seconds) or not 0.1 <= pause_seconds <= 10:
        raise ValueError("pause_seconds must be 0.1..10")
    if wav_path.suffix.lower() != ".wav" or not wav_path.is_file():
        raise ValueError("A real, local WAV file is required")
    try:
        reader = wave.open(str(wav_path), "rb")
    except (wave.Error, EOFError, OSError) as exc:
        raise ValueError("Invalid WAV file") from exc
    with reader as audio:
        if audio.getcomptype() != "NONE" or audio.getsampwidth() != 2 or audio.getnchannels() not in (1, 2):
            raise ValueError("Only uncompressed 16-bit PCM mono/stereo WAV supported")
        channels, rate, count = audio.getnchannels(), audio.getframerate(), audio.getnframes()
        if rate < 8000 or rate > 192000 or count == 0:
            raise ValueError("Unsupported sample rate or empty recording")
        duration = count / rate
        voice_events = _intervals(voice if voice is not None else [], duration, "voice")
        music_events = _intervals(music if music is not None else [], duration, "music")
        sfx_events = _intervals(sfx if sfx is not None else [], duration, "sfx")
        # Analyze in small deterministic windows; do not load entire large media.
        frames_per_window = max(1, round(rate * 0.05))
        total_squares = 0.0
        peak = 0
        clipped = 0
        total_samples = 0
        windows = []
        position = 0
        while position < count:
            raw = audio.readframes(min(frames_per_window, count-position))
            n = len(raw)//2
            if n == 0:
                raise ValueError("Truncated audio samples")
            if len(raw) != n*2 or n%channels:
                raise ValueError("Malformed PCM sample block")
            samples = struct.unpack("<" + "h"*n, raw)
            squares = sum(sample * sample for sample in samples)
            total_squares += squares
            clipped += sum(1 for x in samples if abs(x) >= CLIP_THRESHOLD)
            peak = max(peak, max(abs(x) for x in samples))
            total_samples += n
            window_rms = math.sqrt(squares/n)/PCM16_MAX
            db = 20 * math.log10(window_rms) if window_rms else -120.0
            actual_frames = n//channels
            windows.append({"start_s": position/rate, "end_s": (position+actual_frames)/rate,
                            "rms_dbfs": round(db, 2)})
            position += actual_frames

    rms = math.sqrt(total_squares/total_samples)/PCM16_MAX
    rms_db = 20*math.log10(rms) if rms else -120.0
    peak_db = 20*math.log10(peak/PCM16_MAX) if peak else -120.0
    clipping_fraction = clipped/total_samples
    issues = []
    if clipped:
        issues.append({"severity":"BLOCKER","code":"PCM_SAMPLE_CLIPPING",
                       "evidence":{"clipped_samples":clipped,"fraction":round(clipping_fraction,6)},
                       "message":"PCM samples reach the near-full-scale threshold; inspect the master"})
    if rms_db < -40:
        issues.append({"severity":"REVIEW","code":"LOW_OVERALL_LEVEL",
                       "evidence":{"rms_dbfs":round(rms_db,2)},
                       "message":"Very quiet mix; verify voice audibility and intended silence"})

    # Silence is a measurable low-energy window, NOT a detected speech pause.
    low = []
    streak_start = None
    for w in windows:
        if w["rms_dbfs"] <= silence_dbfs:
            if streak_start is None:
                streak_start = w["start_s"]
        elif streak_start is not None:
            if w["start_s"]-streak_start >= pause_seconds:
                low.append({"start_s":round(streak_start,3),"end_s":round(w["start_s"],3)})
            streak_start = None
    if streak_start is not None and duration-streak_start >= pause_seconds:
        low.append({"start_s":round(streak_start,3),"end_s":round(duration,3)})
    for gap in low:
        overlap = any(gap["start_s"] < v["end_s"] and gap["end_s"] > v["start_s"] for v in voice_events)
        if overlap:
            issues.append({"severity":"REVIEW","code":"LOW_ENERGY_DURING_PLANNED_VOICE",
                           "evidence":gap,
                           "message":"Low-energy interval overlaps scheduled voice; inspect audio and timing"})
    # A fully low-energy expected music/SFX interval is a reproducible
    # discrepancy, but energy alone cannot identify which source played.
    for label, events in (("music", music_events), ("sfx", sfx_events)):
        for event in events:
            matching = [w for w in windows if w["start_s"] < event["end_s"]
                        and w["end_s"] > event["start_s"]]
            if matching and all(w["rms_dbfs"] <= silence_dbfs for w in matching):
                issues.append({"severity": "REVIEW",
                               "code": "LOW_ENERGY_DURING_PLANNED_" + label.upper(),
                               "evidence": event,
                               "message": "Expected audio segment has low measured energy; verify timeline and mix"})
    # Plan gaps are not proof that music or SFX can be heard after the mix.
    for label, events in (("music",music_events),("sfx",sfx_events)):
        if events and not voice_events:
            issues.append({"severity":"REVIEW","code":"NO_VOICE_TIMELINE_FOR_"+label.upper(),
                           "evidence":{"event_count":len(events)},
                           "message":"Cannot evaluate ducking or sync without a voice timeline"})

    return {"status":"REVIEW_REQUIRED" if issues else "NO_SIGNAL_RULE_FINDINGS",
            "path":str(wav_path.resolve()),"channels":channels,"sample_rate":rate,
            "duration_seconds":round(duration,3),
            "peak_dbfs":round(peak_db,2),"rms_dbfs":round(rms_db,2),
            "clipped_samples":clipped,"clipped_fraction":round(clipping_fraction,6),
            "low_energy_intervals":low,"voice_intervals_checked":len(voice_events),
            "music_intervals_checked":len(music_events),"sfx_intervals_checked":len(sfx_events),
            "issues":issues,"audio_listened":False,"speech_recognition_performed":False,
            "voice_sync_verified":False,"creative_mix_approved":False,
            "publishing_performed":False,"writes_performed":False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    parser.add_argument("--cues", type=Path, help="JSON with voice/music/sfx interval arrays")
    args = parser.parse_args()
    try:
        cues = json.loads(args.cues.read_text("utf-8")) if args.cues else {}
        if not isinstance(cues, dict) or set(cues)-{"voice","music","sfx"}:
            raise ValueError("Cues JSON must contain only voice/music/sfx arrays")
        result = review(args.wav, **cues)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,TypeError,KeyError) as exc:
        print(f"AUDIO_REVIEW_FAILED: {exc}",file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
