import streamlit as st
from carousel_studio_module import render_carousel_studio
from animator_app import render_animator
from audio_module import render_audio_manager
from assembly_module import render_unified_assembler

st.set_page_config(page_title="Creator Suite Platform Hub", layout="wide")

st.sidebar.title("🛠️ Creator Suite Navigation")
nav_choice = st.sidebar.radio(
    "Select Module:",
    [
        "Carousel Studio & Data Bridge",
        "Kinetic Animation Engine",
        "Slide Audio & Voiceover Engine",
        "Unified Export & Assembly Engine"
    ]
)

if "bridge_active_tool" in st.session_state:
    if st.session_state["bridge_active_tool"] == "Kinetic Animator":
        nav_choice = "Kinetic Animation Engine"
    elif st.session_state["bridge_active_tool"] == "Audio & Assembler":
        nav_choice = "Unified Export & Assembly Engine"

if nav_choice == "Carousel Studio & Data Bridge":
    render_carousel_studio()
elif nav_choice == "Kinetic Animation Engine":
    render_animator()
elif nav_choice == "Slide Audio & Voiceover Engine":
    render_audio_manager()
elif nav_choice == "Unified Export & Assembly Engine":
    render_unified_assembler()