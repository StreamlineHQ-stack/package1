# platform_hub.py • Master Platform Hub (Onboarding & Tool Router)
import streamlit as st
from license_verifier import verify_license_sidebar
import feature_to_benefit_app
from carousel_studio_module import render_carousel_studio

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

# --- MASTER ONBOARDING DASHBOARD & 3-BUTTON LAYOUT ---
st.markdown("<h1 style='text-align: center;'>⚡ Creator Suite: Master Platform Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Welcome to your intelligent direct-response creator workspace.</p>", unsafe_allow_html=True)
st.divider()

# The Sacred Onboarding UI Container with 3 Action Buttons
with st.container(border=True):
    st.markdown("### 🚀 Intelligent Pre-Flight Onboarding & Workspace Guide")
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    
    with col_inf1:
        if st.button("Start Carousel Studio ➔", key="btn_onboard_carousel", use_container_width=True):
            st.session_state["active_tool_idx"] = 0
            st.rerun()
    with col_inf2:
        if st.button("Go to Feature-to-Benefits ➔", key="btn_onboard_f2b", use_container_width=True):
            st.session_state["active_tool_idx"] = 1
            st.rerun()
    with col_inf3:
        if st.button("Go to Style Inspiration ➔", key="btn_onboard_sia", use_container_width=True):
            st.session_state["active_tool_idx"] = 2
            st.rerun()

st.divider()

# Optional dropdown switcher synced with active tool state
tool_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. 💡 Feature-to-Benefits",
    "3. ✨ Style Inspiration (SIA)",
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
    st.markdown("### ✨ Style Inspiration & Analysis (SIA)")
    st.info("Upload reference swipe slides and configure visual style engine parameters.")