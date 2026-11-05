# carousel_studio_module.py • Complete Standalone Carousel Studio Feature Suite
import json
import base64
import io
import zipfile
import streamlit as st
from app_engine_2 import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

try:
    from templates.november import NOVEMBER_FRAMEWORK_LIBRARY, NOVEMBER_VISUAL_TEMPLATES
except ImportError:
    NOVEMBER_FRAMEWORK_LIBRARY = {}
    NOVEMBER_VISUAL_TEMPLATES = {}

def render_carousel_studio():
    # --- SIDEBAR CONTROLS FOR CAROUSEL STUDIO ---
    with st.sidebar:
        st.title("🎨 Visual Layout Styles")
        
        november_unlocked = st.session_state.get('november_unlocked', False)
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

    tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🛠️ Guided Framework Wizard"])

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
        st.markdown("### 🎯 Direct-Response Framework Builder")
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
            if st.session_state["current_slide"] >= total_slides:
                st.session_state["current_slide"] = total_slides - 1

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
                bg_color, text_color, body_color, tag_color, border_style = "#1a1a1a", "#ffffff", "#d1d1d1", "#ffcc00", "none"

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

            st.markdown("### 📥 Export & Download Deck")
            st.download_button(
                "⚡ Kinetic Data Bridge (.json)", 
                data=json.dumps(slides, indent=2), 
                file_name="carousel_deck_kinetic.json", 
                mime="application/json", 
                use_container_width=True,
                key="cs_download_json"
            )