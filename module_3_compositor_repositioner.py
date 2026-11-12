# module_3_compositor_repositioner.py • Interactive Re-Composition & Repositioning Studio
import streamlit as st
from PIL import Image
import io
import base64

def render_module_3_ui(slide_count, api_key):
    st.markdown("#### 📐 Module 3: Interactive Re-Composition & Repositioning Studio")
    st.info("Customize your asset placement, choose positioning (center, corners, bottom), or upload custom foreground objects to fuse onto your background canvas.")

    bg_file = st.file_uploader("Upload Background Canvas", type=["png", "jpg", "jpeg"], key="m3_bg_upload")
    sub_file = st.file_uploader("Upload Foreground Subject (Transparent PNG recommended)", type=["png", "jpg", "jpeg"], key="m3_sub_upload")

    position_choice = st.selectbox(
        "Select Subject Positioning:",
        ["Center", "Bottom Center", "Top Center", "Custom Overlay"],
        key="m3_pos_select"
    )

    if bg_file and sub_file:
        st.image(bg_file, caption="Background Preview", width=220)
        st.image(sub_file, caption="Subject Preview", width=220)

        if st.button("🚀 Generate Final Composition", type="primary", key="btn_run_m3"):
            with st.spinner("Compositing layers..."):
                bg = Image.open(bg_file).convert("RGBA")
                sub = Image.open(sub_file).convert("RGBA")
                bw, bh = bg.size
                sw, sh = sub.size

                # Calculate placement coordinates based on user choice
                if position_choice == "Center":
                    x = (bw - sw) // 2
                    y = (bh - sh) // 2
                elif position_choice == "Bottom Center":
                    x = (bw - sw) // 2
                    y = bh - sh - int(bh * 0.05)
                elif position_choice == "Top Center":
                    x = (bw - sw) // 2
                    y = int(bh * 0.08)
                else:
                    x, y = 50, 50

                result = bg.copy()
                result.paste(sub, (x, y), mask=sub.split()[-1])

                out = io.BytesIO()
                result.convert("RGB").save(out, format="PNG", optimize=True)
                out.seek(0)
                comp_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = comp_bytes
            st.session_state["visual_brief"] = {
                "design_style": f"Module 3 Custom Composition ({position_choice})",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": comp_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(comp_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Composition generated successfully!")

    if "visual_brief" in st.session_state and "Module 3" in st.session_state["visual_brief"].get("design_style", ""):
        st.divider()
        st.markdown("### 🎨 Final Composed Master Slide Preview")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Final Composition (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "composed_master_slide.png", "image/png", key="dl_m3_comp")

        from sia_universal_renderer import render_universal_canvas
        render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False, api_key=api_key)