"""approval — evidence-based human approval checklist for a manual-publication kit.

This file ONLY evaluates a supplied review record. It never invents approval,
renders media, posts a video or writes a connected Sheet.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GATES = (
    "roteiro", "fatos_fontes", "titulo_thumbnail", "direitos_midias",
    "video_render", "qa_visual", "qa_audio", "legendas", "kit_textual"
)


def evaluate(record: dict) -> dict:
    if not isinstance(record, dict):
        raise ValueError("Review record must be an object")
    production_id = record.get("production_id")
    if not isinstance(production_id, str) or not re.fullmatch(r"(VD|SH)_\d{4,}", production_id):
        raise ValueError("Valid production ID required")
    gates = record.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(GATES):
        raise ValueError("All nine distinct review gates must be present")
    issues = []
    for name in GATES:
        gate = gates[name]
        if not isinstance(gate, dict) or set(gate) != {"status", "evidence"}:
            raise ValueError(f"Gate {name} must have status and evidence")
        if gate["status"] not in ("APROVADO", "PENDENTE", "REPROVADO"):
            raise ValueError(f"Invalid gate state: {name}")
        evidence = gate["evidence"]
        if not isinstance(evidence, str):
            raise ValueError(f"Evidence must be text: {name}")
        if gate["status"] == "APROVADO" and not evidence.strip():
            raise ValueError(f"Approval requires evidence: {name}")
        if gate["status"] != "APROVADO":
            issues.append({"gate": name, "status": gate["status"]})
    decision = record.get("creator_decision")
    if not isinstance(decision, dict) or set(decision) != {"approved", "evidence"}:
        raise ValueError("Creator approval decision required")
    if type(decision["approved"]) is not bool or not isinstance(decision["evidence"], str):
        raise ValueError("Invalid creator approval decision")
    if decision["approved"] and not decision["evidence"].strip():
        raise ValueError("Human approval without evidence is invalid")
    if not decision["approved"]:
        issues.append({"gate": "criador", "status": "PENDENTE"})
    return {
        "status": "KIT_APROVADO_PARA_ENTREGA_MANUAL" if not issues else "REVISAO_PENDENTE",
        "production_id": production_id, "pending": issues,
        "manual_posting_by_creator": True, "posting_performed": False,
        "sheet_writes_performed": False
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("review_json", type=Path)
    args = p.parse_args()
    result = evaluate(json.loads(args.review_json.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
