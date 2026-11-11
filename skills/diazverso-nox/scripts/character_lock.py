#!/usr/bin/env python3
"""character-lock: verify canonical Nox bytes and document manual pose identity comparison.

Does NOT compare characters visually, create images, assert rights or post.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path

PNG=b"\x89PNG\r\n\x1a\n"
CHECKS=("silhouette_proportions","facial_features","palette",
        "costume_accessories","drawing_style","no_redesign")


def _image(path: Path) -> dict:
    if not path.is_file() or not 0 < path.stat().st_size < 30_000_000:
        raise ValueError("Actual bounded PNG required")
    with path.open("rb") as f:
        header=f.read(33)
    if (len(header)!=33 or not header.startswith(PNG) or
        header[8:12]!=b"\x00\x00\x00\x0d" or header[12:16]!=b"IHDR" or
        zlib.crc32(header[12:29]) != struct.unpack(">I",header[29:33])[0]):
        raise ValueError("Invalid PNG header/CRC")
    w,h,depth,color,comp,flt,inter=struct.unpack(">IIBBBBB",header[16:29])
    if (not w or not h or w*h>20_000_000 or depth!=8 or
        color not in (2,3,6) or comp or flt or inter):
        raise ValueError("Unsupported PNG encoding")
    payload=path.read_bytes()
    git_blob=hashlib.sha1(f"blob {len(payload)}\0".encode()+payload).hexdigest()
    return {"width":w,"height":h,"bytes":len(payload),
            "sha256":hashlib.sha256(payload).hexdigest(),"git_blob_sha1":git_blob}


def review(record: dict, root: Path) -> dict:
    if not isinstance(record,dict) or set(record)!={"pose_path","canonical_manifest",
                  "pose_rights_evidence","pose_purpose","reviewer","checks"}:
        raise ValueError("Invalid Character Lock record")
    root=root.resolve(strict=True)
    manifest_file=(root/"assets/manifest.json").resolve()
    if not manifest_file.is_file():
        raise FileNotFoundError("Canonical assets manifest missing")
    manifest=json.loads(manifest_file.read_text("utf-8"))
    entries=[x for x in manifest.get("assets",[])
             if x.get("id")=="brand.nox.canonical"]
    if len(entries)!=1:
        raise ValueError("Canonical Nox entry not unique")
    entry=entries[0]
    source=entry.get("path")
    if source!="assets/brand/nox/Nox.png":
        raise ValueError("Noncanonical Nox source")
    reference=(root/source).resolve()
    if not reference.is_relative_to(root):
        raise ValueError("Canonical path outside root")
    original=_image(reference)
    if (original["width"]!=entry["dimensions"]["width"] or
        original["height"]!=entry["dimensions"]["height"] or
        original["bytes"]!=entry["size_bytes"] or
        original["git_blob_sha1"]!=entry["git_blob_sha1"]):
        raise ValueError("Canonical Nox bytes/geometry disagree with manifest")
    if record["canonical_manifest"]!="assets/manifest.json":
        raise ValueError("Canonical manifest reference required")
    pose=record["pose_path"]
    if not isinstance(pose,str) or not pose.strip():
        raise ValueError("Pose path required")
    candidate=(root/pose).resolve()
    if not candidate.is_relative_to(root) or candidate==reference:
        raise ValueError("Pose must be a separate file within root")
    derivative=_image(candidate)
    if not isinstance(record["pose_rights_evidence"],str) or not record["pose_rights_evidence"].strip():
        raise ValueError("Rights evidence for derived pose required")
    if not isinstance(record["pose_purpose"],str) or not record["pose_purpose"].strip():
        raise ValueError("Pose editorial purpose required")
    if not isinstance(record["reviewer"],str) or not record["reviewer"].strip():
        raise ValueError("Human reviewer required")
    checks=record["checks"]
    if not isinstance(checks,dict) or set(checks)!=set(CHECKS):
        raise ValueError("All Character Lock checks required")
    findings=[]
    for name in CHECKS:
        item=checks[name]
        if not isinstance(item,dict) or set(item)!={"status","evidence"}:
            raise ValueError("Invalid Character Lock check")
        if item["status"] not in ("APROVADO","PENDENTE","REPROVADO") or not isinstance(item["evidence"],str):
            raise ValueError("Invalid Character Lock status/evidence")
        if item["status"]=="APROVADO" and not item["evidence"].strip():
            raise ValueError("Cannot approve Character Lock without evidence")
        if item["status"]!="APROVADO":
            findings.append({"check":name,"status":item["status"]})
    return {
        "status":"CHARACTER_LOCK_EVIDENCE_COMPLETE_AWAITING_VISUAL_AUTHENTICATION"
        if not findings else "CHARACTER_LOCK_NOT_APPROVED",
        "original":original,"candidate":derivative,
        "issues":findings,"pose_file_verified":True,
        "human_visual_comparison_authenticated_by_code":False,
        "identity_recognized_by_code":False,"image_generated_by_code":False,
        "publishing_performed":False
    }


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("record_json",type=Path)
    p.add_argument("--root",required=True,type=Path)
    a=p.parse_args()
    try:
        result=review(json.loads(a.record_json.read_text("utf-8")),a.root)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if not result["issues"] else 2
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print("CHARACTER_LOCK_FAILED: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
