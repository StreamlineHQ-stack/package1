# stage2_extraction_engines.py • Smart Header Zone & Background Preservation Engine
from __future__ import annotations
import os
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Targets the primary header zone where swipe file titles live (top 38% of slide)
    while strictly protecting lower-deck products, subjects, and background scenery.
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
    
    # Create mask for text removal
    mask_arr = np.zeros((h, w), dtype=np.uint8)
    
    # 1. HEADER ZONE TARGETING: Focus aggressive text extraction on the top 38% where titles live (SARINA, NEW DROP, SPRING SALE, etc.)
    header_roi_height = int(h * 0.38)
    header_roi = gray[0:header_roi_height, 0:w]
    
    # Adaptive thresholding specifically inside the header zone to pull out bold and stylized text
    header_thresh = cv2.adaptiveThreshold(header_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 6)
    
    # Dilate header text to make sure solid headers are completely covered
    kernel = np.ones((5, 5), np.uint8)
    header_mask_dilated = cv2.dilate(header_thresh, kernel, iterations=2)
    
    # Place header mask back into full canvas mask array
    mask_arr[0:header_roi_height, 0:w] = header_mask_dilated

    # 2. GENERAL BODY TEXT TARGETING: Lower threshold pass for subtitles or body copy across the rest of the slide
    _, body_thresh = cv2.threshold(gray, 215, 255, cv2.THRESH_BINARY_INV)
    body_contours, _ = cv2.findContours(body_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in body_contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if y > header_roi_height and 10 < area < (w * h * 0.05) and ch < (h * 0.1):
            cv2.drawContours(mask_arr, [cnt], -1, 255, thickness=cv2.FILLED)

    mask = Image.fromarray(mask_arr)

    # 3. Seamless inpainting strictly on the targeted mask areas
    try:
        inpainted_np = cv2.inpaint(np_img, mask_arr, inpaintRadius=7, flags=cv2.INPAINT_NS)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "smart_header_zone_ns_inpaint"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback_passthrough: {str(e)}"

    return cleaned_img, mask, report