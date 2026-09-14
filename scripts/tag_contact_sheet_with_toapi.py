#!/usr/bin/env python3
"""Strict one-SKU contact-sheet tagging through a user-selected ToAPIs model."""

from __future__ import annotations

import argparse
import base64
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps


ENDPOINT = "https://toapis.com/v1/chat/completions"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIEWS = {"front", "three_quarter", "side", "back", "detail", "unknown"}
FRAMINGS = {"full_body", "half_body", "upper_body", "closeup", "unknown"}
SUBJECTS = {"model_person", "product_flatlay", "product_detail", "brand_logo", "scene_background", "unknown"}
GENDERS = {"woman", "man", "ambiguous", "unknown"}
QUALITIES = {"high", "medium", "low", "unknown"}
DETAIL_TYPES = {"fabric", "neckline", "cuff", "zipper", "print_graphic", "stitching", "hem", "pocket", "hardware", "closure", "general_detail"}
HARD_EXCLUDED_DIR_NAMES = {"弃用", "过程文件", "生成结果", "输出结果", "备份", "备份目录"}
SKIP_DIR_PREFIXES = ("_aplus", "_influencer")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def update_status(root: Path, product: str, status: str, **details: Any) -> None:
    path = root / "_aplus_sync_run_status.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        data = {}
    data.setdefault("schema_version", 1)
    data["updated_at"] = now_iso()
    entry = data.setdefault("products", {}).setdefault(product, {})
    entry["analysis"] = {"status": status, "updated_at": now_iso(), **details}
    atomic_json(path, data)


def exact_product(root: Path, name: str) -> Path:
    if not name.strip() or "," in name:
        raise ValueError("--product must contain exactly one direct-child SKU folder name")
    product = root / name
    if not product.is_dir() or product.parent.resolve() != root.resolve():
        raise ValueError(f"Product is not an exact direct-child directory: {name}")
    return product


def is_hard_excluded(path: Path, product: Path) -> bool:
    try:
        parts = path.relative_to(product).parts[:-1]
    except ValueError:
        return True
    for part in parts:
        folded = part.casefold().strip()
        if folded.startswith(SKIP_DIR_PREFIXES):
            return True
        if folded in {name.casefold() for name in HARD_EXCLUDED_DIR_NAMES}:
            return True
        if any(term in folded for term in ("弃用", "过程文件", "生成结果", "输出结果", "备份", "backup")):
            return True
    return False


def candidates(product: Path) -> list[Path]:
    result = [
        path for path in product.rglob("*")
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTS
        and "contact_sheet" not in path.name.casefold()
        and not is_hard_excluded(path, product)
    ]
    return sorted(result, key=lambda p: str(p.relative_to(product)).casefold())


