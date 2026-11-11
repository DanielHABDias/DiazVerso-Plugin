"""publication-kit: assemble a copy-ready kit for MANUAL publication by the creator.

Uses only creator-approved input; never uploads, schedules, publishes, or
pretends files were rendered or inspected. No Google API calls.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def build_kit(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Esperado objeto")
    required = ("production_id", "title", "description", "sources", "tags",
                "video_file", "thumbnail_file", "creator_approved",
                "render_verified", "qa_approved")
    if any(k not in data for k in required):
        raise ValueError("Campos obrigatórios ausentes")
    import re
    if not isinstance(data["production_id"], str) or not re.fullmatch(r"(VD|SH)_\d{4,}", data["production_id"]):
        raise ValueError("ID inválido")
    for key in ("title", "description", "video_file", "thumbnail_file"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError(f"Campo obrigatório inválido: {key}")
    for key in ("sources", "tags"):
        if not isinstance(data[key], list) or any(not isinstance(v, str) or not v.strip() for v in data[key]):
            raise ValueError(f"{key} deve ser uma lista de textos")
    if not data["sources"]:
        raise ValueError("Listar fontes ou declarar explicitamente sem fontes externas na revisão editorial")
    if any(type(data[k]) is not bool for k in ("creator_approved", "render_verified", "qa_approved")):
        raise ValueError("Flags de verificação devem ser booleanas")
    if not isinstance(data.get("affiliate_links", []), list):
        raise ValueError("affiliate_links deve ser uma lista")
    affiliates = data.get("affiliate_links", [])
    for affiliate in affiliates:
        if not isinstance(affiliate, dict) or not isinstance(affiliate.get("name"), str) or not isinstance(affiliate.get("url"), str):
            raise ValueError("Afiliados devem ter nome e URL verificados")
        if affiliate.get("verified_for_production") is not True:
            raise ValueError("Afiliado sem verificação atual para esta produção")
        if not affiliate["url"].startswith("https://"):
            raise ValueError("Link de afiliado deve usar HTTPS")
    chapters = data.get("chapters", [])
    if not isinstance(chapters, list):
        raise ValueError("Capítulos inválidos")
    if chapters and not (data["render_verified"] and data.get("chapters_verified") is True):
        raise ValueError("Timestamps exigem conferência no render final")
    for chapter in chapters:
        if not isinstance(chapter, dict) or not isinstance(chapter.get("seconds"), int) or isinstance(chapter.get("seconds"), bool) or chapter["seconds"] < 0 or not isinstance(chapter.get("title"), str) or not chapter["title"].strip():
            raise ValueError("Capítulo inválido")
    if chapters and [c["seconds"] for c in chapters] != sorted(set(c["seconds"] for c in chapters)):
        raise ValueError("Capítulos devem estar ordenados e sem tempo duplicado")
    pending = [title for key, title in (
        ("creator_approved", "aprovação do criador"),
        ("render_verified", "render final conferido"),
        ("qa_approved", "QA final aprovado")
    ) if not data[key]]
    description = data["description"].strip()
    if affiliates:
        description += "\n\nLinks de afiliados (verificados):\n" + "\n".join(
            f"{a['name']}: {a['url']}" for a in affiliates
        )
        description += "\n\nEste conteúdo contém links de afiliados. Posso receber uma comissão se você comprar por eles."
    if chapters:
        description += "\n\nCapítulos:\n" + "\n".join(
            f"{c['seconds']//3600:02d}:{(c['seconds']//60)%60:02d}:{c['seconds']%60:02d} {c['title']}" for c in chapters
        )
    description += "\n\nFontes:\n" + "\n".join(data["sources"])
    return {
        "status": "KIT PRONTO PARA POSTAGEM MANUAL" if not pending else "KIT PARCIAL — PENDÊNCIAS",
        "production_id": data["production_id"],
        "title": data["title"].strip(),
        "description": description,
        "tags": list(dict.fromkeys(t.strip() for t in data["tags"])),
        "pinned_comment": data.get("pinned_comment", ""),
        "video_file": data["video_file"], "thumbnail_file": data["thumbnail_file"],
        "pending": pending, "posting_mode": "MANUAL_BY_CREATOR",
        "publishing_performed": False, "writes_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerar kit para postagem exclusivamente manual pelo criador")
    parser.add_argument("input", type=Path, help="JSON com dados da produção aprovada")
    args = parser.parse_args()
    print(json.dumps(build_kit(json.loads(args.input.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
