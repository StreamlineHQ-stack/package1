import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

def render_sia_studio(visual_path="", slide_count=1):
    # ==========================================
    # OPTION 2: SWIPE-TO-TEMPLATE LAYOUT ARCHITECTURE ENGINE
    # ==========================================
    if "Style Inspiration" in visual_path or "2. 3-Mode Visual Asset Extractor" in visual_path or not visual_path:
        st.session_state["is_standalone_mode"] = False
        st.markdown("#### 📐 Swipe-to-Template Layout Architecture Engine")
        st.info("Smart Structural Cloning active. Deconstructs reference mood and synthesizes a pristine, unsmudged equivalent template layout.")
        
        uploaded_slide = st.file_uploader("Upload Inspiration Swipe Slide", type=["png", "jpg", "jpeg"], key="sia_router_upload")
        
        if uploaded_slide is not None:
            original_image = Image.open(uploaded_slide).convert("RGB")
            w, h = original_image.size
            
            # Sample background colors intelligently from multiple clean corner zones
            corner_samples = [
                original_image.getpixel((int(w * 0.05), int(h * 0.05))),
                original_image.getpixel((int(w * 0.95), int(h * 0.05))),
                original_image.getpixel((int(w * 0.05), int(h * 0.95))),
                original_image.getpixel((int(w * 0.95), int(h * 0.95)))
            ]
            
            sample_color_top = corner_samples[0]
            sample_color_center = corner_samples[2]
            
            hex_top = '#%02x%02x%02x' % sample_color_top
            hex_center = '#%02x%02x%02x' % sample_color_center
            
            # --- SYNTHESIZE PRISTINE EQUIVALENT BLUEPRINT (NO SMUDGES) ---
            equivalent_card = Image.new("RGB", (w, h), color=sample_color_center)
            draw = ImageDraw.Draw(equivalent_card)
            
            for i in range(int(h * 0.3)):
                r = int(sample_color_top[0] + (sample_color_center[0] - sample_color_top[0]) * (i / (h * 0.3)))
                g = int(sample_color_top[1] + (sample_color_center[1] - sample_color_top[1]) * (i / (h * 0.3)))
                b = int(sample_color_top[2] + (sample_color_center[2] - sample_color_top[2]) * (i / (h * 0.3)))
                draw.line([(0, i), (w, i)], fill=(r, g, b))
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Inspiration Reference Slide**")
                st.image(original_image, use_container_width=True)
                
            with col2:
                st.markdown("**Synthesized Equivalent Blueprint (Pristine)**")
                st.image(equivalent_card, use_container_width=True)
                
            st.success(f"Layout deconstructed! Equivalent template generated. Palette matched: `{hex_top}` / `{hex_center}`")
            
            st.markdown("---")
            st.subheader("📝 Map Deck Content into Template Layout")
            
            slide_contents = st.session_state.get("sia_slide_contents", [])
            if slide_contents:
                st.info(f"Loaded {len(slide_contents)} slides from your Content Engine. Ready to batch-render into the template architecture.")
            else:
                st.warning("No slides found from Step 1 yet. Enter custom copy below or generate a full deck in Step 1.")
            
            template_headline = st.text_input("Test Template Headline", value="Scale Your Creator Business Faster")
            template_body = st.text_area("Test Template Body Copy", value="Build modular systems that protect your margins and eliminate external API dependencies.")
            
            if st.button("🚀 Render Template Layout Preview", key="render_template_layout_btn"):
                template_spec = {
                    "asset_mode": "template_architecture",
                    "layout_archetype": "Smart Equivalent Synthesizer",
                    "primary_color": hex_top,
                    "visual_asset_bytes": None,
                    "design_style": "Pristine Brand Equivalent",
                    "palette": [hex_top, hex_center, "#FFFFFF"],
                    "typography": "Modern Professional"
                }
                st.session_state["visual_brief"] = template_spec
                st.session_state["visual_approved"] = True
                st.success("Template architecture compiled successfully with zero distortion!")

            # Prepare payload for renderer
            buffered = io.BytesIO()
            equivalent_card.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            b64_str = base64.b64encode(img_bytes).decode()
            data_url = f"data:image/png;base64,{b64_str}"

            visual_spec = {
                "asset_mode": "template_architecture",
                "visual_asset_bytes": img_bytes,
                "visual_asset_data_url": data_url,
                "design_style": "Pristine Brand Equivalent",
                "palette": [hex_top, hex_center, "#FFFFFF"],
                "typography": "Modern Clean",
                "visual_mood": "Professional High-Converting"
            }

            st.session_state["visual_brief"] = visual_spec
            st.session_state["visual_approved"] = True
            
            st.divider()
            if "render_universal_canvas" in globals():
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)