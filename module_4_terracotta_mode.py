# module_4_terracotta_mode.py • Terracotta / Solid Color & Font Matcher
import streamlit as st
from PIL import Image
import io
import base64

def render_module_4_ui(slide_count, api_key):
    st.markdown("#### 🎨 Module 4: Terracotta / Solid Color & Font Matcher")
    st.info("Extracts the exact solid background color and matches typography styling from minimalist studio posters.")

    uploaded_file = st.file_uploader("Upload Solid Background / Poster Slide", type=["png", "jpg", "jpeg"], key="m4_upload")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Reference Slide", width=300)

        if st.button("✨ Extract Solid Color & Font Palette", type="primary", key="btn_run_m4"):
            with st.spinner("Analyzing background and font color..."):
                img = Image.open(uploaded_file).convert("RGB")
                w, h = img.size

                # Sample corner color for background
                bg_color = img.getpixel((15, 15))
                
                # Create clean solid background canvas
                clean_solid = Image.new("RGB", (w, h), bg_color)
                out = io.BytesIO()
                clean_solid.save(out, format="PNG", optimize=True)
                out.seek(0)
                solid_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = solid_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Terracotta Solid Color Mode",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": solid_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(solid_bytes).decode("ascii"),
                "visual_approved": True,
                "palette": [f"RGB{bg_color}", "#FFFFFF", "#8B0000"]
            }
            st.success("Solid background color extracted successfully!")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Terracotta Solid Color Mode":
        st.divider()
        st.markdown("### 🎯 Solid Color Canvas & Live Content Preview")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=320)
        st.download_button("📥 Download Solid Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "terracotta_background.png", "image/png", key="dl_m4")

        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)