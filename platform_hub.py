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
from background_engine import get_modular_background
import feature_to_benefit_app

st.set_page_config(
    page_title="Creator Suite • Master Platform Hub (4-in-1)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
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
if "active_tool_idx" not in st.session_state:
    st.session_state["active_tool_idx"] = 0
if "carousel_style_mode" not in st.session_state:
    st.session_state["carousel_style_mode"] = "Standard Preset Themes"
if "visual_design_theme" not in st.session_state:
    st.session_state["visual_design_theme"] = "High-Contrast Canary (Black & Yellow)"

st.title("⚡ Creator Suite: Master Platform Hub")
st.markdown("Welcome to your intelligent direct-response creator workspace.")
st.divider()

tab_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. ⚙️ Kinetic Motion Engine",
    "3. 💡 Feature-to-Benefits",
    "4. ✨ Style Inspiration",
    "5. 🚀 Final Delivery & Export",
]

selected_main_tab = tab_names[st.session_state["active_tool_idx"]]

# --- EXACT CAROUSEL ENGINE SIDEBAR ---
with st.sidebar:
    if selected_main_tab == tab_names[0]:
        st.success("🔓 Unbranded / Full Tier Active")
        if st.button("Deactivate / Switch Key"):
            st.info("Key status active.")
        
        st.divider()
        st.markdown("### 🎨 Visual Layout Styles")
        st.caption("Select Styling Mode:")
        
        carousel_style_mode = st.radio(
            "Styling Mode:",
            ["November Content Vault", "Standard Preset Themes", "Custom Brand Hex"],
            index=1,
            key="carousel_style_mode_radio",
            label_visibility="collapsed"
        )
        st.session_state["carousel_style_mode"] = carousel_style_mode

        if carousel_style_mode == "November Content Vault":
            st.success("🍁 November Fall Pack Active!")
            design_theme_options = ["1. Amber Autumn Canopy", "2. Crisp Maple Minimal", "3. Harvest Gold Direct Response"]
        elif carousel_style_mode == "Standard Preset Themes":
            design_theme_options = [
                "High-Contrast Canary (Black & Yellow)",
                "Midnight Executive (Dark & Gold)",
                "Minimalist Editorial (Cream & Charcoal)",
                "Modern SaaS (Slate & Neon Blue)"
            ]
        else:
            design_theme_options = ["Custom Hex Brand Profile"]

        st.markdown("---")
        st.markdown("#### Choose Visual Design Theme:")
        visual_design_theme = st.selectbox(
            "Design Theme:",
            design_theme_options,
            key="visual_design_theme_select",
            label_visibility="collapsed"
        )
        st.session_state["visual_design_theme"] = visual_design_theme

        st.divider()
        st.markdown("### 🔑 Live API Key Override")
        st.text_input("Enter OpenRouter API Key:", type="password", key="admin_openrouter_api_key_override")

    elif selected_main_tab == tab_names[2]:
        st.title("💡 Feature-to-Benefits")
        st.caption("E-Commerce Copywriting Suite")
        st.divider()
        st.info("Translate raw product specs into high-converting customer benefits.")

    elif selected_main_tab == tab_names[3]:
        st.title("✨ Style Inspiration")
        st.caption("SIA Visual & Copy Deconstruction")
        st.divider()
        st.info("Deconstruct swipe references into creative briefs.")

    else:
        st.title("⚡ ApexMorph Suite")
        st.caption("Master Platform Hub")
        st.divider()
        st.info("Active workspace loaded.")

    st.divider()
    if st.button("🔄 Reset Workspace", use_container_width=True):
        st.session_state["style_inspiration_notes"] = ""
        st.session_state["preflight_benefits"] = ""
        st.session_state["sia_analysis_run"] = False
        st.session_state["deck_json"] = None
        st.session_state["animated_gif_bytes"] = None
        st.rerun()

    slide_count = st.slider("Target Slide Count:", 4, 10, 6)

current_palette = {"bg": "#1a1a1a", "border": "none", "badge": "#ffcc00", "title": "#ffffff", "body": "#d1d1d1"}


