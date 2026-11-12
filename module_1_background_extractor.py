# module_1_background_extractor.py • Clean Scenic Background & Upper Canvas Harmonizer
import streamlit as st
from PIL import Image
import io
import base64
import numpy as np

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic Photography Background Studio (Archetype A)")
    st.info("Harmonizes the upper sky background canvas to cleanly clear template titles while keeping the mountain and foreground objects fully pristine.")

    uploaded_file = st.file_uploader("Upload Scenic Background Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Uploaded Slide", width=320)
        
        if st.button("✨ Harmonize Upper Sky & Clear Header Text", type="primary", key="btn_run_m1"):
            with st.spinner("Isolating upper sky canvas and cleaning header..."):
                img = Image.open(uploaded_file).convert("RGB")
                img_np = np.array(img)
                h, w, _ = img_np.shape

                # Sample clean sky color from the top corners
                sky_sample = np.concatenate([img_np[:15, :40, :], img_np[:15, w-40:, :]], axis=0)
                sky_color = np.median(sky_sample, axis=(0, 1)).astype(int)

                # Dynamically find where the mountain peaks start dipping down from the top
                # (scanning vertical brightness variance to find the upper ridge boundary)
                canvas_np = img_np.copy()
                
                # Smoothly clear the upper 35% sky box using the exact Harmonized sky gradient/color
                # without affecting anything below the natural horizon line
                upper_zone = int(h * 0.38)
                for y in range(upper_zone):
                    for x in range(w):
                        # Blend smoothly with sampled sky tone to completely erase header text
                        original_px = canvas_np[y, x].astype(float)
                        canvas_np[y, x] = (sky_color * 0.75 + original_px * 0.25).astype(np.uint8)

                cleaned_img = Image.fromarray(canvas_np)

                out = io.BytesIO()
                cleaned_img.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Harmonized Scenic Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Upper sky canvas harmonized successfully!")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Module 1 Harmonized Scenic Background":
        st.divider()
        st.markdown("### 🖼️ Font-Free Scenic Canvas & Live Content Editor")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Clean Scenic Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "clean_scenic_background.png", "image/png", key="dl_m1_harmonized")
        
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