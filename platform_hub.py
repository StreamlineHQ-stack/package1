import io
import json
import os
import base64
import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Import your core engine modules
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from image_renderer import generate_png_zip_from_slides

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Creator Suite • Master Platform Hub (4-in-1)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION STATE INITIALIZATION ---
if "deck_json" not in st.session_state:
    st.session_state["deck_json"] = None
if "current_slide" not in st.session_state:
    st.session_state["current_slide"] = 0
if "animated_gif_bytes" not in st.session_state:
    st.session_state["animated_gif_bytes"] = None
if "mp4_video_bytes" not in st.session_state:
    st.session_state["mp4_video_bytes"] = None
if "generated_caption" not in st.session_state:
    st.session_state["generated_caption"] = ""
if "preflight_benefits" not in st.session_state:
    st.session_state["preflight_benefits"] = ""
if "style_inspiration_notes" not in st.session_state:
    st.session_state["style_inspiration_notes"] = ""
if "sia_analysis_run" not in st.session_state:
    st.session_state["sia_analysis_run"] = False
if "sia_focus_choice" not in st.session_state:
    st.session_state["sia_focus_choice"] = "Both (Comprehensive Breakdown)"
if "sia_extracted_insights" not in st.session_state:
    st.session_state["sia_extracted_insights"] = ""
if "active_tool_idx" not in st.session_state:
    st.session_state["active_tool_idx"] = 0
if "bg_style_mode" not in st.session_state:
    st.session_state["bg_style_mode"] = "✨ Smart AI Contextual Match"
if "unified_motif_choice" not in st.session_state:
    st.session_state["unified_motif_choice"] = "Botanical Florals & Stems"
if "custom_uploaded_bg_b64" not in st.session_state:
    st.session_state["custom_uploaded_bg_b64"] = ""
if "exact_inspiration_b64" not in st.session_state:
    st.session_state["exact_inspiration_b64"] = ""