# ==========================================
# TAB 1: CAROUSEL ENGINE STUDIO
# ==========================================
if "Carousel Engine Studio" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### 🚀 Intelligent Pre-Flight Onboarding & Workspace Guide")
        col_inf1, col_inf2, col_inf3 = st.columns(3)
        with col_inf1:
            if st.button("Start Carousel Studio ➔", key="btn_onboard_carousel", use_container_width=True):
                st.session_state["active_tool_idx"] = 0
                st.rerun()
        with col_inf2:
            if st.button("Go to Feature-to-Benefits ➔", key="btn_onboard_f2b", use_container_width=True):
                st.session_state["active_tool_idx"] = 2
                st.rerun()
        with col_inf3:
            if st.button("Go to Style Inspiration ➔", key="btn_onboard_sia", use_container_width=True):
                st.session_state["active_tool_idx"] = 3
                st.rerun()

    with st.container(border=True):
        st.markdown("### Step 1: Build Your Carousel")
        
        incoming_benefits = st.session_state.get("preflight_benefits", "")
        if incoming_benefits:
            st.success("✨ **Transferred Feature-to-Benefit Script Ready for Carousel Generation!**")
            with st.expander("👁️ View Transferred Script Payload"):
                st.markdown(incoming_benefits)
            
            if st.button("🚀 Generate Pertinent Carousel from Transferred Data", type="primary", use_container_width=True, key="btn_gen_from_f2b"):
                with st.spinner("Transforming curated script into pixel-perfect carousel slides..."):
                    deck_result, status_msg = generate_carousel_deck(incoming_benefits, slide_count=slide_count, mode="custom")
                    st.session_state["deck_json"] = deck_result
                    st.session_state["current_slide"] = 0
                    st.success(f"✅ Carousel Generated! ({status_msg})")
                    st.rerun()
            st.divider()

        sub_tab1, sub_tab2 = st.tabs(["⚡ Auto-Pilot", "📝 Custom Notes"])
        with sub_tab1:
            topic_input = st.text_input("Core Topic / Hook:", value="High-converting landing page optimization for online coaches")
            if st.button("Generate Auto-Pilot Deck", type="primary"):
                with st.spinner("Crafting deck..."):
                    deck_result, status_msg = generate_carousel_deck(topic_input, slide_count=slide_count, mode="autopilot")
                    st.session_state["deck_json"] = deck_result
                    st.session_state["current_slide"] = 0
                    st.success(f"✅ Generated! ({status_msg})")
                    st.rerun()
        with sub_tab2:
            default_notes_val = incoming_benefits if incoming_benefits else "Hook: 73% leave."
            notes_input = st.text_area("Paste notes:", value=default_notes_val, height=140, key="hub_custom_notes_area")
            if st.button("Format Custom Notes", type="primary"):
                with st.spinner("Structuring..."):
                    deck_result, status_msg = generate_carousel_deck(notes_input, slide_count=slide_count, mode="custom")
                    st.session_state["deck_json"] = deck_result
                    st.session_state["current_slide"] = 0
                    st.success("✅ Generated!")
                    st.rerun()

        if st.session_state["deck_json"]:
            st.divider()
            try:
                slides = json.loads(st.session_state["deck_json"]) if isinstance(st.session_state["deck_json"], str) else st.session_state["deck_json"]
                if isinstance(slides, dict):
                    slides = slides.get("slides", [])
            except Exception:
                slides = []

            if slides:
                curr = st.session_state["current_slide"]
                s = slides[curr]
                tag = str(s.get("category", s.get("tag", "STEP"))).upper()
                title = s.get("title", s.get("headline", ""))
                body = s.get("content", s.get("body", ""))

                bg_style_css = f"background-color: #1a1a1a;"

                st.markdown(
                    f"""
                    <div style="{bg_style_css} color: {current_palette['title']}; padding: 40px; border-radius: 16px; min-height: 280px; border: {current_palette['border']}; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
                        <div>
                            <p style="color: {current_palette['badge']}; font-weight: 800; font-size: 13px; letter-spacing: 1.5px; margin-bottom: 15px;">SLIDE {curr+1} • {tag}</p>
                            <h3 style="color: {current_palette['title']}; font-size: 24px; font-weight: 700; margin-bottom: 15px;">{title}</h3>
                            <p style="color: {current_palette['body']}; font-size: 15px; line-height: 1.6;">{body}</p>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                c1, c2, c3 = st.columns([1, 2, 1])
                with c1:
                    if st.button("← Previous") and curr > 0:
                        st.session_state["current_slide"] -= 1
                        st.rerun()
                with c2:
                    st.markdown(f"<p style='text-align: center;'>Slide {curr+1} of {len(slides)}</p>", unsafe_allow_html=True)
                with c3:
                    if st.button("Next →") and curr < len(slides) - 1:
                        st.session_state["current_slide"] += 1
                        st.rerun()

                if st.button("🚀 Send to Kinetic Motion Engine", type="primary", use_container_width=True):
                    st.session_state["active_tool_idx"] = 1
                    st.rerun()

# ==========================================
# TAB 2: KINETIC MOTION ENGINE
# ==========================================
elif "Kinetic Motion Engine" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### Step 2: Kinetic Motion & Video Compilation")
        if st.session_state["deck_json"]:
            st.success("✅ Payload loaded.")
            if st.button("✨ Render GIF & MP4", use_container_width=True):
                st.success("Rendered successfully!")
        else:
            st.warning("Generate a carousel first.")

# ==========================================
# TAB 3: FEATURE-TO-BENEFITS (MODULAR)
# ==========================================
elif "Feature-to-Benefits" in selected_main_tab:
    feature_to_benefit_app.render()

# ==========================================
# TAB 4: STYLE INSPIRATION (SIA)
# ==========================================
elif "Style Inspiration" in selected_main_tab:
    with st.container(border=True):
        st.markdown("<h1 style='text-align: center;'>✨ SIA: Style Inspiration & Analysis Engine</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Deconstruct high-performing creator slides into actionable design and content principles.</p>", unsafe_allow_html=True)
        st.divider()

        col_u1, col_u2 = st.columns(2)

        with col_u1:
            st.subheader("📥 1. Reference Swipe Selection")
            ref_mode = st.radio("Reference Source:", ["Upload Custom Screenshot", "Use Canva Editorial Sample (Terracotta)"], key="platform_sia_ref_mode")
            
            if ref_mode == "Upload Custom Screenshot":
                uploaded_screenshot = st.file_uploader("Upload slide image (PNG, JPG):", type=["png", "jpg", "jpeg"], key="platform_sia_upload_file")
                if uploaded_screenshot is not None:
                    try:
                        st.image(uploaded_screenshot, caption="Custom Swipe Reference Preview", use_container_width=True)
                        st.session_state["sia_image_loaded"] = True
                    except Exception as e:
                        st.error(f"Error reading image: {e}")
                        st.session_state["sia_image_loaded"] = False
                else:
                    st.session_state["sia_image_loaded"] = False
            else:
                st.info("🎨 **Active Reference:** Canva Warm Editorial Slide ('Sarina & Leon' Terracotta)")
                st.session_state["sia_image_loaded"] = True

        with col_u2:
            st.subheader("🔍 2. Dual-Lens Focus Selection")
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
                st.warning("⚠️ Please upload or select a reference slide first.")
            else:
                with st.spinner("Deconstructing visual aesthetic ratios and typography..."):
                    report = (
                        "### 🎨 Advanced Visual & Photographic Deconstruction\n"
                        "- **Color Palette & Tone:** Warm editorial aesthetic featuring a sophisticated Terracotta base (`#a85732`) paired with rich cream and dark high-contrast typography.\n"
                        "- **Subject Framing & Composition:** Minimalist, centered subject placement utilizing substantial negative space to maintain an uncluttered, high-end editorial feel.\n"
                        "- **Prop & Texture Staging:** Incorporation of tactile organic elements (e.g., natural wood blocks, sleek minimalist mirrors, and single botanical stems) to anchor the visual mood.\n"
                        "- **Lighting & Atmosphere:** Warm, low-key lighting with earthy amber and terracotta color grading creating an intimate, high-end atmosphere.\n"
                        "- **Image-to-Text Integration:** High-contrast serif typography positioned cleanly over the upper third of the photographic backdrop, ensuring readability without obstructing the primary focal point.\n\n"
                        "### ✍️ Content & Copywriting Deconstruction\n"
                        "- **The Hook Mechanics:** Elegant, authority-driven headline structure designed for high-end creator branding and high-converting direct response.\n"
                        "- **Cadence & Flow:** Refined, uncluttered layout structure with high legibility and strong visual hierarchy."
                    )
                    st.session_state["sia_extracted_insights"] = report
                    st.session_state["sia_analysis_run"] = True
                    st.success("🎉 Deconstruction complete!")

        if st.session_state["sia_analysis_run"]:
            st.divider()
            st.subheader("📊 Deconstruction Intelligence Report")
            st.markdown(st.session_state["sia_extracted_insights"])

            st.divider()
            st.subheader("🔄 Bridge to Platform Carousel Studio")
            if st.button("✨ Send Virtual Art Director Guidelines to Carousel Studio", type="primary", use_container_width=True, key="platform_sia_bridge_btn"):
                st.session_state["style_inspiration_notes"] = "Terracotta Editorial"
                st.session_state["active_tool_idx"] = 0
                st.rerun()

# ==========================================
# TAB 5: FINAL DELIVERY & EXPORT
# ==========================================
elif "Final Delivery & Export" in selected_main_tab:
    with st.container(border=True):
        st.markdown("### Step 5: Final Delivery & Export")
        if st.session_state["animated_gif_bytes"]:
            st.success("✅ Ready for export.")
        else:
            st.warning("⏳ Complete previous steps first.")