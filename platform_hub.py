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
            "bg": custom_colors["bg"], "border": custom_colors["border"], "badge": custom_colors["tag"], 
            "title": custom_colors["text"], "body": custom_colors["body"], "font_family": "Inter", "title_weight": "700", "body_weight": "400"
        }
    elif style_theme == "Warm Editorial":
        return {"bg": "#a85732", "border": "1px solid #8c4728", "badge": "#ffcc00", "title": "#ffffff", "body": "#f4f1ea", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Warning Red Alert":
        return {"bg": "#181212", "border": "1px solid #3d2222", "badge": "#ef4444", "title": "#ffffff", "body": "#e5cdc5", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Minimalist Clean":
        return {"bg": "#ffffff", "border": "1px solid #e0e0e0", "badge": "#0066cc", "title": "#111111", "body": "#444444", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Neon Cyber/Tech":
        return {"bg": "#0b0f19", "border": "1px solid #1e293b", "badge": "#06b6d4", "title": "#f8fafc", "body": "#94a3b8", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Midnight Luxury":
        return {"bg": "#121212", "border": "1px solid #2a2415", "badge": "#d4af37", "title": "#f5e6c8", "body": "#d4c5a9", "font_family": "Inter", "title_weight": "600", "body_weight": "400"}
    elif style_theme == "Emerald Growth":
        return {"bg": "#0a1f1c", "border": "1px solid #133e38", "badge": "#10b981", "title": "#e6f4f1", "body": "#a3cbd0", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Nordic Slate":
        return {"bg": "#1e242b", "border": "1px solid #334155", "badge": "#38bdf8", "title": "#f1f5f9", "body": "#cbd5e1", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Bold Coral Pop":
        return {"bg": "#231818", "border": "1px solid #422929", "badge": "#ff6b6b", "title": "#fff0ed", "body": "#e2c4be", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Monochrome Obsidian":
        return {"bg": "#000000", "border": "1px solid #262626", "badge": "#ffffff", "title": "#ffffff", "body": "#a3a3a3", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    else:  # High-Contrast Canary
        return {"bg": "#1a1a1a", "border": "none", "badge": "#ffcc00", "title": "#ffffff", "body": "#d1d1d1", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}


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

def get_curated_background_url(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64=""):
    if style_mode == "☕ Terracotta Background & White Font":
        return ""

    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"

    if style_mode == "🎯 Exact Inspiration Match (Objects & Layout)":
        return "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80"

    motifs = {
        "Archways, Windows & Doors": [
            "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1080&auto=format&fit=crop&q=80",
        ],
        "Rustic Wood Logs & Textures": [
            "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1546484396-fb3fc6f95f98?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1080&auto=format&fit=crop&q=80",
        ],
        "Botanical Florals & Stems": [
            "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1463936575829-25148e1db1b8?w=1080&auto=format&fit=crop&q=80",
        ],
        "Warm Editorial Amber": [
            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1445053023192-8d45cb66099d?w=1080&auto=format&fit=crop&q=80",
        ]
    }
    
    if style_mode == "🏛️ Unified Editorial Motif":
        selected_key = motif_choice
        if selected_key in motifs:
            urls = motifs[selected_key]
            return urls[slide_index % len(urls)]

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
st.markdown("Welcome to your intelligent direct-response creator workspace. Select a module below to begin.")
st.divider()


# --- ROBUST MODULE SELECTOR ---
tab_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. ⚙️ Kinetic Motion Engine",
    "3. 💡 Feature-to-Benefits",
    "4. ✨ Style Inspiration (24)",
    "5. 🚀 Final Delivery & Export",
]

st.markdown("### 🗂️ Platform Module Selector")

current_selected_tab = st.selectbox(
    "Active Workspace Tool:", 
    tab_names, 
    index=st.session_state["active_tool_idx"],
    label_visibility="collapsed",
    key="active_tool_selectbox"
)

st.session_state["active_tool_idx"] = tab_names.index(current_selected_tab)
selected_main_tab = current_selected_tab
st.divider()


# ==========================================
# STRICTLY CONTEXTUAL SIDEBAR (ROBUST & UNIFIED)
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

    # --- ADVANCED BACKGROUND & VISUAL STYLE CONTROLS ---
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
        st.markdown("#### 🌸 Motif Family Selector")
        unified_motif_choice = st.selectbox(
            "Choose Motif:",
            [
                "Botanical Florals & Stems",
                "Archways, Windows & Doors",
                "Rustic Wood Logs & Textures",
                "Warm Editorial Amber"
            ],
            key="motif_family_selectbox"
        )
        st.session_state["unified_motif_choice"] = unified_motif_choice
        st.caption("💡 *Same motif family across all slides, with unique matching variations per slide.*")

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
        
        st.divider()
        with st.expander("📖 Copywriting Guide"):
            st.markdown("""
                * **The Golden Rule:** Features tell, but benefits sell. Instead of listing what a product *has*, show customers how it *improves their life*.
                * **Usage:** Drop your raw bullet points below to instantly convert them into persuasive listing copy.
            """)
        st.info("💡 **Pro Utility:** Instantly translates dry product specs into compelling customer benefits.")

    elif "Kinetic Motion Engine" in selected_main_tab:
        st.subheader("⚙️ Pro Motion Controls")
        frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20)
        seconds_per_slide = st.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25)
        transition_style = st.selectbox(
            "Kinetic Transition Style:",
            ["Dynamic Slide Up (Pro Easing)", "Smooth Slide Right", "Cinematic Zoom In", "Fade & Snap"]
        )
        transition_speed = st.slider("Transition Speed (Frames):", 2, 15, 6)
        st.divider()
        st.info("💡 **Kinetic Engine:** Renders full-bleed animated GIFs and YUV420p HD MP4 videos.")

    elif "Style Inspiration" in selected_main_tab:
        st.subheader("✨ Virtual Art Director")
        st.markdown("Deconstruct high-performing swipe references into advanced visual and content vectors.")
        st.info("💡 **Tip:** Bridge your deconstructed aesthetic straight into Carousel Studio.")

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


# Default values if sidebar vars are accessed out of scope
watermark_type = "Text Handle"
brand_handle = "@nikki.coachpages"
logo_file = None
logo_base64 = ""
slide_count = 6
frame_rate = 20
seconds_per_slide = 2.5
product_category = "Home & Garden Goods"
output_tone = "High-Converting & Direct"

# --- INTELLIGENT PALETTE OVERRIDE (SIA & SIDEBAR SYNC) ---
if "style_inspiration_notes" in st.session_state and st.session_state["style_inspiration_notes"]:
    current_palette = {
        "bg": "#a85732",
        "border": "1px solid #8c4728",
        "badge": "#ffcc00",
        "title": "#ffffff",
        "body": "#f4f1ea",
        "font_family": "Inter",
        "title_weight": "700",
        "body_weight": "400"
    }
elif bg_style_mode in ["☕ Terracotta Background & White Font", "🎯 Exact Inspiration Match (Objects & Layout)"]:
    current_palette = {
        "bg": "#a85732",
        "border": "1px solid #8c4728",
        "badge": "#ffcc00",
        "title": "#ffffff",
        "body": "#f4f1ea",
        "font_family": "Inter",
        "title_weight": "700",
        "body_weight": "400"
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
        st.markdown("Prep your workspace or jump straight into building your direct-response slide deck using one of the three modes below.")
        
        col_inf1, col_inf2, col_inf3 = st.columns(3)
        with col_inf1:
            st.markdown("#### 🎨 1. Carousel Studio")
            st.markdown("Build direct-response decks with Auto-Pilot, Custom Notes, or 100+ Frameworks.")
        with col_inf2:
            st.markdown("#### 💡 2. Feature-to-Benefits")
            st.markdown("Translate raw product specs into emotional benefits first.")
            if st.button("Go to Feature-to-Benefits ➔", key="btn_onboard_f2b"):
                st.session_state["active_tool_idx"] = 2
                st.session_state["active_tool_selectbox"] = tab_names[2]
                st.rerun()
        with col_inf3:
            st.markdown("#### ✨ 3. Style Inspiration")
            st.markdown("Browse elite design templates and color swipe files.")
            if st.button("Go to Style Inspiration ➔", key="btn_onboard_sia"):
                st.session_state["active_tool_idx"] = 3
                st.session_state["active_tool_selectbox"] = tab_names[3]
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

                watermark_html = ""
                if watermark_type == "Text Handle" and brand_handle:
                    watermark_html = f'<span style="color: {current_palette["body"]}; font-size: 11px; opacity: 0.85; letter-spacing: 1px; text-shadow: 0px 1px 3px rgba(0,0,0,0.8);">{brand_handle}</span>'
                elif watermark_type == "Logo Image" and logo_file is not None and logo_base64:
                    watermark_html = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 25px; object-fit: contain;" />'

                preview_bg_url = get_curated_background_url(bg_style_mode, unified_motif_choice, curr, tag, custom_bg_url, st.session_state.get("custom_uploaded_bg_b64", ""))

                if preview_bg_url:
                    bg_style_css = f"background-image: linear-gradient(rgba(14, 17, 23, 0.4), rgba(14, 17, 23, 0.6)), url('{preview_bg_url}'); background-size: cover; background-position: center;"
                else:
                    bg_style_css = f"background-color: {current_palette['bg']};"

                st.markdown(
                    f"""
                    <div style="{bg_style_css} color: {current_palette['title']}; padding: 40px; border-radius: 16px; min-height: 280px; border: {current_palette['border']}; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
                        <div>
                            <p style="color: {current_palette['badge']}; font-weight: 800; font-size: 13px; letter-spacing: 1.5px; margin-bottom: 15px; text-shadow: 0px 1px 3px rgba(0,0,0,0.8);">SLIDE {curr+1} • {tag}</p>
                            <h3 style="color: {current_palette['title']}; font-size: 24px; font-weight: 700; margin-bottom: 15px; line-height: 1.3; text-shadow: 0px 2px 4px rgba(0,0,0,0.8);">{title}</h3>
                            <p style="color: {current_palette['body']}; font-size: 15px; line-height: 1.6; text-shadow: 0px 1px 3px rgba(0,0,0,0.8);">{body}</p>
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
                    st.session_state["active_tool_selectbox"] = tab_names[1]
                    st.toast("Payload successfully bridged to Kinetic motion engine!", icon="✨")
                    st.rerun()


# ==========================================
# TAB 2: KINETIC MOTION ENGINE
# ==========================================
elif "Kinetic Motion Engine" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### Step 2: Automated JSON Handoff & Pro Full-Bleed Motion Rendering Engine (GIF & MP4)")

        if st.session_state["deck_json"]:
            st.success("✨ Active JSON payload successfully received from Carousel Engine via Platform Bridge!")

            with st.expander("🔍 Inspect Ingested JSON Payload"):
                st.json(st.session_state["deck_json"])

            st.divider()
            st.subheader("🎬 Render Engine Compilation (Full-Bleed GIF & HD MP4)")

            if st.button("✨ Render Premium Kinetic Assets (GIF & MP4)", use_container_width=True):
                with st.spinner("Rendering full-bleed frames and compiling GIF & HD MP4 video assets..."):
                    try:
                        deck_raw = st.session_state["deck_json"]
                        if isinstance(deck_raw, str):
                            try:
                                parsed_raw = json.loads(deck_raw)
                            except Exception:
                                parsed_raw = []
                            if isinstance(parsed_raw, list):
                                slides_data = parsed_raw
                            elif isinstance(parsed_raw, dict):
                                slides_data = parsed_raw.get("slides", [])
                            else:
                                slides_data = []
                        elif isinstance(deck_raw, list):
                            slides_data = deck_raw
                        elif isinstance(deck_raw, dict):
                            slides_data = deck_raw.get("slides", [])
                        else:
                            slides_data = []

                        frames = []
                        numpy_frames = []
                        width, height = 1080, 1080
                        max_text_width = 880

                        badge_font = load_app_font(38)
                        title_font = load_app_font(62)
                        body_font = load_app_font(42)
                        footer_font = load_app_font(30)

                        import numpy as np

                        for idx, slide in enumerate(slides_data, start=1):
                            if isinstance(slide, dict):
                                badge = str(slide.get("category", slide.get("tag", f"SLIDE {idx} | STRATEGY")))
                                title = str(slide.get("title", slide.get("headline", f"Slide Title {idx}")))
                                body = str(slide.get("content", slide.get("body", "Key actionable breakdown...")))
                            else:
                                badge = f"SLIDE {idx} | STRATEGY"
                                title = str(slide)
                                body = ""

                            img = Image.new("RGB", (width, height), color=current_palette["bg"])
                            draw = ImageDraw.Draw(img)

                            draw.text((100, 140), badge.upper(), fill=current_palette["badge"], font=badge_font)

                            temp_img = Image.new("RGB", (width, height))
                            temp_draw = ImageDraw.Draw(temp_img)
                            wrapped_title = wrap_text_to_width(title, title_font, max_text_width, temp_draw)
                            title_y = 230
                            for line in wrapped_title:
                                draw.text((100, title_y), line, fill=current_palette["title"], font=title_font)
                                title_y += 74

                            if body:
                                wrapped_body = wrap_text_to_width(body, body_font, max_text_width, temp_draw)
                                body_y = title_y + 40
                                for line in wrapped_body:
                                    draw.text((100, body_y), line, fill=current_palette["body"], font=body_font)
                                    body_y += 56

                            active_footer = brand_handle if watermark_type == "Text Handle" else "Creator Suite Studio"
                            draw.text((100, height - 160), active_footer, fill="#8b949e", font=footer_font)
                            
                            frames.append(img)
                            fps = frame_rate
                            slide_duration_frames = int(seconds_per_slide * fps)
                            np_arr = np.array(img)
                            for _ in range(slide_duration_frames):
                                numpy_frames.append(np_arr)

                        # 1. Compile GIF
                        gif_buffer = io.BytesIO()
                        if frames:
                            frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                        st.session_state["animated_gif_bytes"] = gif_buffer.getvalue()

                        # 2. Compile HD MP4 Video via imageio with yuv420p
                        try:
                            import imageio
                            mp4_path = "temp_kinetic_output.mp4"
                            imageio.mimwrite(
                                mp4_path,
                                numpy_frames,
                                fps=frame_rate,
                                codec="libx264",
                                quality=8,
                                pixelformat="yuv420p"
                            )
                            with open(mp4_path, "rb") as f:
                                st.session_state["mp4_video_bytes"] = f.read()
                            if os.path.exists(mp4_path):
                                os.remove(mp4_path)
                        except Exception as vid_err:
                            st.session_state["mp4_video_bytes"] = None
                            st.caption(f"MP4 compilation notice: {vid_err}")

                        first_slide = slides_data[0] if slides_data else {}
                        if isinstance(first_slide, dict):
                            cap_title = first_slide.get("title", "Transform Your Coaching Page")
                            cap_body = first_slide.get("content", first_slide.get("body", ""))
                        else:
                            cap_title = str(first_slide)
                            cap_body = ""

                        st.session_state["generated_caption"] = (
                            f"🔥 {cap_title}\n\n{cap_body}\n\nWhich slide hit home for you the most? Drop your thoughts below! 👇\n\n--- \n⚡ Built & animated seamlessly using Carousel Engine & Kinetic Motion Suite."
                        )

                        st.success("🎉 Kinetic full-bleed GIF & HD MP4 Video loops rendered successfully!")
                    except Exception as e:
                        st.error(f"Render error: {e}")
        else:
            st.warning("🔒 No carousel payload found. Please generate a carousel deck in Step 1 first.")


# ==========================================
# TAB 3: FEATURE-TO-BENEFITS (TOOL 3)
# ==========================================
elif "Feature-to-Benefits" in selected_main_tab:
    with st.container(border=True):
        if is_full_suite:
            st.markdown("<h1 style='text-align: center;'>🛍️ E-Commerce Feature-to-Benefit Translator</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Turn dry product specifications into high-converting customer benefits designed to skyrocket your online sales.</p>", unsafe_allow_html=True)
            st.divider()

            col_i1, col_i2 = st.columns(2)
            with col_i1:
                f2b_product = st.text_input("Product Name:", value="Ergonomic Garden Kneeler & Seat")
            with col_i2:
                f2b_buyer = st.text_input("Target Buyer Persona:", value="Home gardeners and seniors who love planting but suffer from sore knees and back pain.")

            f2b_features = st.text_area("Paste Raw Product Features / Specifications (one per line):", height=130, value="- Thick EVA foam padding cushion\n- Heavy-duty steel frame supporting up to 330 lbs\n- Detachable tool pouch with deep pockets\n- Folds flat in one click for easy garage storage")

            if st.button("🚀 Translate Features into High-Converting Benefits", type="primary"):
                with st.spinner("Translating technical specs into irresistible customer benefits..."):
                    parsed_features = [line.strip().lstrip("-*•").strip() for line in f2b_features.split("\n") if line.strip()]
                    
                    benefit_templates = [
                        ("Protects your joints", "say goodbye to aching knees and soreness after a long afternoon in the soil."),
                        ("Provides rock-solid safety", "feel completely secure and stable whether sitting upright or kneeling down."),
                        ("Keeps tools right at your fingertips", "eliminate frustrating trips back to the shed by storing your clippers and gloves on your hip."),
                        ("Saves precious garage space", "tuck it away neatly in seconds with zero hassle when your gardening day is done.")
                    ]
                    
                    benefit_bullets = ""
                    table_rows = ""
                    for idx, feat in enumerate(parsed_features):
                        angle_title, angle_benefit = benefit_templates[idx % len(benefit_templates)]
                        benefit_bullets += f"- **{angle_title}:** Featuring {feat.lower()}, so you can {angle_benefit}\n"
                        table_rows += f"| {feat} | {angle_title} ({angle_benefit}) | High |\n"

                    translation_report = (
                        f"# E-Commerce Feature-to-Benefit Optimization Report\n"
                        f"Product: {f2b_product}\n"
                        f"Category: {product_category}\n"
                        f"Target Buyer: {f2b_buyer}\n"
                        f"Tone: {output_tone}\n\n"
                        f"## 🎁 1. Feature-to-Benefit Translation Matrix\n"
                        f"{benefit_bullets}\n"
                        f"## ✍️ 2. Optimized Listing Bullet Points\n"
                        f"- **Zero Joint Strain:** Thick cushioning absorbs impact so you can garden longer without physical discomfort.\n"
                        f"- **Durable Stability:** Robust frame engineered for secure support and long-lasting seasonal use.\n"
                        f"- **All-in-One Convenience:** Built-in tool pouches keep your gear organized right where you need it.\n"
                        f"- **Effortless Storage:** Folds flat instantly, making it a breeze to pack up and store away.\n\n"
                        f"## 🎯 3. High-Converting Product Description Hook\n"
                        f"\"Tired of aching joints cutting your gardening sessions short? Meet the {f2b_product}—custom-built to give {f2b_buyer} the comfort, support, and ease you deserve. Cultivate your garden, not your back pain!\""
                    )

                    st.success("🎉 Product features successfully translated into high-impact customer benefits!")
                    st.session_state["latest_translation_report"] = translation_report

                    sub_t1, sub_t2, sub_t3 = st.tabs(["📊 Optimization Report", "🔍 Feature-Benefit Table", "📦 JSON Data Export"])
                    with sub_t1:
                        st.markdown(translation_report)
                        st.download_button("📥 Download Copy Report (.txt)", data=translation_report, file_name="listing_copy_report.txt", mime="text/plain")
                    with sub_t2:
                        st.markdown("| Raw Product Feature | Translated Customer Benefit | Sales Impact |\n|---|---|---|\n" + table_rows)
                    with sub_t3:
                        json_pkg = {"product": f2b_product, "features": parsed_features, "report": translation_report}
                        st.code(json.dumps(json_pkg, indent=2), language="json")

            if "latest_translation_report" in st.session_state and st.session_state["latest_translation_report"]:
                st.divider()
                st.markdown("### 🔄 Send Forward to Carousel Studio")
                st.info("Want to turn these generated emotional benefits into a high-converting Instagram carousel deck instantly?")
                if st.button("✨ Send Output Forward & Use in Carousel Studio", type="primary", key="btn_bridge_f2b_carousel"):
                    st.session_state["preflight_benefits"] = f"Product: {f2b_product} | Benefits: {st.session_state['latest_translation_report'][:300]}..."
                    st.session_state["active_tool_idx"] = 0
                    st.session_state["active_tool_selectbox"] = tab_names[0]
                    st.toast("Benefits bridged successfully to Carousel Studio!", icon="✨")
                    st.rerun()

        else:
            st.error("🔒 Locked Module: Feature-to-Benefits Matrix")
            st.warning(
                "**Complete Suite Upgrade Required ($250 Tier)**\n\n"
                "Your current Master Pass ($149) unlocks Carousel Studio and Kinetic Motion Engine. "
                "Upgrade to the **$250 Complete Suite** to instantly unlock Tool 3 (Feature-to-Benefits) and Tool 4 (Style Inspiration) right inside this platform hub!"
            )


# ==========================================
# TAB 4: STYLE INSPIRATION & ANALYSIS ENGINE (SIA)
# ==========================================
elif "Style Inspiration" in selected_main_tab:
    with st.container(border=True):
        if is_full_suite:
            st.markdown("<h1 style='text-align: center;'>✨ SIA: Style Inspiration & Analysis Engine</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Deconstruct high-performing creator slides into actionable content, typography, and advanced photographic visual design principles.</p>", unsafe_allow_html=True)
            st.divider()

            col_u1, col_u2 = st.columns(2)

            with col_u1:
                st.subheader("📥 1. Reference Swipe Selection")
                ref_mode = st.radio("Reference Source:", ["Upload Custom Screenshot", "Use Canva Editorial Sample (Terracotta)"], key="platform_sia_ref_mode")
                
                if ref_mode == "Upload Custom Screenshot":
                    uploaded_screenshot = st.file_uploader("Upload slide image (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"], key="platform_sia_upload_file")
                    if uploaded_screenshot is not None:
                        try:
                            img = Image.open(uploaded_screenshot)
                            st.image(img, caption="Custom Swipe Reference", use_container_width=True)
                            st.session_state["sia_image_loaded"] = True
                        except Exception:
                            st.session_state["sia_image_loaded"] = False
                    else:
                        st.session_state["sia_image_loaded"] = False
                else:
                    st.info("🎨 **Active Reference:** Canva Warm Editorial Slide ('Sarina & Leon' Terracotta Palette)")
                    st.session_state["sia_image_loaded"] = True

            with col_u2:
                st.subheader("🔍 2. Dual-Lens Focus Selection")
                st.markdown("Choose what you want to deconstruct from your reference image:")
                
                focus_vector = st.radio(
                    "Primary Inspiration Vector:",
                    ["Visuals & Design Style", "Content & Copywriting Structure", "Both (Comprehensive Breakdown)"],
                    key="platform_sia_focus_radio"
                )
                st.session_state["sia_focus_choice"] = focus_vector

                st.divider()
                analysis_trigger = st.button("🚀 Run Dual-Lens Deconstruction", type="primary", use_container_width=True, key="platform_sia_run_btn")

            if analysis_trigger:
                if not st.session_state.get("sia_image_loaded", False):
                    st.warning("⚠️ Please select or upload a reference slide first.")
                else:
                    with st.spinner("Deconstructing content cadence and advanced photographic aesthetic ratios..."):
                        if "Visuals" in focus_vector:
                            report = (
                                "### 🎨 Advanced Visual & Photographic Deconstruction\n"
                                "- **Color Palette & Tone:** Warm editorial aesthetic (Terracotta base `#a85732` paired with rich cream and dark typography).\n"
                                "- **Subject Framing & Composition:** Minimalist, centered subject placement utilizing substantial negative space to maintain an uncluttered high-end aesthetic.\n"
                                "- **Prop & Texture Staging:** Incorporation of tactile organic elements (e.g., natural wood blocks, sleek mirrors, and single botanical stems) to anchor the visual mood.\n"
                                "- **Lighting & Atmosphere:** Warm, low-key lighting with earthy amber and terracotta color grading creating an intimate, editorial feel.\n"
                                "- **Image-to-Text Integration:** High-contrast serif typography positioned cleanly over the upper third of the photographic backdrop, ensuring readability without obstructing the primary focal point."
                            )
                        elif "Content" in focus_vector:
                            report = (
                                "### ✍️ Content & Copywriting Deconstruction\n"
                                "- **The Hook Mechanics:** Elegant, authority-driven headline structure designed for high-end branding or event invitations.\n"
                                "- **Tone & Cadence:** Sophisticated, refined, and uncluttered layout structure."
                            )
                        else:
                            report = (
                                "### ⚡ Comprehensive Dual-Lens & Photographic Deconstruction\n"
                                "- **Visual & Photographic Style:** Warm editorial terracotta palette paired with tactile organic props, minimalist centered framing, and low-key amber lighting.\n"
                                "- **Typography & Layout:** High-contrast serif headings with generous tracking layered over atmospheric negative space.\n"
                                "- **Content Structure:** Minimalist authoritative framing designed for premium visual engagement."
                            )

                        st.session_state["sia_extracted_insights"] = report
                        st.session_state["sia_analysis_run"] = True
                        st.success("🎉 Deconstruction complete!")

            if st.session_state["sia_analysis_run"]:
                st.divider()
                st.subheader("📊 Deconstruction Intelligence Report")
                st.markdown(st.session_state["sia_extracted_insights"])

                st.markdown("### 💬 Interactive Refinement Q&A")
                col_qa1, col_qa2 = st.columns(2)
                
                with col_qa1:
                    vis_refinement = st.selectbox("Visual & Photographic Preference:", [
                        "Warm editorial terracotta color palette & lighting",
                        "Tactile prop staging (wood textures & botanical stems)",
                        "Minimalist centered framing & negative space",
                        "High-contrast serif typography layout"
                    ], key="platform_sia_vis_ref")
                
                with col_qa2:
                    content_refinement = st.selectbox("Content Preference:", [
                        "Elegant headline phrasing and spacing",
                        "Sophisticated and refined editorial tone",
                        "Uncluttered, authoritative structure"
                    ], key="platform_sia_cont_ref")

                st.info(f"💡 **Virtual Art Director Mapped:** Visuals (*'{vis_refinement}'*) + Content (*'{content_refinement}'*). Ready to bridge to Carousel Studio.")

                st.divider()
                st.subheader("🔄 Bridge to Platform Carousel Studio")
                st.markdown("Send both your advanced photographic art-director tokens and copywriting structure straight into Tab 1:")
                
                if st.button("✨ Send Virtual Art Director Guidelines to Carousel Studio", type="primary", use_container_width=True, key="platform_sia_bridge_btn"):
                    st.session_state["style_inspiration_notes"] = f"Visual Style: {vis_refinement} | Content Style: {content_refinement}"
                    st.session_state["active_tool_idx"] = 0
                    st.session_state["active_tool_selectbox"] = tab_names[0]
                    st.toast("Virtual Art Director parameters successfully bridged to Carousel Studio!", icon="✨")
                    st.rerun()

            st.divider()
            st.subheader("📦 Standalone Design Token & Style Guide Exports")
            col_ex1, col_ex2 = st.columns(2)
            
            with col_ex1:
                md_content = (
                    f"# SIA Style Guide & Brand Brief\n"
                    f"Vector Focus: {st.session_state['sia_focus_choice']}\n\n"
                    f"{st.session_state['sia_extracted_insights']}"
                )
                st.download_button("📄 Download Full Style Guide (.md)", data=md_content, file_name="sia_style_guide.md", mime="text/markdown", use_container_width=True, key="dl_md_btn")
                
            with col_ex2:
                json_content = json.dumps({
                    "focus_vector": st.session_state["sia_focus_choice"],
                    "color_palette": ["#a85732", "#f4f1ea", "#1a1a1a"],
                    "typography": "High-contrast serif / minimalist sans",
                    "photographic_style": "Warm editorial, centered minimalism, tactile props, low-key amber lighting",
                    "insights": st.session_state["sia_extracted_insights"]
                }, indent=4)
                st.download_button("📥 Download Design Tokens (.json)", data=json_content, file_name="sia_design_tokens.json", mime="application/json", use_container_width=True, key="dl_json_btn")

        else:
            st.error("🔒 Locked Module: Style Inspiration & Analysis Engine")
            st.warning(
                "**Complete Suite Upgrade Required ($250 Tier)**\n\n"
                "Upgrade your license to the **$250 Complete Suite** to unlock Tool 4 (SIA Engine) right inside this platform hub!"
            )


# ==========================================
# TAB 5: FINAL DELIVERY & EXPORT
# ==========================================
elif "Final Delivery & Export" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### Step 5: Final Animated GIF, HD MP4 Video, Slide Package & Social Caption Delivery")

        if st.session_state["animated_gif_bytes"]:
            col_res1, col_res2 = st.columns(2, gap="large")

            with col_res1:
                st.subheader("🎬 Final Motion Assets (GIF & MP4)")
                st.success("✅ Kinetic animation loop and HD video compiled.")

                st.image(
                    st.session_state["animated_gif_bytes"],
                    caption="Rendered Full-Bleed Kinetic Loop Preview",
                    use_container_width=True,
                )

                st.download_button(
                    label="⬇️ Download Rendered Animated GIF (.gif)",
                    data=st.session_state["animated_gif_bytes"],
                    file_name="kinetic_carousel_loop.gif",
                    mime="image/gif",
                    use_container_width=True,
                )

                if st.session_state["mp4_video_bytes"]:
                    st.download_button(
                        label="🎥 Download HD Motion Video (.mp4)",
                        data=st.session_state["mp4_video_bytes"],
                        file_name="kinetic_carousel_video.mp4",
                        mime="video/mp4",
                        use_container_width=True,
                    )

                st.divider()

                if st.session_state["deck_json"]:
                    try:
                        deck_raw = st.session_state["deck_json"]
                        if isinstance(deck_raw, str):
                            parsed_zip = json.loads(deck_raw)
                            if isinstance(parsed_zip, list):
                                slides_list = parsed_zip
                            elif isinstance(parsed_zip, dict):
                                slides_list = parsed_zip.get("slides", [])
                            else:
                                slides_list = []
                        else:
                            slides_list = deck_raw
                            if isinstance(slides_list, dict):
                                slides_list = slides_list.get("slides", [])
                            
                        zip_data = generate_png_zip_from_slides(slides_list, handle_text=brand_handle, palette=current_palette)
                        st.download_button(
                            label="📥 Download Static Slide PNG Package (.zip)",
                            data=zip_data,
                            file_name="carousel_slides_package.zip",
                            mime="application/zip",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.caption(f"PNG package generation note: {e}")

            with col_res2:
                st.subheader("📝 Generated Social Media Caption")
                st.text_area(
                    "Ready-to-Post Caption (Optimized for Engagement):",
                    st.session_state["generated_caption"],
                    height=220,
                )
                st.success("📋 Caption optimized for comments and reach conversion.")
        else:
            st.warning("⏳ Final delivery pending. Complete Step 1 (Carousel Studio) and Step 2 (Kinetic Motion Engine) to compile your assets.")