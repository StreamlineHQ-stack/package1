"""
STAGE 2 — Independent extraction engines (Legacy, OCR Inpaint, Contrast Inpaint, and Texture/Nebula/Banner modes).
"""
from __future__ import annotations
from typing import Optional
import numpy as np
from PIL import Image
import cv2


def _ocr_mask(image: Image.Image, expansion: int = 5) -> tuple[np.ndarray, int]:
    import pytesseract
    from pytesseract import Output
    arr = np.asarray(image.convert("RGB"))
    data = pytesseract.image_to_data(Image.fromarray(arr),
                                     output_type=Output.DICT, config="--psm 11")
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    count = 0
    for i, txt in enumerate(data.get("text", [])):
        if not (txt or "").strip():
            continue
        try:
            conf = float(data["conf"][i])
        except (ValueError, TypeError, KeyError):
            conf = -1
        if conf < 25:
            continue
        x, y = int(data["left"][i]), int(data["top"][i])
        w, h = int(data["width"][i]), int(data["height"][i])
        px, py = max(2, expansion), max(2, expansion)
        x1, y1 = max(0, x-px), max(0, y-py)
        x2, y2 = min(mask.shape[1], x+w+px), min(mask.shape[0], y+h+py)
        if x2 > x1 and y2 > y1:
            mask[y1:y2, x1:x2] = 255
            count += 1
    if expansion > 0 and np.any(mask):
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*expansion+1, 2*expansion+1))
        mask = cv2.dilate(mask, k, iterations=1)
    return mask, count


def _contrast_mask(image: Image.Image, threshold: int = 18, max_region_percent: float = 45.0) -> tuple[np.ndarray, int]:
    arr = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    k = max(21, int(min(h, w)*.12))
    if k % 2 == 0: k += 1
    local = cv2.GaussianBlur(gray, (k, k), 0)
    dark = cv2.subtract(local, gray)
    raw = np.where(dark >= threshold, 255, 0).astype(np.uint8)
    raw = cv2.morphologyEx(raw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    coverage = 100.0 * np.count_nonzero(raw) / (h * w)
    if coverage > max_region_percent:
        return np.zeros_like(raw), 0
    return raw, int(np.count_nonzero(raw))


def _inpaint(image: Image.Image, mask: np.ndarray, radius: float = 5.0, method: str = "telea") -> Image.Image:
    if not np.any(mask):
        return image.convert("RGB").copy()
    src = cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)
    flag = cv2.INPAINT_TELEA if method.lower() == "telea" else cv2.INPAINT_NS
    result = cv2.inpaint(src, mask, float(radius), flag)
    return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))


def run_extraction(image: Image.Image, engine: str = "ocr_inpaint",
                   vision_dna: Optional[dict] = None,
                   expansion: int = 5, radius: float = 5.0,
                   method: str = "telea") -> tuple[Image.Image, Image.Image, dict]:
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL Image")
    engine = engine.lower().strip()
    
    if engine == "legacy":
        try:
            from module_1_background_extractor import erase_text
            cleaned, mask_img = erase_text(image, text_region_percent=100,
                                           inpaint_radius=radius, method=method,
                                           use_ocr=True, darkness_threshold=18,
                                           mask_expansion=expansion)
            mask = np.asarray(mask_img.convert("L"))
            count = int(np.count_nonzero(mask))
        except Exception as exc:
            raise RuntimeError(f"Legacy engine unavailable or failed: {exc}") from exc
            
    elif engine == "ocr_inpaint":
        mask, count = _ocr_mask(image, expansion=expansion)
        cleaned = _inpaint(image, mask, radius, method)
        
    elif engine == "contrast_inpaint":
        mask, count = _contrast_mask(image)
        cleaned = _inpaint(image, mask, radius, method)
        
    elif engine == "texture_cluster":
        # Dual-space HSV color clustering for watercolor / textured typography
        arr = np.asarray(image.convert("RGB"))
        h, w = arr.shape[:2]
        hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)
        mask_bright = cv2.inRange(hsv, np.array([0, 0, 190]), np.array([180, 70, 255]))
        mask_brown = cv2.inRange(hsv, np.array([10, 30, 50]), np.array([35, 255, 200]))
        mask = cv2.bitwise_or(mask_bright, mask_brown)
        count = int(np.count_nonzero(mask))
        cleaned = _inpaint(image, mask, radius, method)
        
    elif engine == "nebula_luminance":
        # High brightness bloom isolation for starry space nebula slides
        arr = np.asarray(image.convert("RGB"))
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=2)
        count = int(np.count_nonzero(mask))
        cleaned = _inpaint(image, mask, radius, method)
        
    else:
        raise ValueError(f"Unknown engine: {engine}")

    total = mask.size
    report = {
        "engine": engine,
        "detected_components_or_pixels": count,
        "masked_pixel_percent": round(100.0 * np.count_nonzero(mask) / total, 3),
        "mask_nonempty": bool(np.any(mask))
    }
    return cleaned, Image.fromarray(mask).convert("RGB"), report