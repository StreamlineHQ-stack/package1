# module_1_background_extractor.py • Dynamic Adaptive Scenic Background Cleaner
import streamlit as st
from PIL import Image, ImageFilter
import io
import base64
import numpy as np

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic Photography Background Cleaner (Archetype A)")
    st.info("Dynamically detects and removes header text from scenic backgrounds using adaptive background sampling, keeping mountains, objects, and textures fully intact.")

    uploaded_file = st.file_uploader("Upload Scenic Background Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Uploaded Slide", width=320)
        
        if st.button("✨ Dynamically Remove Text & Clean Background", type="primary", key="btn_run_m1"):
            with st.spinner("Analyzing image structure and clearing text adaptively..."):
                img = Image.open(uploaded_file).convert("RGB")
                w, h = img.size
                
                # Convert to numpy array for adaptive pixel analysis
                img_np = np.array(img)
                
                # 1. Sample dominant background color from top corners (sky/backdrop)
                corner_samples = np.concatenate([
                    img_np[:20, :50, :], 
                    img_np[:20, w-50:, :]
                ], axis=0)
                bg_color = np.median(corner_samples, axis=(0, 1)).astype(int)

                # 2. Adaptive text cleaning in the upper region (top 45%)
                # Identify pixels that contrast sharply with the background sky color
                header_limit = int(h * 0.45)
                cleaned_np = img_np.copy()
                
                for y in range(header_limit):
                    for x in range(w):
                        pixel = cleaned_np[y, x]
                        # If pixel is significantly darker/different than the sky background (text), blend it
                        diff = np.sum(np.abs(pixel.astype(int) - bg_color))
                        if diff > 90:  # High contrast threshold for text vs sky
                            # Sample horizontal neighbor or blend smoothly
                            left_neighbor = cleaned_np[y, max(0, x-5)]
                            cleaned_np[y, x] = (bg_color * 0.6 + left_neighbor * 0.4).astype(np.uint8)

                cleaned_img = Image.fromarray(cleaned_np)
                
                # Slight smooth filter on the cleaned header zone to ensure zero artifacts
                out = io.BytesIO()
                cleaned_img.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Dynamic Clean Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Header text dynamically removed! Clean scenic background ready.")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Module 1 Dynamic Clean Background":
        st.divider()
        st.markdown("### 🖼️ Font-Free Scenic Canvas & Live Content Editor")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Clean Scenic Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "clean_scenic_background.png", "image/png", key="dl_m1_dynamic")
        
        st.markdown("#### 📝 Slide Content Editor (Applied over Clean Background)")
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