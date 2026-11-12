# module_1_background_extractor.py
"""Module 1: Intelligent Text Eraser / clean background extractor.

Required: streamlit, pillow, numpy, opencv-python
Optional: pytesseract + the Tesseract OCR executable.

OCR locates likely text; a local-contrast mask supplements it. OpenCV
inpainting reconstructs masked pixels. Always inspect the mask and output:
large text, text over detailed objects, and complex textures may need manual work.
"""
from __future__ import annotations
import io
import base64
from typing import Tuple
import cv2
import numpy as np
from PIL import Image


def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)


def _ocr_mask(bgr: np.ndarray, roi_bottom: int) -> np.ndarray:
    h, w = bgr.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    try:
        import pytesseract
        from pytesseract import Output
        roi = bgr[:roi_bottom]
        scale = max(2.0, min(4.0, 1000.0 / max(roi.shape[:2])))
        enlarged = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        data = pytesseract.image_to_data(
            cv2.cvtColor(enlarged, cv2.COLOR_BGR2RGB),
            output_type=Output.DICT, config="--psm 11"
        )
        for i, word in enumerate(data.get("text", [])):
            if not (word or "").strip():
                continue
            try:
                confidence = float(data["conf"][i])
            except (ValueError, TypeError, KeyError):
                confidence = -1
            if confidence < 25:
                continue
            x, y = int(data["left"][i] / scale), int(data["top"][i] / scale)
            ww, hh = int(data["width"][i] / scale), int(data["height"][i] / scale)
            px, py = max(2, int(ww * .045)), max(2, int(hh * .12))
            x1, y1 = max(0, x-px), max(0, y-py)
            x2, y2 = min(w, x+ww+px), min(roi_bottom, y+hh+py)
            if x2 > x1 and y2 > y1:
                mask[y1:y2, x1:x2] = 255
    except Exception:
        # OCR is optional. The contrast detector below remains available.
        pass
    return mask


def _contrast_mask(bgr: np.ndarray, roi_bottom: int, threshold: int) -> np.ndarray:
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)[:roi_bottom]
    k = max(21, int(min(h, w) * .16))
    if k % 2 == 0:
        k += 1
    local_bg = cv2.GaussianBlur(gray, (k, k), 0)
    darkness = cv2.subtract(local_bg, gray)
    raw = np.where(darkness >= threshold, 255, 0).astype(np.uint8)
    raw = cv2.medianBlur(raw, 3)
    raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE,
                           cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    full = np.zeros((h, w), np.uint8)
    full[:roi_bottom] = raw
    return full


def build_text_mask(image: Image.Image, text_region_percent: int = 40,
                    use_ocr: bool = True, darkness_threshold: int = 10,
                    mask_expansion: int = 4) -> np.ndarray:
    """Build a combined mask within the selected upper image region."""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * text_region_percent / 100)))
    mask = np.zeros((h, w), np.uint8)
    if use_ocr:
        mask = cv2.bitwise_or(mask, _ocr_mask(bgr, roi_bottom))
    mask = cv2.bitwise_or(mask, _contrast_mask(bgr, roi_bottom, darkness_threshold))
    if mask_expansion > 0 and np.any(mask):
        size = mask_expansion * 2 + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
        mask = cv2.dilate(mask, kernel, iterations=1)
    return mask


def erase_text(image: Image.Image, text_region_percent: int = 40,
               inpaint_radius: float = 5.0, method: str = "telea",
               use_ocr: bool = True, darkness_threshold: int = 10,
               mask_expansion: int = 4) -> Tuple[Image.Image, Image.Image]:
    """Return (cleaned RGB image, grayscale mask preview as RGB image)."""
    source = _to_bgr(image)
    mask = build_text_mask(image, text_region_percent, use_ocr,
                           darkness_threshold, mask_expansion)
    flag = cv2.INPAINT_TELEA if method.lower() == "telea" else cv2.INPAINT_NS
    cleaned = cv2.inpaint(source, mask, float(inpaint_radius), flag)
    return (Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)),
            Image.fromarray(mask).convert("RGB"))


