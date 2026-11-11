#!/usr/bin/env python3
"""Gera requests portáteis da Google Docs API para UM roteiro Diazverso.

Somente biblioteca padrão Python. Não conecta Drive, não modifica planilhas e
não declara sucesso da criação; a skill executora deve usar o conector Google.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
TEMPLATES = {
    "LONGO": "templates/roteiro-longo-v1.json",
    "SHORT": "templates/roteiro-short-v1.json",
}
SCHEMA = "diazverso-google-doc-template-v1"
STYLE_NAMES = {"TITLE", "SUBTITLE", "HEADING_1", "HEADING_2", "NORMAL_TEXT"}


def utf16_length(value: str) -> int:
    """Índices da Google Docs API são em unidades UTF-16, não em code points."""
    return len(value.encode("utf-16-le")) // 2


def prepare_title(value: str) -> str:
    normalized = " ".join(value.split()).strip()
    if not normalized or len(normalized) > 120:
        raise ValueError("Tema obrigatório com até 120 caracteres")
    return normalized


def requests_for(tipo: str, video_id: str, tema: str) -> dict:
    tipo = tipo.upper().strip()
    if tipo not in TEMPLATES:
        raise ValueError("Tipo inválido: use LONGO ou SHORT")
    expected = "VD" if tipo == "LONGO" else "SH"
    if not re.fullmatch(expected + r"_[0-9]{4,}", video_id):
        raise ValueError(f"ID inválido para {tipo}: {video_id}")
    assunto = prepare_title(tema)
    path = PLUGIN_ROOT / TEMPLATES[tipo]
    template = json.loads(path.read_text(encoding="utf-8"))
    if template.get("schema") != SCHEMA or template.get("tipo") != tipo:
        raise ValueError(f"Template incompatível: {path}")
    paragraphs = template.get("paragraphs")
    if not isinstance(paragraphs, list) or not paragraphs:
        raise ValueError("Template sem parágrafos")
    styled = []
    for obj in paragraphs:
        if not isinstance(obj, dict) or obj.get("style") not in STYLE_NAMES:
            raise ValueError("Estilo de parágrafo inválido")
        text = obj.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Texto vazio no template")
        # Evita repetir instruções ou copiar ID de outra produção.
        text = (text.replace("[VD_####]", video_id)
                    .replace("[SH_####]", video_id)
                    .replace("VD_####", video_id)
                    .replace("SH_####", video_id)
                    .replace("[TEMA]", assunto)
                    .replace("[assunto]", assunto))
        styled.append((text, obj["style"]))

    body = "\n".join(line for line, _ in styled) + "\n"
    requests = [{"insertText": {"endOfSegmentLocation": {}, "text": body}}]
    pos = 1
    bold_labels = set(template.get("bold_labels", []))
    for text, style in styled:
        end = pos + utf16_length(text + "\n")
        if style != "NORMAL_TEXT":
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": pos, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": style},
                    "fields": "namedStyleType",
                }
            })
        if text in bold_labels:
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": pos,
                              "endIndex": pos + utf16_length(text)},
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            })
        pos = end

    return {
        "title": f"{video_id} — {assunto} — Roteiro",
        "type": tipo,
        "id": video_id,
        "requests": requests,
        "expected": {
            "paragraphs": len(styled),
            "last_utf16_index": pos,
            "source_template": TEMPLATES[tipo],
            "host_writing": "NOT_EXECUTED",
            "sheet_sync": "NOT_EXECUTED",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tipo", required=True, choices=tuple(TEMPLATES))
    parser.add_argument("--id", required=True)
    parser.add_argument("--tema", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = requests_for(args.tipo, args.id, args.tema)
        payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ROTEIRO_REQUESTS_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
