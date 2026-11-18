# platform_hub.py • Master Platform Hub (Onboarding, Dropdown & Tool Router)
import streamlit as st
from license_verifier import verify_license_sidebar
import content_engine_module
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

# Verify License
is_licensed = verify_license_sidebar()
if not is_licensed:
    st.stop()

# Initialize tool navigation state
if "active_tool_idx" not in st.session_state:
    st.session_state["active_tool_idx"] = 0

# --- MASTER ONBOARDING DASHBOARD & 7-BUTTON DIRECT ACCESS ---
st.markdown("<h1 style='text-align: center;'>⚡ Creator Suite: Master Platform Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Welcome to your intelligent direct-response creator workspace.</p>", unsafe_allow_html=True)
st.divider()

# The Sacred Onboarding UI Container with Direct Action Buttons
with st.container(border=True):
    st.markdown("### 🚀 Intelligent Pre-Flight Onboarding & Master Tool Suite")
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    
    with col_inf1:
        if st.button("🧠 Content Engine (Step 1) ➔", key="btn_onboard_content", use_container_width=True):
            st.session_state["active_tool_idx"] = 0
            st.rerun()
        if st.button("🎨 Carousel Studio ➔", key="btn_onboard_carousel", use_container_width=True):
            st.session_state["active_tool_idx"] = 1
            st.rerun()
    with col_inf2:
        if st.button("💡 Feature-to-Benefits ➔", key="btn_onboard_f2b", use_container_width=True):
            st.session_state["active_tool_idx"] = 2
            st.rerun()
        if st.button("✨ Style Inspiration (SIA) ➔", key="btn_onboard_sia", use_container_width=True):
            st.session_state["active_tool_idx"] = 3
            st.rerun()
    with col_inf3:
        if st.button("⚡ Kinetic Animator ➔", key="btn_onboard_kinetic", use_container_width=True):
            st.session_state["active_tool_idx"] = 4
            st.rerun()
        if st.button("🎵 Audio Engine ➔", key="btn_onboard_audio", use_container_width=True):
            st.session_state["active_tool_idx"] = 5
            st.rerun()

    if st.button("🎬 Unified Export, Calendar & Staging Hub ➔", key="btn_onboard_export", use_container_width=True):
        st.session_state["active_tool_idx"] = 6
        st.rerun()

st.divider()

# Optional dropdown switcher synced with active tool state
tool_names = [
    "1. 🧠 Content Engine (Step 1)",
    "2. 🎨 Carousel Engine Studio",
    "3. 💡 Feature-to-Benefits",
    "4. ✨ Style Inspiration (SIA)",
    "5. ⚡ Kinetic Animator (Motion Suite)",
    "6. 🎵 Audio Engine",
    "7. 🎬 Unified Export & Staging Hub",
]

selected_tool = st.selectbox("Select Active Tool Suite:", tool_names, index=st.session_state["active_tool_idx"])
st.session_state["active_tool_idx"] = tool_names.index(selected_tool)
st.divider()

# --- ROUTING BASED ON SELECTED TOOL ---
idx = st.session_state["active_tool_idx"]

if idx == 0:
    content_engine_module.render_content_engine()
elif idx == 1:
    render_carousel_studio()
elif idx == 2:
    feature_to_benefit_app.render()
elif idx == 3:
    sia_studio.render_sia_studio("Style Inspiration (SIA)")
elif idx == 4:
    # Routes to Carousel Studio with Kinetic UI flag or direct animator app
    render_carousel_studio()
elif idx == 5:
    audio_module.render_audio_manager()
elif idx == 6:
    assembly_module.render_unified_assembler()