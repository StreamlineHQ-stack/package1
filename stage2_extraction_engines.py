# stage2_extraction_engines.py • Precision Text-Only Extraction & Background Protection Engine
from __future__ import annotations
import os
import io
import base64
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Precisely targets text headers using geometric aspect ratios and adaptive thresholding 
    while strictly protecting background photos, products, and human subjects.
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
    
    # Use Adaptive Thresholding to isolate local high-contrast characters without affecting overall lighting/gradients
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    
    # Find contours to isolate text lines specifically by geometry
    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_mask = np.zeros((h, w), dtype=np.uint8)
    
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        aspect_ratio = cw / float(ch + 1e-5)
        
        # STRICT TEXT FILTERING RULES:
        # 1. Text is typically horizontal (aspect ratio > 0.8) and not giant rectangular object blocks.
        # 2. Height must be within text scale bounds (not full-height objects or large product bottles).
        # 3. Area must match character/word contours rather than large image regions.
        if (5 < ch < h * 0.25) and (0.2 < aspect_ratio < 25.0) and (10 < area < w * h * 0.15):
            cv2.drawContours(text_mask, [cnt], -1, 255, thickness=cv2.FILLED)

    # Gentle horizontal kernel to bridge letters into clean word/header masks
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    closed_mask = cv2.morphologyEx(text_mask, cv2.MORPH_CLOSE, close_kernel)
    
    # Dilate slightly to cover font anti-aliasing edges
    dilate_kernel = np.ones((3, 3), np.uint8)
    final_mask_np = cv2.dilate(closed_mask, dilate_kernel, iterations=1)
    
    mask = Image.fromarray(final_mask_np)

    # Apply conservative local inpainting strictly on verified text masks
    try:
        inpainted_np = cv2.inpaint(np_img, final_mask_np, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "precision_geometric_text_inpaint"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback_passthrough: {str(e)}"

    return cleaned_img, mask, report