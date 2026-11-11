#!/usr/bin/env python3
"""L02/L03: original test script -> timed offline TTS -> H01 decoupage -> Remotion props.

No service credentials, browser, publication, Content Lab, private user speech,
or third-party music. Uses available eSpeak CLI or dev-only meSpeak (GPL) in the independent runner.
The speech/captions are generated from the SAME source and measured WAV length;
this is an integration proof, not verified natural narration or human approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "skills/diazverso-decupagem/scripts"))
from validate_composition import validate  # type: ignore  # noqa: E402

TIMING_OFFSET_FRAMES = 5
MAX_TEXT_CHARS = 150


def read_fixture(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "diazverso-integrated-demo-v1":
        raise ValueError("Unknown fixture schema")
    return data


def wav_frames(path: Path, fps: int) -> tuple[int, dict]:
    with wave.open(str(path), "rb") as reader:
        params = {
            "channels": reader.getnchannels(),
            "sample_width": reader.getsampwidth(),
            "rate": reader.getframerate(),
            "samples": reader.getnframes(),
        }
    if params["channels"] != 1 or params["sample_width"] != 2 or params["rate"] < 8000:
        raise ValueError("Unexpected eSpeak WAV format")
    return math.ceil(params["samples"] * fps / params["rate"]), params


def make_tts(text: str, output: Path) -> None:
    if not text.strip() or len(text) > MAX_TEXT_CHARS or any(ch in text for ch in "\r\n"):
        raise ValueError("Invalid test narration")
    if shutil.which("espeak-ng"):
        cmd = ["espeak-ng", "-v", "pt-br", "-s", "205", "-p", "52", "-w", str(output), text]
    elif shutil.which("espeak"):
        cmd = ["espeak", "-v", "pt-br", "-s", "205", "-p", "52", "-w", str(output), text]
    else:
        # CI fallback: dev-only meSpeak package (GPL); neither the library nor
        # its voice data is included in the Diazverso ZIP. Output is a TEST.
        js = ("const m=require('mespeak');"
              "m.loadConfig(require('mespeak/mespeak_config.json'));"
              "m.loadVoice(require('mespeak/voices/pt.json'));"
              "const wav=m.speak(process.argv[2],{rawdata:'buffer',speed:205,pitch:52});"
              "if(!Buffer.isBuffer(wav)||wav.length<512)throw Error('no speech output');"
              "require('fs').writeFileSync(process.argv[1],wav);")
        cmd = ["node", "-e", js, str(output), text]
    try:
        subprocess.run(cmd, check=True, timeout=35, capture_output=True, cwd=RUNTIME)
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or b"").decode("utf-8", errors="replace")[-1200:]
        raise RuntimeError(f"Offline test TTS failed ({cmd[0]}): {message}") from exc
    if not output.is_file() or output.stat().st_size < 512:
        raise RuntimeError("TTS did not produce a WAV")


def srt_timestamp(frame: int, fps: int) -> str:
    # SRT is rounded to nearest millisecond; frame timing is authoritative.
    ms = round(frame * 1000 / fps)
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, milli = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{milli:03}"


def build_one(kind: str, entry: dict, *, public: Path, out: Path,
              synth=make_tts) -> dict:
    if kind not in {"LONGO", "SHORT"}:
        raise ValueError("Unsupported format")
    fps, width, height = entry["fps"], entry["width"], entry["height"]
    scene_frames = entry["frames_per_scene"]
    if fps != 30 or (width, height) != ((1920, 1080) if kind == "LONGO" else (1080, 1920)):
        raise ValueError("Unexpected format geometry")
    if type(scene_frames) is not int or not 75 <= scene_frames <= 240:
        raise ValueError("Invalid scene duration")
    scenes = entry["scenes"]
    if not isinstance(scenes, list) or not 2 <= len(scenes) <= 12:
        raise ValueError("Demo must have between 2 and 12 scenes")
    if (kind == "SHORT") and not scenes[-1].get("cta"):
        raise ValueError("Short test requires contextual CTA at end")
    prefix = "l02" if kind == "LONGO" else "l03"
    public.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    runtime_scenes, contract_scenes = [], []
    assets = [
        {"id": "nox", "path": "assets/brand/nox/Nox.png", "kind": "image", "rights": "APPROVED"},
        {"id": "background", "path": "skills/diazverso-decupagem/runtime/public/i04-background.svg",
         "kind": "image", "rights": "APPROVED"},
    ]
    srt_lines, audio_evidence = [], []
    for index, item in enumerate(scenes):
        sid = f"S{index+1:02d}"
        if item["id"] != sid:
            raise ValueError("Scene IDs must be ordered sequentially")
        for key in ("title", "objective", "narration"):
            val = item.get(key)
            if not isinstance(val, str) or not val.strip() or len(val) > MAX_TEXT_CHARS:
                raise ValueError(f"Invalid {key}")
        filename = f"{prefix}-{sid.lower()}-voice.wav"
        audio = public / filename
        synth(item["narration"], audio)
        voice_frames, parameters = wav_frames(audio, fps)
        if voice_frames + TIMING_OFFSET_FRAMES + 2 > scene_frames:
            raise ValueError(f"{sid}: narrated WAV overflows scene ({voice_frames} frames)")
        start = index * scene_frames
        cue = {"text": item["narration"], "start_frame": TIMING_OFFSET_FRAMES,
               "duration_frames": voice_frames}
        audio_cue = {"asset_id": f"voice{sid}", "start_frame": TIMING_OFFSET_FRAMES,
                     "duration_frames": voice_frames, "volume": 0.95}
        runtime_scenes.append({
            "id": sid, "start_frame": start, "duration_frames": scene_frames,
            "objective": item["objective"], "narration": item["narration"],
            "title": item["title"], "cta": bool(item.get("cta")),
            "voice_file": filename, "voice_start_frame": TIMING_OFFSET_FRAMES,
            "voice_duration_frames": voice_frames, "caption": cue
        })
        assets.append({"id": f"voice{sid}",
                       "path": f"skills/diazverso-decupagem/runtime/public/{filename}",
                       "kind": "audio", "rights": "APPROVED"})
        contract_scenes.append({
            "id": sid, "start_frame": start, "duration_frames": scene_frames,
            "objective": item["objective"], "visual": f"Nox canônico, parallax e título: {item['title']}",
            "layers": [
                {"asset_id": "background", "motion": "parallax", "z_index": 0},
                {"asset_id": "nox", "motion": "parallax", "z_index": 1},
            ],
            "captions": [cue], "audio": [audio_cue],
        })
        start_frame, end_frame = start + TIMING_OFFSET_FRAMES, start + TIMING_OFFSET_FRAMES + voice_frames
        srt_lines.append(
            f"{index+1}\n{srt_timestamp(start_frame,fps)} --> {srt_timestamp(end_frame,fps)}\n{item['narration']}\n"
        )
        audio_evidence.append({
            "scene": sid, "file": filename, "wav_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
            "voice_start_frame": start_frame, "voice_end_frame": end_frame,
            "wav_samples": parameters["samples"], "wav_rate": parameters["rate"],
            "cue_is_derived_from_wav_samples": True,
        })
    duration = len(scenes) * scene_frames
    contract = {
        "contract_version": "1.0", "production_id": entry["production_id"],
        "script_version": entry["script_version"], "format": kind,
        "fps": fps, "width": width, "height": height,
        "duration_frames": duration, "assets": assets,
        "scenes": contract_scenes,
        "output": {"basename": f"{prefix}-integrated-test", "container": "mp4",
                   "video_codec": "h264"},
    }
    verdict = validate(contract)
    if verdict["status"] != "VALID_CONTRACT":
        raise ValueError("H01 validator rejected integrated plan")
    plan = {
        "demo_only": True, "editorial_approved": False, "publishing_performed": False,
        "production_id": entry["production_id"], "script_version": entry["script_version"],
        "format": kind, "fps": fps, "duration_frames": duration,
        "scenes": runtime_scenes,
    }
    (out / f"{prefix}-input.json").write_text(json.dumps({"plan": plan}, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / f"{prefix}-h01.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / f"{prefix}-captions.srt").write_text("\n".join(srt_lines), encoding="utf-8")
    (out / f"{prefix}-timing-evidence.json").write_text(
        json.dumps({"format": kind, "test_only": True, "voice_model": "local eSpeak/mespeak pt-BR (dev-only, no licensed audio reused)",
                    "audio_evidence": audio_evidence, "speech_caption_alignment": "WAV sample duration -> 30 fps",
                    "human_listening_completed": False},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    return {"format": kind, "scenes": len(scenes), "frames": duration,
            "validated": verdict["status"], "input": str(out / f"{prefix}-input.json"),
            "speech_sync_method": "captions generated from measured WAV sample count"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fixture", type=Path, default=RUNTIME / "fixtures/integrated-demos.json")
    p.add_argument("--public", type=Path, default=RUNTIME / "public")
    p.add_argument("--out", type=Path, default=RUNTIME / "out")
    args = p.parse_args()
    fixture = read_fixture(args.fixture)
    print(json.dumps([
        build_one(kind, fixture[kind], public=args.public, out=args.out)
        for kind in ("LONGO", "SHORT")
    ], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
