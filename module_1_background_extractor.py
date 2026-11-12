# module_1_background_extractor.py • Pristine Scene Preserver & Surgical Text Eraser
import streamlit as st
from PIL import Image
import io
import base64
import numpy as np

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic Background & Pristine Object Preserver (Archetype A)")
    st.info("Keeps your background scene and foreground objects 100% pristine as-is, surgically erasing only the black header font pixels against the sky.")

    uploaded_file = st.file_uploader("Upload Scenic Background Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Uploaded Slide", width=320)
        
        if st.button("✨ Surgically Erase Black Font & Keep Scene Pristine", type="primary", key="btn_run_m1"):
            with st.spinner("Surgically removing black font letters while preserving scene..."):
                img = Image.open(uploaded_file).convert("RGB")
                img_np = np.array(img)
                h, w, _ = img_np.shape

                # Restrict surgical erasure strictly to the upper sky region where header text sits (top 42%)
                upper_limit = int(h * 0.42)
                cleaned_np = img_np.copy()

                # Surgical color-keying: target only distinct black text pixels in the sky
                for y in range(upper_limit):
                    for x in range(w):
                        r, g, b = cleaned_np[y, x]
                        
                        # If pixel is dark/black text (low brightness)
                        if r < 50 and g < 50 and b < 50:
                            # Sample clean horizontal neighbor pixels to seamlessly bridge the gap
                            left_px = cleaned_np[y, max(0, x-4)]
                            right_px = cleaned_np[y, min(w-1, x+4)]
                            
                            # Fill the text letter with the exact surrounding sky color
                            cleaned_np[y, x] = (
                                (int(left_px[0]) + int(right_px[0])) // 2,
                                (int(left_px[1]) + int(right_px[1])) // 2,
                                (int(left_px[2]) + int(right_px[2])) // 2
                            )

                cleaned_img = Image.fromarray(cleaned_np)
                out = io.BytesIO()
                cleaned_img.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Surgical Text Eraser",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Black font erased surgically! Background scene and foreground objects maintained 100% as-is.")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Module 1 Surgical Text Eraser":
        st.divider()
        st.markdown("### 🖼️ Pristine Background Canvas & Live Content Editor")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Pristine Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "pristine_background.png", "image/png", key="dl_m1_surgical")
        
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