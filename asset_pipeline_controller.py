# asset_pipeline_controller.py • Controller for the 3-Mode Asset Pipeline
import streamlit as st

# Import your modular sub-files
from module_1_background_extractor import render_module_1_ui
from module_2_asset_separator import render_module_2_ui
from module_3_compositor_repositioner import render_module_3_ui

def render_asset_pipeline_studio(slide_count, api_key):
    st.markdown("### 🛠️ Advanced 3-Mode Visual Asset Studio")
    st.info("Modular workflow: Select an operational mode below to process your reference slide.")

    # Sub-navigation for the 3 distinct asset modes
    asset_mode_choice = st.radio(
        "Select Asset Pipeline Mode:",
        [
            "Mode 1: Scenic / Background Canvas Extractor (Archetype A & Scene Cleaning)",
            "Mode 2: Two-Output Subject & Background Separator (Archetype B Posters)",
            "Mode 3: Interactive Re-Composition & Repositioning Studio"
        ],
        key="modular_asset_mode_selector"
    )

    st.divider()

    # --- ROUTE TO MODULE 1 ---
    if "Mode 1:" in asset_mode_choice:
        render_module_1_ui(slide_count, api_key)

    # --- ROUTE TO MODULE 2 ---
    elif "Mode 2:" in asset_mode_choice:
        render_module_2_ui(slide_count, api_key)

    # --- ROUTE TO MODULE 3 ---
    elif "Mode 3:" in asset_mode_choice:
        render_module_3_ui(slide_count, api_key)