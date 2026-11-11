"""I03: validated timed captions from verified word-level speech timestamps.

Produces SRT and frame cues for an independent Remotion renderer. It does NOT
transcribe, align audio, render video or certify audiovisual synchronization.
Scenes marked visual_text_only MUST have no spoken audio. No posting.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_captions(words: list[dict], *, fps: int = 30,
                   visual_text_only: list[dict] | None = None,
                   max_words: int = 7) -> dict:
    if type(fps) is not int or fps <= 0 or fps > 120:
        raise ValueError("FPS inválido")
    if type(max_words) is not int or not 1 <= max_words <= 12:
        raise ValueError("Número de palavras por legenda inválido")
    if not isinstance(words, list) or not words:
        raise ValueError("Fornecer timestamps reais de palavras faladas")
    excluded = visual_text_only if visual_text_only is not None else []
    if not isinstance(excluded, list):
        raise ValueError("Intervalos tipográficos inválidos")

    def interval(row: dict, label: str) -> tuple[int, int]:
        if not isinstance(row, dict):
            raise ValueError(f"{label} inválido")
        start, end = row.get("start_ms"), row.get("end_ms")
        if type(start) is not int or type(end) is not int or start < 0 or end <= start:
            raise ValueError(f"{label}: timestamps inválidos")
        return start, end

    intervals = sorted(interval(x, "Intervalo de cena") for x in excluded)
    if any(a[1] > b[0] for a, b in zip(intervals, intervals[1:])):
        raise ValueError("Intervalos tipográficos sobrepostos")
    spoken = []
    previous_end = -1
    for word in words:
        start, end = interval(word, "Palavra")
        text = word.get("text")
        if not isinstance(text, str) or not text.strip() or "\n" in text or "\r" in text:
            raise ValueError("Texto falado inválido")
        if start < previous_end:
            raise ValueError("Palavras sem ordem temporal ou sobrepostas")
        if any(start < b and end > a for a, b in intervals):
            raise ValueError("Uma cena marcada apenas como texto contém fala")
        previous_end = end
        spoken.append((start, end, text.strip()))

    groups = []
    batch = []
    for word in spoken:
        if batch and (len(batch) >= max_words or word[0] - batch[-1][1] > 650
                      or word[1] - batch[0][0] > 2700):
            groups.append(batch)
            batch = []
        batch.append(word)
        if word[2].endswith((".", "!", "?")):
            groups.append(batch)
            batch = []
    if batch:
        groups.append(batch)

    def stamp(ms: int) -> str:
        h, rem = divmod(ms, 3600000)
        m, rem = divmod(rem, 60000)
        s, milli = divmod(rem, 1000)
        return f"{h:02}:{m:02}:{s:02},{milli:03}"

    cues = []
    srt = []
    prev_end_frame = -1
    for i, group in enumerate(groups, 1):
        start, end = group[0][0], group[-1][1]
        start_frame = start * fps // 1000
        end_frame = (end * fps + 999) // 1000
        if start_frame < prev_end_frame:
            raise ValueError("Frames de legenda sobrepostos: aumentar precisão ou reduzir FPS")
        if end_frame <= start_frame:
            end_frame = start_frame + 1
        text = " ".join(w[2] for w in group)
        cues.append({"text": text, "start_ms": start, "end_ms": end,
                     "start_frame": start_frame, "duration_frames": end_frame-start_frame})
        srt.append(f"{i}\n{stamp(start)} --> {stamp(end)}\n{text}")
        prev_end_frame = end_frame
    return {"status": "TIMED_CUES_READY_FOR_RENDER",
            "cues": cues, "srt": "\n\n".join(srt) + "\n",
            "input_timestamp_source": "caller_supplied_verified_words",
            "audio_sync_verified": False, "render_verified": False,
            "publishing_performed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON com words e visual_text_only")
    parser.add_argument("--srt-output", type=Path, help="Local onde salvar SRT (sem postar)")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    result = build_captions(data["words"], fps=data.get("fps", 30),
                            visual_text_only=data.get("visual_text_only", []))
    if args.srt_output:
        args.srt_output.write_text(result["srt"], encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "srt"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
