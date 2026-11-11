#!/usr/bin/env python3
"""L02/L03 technical QA of actual Remotion MP4 and PNG plus WAV-derived cues.

True decoding/voice intelligibility and subjective editorial QA require a
human to inspect/listen to the uploaded artifact. This script never claims it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import wave
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

REPO=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(REPO/"scripts"))
from verify_remotion_outputs import png_dimensions,video_dimensions  # noqa: E402
from review_i04_outputs import has_audio_track  # noqa: E402

SPECS = {
    "l02": {"dims":(1920,1080),"frames":[30,235,540],"format":"LONGO"},
    "l03": {"dims":(1080,1920),"frames":[20,171,300],"format":"SHORT"},
}


def review(prefix:str,out:Path,public:Path)->dict:
    spec=SPECS[prefix]
    input_data=json.loads((out/f"{prefix}-input.json").read_text(encoding="utf-8"))
    plan=input_data["plan"]
    if plan["format"]!=spec["format"] or not plan.get("demo_only") or plan.get("editorial_approved"):
        raise ValueError("Demo input mismatch / publication safety failure")
    mp4=out/f"{prefix}.mp4"
    if not mp4.is_file() or mp4.stat().st_size<1000:
        raise ValueError("No actual rendered MP4")
    if video_dimensions(mp4)!=spec["dims"] or b"avc1" not in mp4.read_bytes():
        raise ValueError("H.264 MP4 dimensions/codec mismatch")
    if not has_audio_track(mp4):
        raise ValueError("Rendered MP4 has no audio track")
    frames=[out/f"{prefix}-frame-{i}.png" for i in spec["frames"]]
    for image in frames:
        if not image.is_file() or png_dimensions(image)!=spec["dims"]:
            raise ValueError(f"Missing or invalid real PNG: {image}")
    with Image.open(frames[0]) as first,Image.open(frames[1]) as middle,Image.open(frames[2]) as last:
        first,middle,last=[x.convert("RGB") for x in (first,middle,last)]
        if not ImageChops.difference(first,middle).getbbox():
            raise ValueError("First and middle frames are pixel-identical")
        if not ImageChops.difference(middle,last).getbbox():
            raise ValueError("Middle and final frames are pixel-identical")
        box=(130,1220,900,1380) if prefix=="l03" else (300,830,1600,1020)
        if max(ImageStat.Stat(first.crop(box)).stddev)<5:
            raise ValueError("Caption region is suspiciously blank")
    evidence=json.loads((out/f"{prefix}-timing-evidence.json").read_text(encoding="utf-8"))
    checked=[]
    for scene,voice in zip(plan["scenes"],evidence["audio_evidence"]):
        file=public/scene["voice_file"]
        if not file.is_file():
            raise ValueError(f"Missing TTS WAV: {file}")
        with wave.open(str(file),"rb") as f:
            samples,rate=f.getnframes(),f.getframerate()
        estimated_frames=(samples*plan["fps"]+rate-1)//rate
        if hashlib.sha256(file.read_bytes()).hexdigest()!=voice["wav_sha256"]:
            raise ValueError("TTS WAV bytes differ from source of timeline")
        if estimated_frames!=scene["voice_duration_frames"]:
            raise ValueError("Caption offset not derived from measured WAV samples")
        if scene["caption"]["text"]!=scene["narration"] or (
            scene["caption"]["start_frame"]!=scene["voice_start_frame"] or
            scene["caption"]["duration_frames"]!=scene["voice_duration_frames"]
        ):
            raise ValueError("Caption and voice segment are misaligned")
        checked.append({"scene":scene["id"],"wav_duration_frames":estimated_frames,
                        "speech_start":scene["start_frame"]+scene["voice_start_frame"],
                        "caption_text_matches_script":True})
    if prefix=="l03" and not plan["scenes"][-1]["cta"]:
        raise ValueError("Short CTA missing")
    srt=(out/f"{prefix}-captions.srt").read_text(encoding="utf-8")
    if "-->" not in srt or len(srt.split("-->"))!=len(plan["scenes"])+1:
        raise ValueError("SRT cue count mismatch")
    return {
        "status":"INTEGRATED_TECHNICAL_QA_PASSED",
        "format":spec["format"],"mp4":mp4.name,
        "dimensions":list(spec["dims"]),"codec_descriptor":"avc1",
        "has_audio_track":True,
        "three_real_frames_checked":[p.name for p in frames],
        "visual_frames_differ":True,"audio_caption_sample_timeline_matches":True,
        "narration_segments":checked,
        "voice_engine":"Offline PT-BR synthetic test voice (eSpeak CLI or meSpeak npm); not a human narrator",
        "no_external_media_and_no_content_lab":True,
        "human_video_and_audio_review_completed":False,
        "speech_recognition_or_phoneme_accuracy_verified":False,
        "creator_approved_script":False,
        "publication_performed":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("out",type=Path)
    p.add_argument("public",type=Path)
    opts=p.parse_args()
    for prefix in SPECS:
        result=review(prefix,opts.out,opts.public)
        (opts.out/f"{prefix}-qa.json").write_text(
            json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":
    main()
