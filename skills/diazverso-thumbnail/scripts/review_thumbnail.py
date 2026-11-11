#!/usr/bin/env python3
"""G03: verify local thumbnail files, dimensions, review evidence and Drive refs.

Uses only stdlib. Header checks do not prove full visual decodability,
text OCR, Nox identity, link reachability or image quality.
No writes, uploads, posting or automatic human approval.
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
from urllib.parse import urlsplit

PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8"
VISUAL_CHECKS = ("mobile_text_legibility", "promise_matches_script",
                 "focal_point", "contrast_readability",
                 "brand_identity", "nox_character_lock")
DRIVE_HOSTS = {"drive.google.com", "docs.google.com"}


def dimensions(path: Path) -> tuple[int,int,str]:
    if not path.is_file() or path.stat().st_size == 0 or path.stat().st_size > 40*1024*1024:
        raise ValueError("Missing/empty/oversized image")
    with path.open("rb") as f:
        first = f.read(32)
        if first.startswith(PNG_SIG):
            if len(first) < 33:
                # the next byte belongs to the chunk CRC
                f.seek(0); first=f.read(33)
            if first[12:16] != b"IHDR" or first[8:12] != b"\x00\x00\x00\x0d":
                raise ValueError("Malformed PNG IHDR")
            if zlib.crc32(first[12:29]) != struct.unpack(">I", first[29:33])[0]:
                raise ValueError("PNG IHDR CRC failure")
            w,h,depth,color,comp,fil,inter=struct.unpack(">IIBBBBB",first[16:29])
            if not w or not h or w*h>20_000_000 or depth!=8 or comp or fil or inter or color not in (0,2,3,4,6):
                raise ValueError("Unsupported PNG thumbnail encoding")
            return w,h,"PNG_HEADER"
        if first.startswith(JPEG_SIG):
            f.seek(2)
            while True:
                marker=f.read(1)
                if not marker:
                    break
                if marker!=b"\xff":
                    continue
                marker=f.read(1)
                while marker==b"\xff":
                    marker=f.read(1)
                if not marker or marker in (b"\xd9",b"\xda"):
                    break
                if marker in (b"\x01",) or 0xd0<=marker[0]<=0xd7:
                    continue
                raw=f.read(2)
                if len(raw)!=2:
                    break
                length=struct.unpack(">H",raw)[0]
                if length<2:
                    raise ValueError("Malformed JPEG segment")
                if marker[0] in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf):
                    payload=f.read(length-2)
                    if len(payload)<5:
                        break
                    h,w=struct.unpack(">HH",payload[1:5])
                    if not w or not h or w*h>20_000_000:
                        raise ValueError("Invalid JPEG dimensions")
                    return w,h,"JPEG_HEADER"
                f.seek(length-2,1)
    raise ValueError("Unsupported or malformed PNG/JPEG header")


def _drive_url(url: object) -> bool:
    if not isinstance(url,str) or not url:
        return False
    try:
        u=urlsplit(url)
        return (u.scheme=="https" and u.hostname in DRIVE_HOSTS
                and not u.username and not u.password
                and bool(u.path.strip("/")) and not u.fragment)
    except ValueError:
        return False


def review(record: dict, root: Path) -> dict:
    if not isinstance(record,dict) or set(record)!={"production_id","brief_id","variants"}:
        raise ValueError("Review requires production_id, brief_id and variants")
    if not isinstance(record["production_id"],str) or not re.fullmatch(r"(VD|SH)_\d{4,}",record["production_id"]):
        raise ValueError("Invalid production ID")
    if not isinstance(record["brief_id"],str) or not record["brief_id"].strip():
        raise ValueError("Brief version/reference required")
    if not isinstance(record["variants"],dict) or set(record["variants"])!={"A","B"}:
        raise ValueError("Two variants A/B required")
    root=root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Image root must be a directory")
    result=[]; findings=[]
    for name in ("A","B"):
        v=record["variants"][name]
        if not isinstance(v,dict) or set(v)!={"path","drive_link","sha256","nox_used","visual_checks","reviewer"}:
            raise ValueError("Variant must provide file, link, digest and human rubric")
        if type(v["nox_used"]) is not bool:
            raise ValueError("nox_used must be explicit boolean")
        if not isinstance(v["path"],str) or not v["path"]:
            raise ValueError("File path missing")
        candidate=(root/v["path"]).resolve()
        if not candidate.is_relative_to(root):
            raise ValueError("Image path outside authorized root")
        if not candidate.is_file():
            findings.append({"variant":name,"code":"LOCAL_FILE_MISSING","severity":"BLOCKER"})
            continue
        try:
            width,height,typ=dimensions(candidate)
        except ValueError as exc:
            findings.append({"variant":name,"code":"INVALID_IMAGE_HEADER","severity":"BLOCKER",
                             "detail":str(exc)})
            continue
        if width<1280 or height<720 or width*9!=height*16:
            findings.append({"variant":name,"code":"DIMENSIONS_NOT_16_9_1280","severity":"BLOCKER",
                             "width":width,"height":height})
        actual=hashlib.sha256(candidate.read_bytes()).hexdigest()
        if not isinstance(v["sha256"],str) or not re.fullmatch("[a-f0-9]{64}",v["sha256"]) or v["sha256"]!=actual:
            findings.append({"variant":name,"code":"FILE_SHA256_MISMATCH","severity":"BLOCKER"})
        if not _drive_url(v["drive_link"]):
            findings.append({"variant":name,"code":"DRIVE_LINK_MISSING_OR_INVALID","severity":"BLOCKER"})
        rubric=v["visual_checks"]
        if not isinstance(rubric,dict) or set(rubric)!=set(VISUAL_CHECKS):
            raise ValueError("Visual review requires all six checks")
        for key in VISUAL_CHECKS:
            check=rubric[key]
            if not isinstance(check,dict) or set(check)!={"status","evidence"}:
                raise ValueError("Malformed visual check")
            status=check["status"]
            if status not in ("APROVADO","PENDENTE","REPROVADO","NAO_APLICAVEL"):
                raise ValueError("Invalid visual review status")
            if not isinstance(check["evidence"],str) or (status=="APROVADO" and not check["evidence"].strip()):
                raise ValueError("Approval requires human evidence")
            if key=="nox_character_lock":
                allowed={"APROVADO"} if v["nox_used"] else {"NAO_APLICAVEL"}
            else:
                allowed={"APROVADO"}
            if status not in allowed:
                findings.append({"variant":name,"code":"HUMAN_CHECK_PENDING_"+key.upper(),
                                 "severity":"BLOCKER"})
        if not isinstance(v["reviewer"],str) or not v["reviewer"].strip():
            findings.append({"variant":name,"code":"HUMAN_REVIEWER_MISSING","severity":"BLOCKER"})
        result.append({"variant":name,"file":str(candidate),
                       "sha256":actual,"width":width,"height":height,
                       "header_type":typ,
                       "pixel_content_decoded":False,
                       "drive_link_syntax_valid":_drive_url(v["drive_link"]),
                       "drive_link_verified_reachable":False})
    return {"status":"BLOCKED" if findings else "READY_FOR_EXTERNAL_REVIEW_AND_READBACK",
            "production_id":record["production_id"],"files":result,
            "findings":findings,"human_evidence_recorded":True,
            "human_approval_authenticated_by_code":False,
            "ocr_performed":False,"nox_identity_recognized_by_code":False,
            "drive_files_read_back":False,"publishing_performed":False}


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("review_json",type=Path)
    p.add_argument("--root",type=Path,required=True)
    a=p.parse_args()
    try:
        out=review(json.loads(a.review_json.read_text("utf-8")),a.root)
        print(json.dumps(out,ensure_ascii=False,indent=2))
        return 0 if out["status"]!="BLOCKED" else 2
    except (ValueError,OSError,TypeError,KeyError) as exc:
        print("THUMBNAIL_REVIEW_FAILED: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
