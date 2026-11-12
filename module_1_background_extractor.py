# module_1_background_extractor.py • Multi-Engine Background & Text Removal Studio
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image

def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)

def run_engine_a_light_sky(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine A: Simple Inpainting for Dark Text on Smooth Light Skies (e.g., Coffee Cup)"""
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

def run_engine_b_rich_gradient(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine B: Advanced Inpainting for Gradients / Posters (e.g., Terracotta/SARINA)"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    lab = cv2.cvtColor(bgr[:roi_bottom], cv2.COLOR_BGR2LAB)
    l_chan, _, _ = cv2.split(lab)
    blur = cv2.GaussianBlur(l_chan, (51, 51), 0)
    diff = cv2.absdiff(l_chan, blur)
    _, thresh = cv2.threshold(diff, 22, 255, cv2.THRESH_BINARY)
    
    mask = np.zeros((h, w), np.uint8)
    mask[:roi_bottom] = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)), iterations=1)
    
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_NS)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def run_engine_c_multi_tier(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Engine C: Multi-Tier / Full-Height Text Eraser (e.g., Split Header + Sub-copy Posters)"""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    gray = cv2.cvtColor(bgr[:roi_bottom], cv2.COLOR_BGR2GRAY)
    # Adaptive thresholding to catch both heavy bold headers and fine paragraph sub-copy
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 10)
    
    # Filter out large image boxes/borders, keep text character strokes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned_thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    mask = np.zeros((h, w), np.uint8)
    mask[:roi_bottom] = cleaned_thresh
    
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
                "Engine C: Multi-Tier / Block Text Eraser (Headers + Sub-copy - e.g., Get In Touch)",
                "Engine A: Simple Text Removal (Smooth Light Sky / Fog - e.g., Coffee Cup)",
                "Engine B: Advanced Text Removal (Rich Gradients / Solid Posters - e.g., Terracotta/SARINA)"
            ],
            key="m1_engine_selector"
        )
        region = st.slider("Target Region Height (%)", 15, 95, 65, key="m1_text_region")
        radius = st.slider("Inpainting Reconstruction Radius", 2.0, 15.0, 5.0, 0.5, key="m1_inpaint_radius")

    if st.button("✨ Run Selected Engine & Clean Background", type="primary", key="btn_run_m1_engine"):
        with st.spinner("Executing background reconstruction..."):
            if "Engine A" in engine_choice:
                cleaned, mask = run_engine_a_light_sky(original, region, radius)
            elif "Engine B" in engine_choice:
                cleaned, mask = run_engine_b_rich_gradient(original, region, radius)
            else:
                cleaned, mask = run_engine_c_multi_tier(original, region, radius)
                
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