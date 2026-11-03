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
        st.markdown("Deconstruct high-performing swipe references into advanced