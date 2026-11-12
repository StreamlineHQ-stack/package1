# asset_pipeline_controller.py • Controller for the Advanced Asset Pipeline
import streamlit as st

from module_1_background_extractor import render_module_1_ui
from module_2_asset_separator import render_module_2_ui
from module_3_compositor_repositioner import render_module_3_ui
from module_4_terracotta_mode import render_module_4_ui

def render_asset_pipeline_studio(slide_count, api_key):
    st.markdown("### 🛠️ Advanced Visual Asset & Decomposition Studio")
    st.info("Select your extraction and composition mode below:")

    asset_mode_choice = st.radio(
        "Select Pipeline Mode:",
        [
            "Mode 1: Scenic Photography Background Cleaner (Text Removal & Layer Isolation)",
            "Mode 2: Two-Output Subject & Background Separator (Posters & Objects)",
            "Mode 3: Interactive Re-Composition & Repositioning Studio",
            "Mode 4: Terracotta / Solid Color & Font Color Matcher"
        ],
        key="modular_asset_mode_selector_v2"
    )

    st.divider()

    if "Mode 1:" in asset_mode_choice:
        render_module_1_ui(slide_count, api_key)
    elif "Mode 2:" in asset_mode_choice:
        render_module_2_ui(slide_count, api_key)
    elif "Mode 3:" in asset_mode_choice:
        render_module_3_ui(slide_count, api_key)
    elif "Mode 4:" in asset_mode_choice:
        render_module_4_ui(slide_count, api_key)