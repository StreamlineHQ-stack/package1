# platform_hub.py • Master Platform Hub (4-in-1 Suite)
import streamlit as st
from license_verifier import verify_license_sidebar
import feature_to_benefit_app
from carousel_studio_module import render_carousel_studio

st.set_page_config(
    page_title="Creator Suite • Master Platform Hub (4-in-1)",
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

# Initialize session state tracking
if "active_tool_idx" not in st.session_state:
    st.session_state["active_tool_idx"] = 0

st.title("⚡ Creator Suite: Master Platform Hub")
st.markdown("Welcome to your intelligent direct-response creator workspace.")
st.divider()

# Master Tab Navigation
tab_names = [
    "1. 🎨 Carousel Engine Studio",
    "2. 💡 Feature-to-Benefits",
    "3. ✨ Style Inspiration (SIA)",
    "4. 🚀 Final Delivery & Export",
]

selected_main_tab = st.selectbox("Select Active Tool Suite:", tab_names, index=st.session_state["active_tool_idx"])

# Map selection back to index
st.session_state["active_tool_idx"] = tab_names.index(selected_main_tab)
st.divider()

# --- TOOL ROUTING ---
if "Carousel Engine Studio" in selected_main_tab:
    render_carousel_studio()

elif "Feature-to-Benefits" in selected_main_tab:
    feature_to_benefit_app.render()

elif "Style Inspiration" in selected_main_tab:
    st.markdown("### ✨ Style Inspiration (SIA) Engine")
    st.info("Upload swipe references and configure your visual style engine parameters.")

elif "Final Delivery & Export" in selected_main_tab:
    st.markdown("### 🚀 Final Delivery & Export Suite")
    st.success("Ready to export your completed master assets and media payloads.")