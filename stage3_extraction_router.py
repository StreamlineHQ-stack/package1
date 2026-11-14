"""
STAGE 3 — Automatic extraction router.
"""
from __future__ import annotations
from typing import Optional
from PIL import Image
from stage2_extraction_engines import run_extraction


def choose_engine(stage1_report: dict) -> dict:
    ocr = stage1_report.get("ocr", {})
    metrics = stage1_report.get("visual_metrics", {})
    words = int(ocr.get("word_count", 0))
    text_area = float(ocr.get("estimated_text_area_percent", 0.0))
    complexity = metrics.get("background_complexity_estimate", "unknown")

    if words == 0:
        return {"engine": "contrast_inpaint", "confidence": 0.30, "manual_review": True, "reason": "No OCR words detected; fallback to contrast."}
    if text_area > 18 or complexity == "high":
        return {"engine": "ocr_inpaint", "confidence": 0.45, "manual_review": True, "reason": "High complexity / large text footprint."}
    return {"engine": "ocr_inpaint", "confidence": 0.72, "manual_review": False, "reason": "Standard targeted OCR masking."}


def process_with_router(image: Image.Image, stage1_report: dict,
                        vision_dna: Optional[dict] = None) -> tuple[Image.Image, Image.Image, dict]:
    decision = choose_engine(stage1_report)
    cleaned, mask, extraction_report = run_extraction(
        image, engine=decision["engine"], vision_dna=vision_dna
    )
    combined = {
        "stage": 3,
        "decision": decision,
        "extraction": extraction_report,
        "status": "completed_needs_review" if decision["manual_review"] else "completed_review_recommended"
    }
    return cleaned, mask, combined