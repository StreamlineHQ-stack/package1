"""
STAGE 1 — Image intelligence (analysis only; never edits pixels).
"""
from __future__ import annotations
from typing import Any, Dict, Optional
import numpy as np
from PIL import Image

try:
    import cv2
except Exception:
    cv2 = None


def _palette(arr: np.ndarray, count: int = 6) -> list:
    im = Image.fromarray(arr).resize((min(160, arr.shape[1]), min(160, arr.shape[0])))
    q = im.quantize(colors=count, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette() or []
    result = []
    for idx, n in q.getcolors() or []:
        p = idx * 3
        if p + 2 < len(pal):
            rgb = pal[p:p+3]
            result.append({"hex": "#{:02X}{:02X}{:02X}".format(*rgb),
                           "rgb": rgb, "approx_share": round(n/(im.width*im.height), 3)})
    return sorted(result, key=lambda x: x["approx_share"], reverse=True)[:count]


def _ocr(arr: np.ndarray) -> dict:
    try:
        import pytesseract
        from pytesseract import Output
        data = pytesseract.image_to_data(Image.fromarray(arr),
                                         output_type=Output.DICT, config="--psm 11")
        words = []
        for i, value in enumerate(data.get("text", [])):
            value = (value or "").strip()
            try:
                conf = float(data["conf"][i])
            except (ValueError, TypeError, KeyError):
                conf = -1
            if not value or conf < 25:
                continue
            x, y = int(data["left"][i]), int(data["top"][i])
            w, h = int(data["width"][i]), int(data["height"][i])
            if w > 0 and h > 0:
                words.append({"text": value, "confidence": round(conf, 1),
                              "bbox": [x, y, x+w, y+h]})

        words.sort(key=lambda z: (z["bbox"][1], z["bbox"][0]))
        blocks = []
        for word in words:
            x1, y1, x2, y2 = word["bbox"]
            target = None
            for block in blocks:
                bx1, by1, bx2, by2 = block["bbox"]
                overlap = max(0, min(y2, by2) - max(y1, by1))
                if overlap >= 0.25 * min(y2-y1, by2-by1):
                    target = block
                    break
            if target is None:
                blocks.append({"bbox": [x1, y1, x2, y2], "words": [word["text"]]})
            else:
                target["bbox"] = [min(target["bbox"][0], x1), min(target["bbox"][1], y1),
                                  max(target["bbox"][2], x2), max(target["bbox"][3], y2)]
                target["words"].append(word["text"])
        for i, block in enumerate(blocks, 1):
            block["id"] = i
            block["text_preview"] = " ".join(block.pop("words"))[:120]
        return {"available": True, "status": "ok", "words": words, "text_regions": blocks}
    except Exception as exc:
        return {"available": False, "status": "ocr_unavailable_or_failed",
                "error": str(exc)[:250], "words": [], "text_regions": []}


def _metrics(arr: np.ndarray) -> dict:
    h, w = arr.shape[:2]
    gray = (cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY) if cv2 is not None
            else np.mean(arr, axis=2).astype("uint8"))
    grid = []
    for r in range(4):
        row = []
        for c in range(4):
            crop = gray[r*h//4:(r+1)*h//4, c*w//4:(c+1)*w//4]
            row.append(round(float(np.std(crop)), 2))
        grid.append(row)
    if cv2 is not None:
        edges = cv2.Canny(gray, 80, 160)
        density = float(np.count_nonzero(edges))/(h*w)
        complexity = "low" if density < .035 else "medium" if density < .09 else "high"
    else:
        density, complexity = None, "unknown_without_opencv"
    return {"edge_density": round(density, 5) if density is not None else None,
            "background_complexity_estimate": complexity,
            "local_complexity_grid_4x4": grid,
            "gray_std": round(float(np.std(gray)), 2)}


def analyze_image_structure(image: Image.Image,
                            vision_dna: Optional[dict] = None) -> Dict[str, Any]:
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL Image")
    arr = np.asarray(image.convert("RGB"))
    h, w = arr.shape[:2]
    ocr = _ocr(arr)
    metrics = _metrics(arr)
    enriched = []
    for region in ocr["text_regions"]:
        x1, y1, x2, y2 = region["bbox"]
        gx = min(3, max(0, int(((x1+x2)/2)/w*4)))
        gy = min(3, max(0, int(((y1+y2)/2)/h*4)))
        local = metrics["local_complexity_grid_4x4"][gy][gx]
        item = dict(region)
        item["local_texture_std"] = local
        item["repair_risk"] = "high" if local >= 45 else "medium" if local >= 22 else "lower"
        enriched.append(item)
    area = sum((r["bbox"][2]-r["bbox"][0])*(r["bbox"][3]-r["bbox"][1])
               for r in enriched)
    ratio = w/h if h else 0
    fmt = "square" if .94 <= ratio <= 1.06 else "landscape" if ratio > 1.06 else "portrait"
    dna = vision_dna if isinstance(vision_dna, dict) else {}
    return {
        "stage": 1, "analysis_only": True,
        "source": {"width": w, "height": h, "aspect_ratio": round(ratio, 4),
                   "format_guess": fmt, "mode": image.mode},
        "palette_estimate": _palette(arr),
        "ocr": {"available": ocr["available"], "status": ocr["status"],
                "error": ocr.get("error"), "word_count": len(ocr["words"]),
                "text_region_count": len(enriched),
                "estimated_text_area_percent": round(area*100/(w*h), 3),
                "text_regions": enriched},
        "visual_metrics": metrics,
        "vision_dna": {
            "provided": bool(dna),
            "design_style": dna.get("design_style"),
            "design_intent": dna.get("design_intent"),
            "motifs_and_objects": dna.get("motifs_and_objects", []),
            "composition": dna.get("composition", {}),
            "palette": dna.get("palette", []),
            "hierarchy": dna.get("hierarchy", []),
            "confidence_and_limits": dna.get("confidence_and_limits")
        }
    }