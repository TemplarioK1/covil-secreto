#!/usr/bin/env python3
"""Organiza e otimiza as imagens referenciadas por um projeto Jekyll."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote
import shutil

import yaml
from PIL import Image, ImageOps

PENDING_DELETE: dict[Path, set[str]] = {}

ROOT = Path(".")
MEDIA_PREFIX = "/media/images/"
LIMITS = {
    "icon": ((640, 400), "icone.webp"),
    "cover": ((1600, 900), "capa.webp"),
}
SCREEN_FIELDS = ("screenshot_1", "screenshot_2", "screenshot_3", "screenshot_4")


def read_project(path: Path):
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.S)
    if not match:
        raise ValueError(f"Front matter YAML não encontrado em {path}")
    data = yaml.safe_load(match.group(1)) or {}
    return raw, match, data


def repo_path(public_path: str) -> Path | None:
    value = unquote(str(public_path or "").strip())
    if not value or value.startswith(("http://", "https://", "//", "data:")):
        return None
    value = value.split("?", 1)[0].split("#", 1)[0]
    if value.startswith(MEDIA_PREFIX):
        relative = value.lstrip("/")
    elif value.startswith("media/images/"):
        relative = value
    else:
        return None
    path = (ROOT / relative).resolve()
    if ROOT.resolve() not in path.parents:
        raise ValueError(f"Caminho de mídia inseguro: {public_path}")
    return path


def optimize(source: Path, destination: Path, max_size: tuple[int, int]) -> Path:
    if not source.is_file():
        raise FileNotFoundError(f"Imagem referenciada não encontrada: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as original:
        if getattr(original, "is_animated", False):
            # Preserve GIFs animados sem remover a animação.
            destination = destination.with_suffix(source.suffix.lower())
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            return destination
        image = ImageOps.exif_transpose(original)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(destination, "WEBP", quality=84, method=6)
    return destination


def download_repo_path(public_path: str) -> Path | None:
    value = unquote(str(public_path or "").strip()).split("?", 1)[0].split("#", 1)[0]
    if not value.startswith("/downloads/") and not value.startswith("downloads/"):
        return None
    path = (ROOT / value.lstrip("/")).resolve()
    if ROOT.resolve() not in path.parents:
        raise ValueError(f"Caminho de download inseguro: {public_path}")
    return path


def is_used_elsewhere(old_public_path: str, current_project: Path) -> bool:
    needle = str(old_public_path).strip()
    for candidate in (ROOT / "_projetos").glob("*.md"):
        if candidate.resolve() == current_project.resolve():
            continue
        if needle in candidate.read_text(encoding="utf-8"):
            return True
    return False


def process_reference(public_path: str, destination_public: str, max_size, current_project: Path):
    source = repo_path(public_path)
    if source is None:
        return public_path
    destination = repo_path(destination_public)
    if destination is None:
        raise ValueError(f"Destino inválido: {destination_public}")
    if source.resolve() == destination.resolve():
        return destination_public
    destination = optimize(source, destination, max_size)
    if destination.suffix.lower() != ".webp":
        destination_public = str(Path(destination_public).with_suffix(destination.suffix))
    PENDING_DELETE.setdefault(source, set()).add(str(public_path).strip())
    return destination_public


def process(project_file: Path) -> bool:
    raw, match, data = read_project(project_file)
    slug = project_file.stem
    changed = False

    for field, (size, filename) in LIMITS.items():
        old = data.get(field)
        if old:
            new = f"{MEDIA_PREFIX}projetos/{slug}/{filename}"
            updated = process_reference(old, new, size, project_file)
            if updated != old:
                data[field] = updated
                changed = True

    legacy = data.get("screenshots")
    if isinstance(legacy, list):
        updated_list = []
        for index, old in enumerate(legacy, start=1):
            new = f"{MEDIA_PREFIX}projetos/{slug}/screenshot-{index:02d}.webp"
            updated = process_reference(old, new, (1280, 720), project_file)
            updated_list.append(updated)
            changed |= updated != old
        data["screenshots"] = updated_list

    for index, field in enumerate(SCREEN_FIELDS, start=1):
        old = data.get(field)
        if old:
            new = f"{MEDIA_PREFIX}projetos/{slug}/screenshots/screenshot-{index:02d}.webp"
            updated = process_reference(old, new, (1280, 720), project_file)
            if updated != old:
                data[field] = updated
                changed = True

    old_download = data.get("download")
    if old_download:
        source_zip = download_repo_path(old_download)
        if source_zip is not None:
            if not source_zip.is_file():
                raise FileNotFoundError(f"Arquivo ZIP referenciado não encontrado: {source_zip}")
            target_zip = ROOT / "downloads" / "projetos" / slug / source_zip.name
            target_zip.parent.mkdir(parents=True, exist_ok=True)
            if source_zip.resolve() != target_zip.resolve():
                shutil.copy2(source_zip, target_zip)
                PENDING_DELETE.setdefault(source_zip.resolve(), set()).add(str(old_download).strip())
                data["download"] = "/" + target_zip.as_posix()
                changed = True

    if changed:
        frontmatter = yaml.safe_dump(
            data, allow_unicode=True, sort_keys=False, default_flow_style=False
        ).rstrip()
        project_file.write_text(
            f"---\n{frontmatter}\n---\n{match.group(2)}",
            encoding="utf-8",
        )
    return changed


def cleanup_pending():
    projects = list((ROOT / "_projetos").glob("*.md"))
    for source, old_refs in PENDING_DELETE.items():
        still_referenced = False
        for candidate in projects:
            content = candidate.read_text(encoding="utf-8")
            if any(old_ref in content for old_ref in old_refs):
                still_referenced = True
                break
        if not still_referenced:
            source.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.all:
        projects = sorted((ROOT / "_projetos").glob("*.md"))
        changed = False
        for project in projects:
            changed = process(project) or changed
    elif args.project:
        project = Path(args.project)
        if not project.is_file() or project.parent != Path("_projetos"):
            raise SystemExit("Informe o caminho de um projeto dentro de _projetos/.")
        changed = process(project)
    else:
        raise SystemExit("Use --project _projetos/arquivo.md ou --all.")
    cleanup_pending()
    print("Imagens e anexos organizados; front matter atualizado." if changed else
          "Nenhuma mídia local pendente para processar.")


if __name__ == "__main__":
    main()
