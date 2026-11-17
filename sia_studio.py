import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

def render_sia_studio(visual_path="", slide_count=1):
    if "Style Inspiration" in visual_path or "2. 3-Mode Visual Asset Extractor" in visual_path or not visual_path:
        st.session_state["is_standalone_mode"] = False
        
        # ==========================================
        # STEP 1: CONTENT ENGINE & FEATURE-TO-BENEFITS
        # ==========================================
        st.markdown("### 📝 Step 1: Content Engine & Feature-to-Benefits")
        st.info("Transform core features, hooks, or offers into structured, high-converting carousel slide copy.")
        
        with st.expander("⚙️ Configure Content Generation Parameters", expanded=True):
            core_topic = st.text_input("Core Topic / Product / Feature", value="AI-Powered Workflow Automation for Creators")
            target_audience = st.text_input("Target Audience", value="Solopreneurs & Online Coaches")
            num_slides = st.slider("Target Slide Count", min_value=3, max_value=10, value=5)
            
            if st.button("✨ Generate Slide Content Deck", key="generate_sia_content_btn"):
                # Generate structured slide content and store in session state
                generated_slides = []
                for i in range(1, num_slides + 1):
                    if i == 1:
                        headline = f"Stop Wasting Hours on {core_topic}"
                        body = f"The old way of handling {core_topic} for {target_audience} is broken. Here is the modern system."
                    elif i == num_slides:
                        headline = "Ready to Scale Your System?"
                        body = "Implement this exact workflow today and reclaim your time. Link in bio to get started."
                    else:
                        headline = f"Pillar {i}: Automated Leverage"
                        body = f"Break down complex tasks into repeatable modules designed specifically for {target_audience}."
                    
                    generated_slides.append({"slide": i, "headline": headline, "body": body})
                
                st.session_state["sia_slide_contents"] = generated_slides
                st.success(f"Successfully generated {num_slides} high-impact slides from your content engine!")

        # Display currently loaded slide contents if available
        slide_contents = st.session_state.get("sia_slide_contents", [])
        if slide_contents:
            st.success(f"✅ Content Engine Active: {len(slide_contents)} slides loaded and ready for layout rendering.")
            with st.expander("👀 View Generated Slide Content Stream"):
                for s in slide_contents:
                    st.markdown(f"**Slide {s['slide']}:** `{s['headline']}` — _{s['body']}_")
        else:
            st.warning("⚠️ No slide content generated yet. Run Step 1 above to populate your deck.")

        st.markdown("---")

        # ==========================================
        # STEP 2: SWIPE-TO-TEMPLATE LAYOUT ARCHITECTURE
        # ==========================================
        st.markdown("### 📐 Step 2: Swipe-to-Template Layout Architecture Engine")
        st.info("Upload reference swipe slide to extract mood, palette, and structural styling.")
        
        uploaded_slide = st.file_uploader("Upload Inspiration Swipe Slide", type=["png", "jpg", "jpeg"], key="sia_router_upload")
        
        hex_top, hex_center = "#111827", "#1f2937"
        equivalent_card = None

        if uploaded_slide is not None:
            original_image = Image.open(uploaded_slide).convert("RGB")
            w, h = original_image.size
            
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
        st.subheader("🚀 Render Batch Deck Preview")
        
        if st.button("Compile & Render All Slides", key="render_template_layout_btn"):
            visual_spec = {
                "asset_mode": "template_architecture",
                "layout_archetype": "Smart Equivalent Synthesizer",
                "primary_color": hex_top,
                "design_style": "Pristine Brand Equivalent",
                "palette": [hex_top, hex_center, "#FFFFFF"],
                "typography": "Modern Clean",
                "visual_mood": "Professional High-Converting"
            }
            st.session_state["visual_brief"] = visual_spec
            st.session_state["visual_approved"] = True
            st.success("Template architecture and content stream successfully compiled!")

        if "render_universal_canvas" in globals() and st.session_state.get("visual_approved"):
            render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)