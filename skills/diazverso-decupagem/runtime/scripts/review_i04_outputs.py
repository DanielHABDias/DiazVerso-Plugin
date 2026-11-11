#!/usr/bin/env python3
"""Automated, reproducible evidence on actual I04 renders (not human visual QA).

The companion GitHub Action uploads the original frames and MP4 for inspection.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "scripts"))
from verify_remotion_outputs import boxes, png_dimensions, video_dimensions  # noqa: E402

DIMS = (1080, 1920)
FRAMES = (15, 105, 200)


def has_audio_track(video: Path) -> bool:
    data = video.read_bytes()
    for outer, begin, end in boxes(data, 0, len(data)):
        if outer != b"moov":
            continue
        for child, ts, te in boxes(data, begin, end):
            if child != b"trak":
                continue
            for inner, ms, me in boxes(data, ts, te):
                if inner != b"mdia":
                    continue
                for kind, hs, he in boxes(data, ms, me):
                    # Handler box: version/flags (4), pre_defined (4),
                    # handler_type (4), e.g. 'soun' for audio.
                    if kind == b"hdlr" and he >= hs + 12 and data[hs+8:hs+12] == b"soun":
                        return True
    return False


def check(folder: Path) -> dict:
    movie = folder / "i04-9x16.mp4"
    if not movie.is_file() or movie.stat().st_size < 1000:
        raise ValueError("I04 rendered movie missing")
    if video_dimensions(movie) != DIMS:
        raise ValueError("I04 video has wrong dimensions")
    if not has_audio_track(movie):
        raise ValueError("I04 video is missing the whoosh audio track")
    if b"avc1" not in movie.read_bytes():
        raise ValueError("H.264 sample description absent")
    frames = [folder / f"i04-frame-{n}.png" for n in FRAMES]
    for frame in frames:
        if png_dimensions(frame) != DIMS:
            raise ValueError(f"Wrong frame resolution: {frame}")
    with Image.open(frames[0]) as first, Image.open(frames[1]) as middle, Image.open(frames[2]) as last:
        first_rgb, mid_rgb, last_rgb = first.convert("RGB"), middle.convert("RGB"), last.convert("RGB")
        if ImageChops.difference(first_rgb,mid_rgb).getbbox() is None:
            raise ValueError("I04 frames are identical despite supposed motion")
        if ImageChops.difference(mid_rgb,last_rgb).getbbox() is None:
            raise ValueError("I04 later frames are identical despite supposed motion")
        # Verify that the caption area has pixel contrast, not that OCR or
        # a human approved the caption's content/placement.
        region = last_rgb.crop((130, 1245, 900, 1410))
        variance = ImageStat.Stat(region).stddev
        if max(variance) < 8:
            raise ValueError("Caption region has insufficient visual variation")
    return {
        "result": "I04_TECHNICAL_RENDER_CHECKS_PASSED",
        "render": str(movie),
        "dimensions": list(DIMS),
        "frames_checked": [str(p) for p in frames],
        "h264_sample_descriptor": True,
        "has_audio_track": True,
        "frames_change": True,
        "caption_region_has_pixel_variation": True,
        "canonical_nox_integrity": "verified separately by prepare_i04_assets.py",
        "spoken_words_or_voice_track": False,
        "speech_caption_sync_verified": False,
        "human_frame_review_performed": False,
        "rights_note": "Nox from approved canonical asset; original generated whoosh and background",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.folder), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
