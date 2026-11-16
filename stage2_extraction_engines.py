# stage2_extraction_engines.py • Effective Header Removal Engine
from __future__ import annotations
import os
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Actively removes header text in the upper region while protecting 
    all focal objects and background photography in the lower half.
    """
    img_rgb = image.convert("RGB")
    np_img = np.array(img_rgb)
    h, w, _ = np_img.shape
    
    report = {
        "engine_used": engine,
        "mode": mode,
        "resolution": f"{w}x{h}",
        "status": "success"
    }

    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    mask_arr = np.zeros((h, w), dtype=np.uint8)
    
    # 1. Target the upper 45% where major swipe-file headers and titles live
    header_limit = int(h * 0.45)
    roi = gray[0:header_limit, 0:w]
    
    # 2. Combine binary and adaptive thresholding to guarantee text isolation
    _, thresh_bin = cv2.threshold(roi, 190, 255, cv2.THRESH_BINARY_INV)
    thresh_adp = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8)
    combined_roi = cv2.bitwise_or(thresh_bin, thresh_adp)
    
    # 3. Morphological closing to bridge individual letters into solid text blocks
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 3))
    closed_roi = cv2.morphologyEx(combined_roi, cv2.MORPH_CLOSE, kernel_close)
    
    # Assign to global mask array
    mask_arr[0:header_limit, 0:w] = closed_roi
    
    # 4. Strict Protection Shield: Ensure nothing in the lower half (below 50% height) is ever touched
    mask_arr[int(h * 0.50):h, :] = 0

    mask = Image.fromarray(mask_arr)

    # 5. Clean localized inpainting
    try:
        inpainted_np = cv2.inpaint(np_img, mask_arr, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "effective_header_inpaint"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback: {str(e)}"

    return cleaned_img, mask, report