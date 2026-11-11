"""I05: objective gate for Short pre-render plans and post-render evidence.

No prediction of retention or automatic publishing. REVIEW_REQUIRED is not
a rejection of creativity; it points to missing or contradictory evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ("hook_seconds", "duration_seconds", "has_payoff", "has_cta",
            "captions", "audio_checked", "links_checked", "safe_area_checked",
            "render_checked", "rights_checked")


def review(data: dict) -> dict:
    if not isinstance(data, dict) or any(k not in data for k in REQUIRED):
        raise ValueError("Dados de revisão insuficientes")
    duration = data["duration_seconds"]
    hook = data["hook_seconds"]
    if any(type(v) not in (int, float) or not 0 < v < 100000 for v in (duration,)):
        raise ValueError("Duração inválida")
    if type(hook) not in (int, float) or not 0 <= hook < duration:
        raise ValueError("Início de gancho inválido")
    for k in ("has_payoff", "has_cta", "audio_checked", "links_checked",
              "safe_area_checked", "render_checked", "rights_checked"):
        if type(data[k]) is not bool:
            raise ValueError(f"Flag de revisão inválida: {k}")
    caption = data["captions"]
    if caption not in ("VERIFIED_SYNC", "NOT_VERIFIED", "TEXT_ONLY_WITHOUT_SPEECH"):
        raise ValueError("Estado de legenda inválido")
    if caption == "TEXT_ONLY_WITHOUT_SPEECH" and data.get("has_speech") is not False:
        raise ValueError("Exceção tipográfica exige comprovação de ausência de fala")
    issues = []
    if hook > 3:
        issues.append({"priority":"EDITORIAL", "field":"hook_seconds",
                       "reason":"Gancho pode estar tardio; avaliar abertura"})
    if duration < 60:
        issues.append({"priority":"EDITORIAL", "field":"duration_seconds",
                       "reason":"Abaixo da preferência editorial de 60 s; não é limite da plataforma"})
    if not data["has_payoff"]:
        issues.append({"priority":"BLOCKER", "field":"has_payoff",
                       "reason":"A promessa do gancho precisa ser respondida"})
    if not data["has_cta"]:
        issues.append({"priority":"EDITORIAL", "field":"has_cta",
                       "reason":"Avaliar CTA contextual ao canal no final"})
    if caption == "NOT_VERIFIED":
        issues.append({"priority":"BLOCKER", "field":"captions",
                       "reason":"Sincronização de legendas não conferida no áudio/render"})
    for field, label in (("audio_checked", "Áudio e mixagem não conferidos"),
                         ("links_checked", "Links/fontes não conferidos"),
                         ("safe_area_checked", "Margens e sobreposições não conferidas em frames"),
                         ("render_checked", "Render final não inspecionado"),
                         ("rights_checked", "Direitos das mídias não verificados")):
        if not data[field]:
            issues.append({"priority":"BLOCKER", "field":field, "reason":label})
    blockers = sum(x["priority"] == "BLOCKER" for x in issues)
    return {
        "status": "REVIEW_REQUIRED" if blockers else ("EDITORIAL_REVIEW" if issues else "READY_FOR_CREATOR_APPROVAL"),
        "issues": issues, "blocker_count": blockers,
        "retention_prediction": None,
        "requires_creator_approval": True,
        "posting_mode": "MANUAL_BY_CREATOR",
        "render_performed": False, "publishing_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    print(json.dumps(review(json.loads(args.input.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
