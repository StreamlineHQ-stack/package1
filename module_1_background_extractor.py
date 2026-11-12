# module_1_background_extractor.py • Robust Hybrid Adaptive Background Studio
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image

def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)

def run_adaptive_hybrid_engine(image: Image.Image, region_pct: int, sensitivity: int, radius: float) -> tuple:
    """Hybrid Adaptive Engine: Uses OpenCV morphological analysis to isolate text strokes across varied backgrounds without relying on external binaries."""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    mask = np.zeros((h, w), np.uint8)
    
    # 1. Convert ROI to grayscale
    roi = bgr[:roi_bottom]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # 2. Adaptive Gaussian thresholding with valid odd block size
    block_size = 35
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, sensitivity)
    
    # 3. Morphological filtering to isolate text character shapes from background gradients
    kernel_chars = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned_chars = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_chars)
    
    # Connect nearby character pixels into word blocks
    kernel_words = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    word_blocks = cv2.morphologyEx(cleaned_chars, cv2.MORPH_CLOSE, kernel_words)
    
    # Place into full canvas mask
    mask[:roi_bottom] = word_blocks
    
    # 4. Dilate slightly for smooth inpainting edge blending
    if np.any(mask):
        dilation_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.dilate(mask, dilation_kernel, iterations=1)

    # 5. Inpaint only the masked text regions
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def _png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()

def render_module_1_ui(slide_count, api_key=None):
    st.markdown("#### 🧠 Module 1: Robust Hybrid Background & Text Studio")
    st.info("Uses advanced adaptive morphology to detect and remove text across light skies, solid posters, and multi-tier layouts without external dependencies.")
    
    uploaded = st.file_uploader("Upload inspiration slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    if uploaded is None:
        return
        
    original = Image.open(uploaded).convert("RGB")
    st.image(original, caption="Original inspiration slide", width=320)
    
    with st.expander("⚙️ Adaptive Engine Controls", expanded=True):
        region = st.slider("Scan Region Height (%)", 20, 95, 80, key="m1_text_region")
        sensitivity = st.slider("Text Detection Sensitivity (C-Constant)", 2, 20, 8, key="m1_sensitivity")
        radius = st.slider("Inpainting Radius", 1.0, 10.0, 3.0, 0.5, key="m1_inpaint_radius")

    if st.button("✨ Clean Background & Remove Text", type="primary", key="btn_run_m1_engine"):
        with st.spinner("Analyzing slide and reconstructing background..."):
            cleaned, mask = run_adaptive_hybrid_engine(original, region, sensitivity, radius)
            clean_bytes, mask_bytes = _png_bytes(cleaned), _png_bytes(mask)
            
            st.session_state["m1_clean_background_bytes"] = clean_bytes
            st.session_state["m1_text_mask_bytes"] = mask_bytes
            st.session_state["extracted_asset_bytes"] = clean_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Adaptive Clean Background",
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
        
        with st.expander("🔍 Inspect Target Mask (White = Text Areas Targeted)"):
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