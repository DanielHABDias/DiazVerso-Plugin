"""publication-kit: assemble a copy-ready kit for MANUAL publication by the creator.

Uses only creator-approved input; never uploads, schedules, publishes, or
pretends files were rendered or inspected. No Google API calls.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


RULE = "─" * 20
DISCLOSURE = ("Os links de compra acima podem ser de afiliado. Se você comprar por eles, o Diazverso pode receber "
              "uma comissão, sem custo adicional para você, e isso ajuda o canal.")
ABOUT = ("No Diazverso, o universo geek ganha histórias, análises, explicações e opiniões.\n\n"
         "Marvel, DC, super-heróis, filmes, séries, animações, games e tudo que faz parte desse universo.\n\n"
         "Inscreva-se no Diazverso:\nhttps://www.youtube.com/@DiazVerso?sub_confirmation=1\n\n"
         "Instagram:\nhttps://www.instagram.com/diazversoyt/")
NOTICE = ("Trechos e materiais de terceiros podem ser utilizados em contextos de comentário, crítica, análise, "
          "informação e entretenimento. Os direitos sobre esses materiais pertencem aos seus respectivos titulares.")


def _section(title: str, body: str) -> str:
    return f"{RULE}\n{title}\n{RULE}\n\n{body}"


def _text(value, key: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Campo obrigatório inválido: {key}")
    return value.strip()


def _url(value, key: str) -> str:
    if not isinstance(value, str) or not value.startswith("https://"):
        raise ValueError(f"Link deve usar HTTPS: {key}")
    return value


def _clock(seconds: int) -> str:
    hours, rest = divmod(seconds, 3600)
    return f"{hours}:{rest // 60:02d}:{rest % 60:02d}" if hours else f"{rest // 60:02d}:{rest % 60:02d}"


def build_description(data: dict, chapters: list) -> str:
    """Descrição no formato do canal (references/descricao.md)."""
    parts = [_text(data.get("opening"), "opening"), _text(data.get("summary"), "summary")]
    if chapters:
        parts.append(_section("CAPÍTULOS", "\n".join(f"{_clock(c['seconds'])} {c['title'].strip()}" for c in chapters)))
    related = data.get("related_videos", [])
    if related:
        parts.append(_section("ASSISTA TAMBÉM", "\n\n".join(
            f"{_text(v.get('title'), 'related_videos.title')}\n{_text(v.get('pitch'), 'related_videos.pitch').rstrip(':')}:\n{_url(v.get('url'), 'related_videos.url')}"
            for v in related)))
    affiliates = data.get("affiliate_links", [])
    if affiliates:
        parts.append(_section("LINKS E RECOMENDAÇÕES", "\n\n".join(
            f"{a['name'].strip().upper()}\n{_text(a.get('pitch'), 'affiliate_links.pitch').rstrip(':')}:\n{a['url']}" for a in affiliates)
            + "\n\n" + DISCLOSURE))
    parts.append(_section("SOBRE O DIAZVERSO", ABOUT))
    credits = ["Obras e arcos abordados:\n" + "\n".join(w.strip() for w in data["works"])]
    credits += [f"{_text(s.get('label'), 'official_sources.label')} — {_text(s.get('about'), 'official_sources.about')}:\n{_url(s.get('url'), 'official_sources.url')}"
                for s in data.get("official_sources", [])]
    music = data.get("music")
    if music:
        tracks = music.get("tracks") or []
        composer = music.get("composer") or {}
        if not tracks:
            raise ValueError("Trilha sem faixas")
        names = [f"“{_text(t.get('title'), 'music.title')}”" for t in tracks]
        joined = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " e " + names[-1]
        label = "Música" if len(names) == 1 else "Músicas"
        lines = [f"{label}: {joined}, de {_text(composer.get('name'), 'music.composer')}."]
        lines += [f"{t['title'].strip()}: {_url(t.get('url'), 'music.url')}" for t in tracks]
        if composer.get("url"):
            lines.append(f"Canal do compositor: {_url(composer['url'], 'music.composer.url')}")
        credits.append("\n".join(lines))
    parts.append(_section("FONTES E CRÉDITOS", "\n\n".join(credits)))
    parts.append(_section("AVISO", NOTICE))
    tags = [t if t.startswith("#") else "#" + t for t in (h.strip().replace(" ", "") for h in data["hashtags"])]
    if "#Diazverso" not in tags:
        tags.append("#Diazverso")
    tags = [t for t in tags if t != "#Diazverso"] + ["#Diazverso"]
    parts.append(f"{RULE}\n\n" + " ".join(tags))
    return "\n\n".join(parts)


def build_kit(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Esperado objeto")
    required = ("production_id", "title", "opening", "summary", "works", "hashtags", "tags",
                "video_file", "thumbnail_file", "creator_approved", "render_verified", "qa_approved")
    if any(k not in data for k in required):
        raise ValueError("Campos obrigatórios ausentes")
    import re
    if not isinstance(data["production_id"], str) or not re.fullmatch(r"(VD|SH)_\d{4,}", data["production_id"]):
        raise ValueError("ID inválido")
    for key in ("title", "video_file", "thumbnail_file"):
        _text(data[key], key)
    for key in ("works", "hashtags", "tags"):
        if not isinstance(data[key], list) or any(not isinstance(v, str) or not v.strip() for v in data[key]):
            raise ValueError(f"{key} deve ser uma lista de textos")
    if not data["works"]:
        raise ValueError("Listar as obras e arcos abordados")
    if any(type(data[k]) is not bool for k in ("creator_approved", "render_verified", "qa_approved")):
        raise ValueError("Flags de verificação devem ser booleanas")
    for key in ("affiliate_links", "related_videos", "official_sources"):
        if not isinstance(data.get(key, []), list):
            raise ValueError(f"{key} deve ser uma lista")
    for affiliate in data.get("affiliate_links", []):
        if not isinstance(affiliate, dict) or not isinstance(affiliate.get("name"), str) or not isinstance(affiliate.get("url"), str):
            raise ValueError("Afiliados devem ter nome e URL verificados")
        if affiliate.get("verified_for_production") is not True:
            raise ValueError("Afiliado sem verificação atual para esta produção")
        _url(affiliate["url"], "affiliate_links.url")
    chapters = data.get("chapters", [])
    if not isinstance(chapters, list):
        raise ValueError("Capítulos inválidos")
    if chapters and not (data["render_verified"] and data.get("chapters_verified") is True):
        raise ValueError("Timestamps exigem conferência no render final")
    for chapter in chapters:
        if not isinstance(chapter, dict) or not isinstance(chapter.get("seconds"), int) or isinstance(chapter.get("seconds"), bool) or chapter["seconds"] < 0 or not isinstance(chapter.get("title"), str) or not chapter["title"].strip():
            raise ValueError("Capítulo inválido")
    seconds = [c["seconds"] for c in chapters]
    if chapters and (seconds != sorted(set(seconds)) or seconds[0] != 0 or len(seconds) < 3 or any(b - a < 10 for a, b in zip(seconds, seconds[1:]))):
        raise ValueError("Capítulos: começar em 00:00, ao menos três, ordenados e com 10 s ou mais cada")
    pending = [title for key, title in (
        ("creator_approved", "aprovação do criador"),
        ("render_verified", "render final conferido"),
        ("qa_approved", "QA final aprovado")
    ) if not data[key]]
    if not chapters:
        pending.append("capítulos com os tempos do render final")
    if not data.get("music"):
        pending.append("créditos da trilha licenciada")
    return {
        "status": "KIT PRONTO PARA POSTAGEM MANUAL" if not pending else "KIT PARCIAL — PENDÊNCIAS",
        "production_id": data["production_id"],
        "title": data["title"].strip(),
        "description": build_description(data, chapters),
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
