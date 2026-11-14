"""
STAGE 4 — Batch benchmark harness.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import time
from PIL import Image
import numpy as np
from stage1_image_intelligence import analyze_image_structure
from stage2_extraction_engines import run_extraction

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}
ENGINES = ["ocr_inpaint", "contrast_inpaint", "texture_cluster", "nebula_luminance", "legacy"]


def benchmark_one(path: Path, output_dir: Path) -> list[dict]:
    image = Image.open(path).convert("RGB")
    analysis = analyze_image_structure(image)
    rows = []
    for engine in ENGINES:
        started = time.perf_counter()
        try:
            clean, mask, report = run_extraction(image, engine=engine)
            elapsed = round(time.perf_counter()-started, 3)
            stem = f"{path.stem}_{engine}"
            clean.save(output_dir / f"{stem}_clean.png")
            mask.save(output_dir / f"{stem}_mask.png")
            rows.append({
                "filename": path.name, "engine": engine, "status": "ok",
                "seconds": elapsed,
                "ocr_words_stage1": analysis["ocr"]["word_count"],
                "stage1_text_area_percent": analysis["ocr"]["estimated_text_area_percent"],
                "complexity": analysis["visual_metrics"]["background_complexity_estimate"],
                "masked_pixel_percent": report["masked_pixel_percent"],
                "mask_nonempty": report["mask_nonempty"],
                "error": ""
            })
        except Exception as exc:
            rows.append({
                "filename": path.name, "engine": engine, "status": "failed",
                "seconds": round(time.perf_counter()-started, 3),
                "ocr_words_stage1": analysis["ocr"]["word_count"],
                "stage1_text_area_percent": analysis["ocr"]["estimated_text_area_percent"],
                "complexity": analysis["visual_metrics"]["background_complexity_estimate"],
                "masked_pixel_percent": "", "mask_nonempty": "",
                "error": str(exc)[:500]
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", default="benchmark_results")
    args = parser.parse_args()
    source = Path(args.input_dir)
    target = Path(args.output_dir)
    target.mkdir(parents=True, exist_ok=True)
    images = sorted(p for p in source.iterdir() if p.suffix.lower() in SUPPORTED)
    
    all_rows = []
    for path in images:
        print(f"Benchmarking: {path.name}")
        all_rows.extend(benchmark_one(path, target))

    csv_path = target / "benchmark_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Done. Results saved to {target.resolve()}")


if __name__ == "__main__":
    main()