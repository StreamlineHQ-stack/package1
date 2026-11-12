# module_1_background_extractor.py • Precise Local Text Inpainting for Scenic Backgrounds
import streamlit as st
from PIL import Image
import io
import base64
import numpy as np

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic Photography Background Studio (Archetype A)")
    st.info("Isolates scenic backgrounds and performs precise local text-stroke inpainting to remove only black/dark font pixels without altering the background.")

    uploaded_file = st.file_uploader("Upload Scenic Background Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Uploaded Slide", width=320)
        
        if st.button("✨ Remove Black Font & Extract Clean Canvas", type="primary", key="btn_run_m1"):
            with st.spinner("Isolating and removing dark font pixels locally..."):
                img = Image.open(uploaded_file).convert("RGB")
                img_np = np.array(img)
                h, w, _ = img_np.shape

                # Focus on the upper half where header text is located
                upper_limit = int(h * 0.55)
                canvas_np = img_np.copy()

                # Local inpainting for dark text strokes against light sky
                for y in range(5, upper_limit - 5):
                    for x in range(5, w - 5):
                        pixel = canvas_np[y, x].astype(float)
                        
                        # Calculate local average of surrounding pixels (excluding the center)
                        neighborhood = canvas_np[y-2:y+3, x-2:x+3, :].astype(float)
                        local_mean = np.mean(neighborhood, axis=(0, 1))
                        
                        # If the pixel is significantly darker than its local neighborhood (i.e., a black letter stroke)
                        brightness = np.mean(pixel)
                        local_brightness = np.mean(local_mean)
                        
                        if local_brightness - brightness > 45 and brightness < 120:
                            # Replace dark text pixel with the smooth local background color
                            canvas_np[y, x] = local_mean.astype(np.uint8)

                cleaned_img = Image.fromarray(canvas_np)

                out = io.BytesIO()
                cleaned_img.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Precise Clean Scenic Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Dark font pixels successfully removed locally!")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Module 1 Precise Clean Scenic Background":
        st.divider()
        st.markdown("### 🖼️ Font-Free Scenic Canvas & Live Content Editor")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Clean Scenic Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "clean_scenic_background.png", "image/png", key="dl_m1_precise")
        
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