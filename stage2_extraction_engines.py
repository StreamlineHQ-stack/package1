# stage2_extraction_engines.py • Shielded Precision Extraction Engine
from __future__ import annotations
import os
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Removes text headers while maintaining an explicit exclusion shield 
    over central/lower focal objects (like flowers, roses, and products).
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
    
    # 1. Target ONLY the upper text region (top 28% of the canvas)
    title_limit = int(h * 0.28)
    roi = gray[0:title_limit, 0:w]
    
    roi_thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 4)
    contours, _ = cv2.findContours(roi_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if (3 < ch < int(title_limit * 0.9)) and (5 < area < int(w * h * 0.08)):
            cv2.drawContours(mask_arr[0:title_limit, 0:w], [cnt], -1, 255, thickness=cv2.FILLED)

    # 2. OBJECT EXCLUSION SHIELD: Explicitly punch a black hole in the mask 
    # over the exact lower-center area where the rose, mirror, and vase sit (preventing any blur)
    shield_x1, shield_x2 = int(w * 0.35), int(w * 0.85)
    shield_y1, shield_y2 = int(h * 0.40), h
    mask_arr[shield_y1:shield_y2, shield_x1:shield_x2] = 0

    mask = Image.fromarray(mask_arr)

    # 3. Clean localized inpainting
    try:
        inpainted_np = cv2.inpaint(np_img, mask_arr, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "shielded_upper_inpaint"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback: {str(e)}"

    return cleaned_img, mask, report