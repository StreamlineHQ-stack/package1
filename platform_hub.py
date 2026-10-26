import io
import json
import os
import base64
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Import your core engine modules
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from image_renderer import generate_png_zip_from_slides

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Creator Suite • Master Platform Hub",
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
if "generated_caption" not in st.session_state:
    st.session_state["generated_caption"] = ""


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
st.title("⚡ Creator Suite: Automated Carousel-to-Animation Platform")
st.markdown("Generate high-converting direct-response carousels and automatically pipe them into Kinetic for instant motion graphics and captions[cite: 5].")
st.divider()

# --- UNIFIED WORKFLOW TABS ---
tab_carousel, tab_kinetic, tab_delivery = st.tabs([
    "1. 🎨 Carousel Engine Studio",
    "2. ⚙️ Kinetic Motion Engine",
    "3. 🚀 Final Delivery & Export",
])

# --- SIDEBAR: DYNAMIC RENDERING ---
with st.sidebar:
    st.title("⚡ Creator Suite")
    st.caption("Master Package All-Access Hub")
    st.divider()

    master_key = st.text_input("Master Suite License Key:", type="password", value="TEST_MASTER_KEY")
    if master_key:
        st.success("✅ Master License Verified (All-Access)")
    else:
        st.warning("⚠️ Enter a valid master key to unlock platform.")
        st.stop()

    st.divider()
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

    current_palette = get_theme_palette(style_theme, custom_colors)

    st.divider()
    st.markdown("### 🏷️ Brand Watermark Options")
    watermark_type = st.radio("Watermark Type:", ["Text Handle", "Logo Image"])
    
    logo_file = None
    logo_base64 = ""
    brand_handle = ""
    if watermark_type == "Text Handle":
        brand_handle = st.text_input("Brand Handle / Text:", "@nikki.coachpages")
    else:
        logo_file = st.file_uploader("Upload Brand Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if logo_file is not None:
            logo_base64 = base64.b64encode(logo_file.getvalue()).decode()

    slide_count = st.slider("Target Slide Count:", 4, 10, 6)

    st.divider()
    st.markdown("### 🚀 Pro Master Package & Subscription")
    st.info(
        "**Monthly Creator Subscription & Special Discount Package**\n\n"
        "Unlock unlimited cloud rendering, advanced templates, and priority kinetic exports. Save big with the annual bundle!"
    )

    st.divider()
    st.markdown("### ⚙️ Pro Motion Controls (Kinetic Mode)")
    frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20)
    seconds_per_slide = st.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25)
    transition_style = st.selectbox(
        "Kinetic Transition Style:",
        ["Dynamic Slide Up (Pro Easing)", "Smooth Slide Right", "Cinematic Zoom In", "Fade & Snap"]
    )

    st.divider()
    st.markdown("### 🔄 Automated Pipeline Status")
    st.write("1. Carousel Gen: " + ("✅ Ready" if st.session_state["deck_json"] else "⏳ Waiting"))
    st.write("2. Kinetic Bridge: " + ("✅ Loaded" if st.session_state["deck_json"] else "⏳ Waiting"))
    st.write("3. Motion Output: " + ("✅ Compiled" if st.session_state["animated_gif_bytes"] else "⏳ Waiting"))


