# platform_hub.py • ApexMorph Platform Hub & Carousel Engine
import streamlit as st
import base64
from background_engine import get_modular_background

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="ApexMorph • AI Carousel Platform Hub",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR: ONBOARDING & LICENSE AUTH ---
st.sidebar.title("🔐 License & Access")
license_key = st.sidebar.text_input("Enter License Key:", type="password", value="••••••••••••")

if license_key:
    st.sidebar.success("Full 4-Tool Suite Unlocked\n($250 Tier)")

st.sidebar.markdown("---")
st.sidebar.title("🎨 Enhanced Background & Visual Style Engine")

style_mode = st.sidebar.radio(
    "Style Mode Control:",
    [
        "🎯 Smart AI Contextual Match",
        "🏛️ Unified Editorial Motif",
        "📂 Custom User Images",
        "☕ Terracotta Background & White Font"
    ]
)

motif_choice = "editorial-luxury"
uploaded_b64 = ""
custom_url = ""

if style_mode == "🏛️ Unified Editorial Motif":
    st.sidebar.markdown("### 🌸 Custom Motif Theme")
    motif_choice = st.sidebar.text_input(
        "Enter Motif Theme (e.g., Sunset, Rose, Luxury, Ocean, Minimalist, shoes, trains, city):",
        value="city"
    )

if style_mode == "📂 Custom User Images":
    st.sidebar.markdown("### 📤 Upload Asset")
    uploaded_file = st.sidebar.file_uploader("Upload Reference Slide / Background", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            if bytes_data:
                uploaded_b64 = base64.b64encode(bytes_data).decode("utf-8")
        except Exception as e:
            st.sidebar.error(f"Upload error: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Workspace"):
    st.rerun()

# --- MAIN WORKSPACE ONBOARDING UI ---
st.markdown("### 🚀 ApexMorph Content & Carousel Orchestrator")

tab_autopilot, tab_notes = st.tabs(["⚡ Auto-Pilot", "📝 Custom Notes"])

with tab_autopilot:
    core_topic = st.text_input("Core Topic / Hook:", value="High-converting landing page optimization for online coaches")
    
    if st.button("Generate Auto-Pilot Deck", type="primary"):
        st.success("Auto-Pilot Deck generated successfully!")

# --- SLIDE TARGET CONFIG ---
target_slide_count = st.slider("Target Slide Count:", min_value=3, max_value=8, value=6)

st.markdown("---")

# --- SLIDE RENDERING & VISUAL ENGINE LOOP ---
for i in range(target_slide_count):
    if i == 0:
        slide_tag = "SLIDE 1 • HOOK"
        slide_title = f"The Brutal Truth About {core_topic}"
        slide_body = "Most creators struggle with high-converting landing page optimization for online coaches because they lack a systematic, friction-free execution framework."
    elif i == 1:
        slide_tag = "SLIDE 2 • PROBLEM"
        slide_title = "Why Standard Approaches Fail"
        slide_body = "Trying to navigate high-converting landing page optimization for online coaches through sheer guesswork leads to high friction, constant burnout, and stalled momentum."
    elif i == 2:
        slide_tag = "SLIDE 3 • AGITATION"
        slide_title = "The True Cost of Inaction"
        slide_body = "Every single day you delay fixing this wastes valuable hours, drains your energy, and leaves high-value opportunities on the table."
    elif i == 3:
        slide_tag = "SLIDE 4 • SOLUTION"
        slide_title = "The Streamlined Solution"
        slide_body = "Enter the streamlined blueprint: a zero-friction system built specifically to master high-converting landing page optimization for online coaches without the fluff."
    elif i == 4:
        slide_tag = "SLIDE 5 • PROOF"
        slide_title = "Engineered for Efficiency"
        slide_body = "Built for speed, high visual contrast, and direct-response impact that commands attention in a crowded feed."
    else:
        slide_tag = f"SLIDE {i+1} • ACTION"
        slide_title = "Take Control Today"
        slide_body = "Stop guessing, stop spinning your wheels, and start executing with precision infrastructure."

    # Resolve background dynamically via background_engine.py
    bg_url = get_modular_background(
        style_mode=style_mode,
        motif_choice=motif_choice,
        slide_index=i,
        slide_tag=slide_tag,
        uploaded_b64=uploaded_b64,
        custom_url=custom_url
    )

    # Render Card Preview
    col_prev, col_nav = st.columns([1, 0.1])
    
    if bg_url:
        st.markdown(
            f"""
            <div style="background-image: url('{bg_url}'); background-size: cover; background-position: center; padding: 50px; border-radius: 16px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <span style="background-color: rgba(0,0,0,0.6); padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; color: #ffcc00; letter-spacing: 1px;">{slide_tag}</span>
                <h2 style="margin-top: 15px; margin-bottom: 10px; font-size: 28px; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">{slide_title}</h2>
                <p style="font-size: 16px; line-height: 1.5; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">{slide_body}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #c45c3d; padding: 50px; border-radius: 16px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <span style="background-color: rgba(0,0,0,0.3); padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; letter-spacing: 1px;">{slide_tag}</span>
                <h2 style="margin-top: 15px; margin-bottom: 10px; font-size: 28px; font-weight: 800;">{slide_title}</h2>
                <p style="font-size: 16px; line-height: 1.5;">{slide_body}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Bottom action navigation
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    st.button("← Previous")
with col_btn2:
    st.button("Next →")

st.markdown("---")
st.button("🚀 Send to Kinetic Motion Engine", type="primary", use_container_width=True)