def load_font(size: int) -> ImageFont.ImageFont:
    for font_path in (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/msyh.ttc")):
        if font_path.exists():
            try:
                return ImageFont.truetype(str(font_path), size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def make_sheet(images: list[Path], output: Path) -> list[dict[str, str]]:
    cols, tile_w, tile_h, label_h = 4, 360, 440, 42
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), "white")
    draw, font = ImageDraw.Draw(sheet), load_font(22)
    manifest: list[dict[str, str]] = []
    for index, path in enumerate(images, start=1):
        image_id = f"I{index:03d}"
        manifest.append({"id": image_id, "path": str(path)})
        try:
            with Image.open(path) as source:
                tile = ImageOps.contain(source.convert("RGB"), (tile_w - 12, tile_h - 12))
        except Exception as exc:
            raise RuntimeError(f"Cannot read candidate image {path}: {exc}") from exc
        x, y = ((index - 1) % cols) * tile_w, ((index - 1) // cols) * (tile_h + label_h)
        sheet.paste(tile, (x + (tile_w - tile.width) // 2, y + (tile_h - tile.height) // 2))
        draw.rectangle((x, y + tile_h, x + tile_w - 1, y + tile_h + label_h - 1), fill="#111827")
        draw.text((x + 10, y + tile_h + 7), image_id, fill="white", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)
    return manifest


def data_url(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("Model response contains no JSON object")
    data = json.loads(cleaned[start : end + 1])
    if not isinstance(data, dict):
        raise ValueError("Model response JSON is not an object")
    return data


def normalize_enum(value: Any, allowed: set[str], field: str, image_id: str) -> str:
    normalized = str(value or "unknown").strip().casefold().replace("-", "_").replace(" ", "_")
    if normalized not in allowed:
        raise ValueError(f"{image_id}.{field} has invalid value: {value!r}")
    return normalized


def validate_tags(raw: dict[str, Any], manifest: list[dict[str, str]], product: Path, model: str) -> dict[str, Any]:
    expected = {item["id"] for item in manifest}
    if set(raw) != expected:
        raise ValueError(f"Tag coverage mismatch; missing={sorted(expected - set(raw))}, extra={sorted(set(raw) - expected)}")
    result: dict[str, Any] = {}
    for item in manifest:
        image_id, tag = item["id"], raw[item["id"]]
        if not isinstance(tag, dict):
            raise ValueError(f"{image_id} is not an object")
        contains_person, usable = tag.get("contains_person"), tag.get("usable_for_identity")
        if not isinstance(contains_person, bool) or not isinstance(usable, bool):
            raise ValueError(f"{image_id} boolean fields are invalid")
        subject = normalize_enum(tag.get("subject_type"), SUBJECTS, "subject_type", image_id)
        view = normalize_enum(tag.get("view"), VIEWS, "view", image_id)
        framing = normalize_enum(tag.get("framing"), FRAMINGS, "framing", image_id)
        gender = normalize_enum(tag.get("gender_presentation"), GENDERS, "gender_presentation", image_id)
        quality = normalize_enum(tag.get("identity_quality"), QUALITIES, "identity_quality", image_id)
        raw_details = tag.get("detail_types") or []
        if not isinstance(raw_details, list):
            raise ValueError(f"{image_id}.detail_types must be an array")
        details = [normalize_enum(value, DETAIL_TYPES, "detail_types", image_id) for value in raw_details]
        if not contains_person:
            subject, gender, usable = (subject if subject != "model_person" else "unknown"), "unknown", False
        if view == "back":
            usable = False
        relative = Path(item["path"]).relative_to(product)
        result[relative.as_posix()] = {
            "contains_person": contains_person, "subject_type": subject, "view": view, "framing": framing,
            "usable_for_identity": usable, "identity_quality": quality, "gender_presentation": gender,
            "detail_types": details,
            "source_folder": relative.parts[0] if len(relative.parts) > 1 else ".",
            "notes": str(tag.get("notes") or "").strip(), "source": model,
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--product", required=True, help="Exactly one direct-child SKU folder name")
    parser.add_argument("--model", required=True, help="Explicit ToAPIs analysis model, e.g. gpt-5.6-sol")
    parser.add_argument("--api-key", default=os.getenv("TOAPIS_API_KEY") or os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--request-timeout", type=int, default=300)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if not args.api_key:
        raise SystemExit("Missing ToAPIs key; set TOAPIS_API_KEY or pass --api-key")
    root = Path(args.root).expanduser().resolve()
    product = exact_product(root, args.product)
    work, tags_path = product / "_aplus_creative_work", product / "_aplus_creative_work" / "aigc_model_view_tags.json"
    images = candidates(product)
    expected_keys = {path.relative_to(product).as_posix() for path in images}
    if tags_path.exists() and not args.overwrite:
        existing = json.loads(tags_path.read_text(encoding="utf-8"))
        if (
            set(existing) == expected_keys
            and existing
            and all(isinstance(v, dict) and v.get("source") == args.model for v in existing.values())
        ):
            update_status(root, product.name, "exists_validated", model=args.model, tags_path=str(tags_path))
            print(tags_path)
            return 0
        raise SystemExit("Existing tags are incomplete or use another source; rerun with --overwrite after review")
    if not images:
        raise SystemExit(f"No allowed candidate images found for {product.name}")
    work.mkdir(parents=True, exist_ok=True)
    sheet_path = work / "analysis_contact_sheet.jpg"
    manifest = make_sheet(images, sheet_path)
    atomic_json(work / "analysis_contact_sheet_manifest.json", [{"id": x["id"], "relative_path": str(Path(x["path"]).relative_to(product))} for x in manifest])
    prompt = (
        "Classify every labeled apparel image in this contact sheet. Return JSON only, keyed by every image ID. Each value must contain "
        "contains_person (boolean), subject_type (model_person, product_flatlay, product_detail, brand_logo, scene_background, unknown), view (front, three_quarter, side, back, detail, unknown), "
        "framing (full_body, half_body, upper_body, closeup, unknown), usable_for_identity (boolean), identity_quality (high, medium, low, unknown), "
        "gender_presentation (woman, man, ambiguous, unknown), detail_types (array chosen from fabric, neckline, cuff, zipper, print_graphic, stitching, hem, pocket, hardware, closure, general_detail), and concise English notes. "
        "Judge only visible pixels. Filenames and folder names are intentionally unavailable and must never be used as evidence. "
        "Product-only images are never identity references. A back-view person is not usable as the sole identity anchor."
    )
    payload = {"model": args.model, "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": data_url(sheet_path)}}]}], "max_tokens": max(2500, len(images) * 320)}
    update_status(root, product.name, "running", model=args.model, candidate_count=len(images), contact_sheet=str(sheet_path))
    try:
        response = requests.post(ENDPOINT, headers={"Authorization": f"Bearer {args.api_key}", "Content-Type": "application/json"}, json=payload, timeout=args.request_timeout)
        response.raise_for_status()
        body = response.json()
        atomic_json(work / "contact_sheet_analysis_raw.json", body)
        content = ((body.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
        if isinstance(content, list):
            content = "\n".join(str(x.get("text", "")) for x in content if isinstance(x, dict))
        tags = validate_tags(extract_json(str(content)), manifest, product, args.model)
        atomic_json(tags_path, tags)
        update_status(root, product.name, "completed", model=args.model, candidate_count=len(tags), tags_path=str(tags_path))
    except Exception as exc:
        update_status(root, product.name, "failed", model=args.model, error=str(exc))
        raise
    print(tags_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
