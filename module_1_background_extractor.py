# module_1_background_extractor.py • Clean Scenic Background & Content Integrator
import streamlit as st
from PIL import Image
import io
import base64

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic Photography Background Studio (Archetype A)")
    st.info("Preserves the pristine scenic photography background as-is, allowing your content textboxes to overlay cleanly over the sky region.")

    uploaded_file = st.file_uploader("Upload Scenic Background Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Uploaded Slide", width=320)
        
        if st.button("✨ Load Scenic Master Canvas", type="primary", key="btn_run_m1"):
            with st.spinner("Preparing pristine scenic background canvas..."):
                img = Image.open(uploaded_file).convert("RGB")
                out = io.BytesIO()
                img.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Pristine Scenic Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Scenic background canvas loaded successfully!")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Module 1 Pristine Scenic Background":
        st.divider()
        st.markdown("### 🖼️ Scenic Master Canvas & Live Content Editor")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Master Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "scenic_master_background.png", "application/octet-stream", key="dl_m1_clean")
        
        st.markdown("#### 📝 Slide Content Editor")
        slides_data = st.session_state.get("sia_slide_contents", [])
        if not slides_data:
            slides_data = [{"headline": f"Slide {i+1} Headline", "body": f"Actionable execution strategy for slide {i+1}.", "category": f"STEP {i+1}"} for i in range(slide_count)]
            st.session_state["sia_slide_contents"] = slides_data

        for idx, slide in enumerate(slides_data):
            with st.expander(f"Slide {idx+1} Content", expanded=(idx==0)):
                slide["headline"] = st.text_input(f"Headline {idx+1}", value=slide.get("headline", ""), key=f"m1_head_{idx}")
                slide["body"] = st.text_area(f"Body {idx+1}", value=slide.get("body", ""), key=f"m1_body_{idx}")
                slide["category"] = st.text_input(f"Category {idx+1}", value=slide.get("category", ""), key=f"m1_cat_{idx}")
        
        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)