"""J05: review verifiable narrative pacing from a scene breakdown.

Heuristic findings are editorial questions, never a prediction of retention,
engagement, YouTube ranking or algorithm behavior. No writes/publication.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VALID_ROLES = {"HOOK", "CONTEXT", "EVIDENCE", "TWIST", "PAYOFF", "CTA", "BREATHER"}
PUNCTUATION = re.compile(r"[^\w\s]", re.UNICODE)


def review(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Expected a scene review object")
    kind = data.get("format")
    if kind not in ("SHORT", "LONGO"):
        raise ValueError("format must be SHORT or LONGO")
    fps = data.get("fps")
    if type(fps) is not int or not 1 <= fps <= 120:
        raise ValueError("fps must be 1..120")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("At least one scene is required")
    issues = []
    previous_end = 0
    seen = set()
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            raise ValueError("Scene must be an object")
        required = {"id", "start_frame", "duration_frames", "role", "narration", "visual_change"}
        if not required.issubset(scene):
            raise ValueError(f"Missing scene keys: {index}")
        sid = scene["id"]
        if not isinstance(sid, str) or not re.fullmatch(r"S\d{2,4}", sid) or sid in seen:
            raise ValueError("Invalid or duplicate scene ID")
        seen.add(sid)
        start, frames = scene["start_frame"], scene["duration_frames"]
        if type(start) is not int or type(frames) is not int or start != previous_end or frames < 1:
            raise ValueError("Scene timeline must be contiguous and positive")
        previous_end = start + frames
        if scene["role"] not in VALID_ROLES:
            raise ValueError("Unknown narrative role")
        if not isinstance(scene["narration"], str):
            raise ValueError("Narration must be text")
        if type(scene["visual_change"]) is not bool:
            raise ValueError("visual_change must be boolean")

        seconds = frames / fps
        long_threshold = 9 if kind == "SHORT" else 22
        if seconds > long_threshold and not scene["visual_change"]:
            issues.append({"scene": sid, "code": "STATIC_LONG_SCENE", "severity": "EDITORIAL",
                           "evidence": {"seconds": round(seconds, 2), "visual_change": False},
                           "suggestion": "Conferir se o quadro sustenta a informação ou precisa de reenquadramento"})
        if scene["role"] == "BREATHER" and seconds < 0.45:
            issues.append({"scene": sid, "code": "VERY_SHORT_BREATHER", "severity": "EDITORIAL",
                           "evidence": {"seconds": round(seconds, 2)},
                           "suggestion": "Verificar se o respiro tem tempo perceptível"})
        if index == 0 and scene["role"] not in ("HOOK", "TWIST"):
            issues.append({"scene": sid, "code": "HOOK_NOT_EXPLICIT", "severity": "EDITORIAL",
                           "evidence": {"role": scene["role"]},
                           "suggestion": "Revisar se a abertura apresenta uma promessa clara"})

    if data.get("total_frames") != previous_end or type(data.get("total_frames")) is not int:
        raise ValueError("total_frames must equal the end of the last scene")
    # Repetition is normalized only for *exact* narrative text; lexical
    # similarity/semantic redundancy requires a human, not a fabricated score.
    previous_narration = None
    for scene in scenes:
        current = PUNCTUATION.sub("", scene["narration"]).casefold().strip()
        current = " ".join(current.split())
        if current and current == previous_narration and len(current) >= 18:
            issues.append({"scene": scene["id"], "code": "ADJACENT_EXACT_REPEAT",
                           "severity": "EDITORIAL", "evidence": {"narration": scene["narration"]},
                           "suggestion": "Verificar se repetir a mesma fala é intencional"})
        previous_narration = current if current else None

    roles = [s["role"] for s in scenes]
    payoff_indices = [i for i, role in enumerate(roles) if role == "PAYOFF"]
    cta_indices = [i for i, role in enumerate(roles) if role == "CTA"]
    if not payoff_indices:
        issues.append({"scene": None, "code": "PAYOFF_MISSING", "severity": "BLOCKER",
                       "evidence": {"roles": roles},
                       "suggestion": "Responder à promessa do gancho antes de finalizar"})
    if not cta_indices:
        issues.append({"scene": None, "code": "CTA_MISSING", "severity": "EDITORIAL",
                       "evidence": {"roles": roles},
                       "suggestion": "Avaliar CTA curto e contextual ao canal"})
    else:
        cta_start = scenes[cta_indices[0]]["start_frame"]
        cta_ratio = cta_start / previous_end
        if cta_ratio < 0.65:
            issues.append({"scene": scenes[cta_indices[0]]["id"],
                           "code": "EARLY_CTA", "severity": "EDITORIAL",
                           "evidence": {"cta_starts_at_fraction": round(cta_ratio, 3)},
                           "suggestion": "Conferir se o CTA interrompe a entrega da tese"})
        if payoff_indices and cta_indices[0] < payoff_indices[0]:
            issues.append({"scene": scenes[cta_indices[0]]["id"],
                           "code": "CTA_BEFORE_PAYOFF", "severity": "EDITORIAL",
                           "evidence": {"cta_index": cta_indices[0], "first_payoff_index": payoff_indices[0]},
                           "suggestion": "Considerar CTA após concluir a ideia principal"})
    if kind == "SHORT" and previous_end / fps < 60:
        issues.append({"scene": None, "code": "SHORT_BELOW_PREFERENCE", "severity": "EDITORIAL",
                       "evidence": {"seconds": round(previous_end / fps, 2)},
                       "suggestion": "Preferência atual do criador: 60 s, sem preencher com enrolação"})

    return {"status": "REQUIRES_EDITORIAL_REVIEW" if issues else "NO_RULE_BASED_FINDINGS",
            "issues": issues, "total_seconds": round(previous_end / fps, 3),
            "scenes_checked": len(scenes), "retention_prediction": None,
            "semantic_redundancy_verified": False, "render_verified": False,
            "creator_approval_required": True, "writes_performed": False,
            "publishing_performed": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()
    try:
        result = review(json.loads(args.input_json.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"PACING_REVIEW_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
