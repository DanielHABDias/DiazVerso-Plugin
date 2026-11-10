#!/usr/bin/env python3
"""B06: monta e inspeciona um pacote MÍNIMO de teste do plugin Diazverso.

Não instala o plugin e não invoca skills em ChatGPT/Codex.
Usa apenas a biblioteca padrão do Python.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "plugin.json",
    "skills/diazverso-setup/SKILL.md",
    "skills/diazverso-core/SKILL.md",
)
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z")
NAME = re.compile(r"[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?\Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def get_text(rel_path: str) -> str:
    path = ROOT / rel_path
    require(path.is_file() and not path.is_symlink(), f"Arquivo ausente/inválido: {rel_path}")
    return path.read_text(encoding="utf-8")


def parse_skill(rel_path: str) -> dict[str, str]:
    body = get_text(rel_path)
    require(len(body.encode("utf-8")) <= 1024 * 1024, f"Skill excede 1 MiB: {rel_path}")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", body, flags=re.S)
    require(match is not None, f"Frontmatter YAML ausente: {rel_path}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key_value = re.fullmatch(r"([a-z][a-z0-9_-]*):\s+(.+)", line)
        require(key_value is not None, f"Campo de frontmatter não suportado: {rel_path}")
        key, value = key_value.groups()
        require(key not in fields, f"Campo duplicado: {key}")
        # As skills V1.0 usam somente strings simples ou entre aspas duplas.
        fields[key] = json.loads(value) if value.startswith('"') else value.strip()
        require(isinstance(fields[key], str), f"Campo não textual: {key}")
    require(fields.get("name") == Path(rel_path).parent.name, f"Nome divergente: {rel_path}")
    require(bool(fields.get("description", "").strip()), f"Descrição vazia: {rel_path}")
    require(bool(body[match.end():].strip()), f"Skill sem instruções: {rel_path}")
    return fields


def validate_sources() -> dict:
    manifest = json.loads(get_text("plugin.json"))
    require(isinstance(manifest, dict), "plugin.json deve ser um objeto")
    require(manifest.get("$schema") == SCHEMA, "Schema portátil incorreto")
    name = manifest.get("name", "")
    require(isinstance(name, str) and NAME.fullmatch(name) is not None, "Nome inválido")
    require("--" not in name and ".." not in name, "Nome contém sequência proibida")
    version = manifest.get("version", "")
    require(isinstance(version, str) and SEMVER.fullmatch(version) is not None, "SemVer inválido")
    for legacy_key in ("skills", "mcpServers", "apps", "interface"):
        require(legacy_key not in manifest, f"Chave não portátil no manifesto: {legacy_key}")
    openai = manifest.get("extensions", {}).get("com.openai", {})
    require(isinstance(openai, dict), "Extensão OpenAI inválida")
    interface = openai.get("interface", {})
    require(isinstance(interface, dict), "Interface OpenAI inválida")
    short = interface.get("shortDescription")
    require(isinstance(short, str) and 0 < len(short) <= 30, "Descrição curta inválida")
    caps = interface.get("capabilities")
    require(isinstance(caps, list) and all(isinstance(x, str) and x.strip() for x in caps), "Capacidades inválidas")
    onboarding = openai.get("onboardingSkill")
    require(onboarding == "./skills/diazverso-setup/SKILL.md", "Onboarding não corresponde à setup")
    require(onboarding[2:] in FILES, "Skill de onboarding ausente do ZIP")

    skills = [parse_skill(path) for path in FILES[1:]]
    names = [skill["name"] for skill in skills]
    require(len(names) == len(set(names)), "Skills com nomes duplicados")
    return {"name": name, "version": version, "skills": names, "onboarding": onboarding}


def package(output: Path) -> dict:
    manifest = validate_sources()
    output = output.expanduser().resolve()
    require(ROOT not in output.parents and output != ROOT, "Arquivo ZIP deve ficar fora do repositório")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for rel_path in FILES:
            info = zipfile.ZipInfo(rel_path, date_time=(2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, (ROOT / rel_path).read_bytes())

    with zipfile.ZipFile(output) as archive:
        require(archive.namelist() == list(FILES), "Layout do ZIP divergente")
        require(archive.testzip() is None, "Falha no CRC do ZIP")
        for rel_path in FILES:
            require(archive.read(rel_path) == (ROOT / rel_path).read_bytes(), f"Arquivo alterado no ZIP: {rel_path}")

    return {
        "result": "PACKAGING_PASS",
        "host_installation": "NOT_TESTED",
        "file": str(output),
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "size_bytes": output.stat().st_size,
        "files": list(FILES),
        **manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=ROOT.parent / "diazverso-plugin-0.1.0-b06-test.zip",
        help="Destino do ZIP; deve ficar fora do repositório",
    )
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"B06 PACKAGING_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
