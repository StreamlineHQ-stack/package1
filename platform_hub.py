# platform_hub.py • Master Platform Hub (Onboarding & Tool Router)
import streamlit as st
from license_verifier import verify_license_sidebar
import feature_to_benefit_app
from carousel_studio_module import render_carousel_studio
import sia_studio
import animator_app
import audio_module
import assembly_module

st.set_page_config(
    page_title="Creator Suite • Master Platform Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit UI artifacts
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# Verify License (persists via session state inside verifier)
is_licensed = verify_license_sidebar()
if not is_licensed:
    st.stop()

# Initialize tool navigation state
if "active_tool_idx" not in st.session_state:
    st.session_state["active_tool_idx"] = 0

# --- BRIDGE SESSION STATE CHECK (Enforces Sequential Flow) ---
if "bridge_active_tool" in st.session_state:
    target = st.session_state["bridge_active_tool"]
    if target == "Kinetic Animator":
        st.session_state["active_tool_idx"] = 3
    elif target == "Audio & Assembler":
        st.session_state["active_tool_idx"] = 5
    del st.session_state["bridge_active_tool"]

# --- MASTER ONBOARDING DASHBOARD & NAVIGATION ---
st.markdown("<h1 style='text-align: center;'>⚡ Creator Suite: Master Platform Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Welcome to your intelligent direct-response creator workspace.</p>", unsafe_allow_html=True)
st.divider()

# The Sacred Onboarding UI Container with Action Buttons
with st.container(border=True):
    st.markdown("### 🚀 Intelligent Pre-Flight Onboarding & Workspace Guide")
    col_inf1, col_inf2, col_inf3, col_inf4 = st.columns(4)
    
    with col_inf1:
        if st.button("Carousel Studio ➔", key="btn_onboard_carousel", use_container_width=True):
            st.session_state["active_tool_idx"] = 0
            st.rerun()
    with col_inf2:
        if st.button("Kinetic Animator ➔", key="btn_onboard_kinetic", use_container_width=True):
            st.session_state["active_tool_idx"] = 3
            st.rerun()
    with col_inf3:
        if st.button("Audio Engine ➔", key="btn_onboard_audio", use_container_width=True):
            st.session_state["active_tool_idx"] = 4
            st.rerun()
    with col_inf4:
        if st.button("Unified Export ➔", key="btn_onboard_export", use_container_width=True):
            st.session_state["active_tool_idx"] = 5
            st.rerun()

st.divider()

# Optional dropdown switcher synced with active tool state
tool_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. 💡 Feature-to-Benefits",
    "3. ✨ Style Inspiration (SIA)",
    "4. ⚡ Kinetic Animation Engine",
    "5. 🎵 Slide Audio & Voiceover Engine",
    "6. 🎬 Unified Export & Assembly Engine",
]

selected_tool = st.selectbox("Select Active Tool Suite:", tool_names, index=st.session_state["active_tool_idx"])
st.session_state["active_tool_idx"] = tool_names.index(selected_tool)
st.divider()

# --- ROUTING BASED ON SELECTED TOOL ---
if st.session_state["active_tool_idx"] == 0:
    render_carousel_studio()

elif st.session_state["active_tool_idx"] == 1:
    feature_to_benefit_app.render()

elif st.session_state["active_tool_idx"] == 2:
    sia_studio.render_sia_studio(selected_tool)

elif st.session_state["active_tool_idx"] == 3:
    animator_app.render_animator()

elif st.session_state["active_tool_idx"] == 4:
    audio_module.render_audio_manager()

elif st.session_state["active_tool_idx"] == 5:
    assembly_module.render_unified_assembler()