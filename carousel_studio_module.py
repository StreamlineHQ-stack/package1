# carousel_studio_module.py • Complete Standalone Carousel Studio Feature Suite
import json
import base64
import io
import os
import zipfile
import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

try:
    from templates.november import NOVEMBER_FRAMEWORK_LIBRARY, NOVEMBER_VISUAL_TEMPLATES
except Exception:
    NOVEMBER_FRAMEWORK_LIBRARY = {}
    NOVEMBER_VISUAL_TEMPLATES = {}

def wrap_text_to_width(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def render_carousel_slide_to_image(slide_data, slide_num, total_slides, bg_color="#1a1a1a", text_color="#ffffff", body_color="#d1d1d1", tag_color="#ffcc00"):
    width, height = 1080, 1080
    max_text_width = 880
    
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        badge_font = ImageFont.truetype("arialbd.ttf", 28)
        title_font = ImageFont.truetype("arialbd.ttf", 52)
        body_font = ImageFont.truetype("arialbd.ttf", 36)
        footer_font = ImageFont.truetype("arialbd.ttf", 24)
    except IOError:
        badge_font = title_font = body_font = footer_font = ImageFont.load_default()

    category = str(slide_data.get("category", f"SLIDE {slide_num}")).upper()
    title = str(slide_data.get("title", f"Slide {slide_num}"))
    body = str(slide_data.get("content", ""))

    margin_x, current_y = 100, 160

    draw.text((margin_x, current_y), f"SLIDE {slide_num} OF {total_slides} • {category}", fill=tag_color, font=badge_font)
    current_y += 70

    for line in wrap_text_to_width(title, title_font, max_text_width, draw):
        draw.text((margin_x, current_y), line, fill=text_color, font=title_font)
        current_y += 65

    current_y += 30
    if body:
        for line in wrap_text_to_width(body, body_font, max_text_width, draw):
            draw.text((margin_x, current_y), line, fill=body_color, font=body_font)
            current_y += 48

    draw.text((width - 380, height - 100), "Nikki's Salon • ApexMorph", fill=body_color, font=footer_font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def render_carousel_studio():
    # --- Check for Kinetic UI Dedicated View Mode (Local Native Bridge) ---
    if st.session_state.get("active_view") == "kinetic_ui":
        st.markdown("<h1 style='text-align: center;'>🧬 Kinetic UI Workspace (Local Suite)</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>High-performance local motion rendering engine running natively inside Carousel Studio.</p>", unsafe_allow_html=True)
        st.divider()
        
        if st.button("← Back to Carousel Studio", type="secondary", key="cs_back_to_studio"):
            st.session_state["active_view"] = "studio"
            st.rerun()
            
        st.divider()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### ⚙️ Pro Motion Control")
            frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20, key="local_fps")
            seconds_per_slide = st.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25, key="local_sps")

        slides_to_render = st.session_state.get("slides_data", [])
        if not slides_to_render:
            try:
                deck_param = st.query_params.get("deck", None)
                if deck_param:
                    if isinstance(deck_param, list):
                        encoded_deck = deck_param[0]
                    else:
                        encoded_deck = deck_param
                    padded_deck = encoded_deck + "=" * (-len(encoded_deck) % 4)
                    decoded_bytes = base64.urlsafe_b64decode(padded_deck.encode("utf-8"))
                    slides_to_render = json.loads(decoded_bytes.decode("utf-8"))
            except Exception:
                pass

        if not slides_to_render and "deck_json" in st.session_state and st.session_state["deck_json"]:
            deck_data = st.session_state["deck_json"]
            if isinstance(deck_data, str):
                try:
                    slides_to_render = json.loads(deck_data)
                except Exception:
                    slides_to_render = []
            else:
                slides_to_render = deck_data

        st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")
        
        col_seq, col_eng = st.columns([1.2, 1])
        with col_seq:
            st.markdown("### Slide Sequence Overview")
            if slides_to_render:
                for idx, slide in enumerate(slides_to_render, start=1):
                    title_text = slide.get("title", f"Slide {idx}") if isinstance(slide, dict) else str(slide)
                    st.markdown(f"**Slide {idx}:** {title_text}")
            else:
                st.info("No active slides found. Generate a carousel first.")

        with col_eng:
            st.markdown("### Production Render Engine")
            if st.button("✨ Render Premium Kinetic Loop (Active Deck)", use_container_width=True, key="local_render_btn"):
                with st.spinner("Rendering animation frames honoring active theme & background..."):
                    frames = []
                    width, height = 1080, 1080
                    max_text_width = 880

                    active_bg_color = st.session_state.get("active_bg_color", "#1a1a1a")
                    bg_img = Image.new("RGB", (width, height), color=active_bg_color)

                    try:
                        badge_font = ImageFont.truetype("arialbd.ttf", 28)
                        title_font = ImageFont.truetype("arialbd.ttf", 52)
                        body_font = ImageFont.truetype("arialbd.ttf", 36)
                        footer_font = ImageFont.truetype("arialbd.ttf", 24)
                    except IOError:
                        badge_font = title_font = body_font = footer_font = ImageFont.load_default()

                    total_slides_render = len(slides_to_render)
                    for idx, slide in enumerate(slides_to_render, start=1):
                        category = str(slide.get("category", f"STEP {idx}")).upper() if isinstance(slide, dict) else f"STEP {idx}"
                        title = str(slide.get("title", f"Slide {idx}")) if isinstance(slide, dict) else str(slide)
                        body = str(slide.get("content", "")) if isinstance(slide, dict) else ""

                        img = bg_img.copy()
                        draw = ImageDraw.Draw(img)
                        margin_x, current_y = 100, 160

                        draw.text((margin_x, current_y), f"SLIDE {idx} OF {total_slides_render} • {category}", fill="#ffcc00", font=badge_font)
                        current_y += 70

                        for line in wrap_text_to_width(title, title_font, max_text_width, draw):
                            draw.text((margin_x, current_y), line, fill="#ffffff", font=title_font)
                            current_y += 65

                        current_y += 30
                        if body:
                            for line in wrap_text_to_width(body, body_font, max_text_width, draw):
                                draw.text((margin_x, current_y), line, fill="#d1d1d1", font=body_font)
                                current_y += 48

                        draw.text((width - 380, height - 100), "Nikki's Salon • ApexMorph", fill="#d1d1d1", font=footer_font)
                        frames.append(img)

                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                    gif_bytes = gif_buffer.getvalue()

                    mp4_bytes = None
                    mp4_error = None
                    try:
                        import imageio
                        import numpy as np

                        fps = int(frame_rate)
                        frames_per_slide = int(fps * seconds_per_slide)

                        paced_frames = []
                        for f in frames:
                            np_f = np.array(f)
                            for _ in range(frames_per_slide):
                                paced_frames.append(np_f)

                        mp4_path = "temp_kinetic_deck_local.mp4"
                        imageio.mimwrite(
                            mp4_path,
                            paced_frames,
                            fps=fps,
                            codec="libx264",
                            quality=8,
                            pixelformat="yuv420p",
                        )
                        with open(mp4_path, "rb") as mf:
                            mp4_bytes = mf.read()
                        os.remove(mp4_path)
                    except Exception as ex:
                        mp4_bytes = None
                        mp4_error = str(ex)
                    
                st.success("🎉 Kinetic Loop rendered successfully!")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="⬇️ Download Animated GIF", 
                        data=gif_bytes, 
                        file_name="kinetic_carousel_loop.gif", 
                        mime="image/gif", 
                        use_container_width=True, 
                        key="local_dl_gif"
                    )
                with col_d2:
                    if mp4_bytes:
                        st.download_button(
                            label="🎬 Download Instagram MP4",
                            data=mp4_bytes,
                            file_name="kinetic_carousel_loop.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                            key="local_dl_mp4"
                        )
                    else:
                        st.warning(f"⚠️ MP4 Export unavailable: {mp4_error}")
        return

    # --- SIDEBAR CONTROLS FOR CAROUSEL STUDIO ---
    with st.sidebar:
        st.title("🎨 Visual Layout Styles")
        
        november_unlocked = st.session_state.get('november_unlocked', True)
        vault_options = ["Standard Preset Themes", "Custom Brand Hex"]
        if november_unlocked:
            vault_options.insert(0, "📦 November Content Vault (Active)")
            
        engine_mode = st.radio("Select Styling Mode:", vault_options, key="cs_engine_mode")
        
        style_theme = "High-Contrast Canary"
        custom_colors = None
        selected_november_bg_url = ""
        
        if "November Content Vault" in engine_mode:
            st.success("🍁 November Fall Pack Active!")
            if NOVEMBER_VISUAL_TEMPLATES:
                selected_bg_name = st.selectbox("Choose Fall Background Texture:", list(NOVEMBER_VISUAL_TEMPLATES.keys()), key="cs_nov_bg")
                selected_november_bg_url = NOVEMBER_VISUAL_TEMPLATES[selected_bg_name]
            else:
                selected_november_bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80"
        elif engine_mode == "Standard Preset Themes":
            theme_options = {
                "High-Contrast Canary": "⚡ High-Contrast Canary (Black & Yellow)",
                "Warning Red Alert": "🚨 Warning Red Alert (Charcoal & Crimson)",
                "Minimalist Clean": "💎 Minimalist Clean (White & Charcoal)",
                "Warm Editorial": "☕ Warm Editorial (Cream & Terracotta)",
                "Neon Cyber/Tech": "⚡ Neon Cyber/Tech (Obsidian & Cyan)",
                "Midnight Luxury": "👑 Midnight Luxury (Dark Obsidian & Gold)",
                "Emerald Growth": "📈 Emerald Growth (Deep Forest & Mint)",
                "Nordic Slate": "❄️ Nordic Slate (Slate Grey & Soft Ice Blue)",
                "Bold Coral Pop": "🔥 Bold Coral Pop (Dark Coral & Warm Cream)",
                "Monochrome Obsidian": "🖤 Monochrome Obsidian (Pure Dark & Crisp White)"
            }
            selected_theme_label = st.selectbox("Choose Visual Design Theme:", list(theme_options.values()), key="cs_theme_select")
            style_theme = [k for k, v in theme_options.items() if v == selected_theme_label][0]
        else:
            st.subheader("🎨 Custom Brand Colors")
            custom_bg = st.color_picker("Background Color", "#0e1117", key="cs_c_bg")
            custom_text = st.color_picker("Main Text Color", "#ffffff", key="cs_c_text")
            custom_body = st.color_picker("Body Text Color", "#b0c4de", key="cs_c_body")
            custom_tag = st.color_picker("Accent / Tag Color", "#ff4b4b", key="cs_c_tag")
            custom_border = st.text_input("Border Style (CSS)", "1px solid #30363d", key="cs_c_border")
            
            custom_colors = {
                "bg": custom_bg, "text": custom_text, "body": custom_body,
                "tag": custom_tag, "border": custom_border
            }
            style_theme = "Custom"

        st.divider()
        st.subheader("🔑 Live API Key Override")
        manual_openrouter = st.text_input("Enter OpenRouter API Key:", type="password", key="cs_manual_key")
        if manual_openrouter:
            st.session_state["admin_openrouter_api_key_override"] = manual_openrouter
            st.success("⚡ OpenRouter API Key Overridden!")

        st.divider()
        st.subheader("💰 Pricing & Watermark Tier")
        pricing_tier = st.radio(
            "Select Access Tier:",
            ["🎉 Special Discount Package (Bookend Engine Branding)", "💎 Full Price Unbranded Access"],
            key="cs_pricing_tier"
        )
        
        is_discount_tier = "Special Discount" in pricing_tier
        logo_file = None
        logo_base64 = ""
        brand_handle = ""
        watermark_type = "Text Handle"
        
        if is_discount_tier:
            st.info("💡 **Discount Active:** Bookend engine credit applied.")
            watermark_type = st.radio("Branding Asset Type:", ["Text Handle", "Logo Image"], key="cs_wm_type_disc")
            if watermark_type == "Text Handle":
                brand_handle = st.text_input("Your Brand Name / Salon Name:", "Nikki's Salon", key="cs_brand_handle_disc")
            else:
                logo_file = st.file_uploader("Upload Brand Logo (PNG/JPG)", type=["png", "jpg", "jpeg"], key="cs_logo_disc")
                if logo_file is not None:
                    logo_base64 = base64.b64encode(logo_file.getvalue()).decode()
        else:
            watermark_type = st.radio("Watermark Type:", ["Text Handle", "Logo Image"], key="cs_wm_type_full")
            if watermark_type == "Text Handle":
                brand_handle = st.text_input("Brand Handle / Text:", "@apexmorph", key="cs_brand_handle_full")
            else:
                logo_file = st.file_uploader("Upload Brand Logo (PNG/JPG)", type=["png", "jpg", "jpeg"], key="cs_logo_full")
                if logo_file is not None:
                    logo_base64 = base64.b64encode(logo_file.getvalue()).decode()

        st.divider()
        slide_count = st.slider("Number of Slides:", min_value=4, max_value=10, value=6, key="cs_slide_count_slider")

    ACTIVE_FRAMEWORK_LIBRARY = FRAMEWORK_LIBRARY.copy()
    if november_unlocked and NOVEMBER_FRAMEWORK_LIBRARY:
        ACTIVE_FRAMEWORK_LIBRARY.update(NOVEMBER_FRAMEWORK_LIBRARY)

    # --- MAIN CAROUSEL STUDIO UI ---
    st.markdown("<h1 style='text-align: center;'>✨ Minimalist Carousel Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])

    with tab1:
        st.markdown("### ⚡ AI Auto-Pilot")
        topic_prompt = st.text_input("Enter your core topic or audience pain point:", "Why is time management important", key="cs_autopilot_input")
        if st.button("Generate Auto-Pilot Carousel", type="primary", key="cs_btn_gen_auto"):
            with st.spinner("Crafting direct-response carousel deck..."):
                st.session_state["deck_json"] = None
                res, status_msg = generate_carousel_deck(topic_prompt, slide_count=slide_count, mode="autopilot")
                st.session_state["deck_json"] = res
                st.session_state["engine_status"] = status_msg
                st.session_state["current_slide"] = 0
                st.rerun()

    with tab2:
        st.markdown("### 📝 Custom Expert Notes")
        custom_notes = st.text_area(
            "Paste your unstructured notes:", 
            height=150, 
            value="Hook: Time management is leverage.\nProblem: People waste hours on low-value tasks.\nCTA: Comment TIME to get the planner.", 
            key="cs_custom_notes_input"
        )
        if st.button("Format Custom Notes", type="primary", key="cs_btn_gen_notes"):
            with st.spinner("Structuring raw notes into slides..."):
                st.session_state["deck_json"] = None
                res, status_msg = generate_carousel_deck(custom_notes, slide_count=slide_count, mode="custom")
                st.session_state["deck_json"] = res
                st.session_state["engine_status"] = status_msg
                st.session_state["current_slide"] = 0
                st.rerun()

    with tab3:
        st.markdown("### 🪄 Guided Framework Wizard")
        col_pillar, col_template = st.columns(2)
        with col_pillar:
            selected_pillar = st.selectbox("Choose Content Pillar:", list(ACTIVE_FRAMEWORK_LIBRARY.keys()), key="cs_pillar_select")
        templates_in_pillar = ACTIVE_FRAMEWORK_LIBRARY[selected_pillar]
        with col_template:
            selected_template_name = st.selectbox("Choose Direct-Response Blueprint:", list(templates_in_pillar.keys()), key="cs_template_select")
        
        template_data = templates_in_pillar[selected_template_name]
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            hook_input = st.text_input("1. Hook / Core Headline", value=template_data["hook"], key="cs_hook_in")
            problem_input = st.text_input("2. Core Problem / Pain", value=template_data["problem"], key="cs_prob_in")
        with col2:
            solution_input = st.text_input("3. Solution / System Steps", value=template_data["solution"], key="cs_sol_in")
            cta_input = st.text_input("4. Call to Action (CTA)", value=template_data["cta"], key="cs_cta_in")
            
        if st.button("Format Framework Carousel", type="primary", key="cs_btn_gen_frame"):
            raw_