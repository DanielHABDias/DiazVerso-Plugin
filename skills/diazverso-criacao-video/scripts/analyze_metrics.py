"""K05: summarize actual post-publication YouTube metrics without API access.

Accept already verified measurements from a source supplied by the creator.
No scheduled fetching, automated posting, or edits to the Ideas spreadsheet.
"""
from __future__ import annotations
from datetime import datetime, timezone
import argparse
import json
import math
from pathlib import Path


FIELDS = {"views", "impressions", "clicks", "likes", "comments",
          "average_view_duration_seconds", "video_duration_seconds",
          "watch_time_hours"}


def analyze(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Dados devem ser um objeto")
    required = ("production_id", "youtube_url", "as_of", "source", "views")
    if any(not isinstance(data.get(k), str) or not data[k].strip()
           for k in required if k != "views"):
        raise ValueError("ID, URL, data da coleta e fonte real são obrigatórios")
    import re
    if not re.fullmatch(r"(?:VD|SH)_\d{4,}", data["production_id"]):
        raise ValueError("ID da produção inválido")
    url = data["youtube_url"]
    if not re.fullmatch(r"https://(?:www\.)?youtube\.com/(?:watch\?v=|shorts/)[A-Za-z0-9_-]{6,}(?:[&#?].*)?|https://youtu\.be/[A-Za-z0-9_-]{6,}(?:[?&#].*)?", url):
        raise ValueError("URL YouTube precisa ser real e válida")
    try:
        when = datetime.fromisoformat(data["as_of"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Data ISO da coleta inválida") from exc
    if when.tzinfo is None:
        raise ValueError("Data de coleta deve conter fuso")
    if when > datetime.now(timezone.utc):
        raise ValueError("Métricas de data futura não são válidas")
    for k in FIELDS & data.keys():
        n = data[k]
        if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or n < 0:
            raise ValueError(f"Métrica inválida: {k}")
    if "views" not in data:
        raise ValueError("Visualizações são obrigatórias")
    if data.get("video_duration_seconds") == 0:
        raise ValueError("Duração do vídeo não pode ser zero")
    result = {"production_id": data["production_id"], "source": data["source"],
              "as_of": data["as_of"], "observed": {k: data[k] for k in sorted(FIELDS & data.keys())},
              "metrics_are_observations_not_causality": True,
              "hypotheses_for_ideas": [], "writes_performed": False}
    if "impressions" in data and "clicks" in data and data["impressions"]:
        if data["clicks"] > data["impressions"]:
            raise ValueError("Cliques não podem superar impressões")
        result["derived_ctr_percent"] = round(100 * data["clicks"] / data["impressions"], 2)
    if "average_view_duration_seconds" in data and "video_duration_seconds" in data:
        ratio = data["average_view_duration_seconds"] / data["video_duration_seconds"]
        result["avg_view_duration_percent"] = round(100 * ratio, 2)
        result["note"] = "Duração média percentual descritiva; pode superar 100% por repetição."
    result["hypotheses_for_ideas"].append({
        "type": "HIPÓTESE PARA PESQUISAR",
        "text": "Comparar tema, embalagem e abertura com outros vídeos do próprio canal antes de inferir o motivo de desempenho.",
        "must_be_approved_before_adding_to_ideas": True
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisar métricas reais fornecidas pelo criador; sem postar ou gravar dados")
    parser.add_argument("snapshot", type=Path, help="Arquivo JSON contendo medições verificadas pelo criador")
    args = parser.parse_args()
    print(json.dumps(analyze(json.loads(args.snapshot.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
