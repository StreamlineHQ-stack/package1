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

# --- CUSTOM SAAS STYLING ---
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .card { background-color: #161b22; padding: 25px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 20px; }
    .step-header { color: #58a6ff; font-weight: bold; font-size: 1.2rem; margin-bottom: 10px; }
    .stButton>button { background-color: #ffcc00; color: #0e1117; font-weight: bold; border-radius: 6px; border: none; }
    .stButton>button:hover { background-color: #e6b800; color: #0e1117; }
    </style>
""",
    unsafe_allow_html=True,
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
    elif style_theme == "Warning Red Alert":
        return {"bg": "#181212", "border": "1px solid #3d2222", "badge": "#ef4444", "title": "#ffffff", "body": "#e5cdc5", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Minimalist Clean":
        return {"bg": "#ffffff", "border": "1px solid #e0e0e0", "badge": "#0066cc", "title": "#111111", "body": "#444444", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Warm Editorial":
        return {"bg": "#fbf9f5", "border": "1px solid #e6dfd3", "badge": "#a85732", "title": "#2c221e", "body": "#5c4e47", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
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


# --- MAIN APP HEADER ---
st.title("⚡ Creator Suite: Master Platform Hub")
st.markdown("Welcome to your intelligent direct-response creator workspace. Select a module below to begin.")
st.divider()


# --- MODULE SELECTOR TABS ---
tab_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. ⚙️ Kinetic Motion Engine",
    "3. 💡 Feature-to-Benefits",
    "4. ✨ Style Inspiration (24)",
    "5. 🚀 Final Delivery & Export",
]

st.markdown("### 🗂️ Platform Module Selector")

if "active_tab_selection" not in st.session_state:
    st.session_state["active_tab_selection"] = tab_names[0]

selected_main_tab = st.selectbox(
    "Active Workspace Tool:", 
    tab_names, 
    index=tab_names.index(st.session_state["active_tab_selection"]) if st.session_state["active_tab_selection"] in tab_names else 0,
    label_visibility="collapsed"
)
st.session_state["active_tab_selection"] = selected_main_tab
st.divider()


# ==========================================
# STRICTLY CONTEXTUAL SIDEBAR
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
            st.markdown(
                "* **The Golden Rule:** Features tell, but benefits sell. Instead of listing what a product *has*, show customers how it *improves their life*.\n"
                "* **Usage:** Drop your raw bullet points below to instantly convert them into persuasive listing copy."
            )
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
    # Force solid terracotta editorial background when SIA brief is active
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
    with st.expander("🚀 Intelligent Pre-