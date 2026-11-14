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

def run_engine_d_nebula(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine D: Nebula Luminance Inpainter for glowing white text over starry/nebula space gradients"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    roi = bgr[:roi_bottom]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Isolate high-brightness glowing pixels (white typography bloom)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Dilate slightly to capture the soft glow halo around the font
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    
    mask = np.zeros((h, w), np.uint8)
    mask[:roi_bottom] = dilated
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")