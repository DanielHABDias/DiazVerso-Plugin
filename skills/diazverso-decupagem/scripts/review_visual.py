#!/usr/bin/env python3
"""J03: inspect real extracted PNG pixels and prepare evidence-based human QA.

Uses only Python stdlib. Supports PNG RGB/RGBA/grayscale 8-bit, noninterlaced.
Detects suspicious blank borders, low tonal range, almost unchanged samples,
and sharp changes; these are REVIEW signals, not proven editing mistakes.
Does not recognize faces/Nox, read embedded text, certify motion or publish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import struct
import sys
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
FRAME_RE = re.compile(r"^frame_(\d{6,9})\.png$")
MAX_PIXELS = 12_000_000
MAX_FILE = 55_000_000
CHECKS = ("cortes", "parallax_fluidez", "legibilidade", "fundo_bordas",
          "enquadramento", "nox_identidade", "consistencia_grafica")


def decode_png(path: Path) -> dict:
    """Decode 8bit PNG to sparse (16x16) RGB samples and border statistics.

    Untrusted image guard: CRC, limited decompression and dimensions.
    """
    if not path.is_file() or path.stat().st_size > MAX_FILE:
        raise ValueError("Missing or oversized PNG")
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Invalid PNG signature")
    offset = 8
    width = height = channels = None
    palette = None
    compressed = []
    saw_iend = False
    saw_idat = False
    while offset + 12 <= len(data):
        n = struct.unpack_from(">I", data, offset)[0]
        end = offset + n + 12
        if end > len(data):
            raise ValueError("Truncated PNG chunk")
        kind = data[offset+4:offset+8]
        payload = data[offset+8:offset+8+n]
        crc = struct.unpack_from(">I", data, offset+8+n)[0]
        if zlib.crc32(kind+payload) != crc:
            raise ValueError("PNG CRC mismatch")
        if kind == b"IHDR":
            if width is not None or n != 13:
                raise ValueError("Duplicate/malformed IHDR")
            width, height, depth, color, compression, filt, interlace = struct.unpack(">IIBBBBB", payload)
            if (width < 1 or height < 1 or width*height > MAX_PIXELS or
                depth != 8 or color not in (0, 2, 6) or
                compression != 0 or filt != 0 or interlace != 0):
                raise ValueError("Unsupported/oversized PNG encoding")
            channels = {0:1, 2:3, 6:4}[color]
        elif kind == b"IDAT":
            if width is None or saw_iend:
                raise ValueError("PNG chunks out of order")
            compressed.append(payload)
            saw_idat = True
        elif kind == b"IEND":
            if n != 0:
                raise ValueError("Invalid IEND")
            saw_iend = True
            offset = end
            break
        elif kind in (b"PLTE", b"tRNS"):
            raise ValueError("Indexed PNG unsupported")
        offset = end
    if not saw_iend or not saw_idat or offset != len(data):
        raise ValueError("Incomplete PNG")
    stride = width*channels
    expected = height*(stride+1)
    inflater = zlib.decompressobj()
    parts = []
    used = 0
    for chunk in compressed:
        block = inflater.decompress(chunk, expected-used+1)
        used += len(block)
        if used > expected or inflater.unconsumed_tail:
            raise ValueError("Decompressed image exceeds declared geometry")
        parts.append(block)
    tail = inflater.flush(expected-used+1)
    used += len(tail)
    parts.append(tail)
    if used != expected or not inflater.eof or inflater.unused_data:
        raise ValueError("PNG raw buffer length/decompression mismatch")
    raw = b"".join(parts)

    # Compute samples at evenly distributed coordinates without retaining RGB frame.
    xs = sorted(set(round((width-1)*i/15) for i in range(16)))
    ys = set(round((height-1)*i/15) for i in range(16))
    samples = []
    edge_black = edge_total = 0
    previous = bytearray(stride)
    ptr = 0
    alpha_warning = False
    for y in range(height):
        predictor = raw[ptr]
        ptr += 1
        scan = bytearray(raw[ptr:ptr+stride])
        ptr += stride
        if predictor not in range(5):
            raise ValueError("Invalid PNG filter")
        for i in range(stride):
            left = scan[i-channels] if i>=channels else 0
            above = previous[i]
            upper_left = previous[i-channels] if i>=channels else 0
            if predictor == 1:
                scan[i] = (scan[i]+left)&255
            elif predictor == 2:
                scan[i] = (scan[i]+above)&255
            elif predictor == 3:
                scan[i] = (scan[i]+((left+above)//2))&255
            elif predictor == 4:
                p = left+above-upper_left
                da, db, dc = abs(p-left),abs(p-above),abs(p-upper_left)
                scan[i] = (scan[i]+(left if da<=db and da<=dc else (above if db<=dc else upper_left)))&255
        if y in ys:
            for x in xs:
                ix = x*channels
                rgb = (scan[ix],)*3 if channels==1 else tuple(scan[ix:ix+3])
                if channels==4 and scan[ix+3] < 255:
                    alpha_warning = True
                samples.append(rgb)
                if x in (xs[0], xs[-1]) or y in (min(ys), max(ys)):
                    edge_total += 1
                    if max(rgb) <= 12:
                        edge_black += 1
        previous = scan

    luminances = [0.2126*r+0.7152*g+0.0722*b for r,g,b in samples]
    mean = sum(luminances)/len(luminances)
    ordered = sorted(luminances)
    spread = ordered[int(0.95*(len(ordered)-1))]-ordered[int(0.05*(len(ordered)-1))]
    return {
        "width": width, "height": height,
        "pixel_hash": hashlib.sha256(data).hexdigest(),
        "mean_luma": round(mean,2),
        "tonal_range_p5_p95": round(spread,2),
        "sample_edge_black_fraction": round(edge_black/max(1,edge_total),3),
        "alpha_sample_detected": alpha_warning,
        "samples": samples,
    }


def compare(a: dict, b: dict) -> float:
    if (a["width"], a["height"]) != (b["width"], b["height"]):
        raise ValueError("Cannot compare different frame dimensions")
    return round(sum(sum(abs(v-w) for v,w in zip(p,q))
                     for p,q in zip(a["samples"],b["samples"]))
                 / (3*len(a["samples"])*255), 5)


def review(manifest: dict, *, fps: int, manual: dict | None = None) -> dict:
    """Manifest uses J02 {frames:[{frame,path,sha256,reasons}]}.

    Manual checklist is recorded as notes for traceability, not converted into
    a machine-verified result; approval belongs to J08 with separate evidence.
    """
    if type(fps) is not int or not 1<=fps<=120:
        raise ValueError("Invalid FPS")
    rows = manifest.get("frames") if isinstance(manifest, dict) else None
    if not isinstance(rows,list) or not rows:
        raise ValueError("J02 frame manifest required, not an extraction plan")
    if manual is not None:
        if not isinstance(manual,dict) or set(manual) != set(CHECKS):
            raise ValueError("Manual review must cover every visual category")
        for name,item in manual.items():
            if (not isinstance(item,dict) or set(item)!={"status","evidence"} or
                item["status"] not in ("APROVADO","REVISAR","PENDENTE") or
                not isinstance(item["evidence"],str) or
                (item["status"]=="APROVADO" and not item["evidence"].strip())):
                raise ValueError("Invalid manual evidence for "+name)
    frames = []
    findings = []
    previous = None
    ids=set()
    for row in rows:
        if not isinstance(row,dict) or not {"frame","path","sha256","reasons"}<=set(row):
            raise ValueError("Malformed extraction row")
        frame=row["frame"]
        path=Path(row["path"])
        if (type(frame) is not int or frame<0 or frame in ids or
            not FRAME_RE.fullmatch(path.name) or int(FRAME_RE.fullmatch(path.name).group(1))!=frame):
            raise ValueError("Frame IDs and filenames must agree and be unique")
        if not isinstance(row["reasons"],list) or not all(isinstance(x,str) for x in row["reasons"]):
            raise ValueError("Invalid frame reasons")
        if not isinstance(row["sha256"],str) or not re.fullmatch("[a-f0-9]{64}",row["sha256"]):
            raise ValueError("Invalid SHA-256 receipt")
        ids.add(frame)
        image=decode_png(path)
        if image["pixel_hash"] != row["sha256"]:
            raise ValueError("Frame bytes differ from J02 SHA-256 evidence")
        if previous is not None and frame<=previous["frame"]:
            raise ValueError("Frame manifest must be sorted")
        if image["tonal_range_p5_p95"] < 16:
            findings.append({"frame":frame,"code":"LOW_TONAL_VARIATION",
                             "severity":"REVIEW","evidence":{"tonal_range":image["tonal_range_p5_p95"]},
                             "note":"Uniform frame may be intentional; inspect typography/background"})
        if image["sample_edge_black_fraction"]>=0.92:
            findings.append({"frame":frame,"code":"DARK_FRAME_BORDER",
                             "severity":"REVIEW",
                             "evidence":{"border_fraction":image["sample_edge_black_fraction"]},
                             "note":"Edges look dark; deliberate letterbox or unintended empty canvas?"})
        if image["alpha_sample_detected"]:
            findings.append({"frame":frame,"code":"TRANSPARENCY_IN_OUTPUT",
                             "severity":"REVIEW","evidence":{"alpha_samples":True},
                             "note":"Final composited image should generally be opaque"})
        item={"frame":frame,"path":str(path.resolve()),"sha256":image["pixel_hash"],
              "reasons":row["reasons"],"mean_luma":image["mean_luma"],
              "tonal_range":image["tonal_range_p5_p95"]}
        if previous is not None:
            delta=compare(image,previous["image"])
            frame_gap=frame-previous["frame"]
            item["delta_from_previous"] = delta
            # Distinct frames sampled at least half a second apart.
            if frame_gap>=max(1,fps//2) and delta<=0.003:
                findings.append({"frame":frame,"code":"NEAR_IDENTICAL_SAMPLED_FRAMES",
                                 "severity":"REVIEW","evidence":{"prior_frame":previous["frame"],
                                   "frame_gap":frame_gap,"normalized_delta":delta},
                                 "note":"Possible frozen/unchanged visual; may be an intentional hold"})
            if frame_gap==1 and delta>=0.72:
                findings.append({"frame":frame,"code":"ABRUPT_VISUAL_CHANGE",
                                 "severity":"REVIEW","evidence":{"prior_frame":previous["frame"],
                                   "normalized_delta":delta},
                                 "note":"Potential cut/flash at adjacent samples; inspect transition"})
        frames.append(item)
        previous={"frame":frame,"image":image}

    unapproved = [] if manual is None else [k for k,v in manual.items() if v["status"]!="APROVADO"]
    return {"status":"VISUAL_REVIEW_REQUIRED",
            "frames_analyzed":len(frames), "frame_evidence":frames,
            "findings":findings,"manual_checks":list(CHECKS),
            "manual_evidence_recorded":manual is not None,
            "manual_pending":list(CHECKS) if manual is None else unapproved,
            "visual_qa_approved_by_code":False,
            "nox_identity_recognized":False,
            "text_legibility_verified_by_code":False,
            "motion_continuity_verified":False,
            "publishing_performed":False,
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("j02_extraction_json",type=Path)
    parser.add_argument("--fps",type=int,required=True)
    parser.add_argument("--manual",type=Path,
                        help="Optional full human rubric with status and evidence")
    args=parser.parse_args()
    try:
        data=json.loads(args.j02_extraction_json.read_text(encoding="utf-8"))
        manual=json.loads(args.manual.read_text(encoding="utf-8")) if args.manual else None
        result=review(data,fps=args.fps,manual=manual)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError,zlib.error) as exc:
        print("VISUAL_REVIEW_FAILED: "+str(exc),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