def _png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()


def render_module_1_ui(slide_count, api_key=None):
    """Streamlit UI; preserves the Creator Suite hand-off/session-state keys."""
    import streamlit as st
    st.markdown("#### 🌄 Module 1: Intelligent Text Eraser")
    st.info("Remove existing text and reconstruct the background for reuse in the Carousel Engine.")
    uploaded = st.file_uploader("Upload inspiration slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    if uploaded is None:
        return
    original = Image.open(uploaded).convert("RGB")
    st.image(original, caption="Original slide", width=320)
    with st.expander("Detection settings", expanded=True):
        region = st.slider("Search within top portion (%)", 15, 70, 40, key="m1_text_region")
        use_ocr = st.checkbox("Use OCR text detection (recommended)", True, key="m1_use_ocr")
        threshold = st.slider("Dark-text sensitivity", 8, 60, 10, key="m1_darkness_threshold")
        expansion = st.slider("Mask edge expansion", 0, 8, 4, key="m1_mask_expansion")
        radius = st.slider("Inpainting radius", 2.0, 12.0, 5.0, .5, key="m1_inpaint_radius")
        method = st.selectbox("Reconstruction method", ["telea", "ns"],
                              format_func=lambda x: "Telea (recommended)" if x == "telea" else "Navier-Stokes",
                              key="m1_inpaint_method")
    if st.button("✨ Detect & Remove Text", type="primary", key="btn_run_m1"):
        with st.spinner("Detecting text and reconstructing background..."):
            cleaned, mask = erase_text(original, region, radius, method, use_ocr, threshold, expansion)
            clean_bytes, mask_bytes = _png_bytes(cleaned), _png_bytes(mask)
            st.session_state["m1_clean_background_bytes"] = clean_bytes
            st.session_state["m1_text_mask_bytes"] = mask_bytes
            st.session_state["extracted_asset_bytes"] = clean_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Clean Scenic Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": clean_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(clean_bytes).decode("ascii"),
                "visual_approved": True,
            }
    if "m1_clean_background_bytes" in st.session_state:
        st.divider()
        st.markdown("### Clean background preview")
        st.image(st.session_state["m1_clean_background_bytes"], width=350)
        with st.expander("Inspect detected mask"):
            st.caption("White pixels are areas the engine attempted to reconstruct. If scenery is white, adjust the region or sensitivity.")
            st.image(st.session_state["m1_text_mask_bytes"], width=350)
        st.download_button("📥 Download clean background (.png)",
                           st.session_state["m1_clean_background_bytes"],
                           "clean_scenic_background.png", "image/png", key="dl_m1_erased")
        # Existing content editor and renderer hand-off retained.
        st.markdown("#### 📝 Slide Content Editor")
        slides_data = st.session_state.get("sia_slide_contents", [])
        if not slides_data:
            slides_data = [{"headline": f"Slide {i+1} Headline",
                            "body": f"Actionable execution strategy for slide {i+1}.",
                            "category": f"STEP {i+1}"} for i in range(slide_count)]
            st.session_state["sia_slide_contents"] = slides_data
        for idx, slide in enumerate(slides_data):
            with st.expander(f"Slide {idx+1} Content", expanded=(idx == 0)):
                slide["headline"] = st.text_input(f"Headline {idx+1}", value=slide.get("headline", ""), key=f"m1_head_{idx}")
                slide["body"] = st.text_area(f"Body {idx+1}", value=slide.get("body", ""), key=f"m1_body_{idx}")
                slide["category"] = st.text_input(f"Category {idx+1}", value=slide.get("category", ""), key=f"m1_cat_{idx}")
        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count,
                                content_only_mode=False, standalone_mode=False)
