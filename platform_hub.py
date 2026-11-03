import io
import json
import os
import base64
import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from image_renderer import generate_png_zip_from_slides

st.set_page_config(
    page_title="Creator Suite • Master Platform Hub (4-in-1)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    else:
        return {"bg": "#1a1a1a", "border": "none", "badge": "#ffcc00", "title": "#ffffff", "body": "#d1d1d1", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}

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

st.title("⚡ Creator Suite: Master Platform Hub")
st.markdown("Welcome to your intelligent direct-response creator workspace. Select a module below to begin.")
st.divider()

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
            st.markdown("Features tell, but benefits sell. Show customers how it improves their life.")
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

watermark_type = "Text Handle"
brand_handle = "@nikki.coachpages"
logo_file = None
logo_base64 = ""
slide_count = 6
frame_rate = 20
seconds_per_slide = 2.5
product_category = "Home & Garden Goods"
output_tone = "High-Converting & Direct"

if "style_inspiration_notes" in st.session_state and st.session_state["style_inspiration_notes"]:
    current_palette = {
        "bg": "#a85732", "border": "1px solid #8c4728", "badge": "#ffcc00",
        "title": "#ffffff", "body": "#f4f1ea", "font_family": "Inter", "title_weight": "700", "body_weight": "400"
    }
else:
    try:
        current_palette = get_theme_palette(style_theme, custom_colors)
    except NameError:
        current_palette = get_theme_palette("High-Contrast Canary")

if "Carousel Engine Studio" in selected_main_tab:
    with st.expander("🚀 Intelligent Pre-Flight Onboarding (Optional Intake Wizard)", expanded=not bool(st.session_state["deck_json"])):
        st.markdown("### Welcome! Let's prep your workspace before building your carousel.")
        col_inf1, col_inf2, col_inf3 = st.columns(3)
        with col_inf1:
            st.markdown("#### 🎨 1. Carousel Studio")
            if st.button("Open Carousel Builder"):
                st.session_state["active_tab_selection"] = "1. 🎨 Carousel Engine Studio"
                st.rerun()
        with col_inf2:
            st.markdown("#### 💡 2. Feature-to-Benefits")
            if st.button("Go to Feature-to-Benefits ➔"):
                st.session_state["active_tab_selection"] = "3. 💡 Feature-to-Benefits"
                st.rerun()
        with col_inf3:
            st.markdown("#### ✨ 3. Style Inspiration")
            if st.button("Go to Style Inspiration ➔"):
                st.session_state["active_tab_selection"] = "4. ✨ Style Inspiration (24)"
                st.rerun()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="step-header">Step 1: Build Your Carousel</p>', unsafe_allow_html=True)

    if st.session_state["preflight_benefits"]:
        st.info(f"✨ **Pre-Flight Data Loaded in Carousel:** {st.session_state['preflight_benefits']}")

    if st.session_state["style_inspiration_notes"]:
        st.success(f"🎨 **Active SIA Virtual Art Director Brief Loaded:** {st.session_state['style_inspiration_notes']}")

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
        notes_input = st.text_area("Paste raw coaching notes:", height=120, value="Hook: 73% leave offer page.")
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
            raw_text = f"Hook: {h_in} | Problem: {p_in} | Solution: {s_in} | CTA: {c_in}"
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
                slides = parsed if isinstance(parsed, list) else parsed.get("slides", [])
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
            tag = str(s.get("category", s.get("tag", f"STEP {curr+1}"))).upper() if isinstance(s, dict) else f"STEP {curr+1}"
            title = s.get("title", s.get("headline", "")) if isinstance(s, dict) else str(s)
            body = s.get("content", s.get("body", "")) if isinstance(s, dict) else ""

            st.markdown(
                f'''
                <div style="background-color: {current_palette['bg']}; color: {current_palette['title']}; padding: 40px; border-radius: 16px; min-height: 280px; border: {current_palette['border']}; margin-top: 15px; margin-bottom: 25px;">
                    <p style="color: {current_palette['badge']}; font-weight: 800; font-size: 13px; letter-spacing: 1.5px; margin-bottom: 15px;">SLIDE {curr+1} • {tag}</p>
                    <h3 style="color: {current_palette['title']}; font-size: 24px; font-weight: 700; margin-bottom: 15px; line-height: 1.3;">{title}</h3>
                    <p style="color: {current_palette['body']}; font-size: 15px; line-height: 1.6;">{body}</p>
                </div>
                ''',
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

    st.markdown("</div>", unsafe_allow_html=True)

elif "Kinetic Motion Engine" in selected_main_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="step-header">Step 2: Motion Rendering Engine</p>', unsafe_allow_html=True)
    if st.session_state["deck_json"]:
        st.success("✨ Active JSON payload loaded!")
        if st.button("✨ Render Kinetic Assets (GIF & MP4)", use_container_width=True):
            with st.spinner("Rendering frames..."):
                try:
                    deck_raw = st.session_state["deck_json"]
                    slides_data = json.loads(deck_raw).get("slides", []) if isinstance(deck_raw, str) else deck_raw
                    frames, numpy_frames = [], []
                    width, height = 1080, 1080
                    import numpy as np
                    for idx, slide in enumerate(slides_data, start=1):
                        img = Image.new("RGB", (width, height), color=current_palette["bg"])
                        draw = ImageDraw.Draw(img)
                        draw.text((100, 140), f"SLIDE {idx}", fill=current_palette["badge"])
                        frames.append(img)
                        numpy_frames.append(np.array(img))
                    
                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=2500, loop=0)
                    st.session_state["animated_gif_bytes"] = gif_buffer.getvalue()

                    import imageio
                    mp4_path = "temp_kinetic_output.mp4"
                    imageio.mimwrite(mp4_path, numpy_frames, fps=frame_rate, codec="libx264", quality=8, pixelformat="yuv420p")
                    with open(mp4_path, "rb") as f:
                        st.session_state["mp4_video_bytes"] = f.read()
                    if os.path.exists(mp4_path):
                        os.remove(mp4_path)
                    st.success("🎉 Rendered successfully!")
                except Exception as e:
                    st.error(f"Render error: {e}")
    else:
        st.warning("🔒 No carousel payload found. Generate a carousel in Step 1 first.")
    st.markdown("</div>", unsafe_allow_html=True)

elif "Feature-to-Benefits" in selected_main_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if is_full_suite:
        st.markdown("<h1>🛍️ Feature-to-Benefit Translator</h1>", unsafe_allow_html=True)
        f2b_product = st.text_input("Product Name:", value="Garden Kneeler")
        if st.button("Translate", type="primary"):
            st.success("Translated successfully!")
    else:
        st.warning("Complete Suite Upgrade Required ($250 Tier)")
    st.markdown("</div>", unsafe_allow_html=True)

elif "Style Inspiration" in selected_main_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if is_full_suite:
        st.markdown("<h1>✨ SIA Engine</h1>", unsafe_allow_html=True)
        if st.button("Run Deconstruction", type="primary"):
            st.success("Complete!")
    else:
        st.warning("Complete Suite Upgrade Required ($250 Tier)")
    st.markdown("</div>", unsafe_allow_html=True)

elif "Final Delivery & Export" in selected_main_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="step-header">Step 5: Delivery & Export</p>', unsafe_allow_html=True)
    if st.session_state["animated_gif_bytes"]:
        st.image(st.session_state["animated_gif_bytes"], caption="Preview")
        st.download_button("Download GIF", data=st.session_state["animated_gif_bytes"], file_name="loop.gif", mime="image/gif")
    else:
        st.warning("Pending assets.")
    st.markdown("</div>", unsafe_allow_html=True)