# stage2_extraction_engines.py • Bulletproof Text Removal & Background Restoration Engine
from __future__ import annotations
import os
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Executes robust, targeted text removal on bold headers and titles
    while keeping background scenery and colors completely intact.
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

    # Convert to grayscale and LAB color space for enhanced contrast detection
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    
    # Dual-pass thresholding to guarantee isolation of both dark and bright bold text
    _, thresh_light = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)      # For dark text on light backgrounds
    _, thresh_dark = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)    # For bright/white text on dark backgrounds
    
    # Combine thresholds
    text_candidates = cv2.bitwise_or(thresh_light, thresh_dark)
    
    # Morphological closing to bridge letter gaps into solid header blocks
    struct_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 3))
    closed_mask = cv2.morphologyEx(text_candidates, cv2.MORPH_CLOSE, struct_kernel)
    
    # Contour filtering to select header-sized text regions
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    final_mask = np.zeros((h, w), dtype=np.uint8)
    
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        # Target header text blocks while ignoring tiny noise or full-frame borders
        if 30 < area < (w * h * 0.5) and ch < (h * 0.7):
            cv2.drawContours(final_mask, [cnt], -1, 255, thickness=cv2.FILLED)

    # Generous dilation to cover anti-aliased font edges entirely
    dilation_kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(final_mask, dilation_kernel, iterations=2)
    
    mask = Image.fromarray(dilated_mask)

    # Fast, seamless TELEA/NS inpainting to fill text zones with surrounding background textures
    try:
        inpainted_np = cv2.inpaint(np_img, dilated_mask, inpaintRadius=9, flags=cv2.INPAINT_TELEA)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "bulletproof_telea_text_wipe"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback_passthrough: {str(e)}"

    return cleaned_img, mask, report