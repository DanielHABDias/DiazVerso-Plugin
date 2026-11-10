#!/usr/bin/env python3
"""Constrói e inspeciona um ZIP reproduzível do plugin Diazverso (stdlib Python).

Não instala plugins, não executa scripts das skills e não envia mídia a serviços.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
DOCS = (
    "docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md",
    "docs/ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md",
    "docs/RASCUNHO_IDENTIDADE_DIAZVERSO_1.0.md",
    "docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md",
    "docs/DECISOES_E_CONTEXTO.md",
    "docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md",
    "docs/TERCEIROS_E_LICENCAS.md",
)
ALLOWED_SUFFIXES = {".md", ".json", ".py", ".ts", ".tsx", ".yaml",
                    ".yml", ".png", ".jpg", ".jpeg", ".webp", ".mp3",
                    ".wav", ".txt", ".gitkeep"}
FORBIDDEN_NAMES = {".env", ".env.local", "id_rsa", "credentials.json", "secret.json"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_allowed(path: Path) -> bool:
    # Path.suffix devolve "" para dotfiles como ".gitkeep".
    # Aceitar somente o marcador conhecido, não qualquer dotfile.
    return path.name in {"LICENSE", ".gitkeep"} or path.suffix.lower() in ALLOWED_SUFFIXES


def collect() -> tuple[list[str], dict]:
    manifest_path = ROOT / "plugin.json"
    require(manifest_path.is_file(), "plugin.json ausente")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(isinstance(manifest, dict) and manifest.get("$schema") == SCHEMA,
            "Manifesto não é Agent Plugins 1.0")
    require(manifest.get("name") == "diazverso", "Nome inesperado")
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", ""))),
            "Versão deve ser SemVer simples")

    paths: list[Path] = [manifest_path]
    for folder_name in ("skills", "assets", "schemas"):
        folder = ROOT / folder_name
        require(folder.is_dir(), f"Pasta essencial ausente: {folder_name}")
        paths.extend(p for p in folder.rglob("*") if p.is_file())
    for name in DOCS:
        file = ROOT / name
        if file.is_file():
            paths.append(file)

    checked = []
    for file in paths:
        require(not file.is_symlink(), f"Symlink proibido: {file}")
        rel = file.relative_to(ROOT).as_posix()
        require(file.name not in FORBIDDEN_NAMES, f"Arquivo confidencial: {rel}")
        require(is_allowed(file) or rel == "plugin.json", f"Extensão inesperada: {rel}")
        require(".." not in Path(rel).parts, f"Caminho inseguro: {rel}")
        checked.append(rel)
    unique = sorted(set(checked))
    require(len(unique) == len(checked), "Arquivos duplicados no pacote")

    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    require(len(skills) >= 2, "O pacote precisa ter pelo menos duas skills")
    names: list[str] = []
    for file in skills:
        text = file.read_text(encoding="utf-8")
        require(len(text.encode("utf-8")) <= 1024 * 1024,
                f"Skill excede 1 MiB: {file}")
        fm = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        require(fm is not None, f"Frontmatter inválido: {file}")
        name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm.group(1), re.M)
        desc = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        require(name is not None and name.group(1) == file.parent.name,
                f"Nome/pasta divergentes: {file}")
        require(desc is not None and desc.group(1).strip().strip('"'),
                f"Descrição vazia: {file}")
        names.append(name.group(1))
    require(len(set(names)) == len(names), "Nomes de skills duplicados")

    entry = manifest.get("extensions", {}).get("com.openai", {}).get("onboardingSkill")
    require(entry == "./skills/diazverso-setup/SKILL.md",
            "Onboarding do manifesto não corresponde à setup")
    require(entry[2:] in unique, "Onboarding ausente do pacote")

    for name in ("context-optimization", "video-editing",
                 "analyze-video-editing", "find-broll"):
        require(f"skills/{name}/SKILL.md" in unique and
                f"skills/{name}/LICENSE" in unique,
                f"Skill externa incompleta ou sem licença: {name}")

    asset_manifest = json.loads((ROOT / "assets/manifest.json").read_text(encoding="utf-8"))
    for item in asset_manifest["assets"]:
        rel = item["path"]
        require(rel in unique, f"Asset referenciado não empacotado: {rel}")
        data = (ROOT / rel).read_bytes()
        require(len(data) == item["size_bytes"], f"Tamanho inválido: {rel}")
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(git_blob == item["git_blob_sha1"], f"Hash Git divergente: {rel}")
        if item["mime_type"] == "image/png":
            validate_png(data)
    return unique, manifest


def validate_png(data: bytes) -> None:
    require(data.startswith(b"\x89PNG\r\n\x1a\n"), "PNG inválido")
    offset, found_iend, found_idat = 8, False, False
    while offset + 12 <= len(data):
        size = struct.unpack_from(">I", data, offset)[0]
        limit = offset + 12 + size
        require(limit <= len(data), "Chunk PNG truncado")
        chunk = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + size]
        expected = struct.unpack_from(">I", data, offset + 8 + size)[0]
        require(zlib.crc32(chunk + payload) == expected, f"CRC PNG errado: {chunk!r}")
        found_idat |= chunk == b"IDAT"
        offset = limit
        if chunk == b"IEND":
            found_iend = True
            break
    require(found_idat and found_iend and offset == len(data), "PNG incompleto")


def package(output: Path) -> dict:
    paths, manifest = collect()
    output = output.expanduser().resolve()
    require(ROOT not in output.parents and output != ROOT,
            "ZIP deve estar fora do repositório")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for rel in paths:
            info = zipfile.ZipInfo(rel, date_time=(2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, (ROOT / rel).read_bytes())
    with zipfile.ZipFile(output, "r") as archive:
        require(archive.namelist() == paths, "Lista de arquivos divergente")
        require(archive.testzip() is None, "Falha CRC do ZIP")
        for rel in paths:
            require(archive.read(rel) == (ROOT / rel).read_bytes(),
                    f"Arquivo mudou no ZIP: {rel}")
    return {
        "result": "PACKAGE_VALIDATED",
        "host_installation": "NOT_TESTED",
        "plugin": manifest["name"],
        "version": manifest["version"],
        "files": len(paths),
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "size_bytes": output.stat().st_size,
        "output": str(output),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT.parent / "diazverso-plugin-full.zip")
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output), ensure_ascii=False, indent=2))
        return 0
    except (OSError, KeyError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"PACKAGE_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
