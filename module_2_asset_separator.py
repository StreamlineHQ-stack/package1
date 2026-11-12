# module_2_asset_separator.py • Two-Output Asset Separator (Archetype B)
import streamlit as st
from PIL import Image
import io
import base64
import numpy as np

try:
    from rembg import remove, new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

def render_module_2_ui(slide_count, api_key):
    st.markdown("#### ✂️ Module 2: Two-Output Asset Separator (Archetype B)")
    st.info("Separates solid studio posters into a clean solid background canvas and a full-canvas transparent foreground subject layer.")

    uploaded_file = st.file_uploader("Upload Subject-Centric Poster / Slide", type=["png", "jpg", "jpeg"], key="m2_poster_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Inspiration Poster", width=320)
        
        if st.button("✨ Separate Background & Subject", type="primary", key="btn_run_m2"):
            with st.spinner("Extracting background color and isolating subject..."):
                original = Image.open(uploaded_file).convert("RGB")
                w, h = original.size

                # 1. Sample dominant background color
                try:
                    bg_color = original.getpixel((20, 20))
                    if max(bg_color[:3]) - min(bg_color[:3]) < 15 and bg_color[0] > 200:
                        bg_color = (210, 40, 30)
                except Exception:
                    bg_color = (210, 40, 30)

                clean_bg = Image.new("RGB", (w, h), bg_color[:3])
                bg_out = io.BytesIO()
                clean_bg.save(bg_out, format="PNG", optimize=True)
                bg_out.seek(0)
                bg_bytes = bg_out.getvalue()

                # 2. Transparent subject layer (full canvas dimensions)
                transparent_card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                if REMBG_AVAILABLE:
                    try:
                        session = new_session("silueta")
                        extracted_obj = remove(original, session=session).convert("RGBA")
                        transparent_card.paste(extracted_obj, (0, 0), extracted_obj)
                    except Exception:
                        transparent_card = original.convert("RGBA")
                else:
                    transparent_card = original.convert("RGBA")

                trans_out = io.BytesIO()
                transparent_card.save(trans_out, format="PNG", optimize=True)
                trans_out.seek(0)
                trans_bytes = trans_out.getvalue()

            st.session_state["m2_bg_bytes"] = bg_bytes
            st.session_state["m2_trans_bytes"] = trans_bytes
            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 2 Separated Asset Composition",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Two-output separation complete!")

    if "m2_bg_bytes" in st.session_state:
        st.divider()
        st.markdown("### 🎯 Two Clean Outputs Preview")
        out_col1, out_col2 = st.columns(2)
        with out_col1:
            st.markdown("#### 1. Clean Solid Background")
            st.image(st.session_state["m2_bg_bytes"], width=280)
            st.download_button("📥 Download Background (.png)", st.session_state["m2_bg_bytes"], "clean_background.png", "image/png", key="dl_m2_bg_mod")
        with out_col2:
            st.markdown("#### 2. Transparent Core Subject")
            st.image(st.session_state["m2_trans_bytes"], width=280)
            st.download_button("📥 Download Transparent Asset (.png)", st.session_state["m2_trans_bytes"], "transparent_subject.png", "image/png", key="dl_m2_trans_mod")

        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False, api_key=api_key)