import streamlit as st
import json
import base64
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY  # Modular 100-template library data import
from license_verifier import verify_license_sidebar  # Secure license key verification module

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Minimalist Carousel Engine",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LICENSE KEY VERIFICATION ---
is_licensed = verify_license_sidebar()

# If you want to block the app until they enter a valid key, keep this check:
if not is_licensed:
    st.stop()  # Halts execution here until a valid license key is entered

# --- INITIALIZE SESSION STATE ---
if "deck_json" not in st.session_state:
    st.session_state["deck_json"] = None
if "current_slide" not in st.session_state:
    st.session_state["current_slide"] = 0

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🎨 Visual Layout Styles")
    
    # Theme Mode Selection (Presets vs Custom Hex Picker)
    theme_mode = st.radio("Styling Mode:", ["Preset Themes", "Custom Brand Hex"])
    
    if theme_mode == "Preset Themes":
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
        
        selected_theme_label = st.selectbox(
            "Choose Visual Design Theme:",
            list(theme_options.values())
        )
        style_theme = [k for k, v in theme_options.items() if v == selected_theme_label][0]
        custom_colors = None
    else:
        st.subheader("🎨 Custom Brand Colors")
        custom_bg = st.color_picker("Background Color", "#0e1117")
        custom_text = st.color_picker("Main Text Color", "#ffffff")
        custom_body = st.color_picker("Body Text Color", "#b0c4de")
        custom_tag = st.color_picker("Accent / Tag Color", "#ff4b4b")
        custom_border = st.text_input("Border Style (CSS)", "1px solid #30363d")
        
        custom_colors = {
            "bg": custom_bg,
            "text": custom_text,
            "body": custom_body,
            "tag": custom_tag,
            "border": custom_border
        }
        style_theme = "Custom"

    st.divider()
    st.subheader("🏷️ Brand Watermark Options")
    watermark_type = st.radio("Watermark Type:", ["Text Handle", "Logo Image"])
    
    logo_file = None
    logo_base64 = ""
    brand_handle = ""
    
    if watermark_type == "Text Handle":
        brand_handle = st.text_input("Brand Handle / Text:", "@nikki.coachpages")
    else:
        logo_file = st.file_uploader("Upload Brand Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if logo_file is not None:
            logo_bytes = logo_file.getvalue()
            logo_base64 = base64.b64encode(logo_bytes).decode()

    st.divider()
    st.subheader("⚙️ Deck Settings")
    slide_count = st.slider("Number of Slides:", min_value=4, max_value=10, value=6)
    
    st.info("🚀 *Production Ready:* Lean, High-Performance Mode.")

# --- MAIN HEADER ---
st.markdown("<h1 style='text-align: center;'>✨ Minimalist Carousel Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks.</p>", unsafe_allow_html=True)

# --- TABS FOR GENERATION MODES ---
tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🛠️ Guided Framework Wizard"])

# TAB 1: AUTO-PILOT
with tab1:
    st.markdown("### ⚡ AI Auto-Pilot")
    topic_prompt = st.text_input("Enter your core topic or audience pain point:", "High-converting landing page optimization for online coaches")
    
    if st.button("Generate Auto-Pilot Carousel", type="primary"):
        with st.spinner("Crafting direct-response carousel deck..."):
            res = generate_carousel_deck(topic_prompt, slide_count=slide_count, mode="autopilot")
            st.session_state["deck_json"] = res
            st.session_state["current_slide"] = 0
            st.rerun()

# TAB 2: BRAIN DUMP / CUSTOM NOTES
with tab2:
    st.markdown("### 📝 Custom Expert Notes")
    custom_notes = st.text_area(
        "Paste your unstructured notes or raw coaching insights:",
        height=150,
        value="Hook Element: 73% of prospects leave your offer page without buying. Here is why.\nProblem/Agitation: Friction points and vague copy force users to think too hard.\nSolution/Steps: Audit your top-of-fold message, CTA clarity, and page speed.\nCall to Action: Comment 'AUDIT' to grab the full landing page checklist."
    )
    
    if st.button("Format Custom Notes", type="primary"):
        with st.spinner("Structuring raw notes into slides..."):
            res = generate_carousel_deck(custom_notes, slide_count=slide_count, mode="custom")
            st.session_state["deck_json"] = res
            st.session_state["current_slide"] = 0
            st.rerun()

# TAB 3: GUIDED FRAMEWORK WIZARD
with tab3:
    st.markdown("### 🎯 Direct-Response Framework Builder (100 Blueprints Included)")
    
    col_pillar, col_template = st.columns(2)
    with col_pillar:
        selected_pillar = st.selectbox("Choose Content Pillar:", list(FRAMEWORK_LIBRARY.keys()))
    
    templates_in_pillar = FRAMEWORK_LIBRARY[selected_pillar]
    with col_template:
        selected_template_name = st.selectbox("Choose Direct-Response Blueprint:", list(templates_in_pillar.keys()))
    
    template_data = templates_in_pillar[selected_template_name]
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        hook_input = st.text_input("1. Hook / Core Headline", value=template_data["hook"])
        problem_input = st.text_input("2. Core Problem / Pain", value=template_data["problem"])
    with col2:
        solution_input = st.text_input("3. Solution / System Steps", value=template_data["solution"])
        cta_input = st.text_input("4. Call to Action (CTA)", value=template_data["cta"])
        
    if st.button("Format Framework Carousel", type="primary"):
        raw_framework_text = f"Hook Element: {hook_input}\nProblem/Agitation: {problem_input}\nSolution/Steps: {solution_input}\nCall to Action: {cta_input}"
        
        with st.spinner("Building direct-response carousel deck..."):
            res = generate_carousel_deck(raw_framework_text, slide_count=slide_count, mode="framework")
            st.session_state["deck_json"] = res
            st.session_state["current_slide"] = 0
            st.rerun()

# --- CAROUSEL RENDERER & SLIDE VIEWER (STRICTLY SYNCHRONIZED) ---
if st.session_state["deck_json"]:
    st.divider()
    deck_data = st.session_state["deck_json"]
    
    # Defensive slide extraction
    slides = []
    if isinstance(deck_data, dict):
        slides = deck_data.get("slides", [])
    elif isinstance(deck_data, str):
        try:
            parsed = json.loads(deck_data)
            if isinstance(parsed, dict):
                slides = parsed.get("slides", [])
            elif isinstance(parsed, list):
                slides = parsed
        except Exception:
            slides = []
    elif isinstance(deck_data, list):
        slides = deck_data
        
    total_slides = len(slides)
    
    if total_slides > 0:
        if st.session_state["current_slide"] >= total_slides:
            st.session_state["current_slide"] = total_slides - 1

        # Navigation controls with explicit st.rerun()
        col_prev, col_status, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.button("← Previous", use_container_width=True):
                if st.session_state["current_slide"] > 0:
                    st.session_state["current_slide"] -= 1
                    st.rerun()
                
        with col_status:
            st.markdown(f"<h4 style='text-align: center;'>Slide {st.session_state['current_slide'] + 1} of {total_slides}</h4>", unsafe_allow_html=True)
            
        with col_next:
            if st.button("Next →", use_container_width=True):
                if st.session_state["current_slide"] < total_slides - 1:
                    st.session_state["current_slide"] += 1
                    st.rerun()
                
        # SINGLE SOURCE OF TRUTH FOR INDEXING
        current_idx = st.session_state["current_slide"]
        display_slide_num = current_idx + 1
        slide = slides[current_idx]
        
        # Robust tag, title, and body extraction
        if isinstance(slide, dict):
            raw_tag = slide.get("tag") or slide.get("category") or slide.get("type")
            if not raw_tag or raw_tag.upper() == "SLIDE":
                if current_idx == 0:
                    raw_tag = "HOOK"
                elif current_idx == total_slides - 1:
                    raw_tag = "CTA"
                else:
                    raw_tag = f"STEP {current_idx}"
            tag = str(raw_tag).upper()
            title = slide.get("title") or slide.get("headline") or ""
            body = slide.get("body") or slide.get("content") or ""
        else:
            tag = f"STEP {display_slide_num}"
            title = str(slide)
            body = ""
        
        # --- EXPANDED VISUAL THEME & CUSTOM HEX STYLING ENGINE ---
        if style_theme == "Custom" and custom_colors:
            bg_color = custom_colors["bg"]
            text_color = custom_colors["text"]
            body_color = custom_colors["body"]
            tag_color = custom_colors["tag"]
            border_style = custom_colors["border"]
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
        else: # High-Contrast Canary
            bg_color, text_color, body_color, tag_color, border_style = "#1a1a1a", "#ffffff", "#d1d1d1", "#ffcc00", "none"

        # Dynamically build watermark HTML (Text or Logo Image)
        watermark_html = ""
        if watermark_type == "Text Handle" and brand_handle:
            watermark_html = f'<span style="color: {body_color}; font-size: 11px; opacity: 0.7; letter-spacing: 1px;">{brand_handle}</span>'
        elif watermark_type == "Logo Image" and logo_file is not None and logo_base64:
            watermark_html = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 25px; object-fit: contain;" />'

        # Render Slide Preview Box with Flexible Watermark
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
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
        
        # Slide Content Editor
        with st.expander(f"✏️ Edit Slide {display_slide_num} Content"):
            new_tag = st.text_input("Slide Category/Tag:", value=tag, key=f"tag_{current_idx}")
            new_title = st.text_input("Slide Title:", value=title, key=f"title_{current_idx}")
            new_body = st.text_area("Slide Body Content:", value=body, key=f"body_{current_idx}")
            
            if isinstance(slides[current_idx], dict):
                slides[current_idx]["tag"] = new_tag
                slides[current_idx]["title"] = new_title
                slides[current_idx]["body"] = new_body

        # --- EXPORT & DOWNLOAD SUITE ---
        st.subheader("📥 Export & Download Deck")
        
        # 1. Build Markdown Export String
        markdown_output = f"# Creator Studio Carousel Deck\n\n"
        for idx, s in enumerate(slides):
            if isinstance(s, dict):
                s_tag = str(s.get("tag", f"SLIDE {idx+1}")).upper()
                s_title = s.get("title", "")
                s_body = s.get("body", "")
            else:
                s_tag = f"SLIDE {idx+1}"
                s_title = str(s)
                s_body = ""
            markdown_output += f"### Slide {idx+1} • {s_tag}\n**{s_title}**\n\n{s_body}\n\n---\n\n"
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download as Markdown (.md)",
                data=markdown_output,
                file_name="carousel_deck.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_dl2:
            json_output = json.dumps(slides, indent=2)
            st.download_button(
                label="📥 Download as JSON (.json)",
                data=json_output,
                file_name="carousel_deck.json",
                mime="application/json",
                use_container_width=True
            )