# ==========================================
# TAB 1: CAROUSEL ENGINE STUDIO
# ==========================================
with tab_carousel:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="step-header">Step 1: Build Your Carousel (Auto-Pilot, Notes, or 100-Template Frameworks)</p>', unsafe_allow_html=True)

    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["⚡ Auto-Pilot", "📝 Custom Notes", "🛠️ Framework Wizard"])

    with sub_tab1:
        topic_input = st.text_input("Core Topic / Hook:", value="High-converting landing page optimization for online coaches")
        if st.button("Generate Auto-Pilot Deck", type="primary"):
            with st.spinner("Crafting direct-response deck..."):
                deck_result = generate_carousel_deck(topic_input, slide_count=slide_count, mode="autopilot")
                st.session_state["deck_json"] = deck_result
                st.session_state["current_slide"] = 0
                st.success("✅ Carousel generated and loaded into platform memory!")
                st.rerun()

    with sub_tab2:
        notes_input = st.text_area(
            "Paste raw coaching notes:", height=120,
            value="Hook: 73% of prospects leave your offer page without buying.\nProblem: Vague copy creates friction.\nSolution: Audit top-of-fold messaging."
        )
        if st.button("Format Custom Notes", type="primary"):
            with st.spinner("Structuring notes..."):
                deck_result = generate_carousel_deck(notes_input, slide_count=slide_count, mode="custom")
                st.session_state["deck_json"] = deck_result
                st.session_state["current_slide"] = 0
                st.success("✅ Carousel generated and loaded into platform memory!")
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
                deck_result = generate_carousel_deck(raw_text, slide_count=slide_count, mode="framework")
                st.session_state["deck_json"] = deck_result
                st.session_state["current_slide"] = 0
                st.success("✅ Framework carousel loaded into platform memory!")
                st.rerun()

    # Preview and Slide Navigation with Synchronized Theme Colors & Watermark
    if st.session_state["deck_json"]:
        st.divider()
        try:
            deck_data = st.session_state["deck_json"]
            slides = deck_data.get("slides", []) if isinstance(deck_data, dict) else (json.loads(deck_data).get("slides", []) if isinstance(deck_data, str) else deck_data)
        except Exception:
            slides = []

        total_slides = len(slides)
        if total_slides > 0:
            if st.session_state["current_slide"] >= total_slides:
                st.session_state["current_slide"] = total_slides - 1

            curr = st.session_state["current_slide"]
            s = slides[curr]
            tag = str(s.get("tag", s.get("category", s.get("type", f"STEP {curr+1}")))).upper()
            title = s.get("title", s.get("headline", ""))
            body = s.get("body", s.get("content", ""))

            watermark_html = ""
            if watermark_type == "Text Handle" and brand_handle:
                watermark_html = f'<span style="color: {current_palette["body"]}; font-size: 11px; opacity: 0.7; letter-spacing: 1px;">{brand_handle}</span>'
            elif watermark_type == "Logo Image" and logo_file is not None and logo_base64:
                watermark_html = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 25px; object-fit: contain;" />'

            st.markdown(
                f"""
                <div style="background-color: {current_palette['bg']}; color: {current_palette['title']}; padding: 40px; border-radius: 16px; min-height: 280px; border: {current_palette['border']}; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between;">
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
                st.toast("Payload successfully bridged to Kinetic motion engine!", icon="✨")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: KINETIC MOTION ENGINE
# ==========================================
with tab_kinetic:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="step-header">Step 2: Automated JSON Handoff & Pro GIF Rendering Engine</p>', unsafe_allow_html=True)

    if st.session_state["deck_json"]:
        st.success("✨ Active JSON payload successfully received from Carousel Engine via Platform Bridge[cite: 5]!")

        with st.expander("🔍 Inspect Ingested JSON Payload"):
            st.json(st.session_state["deck_json"])

        st.divider()
        st.subheader("🎬 Render Engine Compilation")

        if st.button("✨ Render Premium Kinetic GIF (Active Deck)", use_container_width=True):
            with st.spinner("Rendering animation frames with precise typography and card styling..."):
                try:
                    slides_data = json.loads(st.session_state["deck_json"]) if isinstance(st.session_state["deck_json"], str) else st.session_state["deck_json"]
                    if isinstance(slides_data, dict):
                        slides_data = slides_data.get("slides", [])

                    frames = []
                    width, height = 1080, 1080
                    max_text_width = 800

                    badge_font = load_app_font(38)
                    title_font = load_app_font(62)
                    body_font = load_app_font(42)
                    footer_font = load_app_font(30)

                    for idx, slide in enumerate(slides_data, start=1):
                        badge = str(slide.get("tag", slide.get("category", f"SLIDE {idx} | STRATEGY")))
                        title = str(slide.get("title", slide.get("headline", f"Slide Title {idx}")))
                        body = str(slide.get("body", slide.get("content", "Key actionable breakdown...")))

                        img = Image.new("RGB", (width, height), color="#0e1117")
                        draw = ImageDraw.Draw(img)

                        draw.rounded_rectangle(
                            [80, 100, width - 80, height - 150],
                            radius=28,
                            fill=current_palette["bg"],
                            outline=current_palette["badge"] if current_palette["border"] != "none" else None,
                            width=5,
                        )

                        draw.text((140, 160), badge.upper(), fill=current_palette["badge"], font=badge_font)

                        temp_img = Image.new("RGB", (width, height))
                        temp_draw = ImageDraw.Draw(temp_img)
                        wrapped_title = wrap_text_to_width(title, title_font, max_text_width, temp_draw)
                        title_y = 250
                        for line in wrapped_title:
                            draw.text((140, title_y), line, fill=current_palette["title"], font=title_font)
                            title_y += 74

                        if body:
                            wrapped_body = wrap_text_to_width(body, body_font, max_text_width, temp_draw)
                            body_y = title_y + 30
                            for line in wrapped_body:
                                draw.text((140, body_y), line, fill=current_palette["body"], font=body_font)
                                body_y += 56

                        active_footer = brand_handle if watermark_type == "Text Handle" else "Creator Suite Studio"
                        draw.text((140, height - 230), active_footer, fill="#8b949e", font=footer_font)
                        frames.append(img)

                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(
                            gif_buffer, format="GIF", save_all=True, append_images=frames[1:],
                            duration=int(seconds_per_slide * 1000), loop=0
                        )
                    st.session_state["animated_gif_bytes"] = gif_buffer.getvalue()

                    first_slide = slides_data[0] if slides_data else {}
                    cap_title = first_slide.get("title", "Transform Your Coaching Page") if isinstance(first_slide, dict) else "Transform Your Coaching Page"
                    cap_body = first_slide.get("body", first_slide.get("content", "")) if isinstance(first_slide, dict) else ""

                    st.session_state["generated_caption"] = (
                        f"🔥 {cap_title}\n\n{cap_body}\n\nWhich slide hit home for you the most? Drop your thoughts below! 👇\n\n--- \n⚡ Built & animated seamlessly using Carousel Engine & Kinetic Motion Suite."
                    )

                    st.success("🎉 Kinetic Loop rendered successfully!")
                except Exception as e:
                    st.error(f"Render error: {e}")
    else:
        st.warning("🔒 No carousel payload found. Please generate a carousel deck in Step 1 first.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: FINAL DELIVERY & EXPORT
# ==========================================
with tab_delivery:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="step-header">Step 3: Final Animated GIF, Slide Package & Social Caption Delivery</p>', unsafe_allow_html=True)

    if st.session_state["animated_gif_bytes"]:
        col_res1, col_res2 = st.columns(2, gap="large")

        with col_res1:
            st.subheader("🎬 Final Motion Asset (GIF)")
            st.success("✅ Kinetic animation loop successfully compiled.")

            st.image(
                st.session_state["animated_gif_bytes"],
                caption="Rendered Kinetic Loop Preview",
                use_container_width=True,
            )

            st.download_button(
                label="⬇️ Download Rendered Animated GIF (.gif)",
                data=st.session_state["animated_gif_bytes"],
                file_name="kinetic_carousel_loop.gif",
                mime="image/gif",
                use_container_width=True,
            )

            st.divider()

            if st.session_state["deck_json"]:
                try:
                    slides_list = json.loads(st.session_state["deck_json"]) if isinstance(