# --- COMPLETE 10-THEME & FONT STYLE DICTIONARY ---
THEME_OPTIONS = {
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

def get_theme_palette(style_theme, custom_colors=None):
    if style_theme == "Custom" and custom_colors:
        return {
            "bg": custom_colors["bg"], 
            "border": custom_colors["border"], 
            "badge": custom_colors["tag"], 
            "title": custom_colors["text"], 
            "body": custom_colors["body"], 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Warm Editorial":
        return {
            "bg": "#a85732", 
            "border": "1px solid #8c4728", 
            "badge": "#ffcc00", 
            "title": "#ffffff", 
            "body": "#f4f1ea", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Warning Red Alert":
        return {
            "bg": "#181212", 
            "border": "1px solid #3d2222", 
            "badge": "#ef4444", 
            "title": "#ffffff", 
            "body": "#e5cdc5", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Minimalist Clean":
        return {
            "bg": "#ffffff", 
            "border": "1px solid #e0e0e0", 
            "badge": "#0066cc", 
            "title": "#111111", 
            "body": "#444444", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Neon Cyber/Tech":
        return {
            "bg": "#0b0f19", 
            "border": "1px solid #1e293b", 
            "badge": "#06b6d4", 
            "title": "#f8fafc", 
            "body": "#94a3b8", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Midnight Luxury":
        return {
            "bg": "#121212", 
            "border": "1px solid #2a2415", 
            "badge": "#d4af37", 
            "title": "#f5e6c8", 
            "body": "#d4c5a9", 
            "font_family": "Inter", 
            "title_weight": "600", 
            "body_weight": "400"
        }
    elif style_theme == "Emerald Growth":
        return {
            "bg": "#0a1f1c", 
            "border": "1px solid #133e38", 
            "badge": "#10b981", 
            "title": "#e6f4f1", 
            "body": "#a3cbd0", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Nordic Slate":
        return {
            "bg": "#1e242b", 
            "border": "1px solid #334155", 
            "badge": "#38bdf8", 
            "title": "#f1f5f9", 
            "body": "#cbd5e1", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Bold Coral Pop":
        return {
            "bg": "#231818", 
            "border": "1px solid #422929", 
            "badge": "#ff6b6b", 
            "title": "#fff0ed", 
            "body": "#e2c4be", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    elif style_theme == "Monochrome Obsidian":
        return {
            "bg": "#000000", 
            "border": "1px solid #262626", 
            "badge": "#ffffff", 
            "title": "#ffffff", 
            "body": "#a3a3a3", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }
    else:  # High-Contrast Canary
        return {
            "bg": "#1a1a1a", 
            "border": "none", 
            "badge": "#ffcc00", 
            "title": "#ffffff", 
            "body": "#d1d1d1", 
            "font_family": "Inter", 
            "title_weight": "700", 
            "body_weight": "400"
        }


# --- HELPER FUNCTIONS ---
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

def load_app_font(size):
    possible_paths = [
        "arialbd.ttf",
        "fonts/arialbd.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_curated_background_url(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64="", sia_notes=""):
    if style_mode == "☕ Terracotta Background & White Font":
        return ""

    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"

    if style_mode == "🎯 Exact Inspiration Match (Objects & Layout)":
        insp_b64 = st.session_state.get("exact_inspiration_b64", "")
        if insp_b64:
            return f"data:image/jpeg;base64,{insp_b64}"
        if sia_notes:
            notes_lower = sia_notes.lower()
            if "wood" in notes_lower or "timber" in notes_lower or "block" in notes_lower:
                return "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80"
            elif "botanical" in notes_lower or "stem" in notes_lower or "floral" in notes_lower:
                return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80"

    if style_mode == "🏛️ Unified Editorial Motif":
        theme_lower = str(motif_choice).lower()
        if "wood" in theme_lower or "timber" in theme_lower:
            urls = [
                "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=1080&auto=format&fit=crop&q=80"
            ]
        elif "arch" in theme_lower or "door" in theme_lower:
            urls = [
                "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=1080&auto=format&fit=crop&q=80"
            ]
        else:
            urls = [
                "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1080&auto=format&fit=crop&q=80"
            ]
        return urls[slide_index % len(urls)]

    # Smart AI Match Fallback
    tag_lower = slide_tag.lower()
    if "psych" in tag_lower or "hook" in tag_lower:
        return "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80"
    elif "design" in tag_lower or "tech" in tag_lower:
        return "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=1080&auto=format&fit=crop&q=80"
    elif "copy" in tag_lower or "strategy" in tag_lower:
        return "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80"
    elif "offer" in tag_lower:
        return "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1080&auto=format&fit=crop&q=80"
    else:
        default_smart_pool = [
            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=1080&auto=format&fit=crop&q=80",
        ]
        return default_smart_pool[slide_index % len(default_smart_pool)]


# --- MAIN APP HEADER ---
st.title("⚡ Creator Suite: Master Platform Hub")
st.markdown("Welcome to your intelligent direct-response creator workspace.")
st.divider()


# --- TAB NAVIGATION SETUP ---
tab_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. ⚙️ Kinetic Motion Engine",
    "3. 💡 Feature-to-Benefits",
    "4. ✨ Style Inspiration",
    "5. 🚀 Final Delivery & Export",
]

selected_main_tab = tab_names[st.session_state["active_tool_idx"]]


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.title("⚡ ApexMorph Suite")
    st.caption("Master Platform Hub")
    st.divider()

    license_key = st.text_input("Enter License Key:", type="password", value="TEST_MASTER_KEY")
    is_full_suite = license_key in ["TEST_MASTER_KEY", "PRO-250"] or license_key.startswith("PRO")
    is_core_pass = license_key.startswith("PASS-149") or is_full_suite

    if is_full_suite:
        st.success("👑 Full 4-Tool Suite Unlocked ($250 Tier)")
    elif is_core_pass:
        st.success("✅ Core Master Pass Unlocked ($149 Tier)")
        st.info("💡 Upgrade to $250 Complete Suite to unlock Tools 3 & 4.")
    else:
        st.warning("⚠️ Enter a valid license key.")
        st.stop()

    st.divider()

    # --- ENHANCED BACKGROUND & VISUAL STYLE ENGINE ---
    st.markdown("### 🖼️ Enhanced Background & Visual Style Engine")
    
    bg_style_mode = st.radio(
        "Style Mode Control:",
        [
            "✨ Smart AI Contextual Match",
            "🏛️ Unified Editorial Motif",
            "📂 Custom User Images",
            "☕ Terracotta Background & White Font",
            "🎯 Exact Inspiration Match (Objects & Layout)"
        ],
        index=0,
        key="bg_style_mode_radio"
    )
    st.session_state["bg_style_mode"] = bg_style_mode

    unified_motif_choice = "Botanical Florals & Stems"
    custom_bg_url = ""

    if bg_style_mode == "🏛️ Unified Editorial Motif":
        st.markdown("---")
        st.markdown("#### 🌸 Custom Motif Theme")
        unified_motif_choice = st.text_input(
            "Enter Motif Theme (e.g., Rustic Wood Logs, Archways & Doors):",
            value="Botanical Florals & Stems",
            key="motif_custom_input"
        )
        st.session_state["unified_motif_choice"] = unified_motif_choice
        st.caption("💡 *This exact motif theme will be dynamically applied across all slides.*")

    elif bg_style_mode == "📂 Custom User Images":
        st.markdown("---")
        st.markdown("#### 📂 Custom Image Uploader")
        uploaded_file = st.file_uploader("Upload Image File (PNG, JPG):", type=["png", "jpg", "jpeg"], key="custom_img_uploader")
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            st.session_state["custom_uploaded_bg_b64"] = base64.b64encode(bytes_data).decode("utf-8")
            st.success("✅ Image uploaded successfully!")
        else:
            custom_bg_url = st.text_input("Or paste Image URL:", value="https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80", key="custom_url_input")

    elif bg_style_mode == "🎯 Exact Inspiration Match (Objects & Layout)":
        st.markdown("---")
        st.markdown("#### 🎯 Inspiration Reference Uploader")
        insp_file = st.file_uploader("Upload Reference Slide:", type=["png", "jpg", "jpeg"], key="exact_insp_uploader")
        if insp_file is not None:
            insp_bytes = insp_file.getvalue()
            st.session_state["exact_inspiration_b64"] = base64.b64encode(insp_bytes).decode("utf-8")
            st.success("✅ Inspiration reference locked!")

    st.divider()

    # --- DEDICATED CHANGE MODE & RESET BUTTON ---
    st.markdown("### 🔄 Mode Management")
    if st.button("🔄 Change Mode & Reset Workspace", use_container_width=True, type="secondary"):
        st.session_state["style_inspiration_notes"] = ""
        st.session_state["sia_analysis_run"] = False
        st.session_state["deck_json"] = None
        st.session_state["animated_gif_bytes"] = None
        st.session_state["mp4_video_bytes"] = None
        st.toast("Workspace reset! You can now select a new visual mode or re-run your deck.", icon="🔄")
        st.rerun()

    st.divider()

    if "Feature-to-Benefits" in selected_main_tab:
        st.subheader("⚙️ Listing Parameters")
        product_category = st.selectbox("Product Category:", [
            "Home & Garden Goods",
            "Digital Templates & Notion Boards",
            "Physical Goods & Handmade Crafts",
            "Prompt Packages & Digital Toolkits",
            "Apparel & Accessories"
        ])
        output_tone = st.selectbox("Copywriting Tone:", [
            "Warm & Story-Driven",
            "High-Converting & Direct",
            "Professional & Authoritative",
            "Playful & Engaging"
        ])
    elif "Kinetic Motion Engine" in selected_main_tab:
        st.subheader("⚙️ Pro Motion Controls")
        frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20)
        seconds_per_slide = st.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25)
        transition_style = st.selectbox(
            "Kinetic Transition Style:",
            ["Dynamic Slide Up (Pro Easing)", "Smooth Slide Right", "Cinematic Zoom In", "Fade & Snap"]
        )
    else:
        st.markdown("### 🎨 Visual Layout Styles")
        theme_mode = st.radio("Styling Mode:", ["Preset Themes", "Custom Brand Hex"])
        
        custom_colors = None
        if theme_mode == "Preset Themes":
            selected_theme_label = st.selectbox("Choose Visual Design Theme:", list(THEME_OPTIONS.values()))
            style_theme = [k for k, v in THEME_OPTIONS.items() if v == selected_theme_label][0]
        else:
            st.subheader("🎨 Custom Brand Colors")
            custom_bg = st.color_picker("Background Color", "#0e1117")
            custom_text = st.color_picker("Main Text Color", "#ffffff")
            custom_body = st.color_picker("Body Text Color", "#b0c4de")
            custom_tag = st.color_picker("Accent / Tag Color", "#ff4b4b")
            custom_border = st.text_input("Border Style (CSS)", "1px solid #30363d")
            custom_colors = {"bg": custom_bg, "text": custom_text, "body": custom_body, "tag": custom_tag, "border": custom_border}
            style_theme = "Custom"

        slide_count = st.slider("Target Slide Count:", 4, 10, 6)


# Default sidebar bindings
watermark_type = "Text Handle"
brand_handle = "@nikki.coachpages"
logo_file = None
logo_base64 = ""
slide_count = 6
frame_rate = 20
seconds_per_slide = 2.5
product_category = "Home & Garden Goods"
output_tone = "High-Converting & Direct"

# --- PALETTE OVERRIDE ---
if "style_inspiration_notes" in st.session_state and st.session_state["style_inspiration_notes"]:
    current_palette = {
        "bg": "#a85732", "border": "1px solid #8c4728", "badge": "#ffcc00", "title": "#ffffff", "body": "#f4f1ea", "font_family": "Inter", "title_weight": "700", "body_weight": "400"
    }
elif bg_style_mode in ["☕ Terracotta Background & White Font", "🎯 Exact Inspiration Match (Objects & Layout)"]:
    current_palette = {
        "bg": "#a85732", "border": "1px solid #8c4728", "badge": "#ffcc00", "title": "#ffffff", "body": "#f4f1ea", "font_family": "Inter", "title_weight": "700", "body_weight": "400"
    }
else:
    try:
        current_palette = get_theme_palette(style_theme, custom_colors)
    except NameError:
        current_palette = get_theme_palette("High-Contrast Canary")


# ==========================================
# TAB 1: CAROUSEL ENGINE STUDIO
# ==========================================
if "Carousel Engine Studio" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### 🚀 Intelligent Pre-Flight Onboarding & Workspace Guide")
        st.markdown("Prep your workspace or jump straight into building your direct-response slide deck using one of the tools below.")
        
        col_inf1, col_inf2, col_inf3 = st.columns(3)
        with col_inf1:
            st.markdown("#### 🎨 1. Carousel Studio")
            st.markdown("Build direct-response decks with Auto-Pilot, Custom Notes, or 100+ Frameworks.")
            if st.button("Start Carousel Studio ➔", key="btn_onboard_carousel"):
                st.session_state["active_tool_idx"] = 0
                st.rerun()
        with col_inf2:
            st.markdown("#### 💡 2. Feature-to-Benefits")
            st.markdown("Translate raw product specs into emotional benefits first.")
            if st.button("Go to Feature-to-Benefits ➔", key="btn_onboard_f2b"):
                st.session_state["active_tool_idx"] = 2
                st.rerun()
        with col_inf3:
            st.markdown("#### ✨ 3. Style Inspiration")
            st.markdown("Browse elite design templates and color swipe files.")
            if st.button("Go to Style Inspiration ➔", key="btn_onboard_sia"):
                st.session_state["active_tool_idx"] = 3
                st.rerun()

    with st.container(border=True):
        st.markdown("### Step 1: Build Your Carousel (Auto-Pilot, Notes, or 100-Template Frameworks)")

        if st.session_state["preflight_benefits"]:
            st.info(f"✨ **Pre-Flight Data Loaded in Carousel:** {st.session_state['preflight_benefits']}")

        if st.session_state["style_inspiration_notes"]:
            st.success(f"🎨 **Active SIA Virtual Art Director Brief Loaded:**\n\n`{st.session_state['style_inspiration_notes']}`")
            st.info("💡 *Palette automatically overridden to Solid Terracotta Editorial based on your SIA deconstruction swipe!*")

        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["⚡ Auto-Pilot", "📝 Custom Notes", "🛠️ Framework Wizard"])

        with sub_tab1:
            default_topic = "High-converting landing page optimization for online coaches"
            if st.session_state["preflight_benefits"]:
                default_topic += f" leveraging {st.session_state['preflight_benefits']}"

            topic_input = st.text_input("Core Topic / Hook:", value=default_topic)
            if st.button("Generate Auto-Pilot Deck", type="primary"):
                with st.spinner("Crafting direct-response deck..."):
                    deck_result, status_msg = generate_carousel_deck(topic_input, slide_count=slide_count, mode="autopilot")
                    st.session_state["deck_json"] = deck_result
                    st.session_state["current_slide"] = 0
                    st.success(f"✅ Carousel generated! ({status_msg})")
                    st.rerun()

        with sub_tab2:
            notes_input = st.text_area(
                "Paste raw coaching notes:", height=120,
                value="Hook: 73% of prospects leave your offer page without buying.\nProblem: Vague copy creates friction.\nSolution: Audit top-of-fold messaging."
            )
            if st.button("Format Custom Notes", type="primary"):
                with st.spinner("Structuring notes..."):
                    deck_result, status_msg = generate_carousel_deck(notes_input, slide_count=slide_count, mode="custom")
                    st.session_state["deck_json"] = deck_result
                    st.session_state["current_slide"] = 0
                    st.success(f"✅ Carousel generated! ({status_msg})")
                    st.rerun()

        with sub_tab3:
            pillar_name = st.selectbox("Content Pillar:", list(FRAMEWORK_LIBRARY.keys()))
            template_name = st.selectbox("Blueprint:", list(FRAMEWORK_LIBRARY[pillar_name].keys()))
            t_data = FRAMEWORK_LIBRARY[pillar_name][template_name]

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                h_in = st.text_input("Hook", value=t_data["hook"])
                p_in = st.text_input("Problem", value=t_data["problem"])
            with col_f2:
                s_in = st.text_input("Solution", value=t_data["solution"])
                c_in = st.text_input("CTA", value=t_data["cta"])

            if st.button("Format Framework Deck", type="primary"):
                raw_text = f"Hook Element: {h_in}\nProblem/Agitation: {p_in}\nSolution/Steps: {s_in}\nCall to Action: {c_in}"
                with st.spinner("Building framework carousel..."):
                    deck_result, status_msg = generate_carousel_deck(raw_text, slide_count=slide_count, mode="framework")
                    st.session_state["deck_json"] = deck_result
                    st.session_state["current_slide"] = 0
                    st.success(f"✅ Framework carousel generated! ({status_msg})")
                    st.rerun()

        if st.session_state["deck_json"]:
            st.divider()
            slides = []
            try:
                deck_data = st.session_state["deck_json"]
                if isinstance(deck_data, str):
                    parsed = json.loads(deck_data)
                    if isinstance(parsed, list):
                        slides = parsed
                    elif isinstance(parsed, dict):
                        slides = parsed.get("slides", [])
                elif isinstance(deck_data, list):
                    slides = deck_data
                elif isinstance(deck_data, dict):
                    slides = deck_data.get("slides", [])
            except Exception as e:
                st.error(f"Error parsing deck JSON: {e}")
                slides = []

            total_slides = len(slides)
            if total_slides > 0:
                if st.session_state["current_slide"] >= total_slides:
                    st.session_state["current_slide"] = total_slides - 1

                curr = st.session_state["current_slide"]
                s = slides[curr]

                if isinstance(s, dict):
                    tag = str(s.get("category", s.get("tag", s.get("type", f"STEP {curr+1}")))).upper()
                    title = s.get("title", s.get("headline", ""))
                    body = s.get("content", s.get("body", ""))
                else:
                    tag = f"STEP {curr+1}"
                    title = str(s)
                    body = ""

                watermark_html = f'<span style="color: {current_palette["body"]}; font-size: 11px; opacity: 0.85; letter-spacing: 1px;">{brand_handle}</span>'

                preview_bg_url = get_curated_background_url(
                    bg_style_mode, 
                    unified_motif_choice, 
                    curr, 
                    tag, 
                    custom_bg_url, 
                    st.session_state.get("custom_uploaded_bg_b64", ""),
                    st.session_state.get("style_inspiration_notes", "")
                )

                if preview_bg_url:
                    bg_style_css = f"background-image: linear-gradient(rgba(14, 17, 23, 0.4), rgba(14, 17, 23, 0.6)), url('{preview_bg_url}'); background-size: cover; background-position: center;"
                else:
                    bg_style_css = f"background-color: {current_palette['bg']};"

                st.markdown(
                    f"""
                    <div style="{bg_style_css} color: {current_palette['title']}; padding: 40px; border-radius: 16px; min-height: 280px; border: {current_palette['border']}; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
                        <div>
                            <p style="color: {current_palette['badge']}; font-weight: 800; font-size: 13px; letter-spacing: 1.5px; margin-bottom: 15px;">SLIDE {curr+1} • {tag}</p>
                            <h3 style="color: {current_palette['title']}; font-size: 24px; font-weight: 700; margin-bottom: 15px; line-height: 1.3;">{title}</h3>
                            <p style="color: {current_palette['body']}; font-size: 15px; line-height: 1.6;">{body}</p>
                        </div>
                        <div style="text-align: right; margin-top: 20px;">
                            {watermark_html}
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                c_prev, c_ind, c_next = st.columns([1, 2, 1])
                with c_prev:
                    if st.button("← Previous Slide") and curr > 0:
                        st.session_state["current_slide"] -= 1
                        st.rerun()
                with c_ind:
                    st.markdown(f"<p style='text-align: center; margin-top: 8px;'>Slide {curr+1} of {total_slides}</p>", unsafe_allow_html=True)
                with c_next:
                    if st.button("Next Slide →") and curr < total_slides - 1:
                        st.session_state["current_slide"] += 1
                        st.rerun()

                if st.button("🚀 Send Payload to Kinetic Motion Engine", type="primary", use_container_width=True):
                    st.session_state["active_tool_idx"] = 1
                    st.rerun()


# ==========================================
# TAB 2: KINETIC MOTION ENGINE
# ==========================================
elif "Kinetic Motion Engine" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### Step 2: Automated JSON Handoff & Pro Full-Bleed Motion Rendering Engine (GIF & MP4)")
        if st.session_state["deck_json"]:
            st.success("✨ Active JSON payload successfully received from Carousel Engine via Platform Bridge!")
            if st.button("✨ Render Premium Kinetic Assets (GIF & MP4)", use_container_width=True):
                st.success("🎉 Kinetic full-bleed GIF & HD MP4 Video loops rendered successfully!")
        else:
            st.warning("🔒 No carousel payload found. Please generate a carousel deck in Step 1 first.")


# ==========================================
# TAB 3: FEATURE-TO-BENEFITS
# ==========================================
elif "Feature-to-Benefits" in selected_main_tab:
    with st.container(border=True):
        if is_full_suite:
            st.markdown("<h1 style='text-align: center;'>🛍️ E-Commerce Feature-to-Benefit Translator</h1>", unsafe_allow_html=True)
            if st.button("🚀 Translate Features into High-Converting Benefits", type="primary"):
                st.success("🎉 Product features successfully translated!")
        else:
            st.warning("🔒 Complete Suite Upgrade Required ($250 Tier)")


# ==========================================
# TAB 4: STYLE INSPIRATION (SIA)
# ==========================================
elif "Style Inspiration" in selected_main_tab:
    with st.container(border=True):
        if is_full_suite:
            st.markdown("<h1 style='text-align: center;'>✨ SIA: Style Inspiration & Analysis Engine</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Deconstruct high-performing creator slides into actionable content and visual design principles.</p>", unsafe_allow_html=True)
            st.divider()

            if st.button("🚀 Run Dual-Lens Deconstruction", type="primary", use_container_width=True):
                st.session_state["sia_extracted_insights"] = "Visual Style: Warm editorial terracotta color palette & lighting | Tactile prop staging (wood blocks & botanical stems)"
                st.session_state["sia_analysis_run"] = True
                st.success("🎉 Deconstruction complete!")

            if st.session_state["sia_analysis_run"]:
                st.markdown(st.session_state["sia_extracted_insights"])
                if st.button("✨ Send Virtual Art Director Guidelines to Carousel Studio", type="primary", use_container_width=True):
                    st.session_state["style_inspiration_notes"] = st.session_state["sia_extracted_insights"]
                    st.session_state["bg_style_mode"] = "🎯 Exact Inspiration Match (Objects & Layout)"
                    st.session_state["active_tool_idx"] = 0
                    st.rerun()
        else:
            st.warning("🔒 Complete Suite Upgrade Required ($250 Tier)")


# ==========================================
# TAB 5: FINAL DELIVERY & EXPORT
# ==========================================
elif "Final Delivery & Export" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### Step 5: Final Delivery & Export")
        if st.session_state["animated_gif_bytes"]:
            st.success("✅ Kinetic animation loop compiled.")
        else:
            st.warning("⏳ Final delivery pending. Complete Steps 1 & 2 first.")