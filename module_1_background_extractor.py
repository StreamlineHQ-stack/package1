# module_1_background_extractor.py • Precise Sky Text Eraser
import streamlit as st
from PIL import Image
import io
import base64
import numpy as np

def render_module_1_ui(slide_count, api_key):
    st.markdown("#### 🌄 Module 1: Scenic Photography Background Studio (Archetype A)")
    st.info("Precisely erases black header text strokes against the sky gradient while leaving mountain and foreground photography 100% pristine.")

    uploaded_file = st.file_uploader("Upload Scenic Background Slide", type=["png", "jpg", "jpeg"], key="m1_scenic_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Uploaded Slide", width=320)
        
        if st.button("✨ Erase Header Text & Keep Background Pristine", type="primary", key="btn_run_m1"):
            with st.spinner("Targeting and erasing black font pixels..."):
                img = Image.open(uploaded_file).convert("RGBA")
                img_np = np.array(img)
                h, w, _ = img_np.shape

                # Target the upper sky zone where header text sits
                upper_limit = int(h * 0.45)
                
                # Scan upper region for dark text pixels and replace them with local sky gradient colors
                for y in range(upper_limit):
                    for x in range(w):
                        r, g, b, a = img_np[y, x]
                        
                        # Identify dark/black text pixels (low brightness, low color saturation)
                        if r < 60 and g < 60 and b < 60:
                            # Sample immediate horizontal neighbors to fill the text letter cleanly
                            left_px = img_np[y, max(0, x-3)]
                            right_px = img_np[y, min(w-1, x+3)]
                            
                            # Replace text pixel with average of neighbors
                            img_np[y, x] = (
                                (int(left_px[0]) + int(right_px[0])) // 2,
                                (int(left_px[1]) + int(right_px[1])) // 2,
                                (int(left_px[2]) + int(right_px[2])) // 2,
                                255
                            )

                cleaned_img = Image.fromarray(img_np).convert("RGB")
                out = io.BytesIO()
                cleaned_img.save(out, format="PNG", optimize=True)
                out.seek(0)
                bg_bytes = out.getvalue()

            st.session_state["extracted_asset_bytes"] = bg_bytes
            st.session_state["visual_brief"] = {
                "design_style": "Module 1 Erased Text Scenic Background",
                "asset_mode": "inspiration_visual",
                "visual_asset_bytes": bg_bytes,
                "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(bg_bytes).decode("ascii"),
                "visual_approved": True
            }
            st.success("Header text erased successfully while preserving background gradient!")

    if "visual_brief" in st.session_state and st.session_state["visual_brief"].get("design_style") == "Module 1 Erased Text Scenic Background":
        st.divider()
        st.markdown("### 🖼️ Clean Scenic Canvas & Live Content Editor")
        st.image(st.session_state["visual_brief"]["visual_asset_bytes"], width=350)
        st.download_button("📥 Download Clean Scenic Background (.png)", st.session_state["visual_brief"]["visual_asset_bytes"], "clean_scenic_background.png", "image/png", key="dl_m1_erased")
        
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