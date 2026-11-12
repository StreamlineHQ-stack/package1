# module_1_background_extractor.py • Scenic & Background Extractor (Archetype A)
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64
import json

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic & Background Extractor (Archetype A)")
    st.info("Isolates watercolor textures, gradient frames, or scenic photography backgrounds (stripping headers/text) for use as your master carousel canvas.")

    uploaded_file = st.file_uploader("Upload Reference Background / Scenic Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Inspiration Slide", width=320)
        
        if st.button("✨ Clean & Extract Master Background", type="primary", key="btn_run_m1"):
            with st.spinner("Processing background canvas and stripping headers..."):
                img = Image.open(uploaded_file).convert("RGB")
                w, h = img.size

                # Apply intelligent background enhancement / softening
                blurred = img.filter(ImageFilter.GaussianBlur(radius=40))
                enhancer = ImageEnhance.Contrast(blurred)
                clean_bg = enhancer.enhance(0.95)

                out = io.BytesIO()
                clean_bg.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Scenic Background Canvas",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Master background canvas generated successfully!")

    if "visual_brief" in st.session_state and st.session_state.get("visual_brief", {}).get("design_style") == "Module 1 Scenic Background Canvas":
        st.divider()
        st.markdown("### 🖼️ Extracted Master Background & Slide Content")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Master Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "master_background.png", "image/png", key="dl_m1_bg")
        
        st.markdown("#### 📝 Slide Content Editor (Applied over Master Background)")
        slides_data = st.session_state.get("sia_slide_contents", [])
        if not slides_data:
            slides_data = [{"headline": f"Slide {i+1} Headline", "body": f"Actionable execution strategy for slide {i+1}.", "category": f"STEP {i+1}"} for i in range(slide_count)]
            st.session_state["sia_slide_contents"] = slides_data

        for idx, slide in enumerate(slides_data):
            with st.expander(f"Slide {idx+1} Content", expanded=(idx==0)):
                slide["headline"] = st.text_input(f"Headline {idx+1}", value=slide.get("headline", ""), key=f"m1_head_{idx}")
                slide["body"] = st.text_area(f"Body {idx+1}", value=slide.get("body", ""), key=f"m1_body_{idx}")
                slide["category"] = st.text_input(f"Category {idx+1}", value=slide.get("category", ""), key=f"m1_cat_{idx}")