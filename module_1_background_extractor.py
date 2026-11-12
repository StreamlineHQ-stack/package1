# module_1_background_extractor.py • Full-Canvas Multi-Tier Text Eraser
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image

def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)

def run_full_canvas_engine(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine C/D: Full-Height Multi-Tier Text Eraser (Catches top headers + middle paragraphs)"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    mask = np.zeros((h, w), np.uint8)
    
    # 1. Contrast/Darkness detection across the full selected region
    gray = cv2.cvtColor(bgr[:roi_bottom], cv2.COLOR_BGR2GRAY)
    k = max(21, int(min(h, w) * .12))
    if k % 2 == 0: k += 1
    local_bg = cv2.GaussianBlur(gray, (k, k), 0)
    darkness = cv2.subtract(local_bg, gray)
    
    raw = np.where(darkness >= 8, 255, 0).astype(np.uint8)
    mask[:roi_bottom] = cv2.medianBlur(raw, 3)

    # 2. Optional OCR bounding-box integration to catch styled text
    try:
        import pytesseract
        from pytesseract import Output
        roi = bgr[:roi_bottom]
        scale = 2.0
        enlarged = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        data = pytesseract.image_to_data(
            cv2.cvtColor(enlarged, cv2.COLOR_BGR2RGB),
            output_type=Output.DICT, config="--psm 11"
        )
        for i, word in enumerate(data.get("text", [])):
            if not (word or "").strip():
                continue
            try:
                conf = float(data["conf"][i])
            except (ValueError, TypeError, KeyError):
                conf = -1
            if conf < 10:
                continue
            x = int(data["left"][i] / scale)
            y = int(data["top"][i] / scale)
            ww = int(data["width"][i] / scale)
            hh = int(data["height"][i] / scale)
            x1, y1 = max(0, x - 4), max(0, y - 4)
            x2, y2 = min(w, x + ww + 4), min(roi_bottom, y + hh + 4)
            mask[y1:y2, x1:x2] = 255
    except Exception:
        pass

    # Dilate mask slightly for smooth inpainting
    if np.any(mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask = cv2.dilate(mask, kernel, iterations=1)

    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def _png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()

def render_module_1_ui(slide_count, api_key=None):
    st.markdown("#### 🧠 Module 1: Intelligent Multi-Engine Background & Text Studio")
    st.info("Select your processing engine based on the inspiration slide layout.")
    
    uploaded = st.file_uploader("Upload inspiration slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    if uploaded is None:
        return
        
    original = Image.open(uploaded).convert("RGB")
    st.image(original, caption="Original inspiration slide", width=320)
    
    with st.expander("⚙️ Process Selector & Engine Settings", expanded=True):
        engine_choice = st.selectbox(
            "Select Processing Engine:",
            [
                "Engine C/D: Full-Canvas Multi-Tier Eraser (Top Headers + Middle Paragraphs)",
                "Engine A: Simple Text Removal (Smooth Light Sky / Fog)",
                "Engine B: Advanced Text Removal (Rich Gradients / Solid Posters)"
            ],
            key="m1_engine_selector"
        )
        # Default region set high to 90% so it covers paragraphs in the middle
        region = st.slider("Target Region Height (%)", 15, 95, 90, key="m1_text_region")
        radius = st.slider("Inpainting Reconstruction Radius", 2.0, 15.0, 5.0, 0.5, key="m1_inpaint_radius")

    if st.button("✨ Run Selected Engine & Clean Background", type="primary", key="btn_run_m1_engine"):
        with st.spinner("Executing background reconstruction..."):
            if "Engine A" in engine_choice:
                from module_1_background_extractor import run_engine_a_light_sky
                cleaned, mask = run_engine_a_light_sky(original, region, radius)
            elif "Engine B" in engine_choice:
                from module_1_background_extractor import run_engine_b_rich_gradient
                cleaned, mask = run_engine_b_rich_gradient(original, region, radius)
            else:
                cleaned, mask = run_full_canvas_engine(original, region, radius)
                
            clean_bytes, mask_bytes = _png_bytes(cleaned), _png_bytes(mask)
            st.session_state["m1_clean_background_bytes"] = clean_bytes
            st.session_state["m1_text_mask_bytes"] = mask_bytes
            st.session_state["extracted_asset_bytes"] = clean_bytes
            st.session_state["visual_brief"] = {
                "design_style": f"Module 1 Clean Background ({engine_choice[:8]})",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": clean_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(clean_bytes).decode("ascii"),
                "visual_approved": True,
            }
            st.success("Background cleaned successfully!")

    if "m1_clean_background_bytes" in st.session_state:
        st.divider()
        st.markdown("### 🖼️ Clean Background Asset Preview")
        st.image(st.session_state["m1_clean_background_bytes"], width=350)
        
        with st.expander("🔍 Inspect Reconstruction Mask"):
            st.image(st.session_state["m1_text_mask_bytes"], width=350)
            
        st.download_button(
            "📥 Download Clean Background (.png)",
            st.session_state["m1_clean_background_bytes"],
            "clean_background.png",
            "image/png",
            key="dl_m1_engine_output"
        )
        
        st.markdown("#### 📝 Slide Content Editor")
        slides_data = st.session_state.get("sia_slide_contents", [])
        if not slides_data:
            slides_data = [{"headline": f"Slide {i+1} Headline", "body": f"Actionable execution strategy for slide {i+1}.", "category": f"STEP {i+1}"} for i in range(slide_count)]
            st.session_state["sia_slide_contents"] = slides_data
            
        for idx, slide in enumerate(slides_data):
            with st.expander(f"Slide {idx+1} Content", expanded=(idx == 0)):
                slide["headline"] = st.text_input(f"Headline {idx+1}", value=slide.get("headline", ""), key=f"m1_head_{idx}")
                slide["body"] = st.text_area(f"Body {idx+1}", value=slide.get("body", ""), key=f"m1_body_{idx}")
                slide["category"] = st.text_input(f"Category {idx+1}", value=slide.get("category", ""), key=f"m1_cat_{idx}")
                
        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)