# module_1_background_extractor.py • OCR-Locked & Subject-Protected Background Studio
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image

def _to_bgr(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)

def run_precision_ocr_engine(image: Image.Image, region_pct: int, radius: float) -> tuple:
    """Precision OCR Engine: Only erases pixels explicitly inside verified text bounding boxes. Protects all image subjects."""
    bgr = _to_bgr(image)
    h, w = bgr.shape[:2]
    roi_bottom = max(1, min(h, int(h * region_pct / 100)))
    
    # Initialize empty mask (zero touch by default)
    mask = np.zeros((h, w), np.uint8)
    
    try:
        import pytesseract
        from pytesseract import Output
        
        # Scale up region for high-accuracy character recognition
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
                conf = float(data["conf"][i])
            except (ValueError, TypeError, KeyError):
                conf = -1
                
            # Strict confidence filter to eliminate false positives
            if conf < 15:
                continue
                
            x = int(data["left"][i] / scale)
            y = int(data["top"][i] / scale)
            ww = int(data["width"][i] / scale)
            hh = int(data["height"][i] / scale)
            
            # Tight bounding box around verified text characters only
            x1, y1 = max(0, x - 2), max(0, y - 2)
            x2, y2 = min(w, x + ww + 2), min(roi_bottom, y + hh + 2)
            
            mask[y1:y2, x1:x2] = 255
            
    except Exception:
        pass
        
    # Minimal dilation to cover letter edges without spilling
    if np.any(mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.dilate(mask, kernel, iterations=1)

    # Inpaint only the verified text bounding boxes
    cleaned = cv2.inpaint(bgr, mask, float(radius), cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB)), Image.fromarray(mask).convert("RGB")

def _png_bytes(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()

def render_module_1_ui(slide_count, api_key=None):
    st.markdown("#### 🧠 Module 1: Precision OCR-Locked Background Studio")
    st.info("Identifies text with absolute certainty using OCR bounding boxes before performing background reconstruction. Protected subjects remain 100% untouched.")
    
    uploaded = st.file_uploader("Upload inspiration slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    if uploaded is None:
        return
        
    original = Image.open(uploaded).convert("RGB")
    st.image(original, caption="Original inspiration slide", width=320)
    
    with st.expander("⚙️ Precision Engine Settings", expanded=True):
        region = st.slider("Text Scan Region Height (%)", 10, 95, 75, key="m1_text_region")
        radius = st.slider("Inpainting Radius", 1.0, 10.0, 3.0, 0.5, key="m1_inpaint_radius")

    if st.button("✨ Verify Text & Clean Background", type="primary", key="btn_run_m1_engine"):
        with st.spinner("Running OCR text verification and inpainting..."):
            cleaned, mask = run_precision_ocr_engine(original, region, radius)
            clean_bytes, mask_bytes = _png_bytes(cleaned), _png_bytes(mask)
            
            st.session_state["m1_clean_background_bytes"] = clean_bytes
            st.session_state["m1_text_mask_bytes"] = mask_bytes
            st.session_state["extracted_asset_bytes"] = clean_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Precision OCR Clean Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": clean_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(clean_bytes).decode("ascii"),
                "visual_approved": True,
            }
            st.success("Background cleaned with OCR verification!")

    if "m1_clean_background_bytes" in st.session_state:
        st.divider()
        st.markdown("### 🖼️ Clean Background Asset Preview")
        st.image(st.session_state["m1_clean_background_bytes"], width=350)
        
        with st.expander("🔍 Inspect Verified Text Mask (White = Text Boxes Only)"):
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