# stage2_extraction_engines.py • High-Performance Text Wipe & Background Preservation Engine
from __future__ import annotations
import os
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Executes aggressive yet safe text removal, targeting large display fonts 
    and headers without destroying background images or colors.
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

    # Convert to grayscale
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    
    # 1. Multi-scale thresholding to capture both dark/light bold text and thin subtitles
    _, thresh_dark = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    
    # Adaptive thresholding for subtle or textured headers
    thresh_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    
    # Combine thresholds to ensure large bold headers (like NEW DROP & SARINA) are fully captured
    combined_thresh = cv2.bitwise_or(thresh_dark, thresh_adaptive)
    
    # 2. Contour filtering to isolate text-like connected components and eliminate small background noise
    contours, _ = cv2.findContours(combined_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_mask = np.zeros((h, w), dtype=np.uint8)
    
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        # Filter out tiny specks or massive full-screen blocks, keeping text and headers
        if 15 < area < (w * h * 0.4) and ch < (h * 0.6):
            cv2.drawContours(text_mask, [cnt], -1, 255, thickness=cv2.FILLED)

    # 3. Dilate the mask generously so it fully covers thick stylized lettering without ghost edges
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(text_mask, kernel, iterations=2)
    
    mask = Image.fromarray(dilated_mask)

    # 4. Perform robust Navier-Stokes or Telea inpainting to seamlessly fill text areas with background scenery
    try:
        inpainted_np = cv2.inpaint(np_img, dilated_mask, inpaintRadius=7, flags=cv2.INPAINT_NS)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "robust_contour_ns_inpaint"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback_error: {str(e)}"

    return cleaned_img, mask, report