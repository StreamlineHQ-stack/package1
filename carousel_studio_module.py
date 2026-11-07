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

    draw.text((width - 320, height - 100), "Nikki's Salon • ApexMorph", fill=body_color, font=footer_font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def render_carousel_studio():
    # --- KINETIC UI WORKSPACE HANDLER ---
    if st.session_state.get("active_view") == "kinetic_ui":
        st.markdown("<h1 style='text-align: center;'>🧬 Kinetic UI Motion Suite</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>High-performance local motion rendering engine running natively.</p>", unsafe_allow_html=True)
        st.divider()
        
        if st.button("← Back to Carousel Studio", type="secondary", key="cs_back_to_studio"):
            st.session_state["active_view"] = "studio"
            st.rerun()
            
        st.divider()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### ⚙️ Pro Motion Control")
            frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20, key="cs_local_fps")
            seconds_per_slide = st.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25, key="cs_local_sps")
            transition_style = st.selectbox(
                "Kinetic Transition Style:",
                [
                    "Dynamic Slide Up (Pro Easing)",
                    "Smooth Slide Right",
                    "Cinematic Zoom In",
                    "Fade & Snap",
                ],
                key="cs_local_transition"
            )
            transition_speed = st.slider("Transition Speed (Frames):", 2, 15, 6, key="cs_local_trans_speed")

        slides_to_render = st.session_state.get("slides_data", [])
        if not slides_to_render:
            slides_to_render = st.session_state.get("deck_json", [])

        st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")
        
        col_seq, col_eng = st.columns([1.2, 1.4])
        with col_seq:
            st.markdown("### Slide Sequence Overview")
            if slides_to_render:
                for idx, slide in enumerate(slides_to_render, start=1):
                    title_text = slide.get("title", f"Slide {idx}") if isinstance(slide, dict) else str(slide)
                    st.markdown(f"**Slide {idx}:** {title_text}")
            else:
                st.info("No active slide deck found. Generate or select a deck first.")

            st.markdown("### Production Render Engine")
            render_btn = st.button("✨ Render Premium Kinetic Loop (Active Deck)", use_container_width=True, key="cs_local_render_btn")

            if render_btn:
                with st.spinner("Rendering animation frames from actual deck cards..."):
                    frames = []
                    for idx, slide in enumerate(slides_to_render, start=1):
                        bg_col = slide.get("bg_color", "#1a1a1a") if isinstance(slide, dict) else "#1a1a1a"
                        png_bytes = render_carousel_slide_to_image(
                            slide_data=slide if isinstance(slide, dict) else {"title": str(slide), "content": ""},
                            slide_num=idx,
                            total_slides=len(slides_to_render),
                            bg_color=bg_col
                        )
                        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
                        frames.append(img)

                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                    st.session_state["cs_last_rendered_gif"] = gif_buffer.getvalue()

                    mp4_bytes = None
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

                        mp4_path = "temp_kinetic_deck_cs.mp4"
                        imageio.mimwrite(
                            mp4_path,
                            paced_frames,
                            fps=fps,
                            codec="libx264",
                            pixelformat="yuv420p",
                            output_params=['-crf', '10', '-preset', 'slow']
                        )
                        with open(mp4_path, "rb") as mf:
                            mp4_bytes = mf.read()
                        os.remove(mp4_path)
                        st.session_state["cs_last_rendered_mp4"] = mp4_bytes
                    except Exception:
                        st.session_state["cs_last_rendered_mp4"] = None
                    
                st.success("🎉 Kinetic Loop rendered successfully from your actual deck cards!")

            if "cs_last_rendered_mp4" in st.session_state and st.session_state["cs_last_rendered_mp4"]:
                st.markdown("---")
                st.markdown("#### 👁️ Live Loop Preview")
                mp4_bytes = st.session_state["cs_last_rendered_mp4"]
                b64_mp4 = base64.b64encode(mp4_bytes).decode("utf-8")
                st.markdown(
                    f'<div style="width: 100%; display: flex; justify-content: center; background: #000; padding: 10px; border-radius: 12px; border: 2px solid #ffcc00; box-sizing: border-box; margin-bottom: 20px;">'
                    f'<video width="100%" autoplay loop muted playsinline style="border-radius: 8px; display: block; max-width: 280px; height: auto;">'
                    f'<source src="data:video/mp4;base64,{b64_mp4}" type="video/mp4">'
                    f'Your browser does not support the video tag.'
                    f'</video>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                st.markdown("#### 📥 Download Package")
                if "cs_last_rendered_gif" in st.session_state:
                    st.download_button(
                        label="⬇️ Download Animated GIF",
                        data=st.session_state["cs_last_rendered_gif"],
                        file_name="carousel_kinetic_loop.gif",
                        mime="image/gif",
                        use_container_width=True,
                        key="cs_dl_gif"
                    )
                st.download_button(
                    label="🎬 Download MP4 Video (Instagram Feed / Reels)",
                    data=mp4_bytes,
                    file_name="carousel_kinetic_loop.mp4",
                    mime="video/mp4",
                    use_container_width=True,
                    key="cs_dl_mp4"
                )
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
            raw_text = f"Hook: {hook_input}\nProblem: {problem_input}\nSolution: {solution_input}\nCTA: {cta_input}"
            with st.spinner("Building direct-response carousel deck..."):
                st.session_state["deck_json"] = None
                res, status_msg = generate_carousel_deck(raw_text, slide_count=slide_count, mode="framework")
                st.session_state["deck_json"] = res
                st.session_state["engine_status"] = status_msg
                st.session_state["current_slide"] = 0
                st.rerun()

    if st.session_state.get("engine_status"):
        st.success(f"Status: {st.session_state['engine_status']}")

    # --- SLIDE PREVIEW & EDIT SUITE ---
    if st.session_state.get("deck_json"):
        st.divider()
        deck_data = st.session_state["deck_json"]
        slides = []
        try:
            if isinstance(deck_data, str):
                slides = json.loads(deck_data)
            elif isinstance(deck_data, list):
                slides = deck_data
        except Exception:
            slides = []
            
        total_slides = len(slides)
        if total_slides > 0:
            if "current_slide" not in st.session_state:
                st.session_state["current_slide"] = 0
            if st.session_state["current_slide"] >= total_slides:
                st.session_state["current_slide"] = 0

            col_prev, col_status, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("← Previous", use_container_width=True, key="cs_prev_slide"):
                    if st.session_state["current_slide"] > 0:
                        st.session_state["current_slide"] -= 1
                        st.rerun()
            with col_status:
                st.markdown(f"<h4 style='text-align: center;'>Slide {st.session_state['current_slide'] + 1} of {total_slides}</h4>", unsafe_allow_html=True)
            with col_next:
                if st.button("Next →", use_container_width=True, key="cs_next_slide"):
                    if st.session_state["current_slide"] < total_slides - 1:
                        st.session_state["current_slide"] += 1
                        st.rerun()
                    
            current_idx = st.session_state["current_slide"]
            display_slide_num = current_idx + 1
            slide = slides[current_idx]
            
            tag = str(slide.get("category", f"STEP {display_slide_num}")).upper()
            title = slide.get("title", f"Slide {display_slide_num}")
            body = slide.get("content", "")
            
            # Theme color mapping
            if style_theme == "Custom" and custom_colors:
                bg_color, text_color, body_color, tag_color, border_style = custom_colors["bg"], custom_colors["text"], custom_colors["body"], custom_colors["tag"], custom_colors["border"]
            elif style_theme == "High-Contrast Canary":
                bg_color, text_color, body_color, tag_color, border_style = "#0a0a0a", "#ffffff", "#e5e7eb", "#ffcc00", "1px solid #222222"
            elif style_theme == "Warning Red Alert":
                bg_color, text_color, body_color, tag_color, border_style = "#181212", "#ffffff", "#e5cdc5", "#ef4444", "1px solid #3d2222"
            elif style_theme == "Minimalist Clean":
                bg_color, text_color, body_color, tag_color, border_style = "#ffffff", "#111111", "#444444", "#0066cc", "1px solid #e0e0e0"
            elif style_theme == "Warm Editorial":
                bg_color, text_color, body_color, tag_color, border_style = "#fbf9f5", "#2c221e", "#5c4e47", "#a85732", "1px solid #e6dfd3"
            elif style_theme == "Neon Cyber/Tech":
                bg_color, text_color, body_color, tag_color, border_style = "#0b0f19", "#f8fafc", "#94a3b8", "#06b6d4", "1px solid #1e293b"
            elif style_theme == "Midnight Luxury":
                bg_color, text_color, body_color, tag_color, border_style = "#121212", "#f5e6c8", "#d4c5a9", "#d4af37", "1px solid #2a2415"
            elif style_theme == "Emerald Growth":
                bg_color, text_color, body_color, tag_color, border_style = "#0a1f1c", "#e6f4f1", "#a3cbd0", "#10b981", "1px solid #133e38"
            elif style_theme == "Nordic Slate":
                bg_color, text_color, body_color, tag_color, border_style = "#1e242b", "#f1f5f9", "#cbd5e1", "#38bdf8", "1px solid #334155"
            elif style_theme == "Bold Coral Pop":
                bg_color, text_color, body_color, tag_color, border_style = "#231818", "#fff0ed", "#e2c4be", "#ff6b6b", "1px solid #422929"
            elif style_theme == "Monochrome Obsidian":
                bg_color, text_color, body_color, tag_color, border_style = "#000000", "#ffffff", "#a3a3a3", "#ffffff", "1px solid #262626"
            else:
                bg_color, text_color, body_color, tag_color, border_style = "#a85732", "#ffffff", "#e5e7eb", "#ffcc00", "none"

            # Inject bg_color into slide dictionaries so Animator reads them correctly
            for s in slides:
                if isinstance(s, dict):
                    s["bg_color"] = bg_color

            is_opening = (current_idx == 0)
            is_final = (current_idx == total_slides - 1)
            watermark_html = ""
            
            if is_discount_tier:
                if is_opening or is_final:
                    b_name = brand_handle or "Apex Morph"
                    watermark_html = f'<span style="color: {body_color}; font-size: 11px; opacity: 0.8; font-weight: 600;">{b_name} • ⚡ Carousel Engine</span>'
                else:
                    watermark_html = f'<span style="color: {body_color}; font-size: 11px; opacity: 0.7;">{brand_handle or "Apex Morph"}</span>'
            else:
                if watermark_type == "Text Handle" and brand_handle:
                    watermark_html = f'<span style="color: {body_color}; font-size: 11px; opacity: 0.7;">{brand_handle}</span>'
                elif watermark_type == "Logo Image" and logo_file is not None and logo_base64:
                    watermark_html = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 25px; object-fit: contain;" />'

            if selected_november_bg_url:
                css_bg = f"background: linear-gradient(rgba(15, 10, 5, 0.82), rgba(25, 15, 8, 0.88)), url('{selected_november_bg_url}'); background-size: cover; background-position: center;"
            else:
                css_bg = f"background-color: {bg_color};"

            st.markdown(
                f"""
                <div style="
                    {css_bg}
                    color: {text_color};
                    padding: 40px;
                    border-radius: 16px;
                    min-height: 280px;
                    border: {border_style};
                    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                    font-family: 'Inter', sans-serif;
                    margin-top: 15px;
                    margin-bottom: 25px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                ">
                    <div>
                        <p style="color: {tag_color}; font-weight: 800; font-size: 13px; letter-spacing: 1.5px; margin-bottom: 15px;">SLIDE {display_slide_num} • {tag}</p>
                        <h2 style="color: {text_color}; font-size: 26px; font-weight: 700; margin-bottom: 15px; line-height: 1.3;">{title}</h2>
                        <p style="color: {body_color}; font-size: 16px; line-height: 1.6;">{body}</p>
                    </div>
                    <div style="text-align: right; margin-top: 20px;">
                        {watermark_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            with st.expander(f"✏️ Edit Slide {display_slide_num} Content"):
                new_tag = st.text_input("Slide Category/Tag:", value=tag, key=f"cs_tag_{current_idx}")
                new_title = st.text_input("Slide Title:", value=title, key=f"cs_title_{current_idx}")
                new_body = st.text_area("Slide Body Content:", value=body, key=f"cs_body_{current_idx}")
                if isinstance(slides[current_idx], dict):
                    slides[current_idx]["category"] = new_tag
                    slides[current_idx]["title"] = new_title
                    slides[current_idx]["content"] = new_body

            st.markdown("### ⚡ Kinetic Data Bridge & Export")
            
            col_bridge_btn, col_zip_btn, col_download_btn = st.columns(3)
            
            with col_bridge_btn:
                if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="cs_open_local_kinetic"):
                    st.session_state["slides_data"] = slides
                    st.session_state["active_view"] = "kinetic_ui"
                    st.rerun()

            with col_zip_btn:
                if st.button("📦 Download Images (.zip)", type="primary", use_container_width=True, key="cs_gen_zip_imgs"):
                    with st.spinner("Rendering high-res Instagram PNG slide images into ZIP archive..."):
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                            for idx, s in enumerate(slides):
                                img_bytes = render_carousel_slide_to_image(
                                    slide_data=s,
                                    slide_num=idx + 1,
                                    total_slides=total_slides,
                                    bg_color=bg_color,
                                    text_color=text_color,
                                    body_color=body_color,
                                    tag_color=tag_color
                                )
                                zip_file.writestr(f"carousel_slide_{idx+1}.png", img_bytes)
                        zip_buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Click Here to Download .zip Archive",
                            data=zip_buffer,
                            file_name="instagram_carousel_images.zip",
                            mime="application/zip",
                            use_container_width=True,
                            key="cs_actual_download_btn"
                        )
            
            with col_download_btn:
                st.download_button(
                    "📥 Download JSON File", 
                    data=json.dumps(slides, indent=2), 
                    file_name="carousel_deck_kinetic.json", 
                    mime="application/json", 
                    use_container_width=True,
                    key="cs_download_json"
                )
