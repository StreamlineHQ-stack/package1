# module_1_background_extractor.py • 4-Engine Multi-Studio Background Extractor
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image

def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)

def run_engine_a_scenic(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine A: Pristine local-contrast inpainting for scenic backgrounds & light skies"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)[:roi_bottom]
    k = max(21, int(min(h, w) * .16))
    if k % 2 == 0: k += 1
    local_bg = cv2.GaussianBlur(gray, (k, k), 0)
    darkness = cv2.subtract(local_bg, gray)
    
    mask = np.zeros((h, w), np.uint8)
    raw = np.where(darkness >= 10, 255, 0).astype(np.uint8)
    mask[:roi_bottom] = cv2.medianBlur(raw, 3)
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def run_engine_b_poster(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine B: LAB-channel variance inpainting for solid/gradient studio posters (SARINA)"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    lab = cv2.cvtColor(bgr[:roi_bottom], cv2.COLOR_BGR2LAB)
    l_chan, _, _ = cv2.split(lab)
    
    blur = cv2.GaussianBlur(l_chan, (51, 51), 0)
    diff = cv2.absdiff(l_chan, blur)
    _, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
    
    mask = np.zeros((h, w), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask[:roi_bottom] = cv2.dilate(thresh, kernel, iterations=1)
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_NS)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def run_engine_d_textured_and_glowing(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine D: Dual-Space Color Clustering & Morphological Isolation for Watercolor & Glowing Text"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    roi = bgr[:roi_bottom]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Isolate low-saturation or extreme brightness text (catches glowing white stars text and brown watercolor text)
    lower_val = np.array([0, 0, 180])
    upper_val = np.array([180, 80, 255])
    mask_bright = cv2.inRange(hsv, lower_val, upper_val)
    
    # Also catch dark brownish/golden tones typical of watercolor typography
    lower_brown = np.array([10, 30, 50])
    upper_brown = np.array([35, 255, 200])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    
    combined_roi = cv2.bitwise_or(mask_bright, mask_brown)
    
    # Clean up specks using morphological opening and closing
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned_mask = cv2.morphologyEx(combined_roi, cv2.MORPH_OPEN, kernel)
    closed_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 3)))
    
    mask = np.zeros((h, w), np.uint8)
    mask[:roi_bottom] = cv2.dilate(closed_mask, kernel, iterations=1)
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def _png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()