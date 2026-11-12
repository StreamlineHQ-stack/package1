# module_1_background_extractor.py • Proven Multi-Engine Background Studio
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image

def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)

def run_engine_a_scenic(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine A: Proven local-contrast inpainting for scenic backgrounds & light skies (e.g., Coffee Cup)"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)[:roi_bottom]
    k = max(21, int(min(h, w) * .16))
    if k % 2 == 0:
        k += 1
    local_bg = cv2.GaussianBlur(gray, (k, k), 0)
    darkness = cv2.subtract(local_bg, gray)
    
    mask = np.zeros((h, w), np.uint8)
    raw = np.where(darkness >= 10, 255, 0).astype(np.uint8)
    mask[:roi_bottom] = cv2.medianBlur(raw, 3)
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def run_engine_b_poster(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine B: Proven LAB-channel variance inpainting for solid/gradient studio posters (e.g., SARINA)"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    lab = cv2.cvtColor(bgr[:roi_bottom], cv2.COLOR_BGR2LAB)
    l_chan, _, _ = cv2.split(lab)
    
    blur = cv2.GaussianBlur(l_chan, (51, 51), 0)
    diff = cv2.absdiff(l_chan, blur)
    _, thresh = cv2.threshold(diff, 22, 255, cv2.THRESH_BINARY)
    
    mask = np.zeros((h, w), np.uint8)
    mask[:roi_bottom] = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_NS)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def _png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()

def render_module_1_ui(slide_count, api_key=None):
    st.markdown("#### 🧠 Module 1: Multi-Engine Background Studio")
    st.info("Select the proven processing engine that matches your slide type for clean, artifact-free text removal.")
    
    uploaded = st.file_uploader("Upload inspiration slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    if uploaded is None:
        return
        
    original = Image.open(uploaded).convert("RGB")
    st.image(original, caption="Original inspiration slide", width=320)
    
    with st.expander("⚙️ Engine Selector & Controls", expanded=True):
        engine_choice = st.selectbox(
            "Select Processing Engine:",
            [
                "Engine A: Scenic Sky & Landscape (e.g., Coffee Cup / Mountain)",
                "Engine B: Studio Poster & Rich Gradient (e.g., SARINA Poster)"
            ],
            key="m1_engine_selector"
        )
        region = st.slider("Scan Region Height (%)", 20, 95, 45, key="m1_text_region")
        radius = st.slider("Inpainting Radius", 1.0, 10.0, 5.0, 0.5, key="m1_inpaint_radius")

    if st.button("✨ Run Engine & Clean Background", type="primary", key="btn_run_m1_engine"):
        with st.spinner("Processing background reconstruction..."):
            if "Engine A" in engine_choice:
                cleaned, mask = run_engine_a_scenic(original, region, radius)
            else:
                cleaned, mask = run_engine_b_poster(original, region, radius)
                
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
        
        with st.expander("🔍 Inspect Target Mask"):
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