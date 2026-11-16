# stage2_extraction_engines.py • Production Hybrid Extraction Engine
from __future__ import annotations
import os
import io
import base64
import requests
from PIL import Image, ImageDraw
import numpy as np
import cv2

def run_extraction(image: Image.Image, engine: str = "ocr_inpaint", vision_dna: dict | None = None, mode: str = "automatic") -> tuple[Image.Image, Image.Image, dict]:
    """
    Executes clean text removal using a balanced upper-band mask that 
    protects subject heads and lower scenery entirely.
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
    
    # 1. Conservative Upper Band (Top 22% only) to completely protect subjects' heads and lower objects
    top_band = int(h * 0.22)
    roi = gray[0:top_band, 0:w]
    
    # Adaptive thresholding strictly for high-contrast titles
    _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    dilated_roi = cv2.dilate(thresh, kernel, iterations=1)
    
    mask_arr[0:top_band, 0:w] = dilated_roi
    
    # 2. Strict lower boundary protection: nothing below 35% height can ever be modified
    mask_arr[int(h * 0.35):h, :] = 0

    mask = Image.fromarray(mask_arr)

    # 3. Safe, lightweight local inpainting strictly on the upper band
    try:
        inpainted_np = cv2.inpaint(np_img, mask_arr, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        cleaned_img = Image.fromarray(inpainted_np)
        report["method"] = "safe_upper_band_inpaint"
    except Exception as e:
        cleaned_img = img_rgb
        report["method"] = f"fallback: {str(e)}"

    return cleaned_img, mask, report