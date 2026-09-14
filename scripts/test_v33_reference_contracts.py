#!/usr/bin/env python3
"""Focused regression tests for v3.3 semantic reference contracts."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def load_module(filename: str, name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_module("build_module_reference_images.py", "v33_builder")
generator = load_module("generate_modules_toapi.py", "v33_generator")
tagger = load_module("tag_contact_sheet_with_toapi.py", "v33_tagger")


class V33ReferenceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.sku = self.root / "SKU-A"
        self.sku.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def image(self, relative: str) -> Path:
        path = self.sku / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"test")
        return path

    def set_tags(self, tags: dict[str, dict]) -> None:
        builder.MODEL_VIEW_TAG_PRODUCT_DIR = self.sku
        builder.MODEL_VIEW_TAGS = {key.casefold(): {"source": "visual-model", **value} for key, value in tags.items()}

    def test_hard_excluded_directories_never_become_candidates(self) -> None:
        allowed = self.image("素材/detail.jpg")
        self.image("弃用/detail.jpg")
        self.image("过程文件/front.jpg")
        self.image("生成结果/out.jpg")
        self.image("历史备份/back.jpg")
        self.assertEqual(tagger.candidates(self.sku), [allowed])
        self.assertEqual(builder.product_images(self.sku), [allowed])

    def test_exact_relative_tag_key_prevents_basename_fallback(self) -> None:
        one = self.image("素材/same.jpg")
        two = self.image("上身1/same.jpg")
        self.set_tags({"素材/same.jpg": {"subject_type": "product_detail", "contains_person": False}})
        self.assertTrue(builder.model_view_tag(one))
        self.assertEqual(builder.model_view_tag(two), {})
        with self.assertRaisesRegex(RuntimeError, "missing=.*上身1/same.jpg"):
            builder.validate_semantic_tag_coverage(self.sku)

    def test_dynamic_multi_angle_requires_front_and_back_but_side_is_optional(self) -> None:
        front = self.image("AIGC/a.jpg")
        back = self.image("AIGC/b.jpg")
        self.set_tags({
            "AIGC/a.jpg": {"subject_type": "model_person", "contains_person": True, "view": "front"},
            "AIGC/b.jpg": {"subject_type": "model_person", "contains_person": True, "view": "back"},
        })
        sources = {"model_front": [front], "model_back": [back], "model_side": []}
        refs, contract = builder.select_dynamic_contract_refs(self.sku, "model_multi_angle", sources, front, 6)
        self.assertEqual(refs, [front.resolve(), back.resolve()])
        self.assertEqual(contract["required_roles"], {"model_front": 1, "model_back": 1})

    def test_module_function_is_detected_from_semantics_not_section_number(self) -> None:
        role, _ = builder.detect_module_role("展示模特正侧背，多角度强调版型", 4)
        self.assertEqual(role, "model_multi_angle")
        role, _ = builder.detect_module_role("模特搭配产品平铺正背面", 2)
        self.assertEqual(role, "model_flatlay")

    def test_no_reference_contract_is_an_explicit_empty_list(self) -> None:
        refs, contract = builder.select_dynamic_contract_refs(self.sku, "no_reference", {}, None, 6)
        self.assertEqual(refs, [])
        self.assertEqual(contract["required_roles"], {})

    def test_model_flatlay_missing_product_back_fails_without_fallback(self) -> None:
        model = self.image("AIGC/model.jpg")
        flat_front = self.image("素材/front.jpg")
        self.set_tags({
            "AIGC/model.jpg": {"subject_type": "model_person", "contains_person": True, "view": "front"},
            "素材/front.jpg": {"subject_type": "product_flatlay", "contains_person": False, "view": "front"},
        })
        sources = {"model_front": [model], "model_side": [], "product_front": [flat_front], "product_back": [], "product_detail": []}
        with self.assertRaisesRegex(RuntimeError, "product_back"):
            builder.select_dynamic_contract_refs(self.sku, "model_flatlay", sources, model, 6)

    def test_detail_contract_prefers_semantically_verified_material_source(self) -> None:
        material = self.image("素材/detail.jpg")
        other = self.image("上身1/detail.jpg")
        self.set_tags({
            "素材/detail.jpg": {"subject_type": "product_detail", "contains_person": False, "view": "detail", "detail_types": ["fabric"]},
            "上身1/detail.jpg": {"subject_type": "product_detail", "contains_person": False, "view": "detail", "detail_types": ["fabric"]},
        })
        sources = {"fabric_closeup": [other, material], "construction_detail": [], "graphic_detail": [], "product_detail": []}
        refs, _ = builder.select_dynamic_contract_refs(self.sku, "fabric_detail", sources, None, 1)
        self.assertEqual(refs, [material.resolve()])

    def test_external_and_excluded_references_are_rejected_at_upload_boundary(self) -> None:
        outside = self.root / "old-sku.jpg"
        outside.write_bytes(b"test")
        excluded = self.image("弃用/old.jpg")
        with self.assertRaisesRegex(RuntimeError, "outside current SKU"):
            generator.validate_current_sku_reference(self.sku, outside)
        with self.assertRaisesRegex(RuntimeError, "hard-excluded"):
            generator.validate_current_sku_reference(self.sku, excluded)

    def test_reference_map_rejects_stale_external_paths(self) -> None:
        work = self.sku / "_aplus_creative_work"
        work.mkdir()
        outside = self.root / "old.jpg"
        outside.write_bytes(b"test")
        (work / "module_reference_images.json").write_text(
            json.dumps({"section-01.txt": [str(outside)]}), encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "outside current SKU"):
            generator.load_module_reference_map(self.sku)


if __name__ == "__main__":
    unittest.main()
