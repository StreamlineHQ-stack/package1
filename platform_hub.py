# platform_hub.py • Master Platform Hub (Onboarding & Tool Router)
import streamlit as st
from license_verifier import verify_license_sidebar
import content_engine_module
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

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

is_licensed = verify_license_sidebar()
if not is_licensed:
    st.stop()

if "active_tool_idx" not in st.session_state:
    st.session_state["active_tool_idx"] = 0

st.markdown("<h1 style='text-align: center;'>⚡ Creator Suite: Master Platform Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Welcome to your intelligent direct-response creator workspace.</p>", unsafe_allow_html=True)
st.divider()

with st.container(border=True):
    st.markdown("### 🚀 Master Tool Suite Direct Access")
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1:
        if st.button("🧠 Content Engine (Step 1)", key="btn_tool_content", use_container_width=True):
            st.session_state["active_tool_idx"] = 0
            st.rerun()
        if st.button("🎨 Carousel Studio", key="btn_tool_carousel", use_container_width=True):
            st.session_state["active_tool_idx"] = 1
            st.rerun()
    with col_inf2:
        if st.button("💡 Feature-to-Benefits", key="btn_tool_f2b", use_container_width=True):
            st.session_state["active_tool_idx"] = 2
            st.rerun()
        if st.button("✨ Style Inspiration (SIA)", key="btn_tool_sia", use_container_width=True):
            st.session_state["active_tool_idx"] = 3
            st.rerun()
    with col_inf3:
        if st.button("⚡ Kinetic Animator", key="btn_tool_kinetic", use_container_width=True):
            st.session_state["active_tool_idx"] = 4
            st.rerun()
        if st.button("🎵 Audio Engine", key="btn_tool_audio", use_container_width=True):
            st.session_state["active_tool_idx"] = 5
            st.rerun()

    # Full width row for Unified Export
    if st.button("🎬 Unified Export & Staging Hub", key="btn_tool_export", use_container_width=True):
        st.session_state["active_tool_idx"] = 6
        st.rerun()

st.divider()

idx = st.session_state["active_tool_idx"]

if idx == 0:
    content_engine_module.render_content_engine()
elif idx == 1:
    render_carousel_studio()
elif idx == 2:
    import feature_to_benefit_app
    feature_to_benefit_app.render()
elif idx == 3:
    sia_studio.render_sia_studio("Style Inspiration (SIA)")
elif idx == 4:
    animator_app.render_animator()
elif idx == 5:
    audio_module.render_audio_manager()
elif idx == 6:
    assembly_module.render_unified_assembler()