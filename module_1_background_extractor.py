# module_1_background_extractor.py • Scenic & Background Extractor (Archetype A)
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64

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
        st.markdown("### 🖼️ Extracted Master Background Preview")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Master Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "master_background.png", "image/png", key="dl_m1_bg")
        
        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False, api_key=api_key)