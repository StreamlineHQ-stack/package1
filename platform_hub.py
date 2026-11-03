import io
import json
import os
import base64
import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Import your core engine modules
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from image_renderer import generate_png_zip_from_slides

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Creator Suite • Master Platform Hub (4-in-1)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM SAAS STYLING ---
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .card { background-color: #161b22; padding: 25px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 20px; }
    .step-header { color: #58a6ff; font-weight: bold; font-size: 1.2rem; margin-bottom: 10px; }
    .stButton>button { background-color: #ffcc00; color: #0e1117; font-weight: bold; border-radius: 6px; border: none; }
    .stButton>button:hover { background-color: #e6b800; color: #0e1117; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SESSION STATE INITIALIZATION ---
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


# --- COMPLETE 10-THEME & FONT STYLE DICTIONARY ---
THEME_OPTIONS = {
    "High-Contrast Canary": "⚡ High-Contrast Canary (Black & Yellow)",
    "Warning Red Alert": "🚨 Warning Red Alert (Charcoal & Crimson)",
    "Minimalist Clean": "💎 Minimalist Clean (White & Charcoal)",
    "Warm Editorial": "☕ Warm Editorial (Cream & Terracotta)",
    "Neon Cyber/Tech": "⚡ Neon Cyber/Tech (Obsidian & Cyan)",
    "Midnight Luxury": "👑 Midnight Luxury (Dark Obsidian & Gold)",
    "Emerald Growth": "📈 Emerald Growth (Deep Forest & Mint)",
    "Nordic Slate": "❄️ Nordic Slate (Slate Grey & Soft Ice Blue)",
    "Bold Coral Pop": "🔥 Bold Coral Pop (Dark Coral & Warm Cream)",
    "Monochrome Obsidian": "🖤 Monochrome Obsidian (Pure Dark & Crisp White)"
}

def get_theme_palette(style_theme, custom_colors=None):
    if style_theme == "Custom" and custom_colors:
        return {
            "bg": custom_colors["bg"], "border": custom_colors["border"], "badge": custom_colors["tag"], 
            "title": custom_colors["text"], "body": custom_colors["body"], "font_family": "Inter", "title_weight": "700", "body_weight": "400"
        }
    elif style_theme == "Warning Red Alert":
        return {"bg": "#181212", "border": "1px solid #3d2222", "badge": "#ef4444", "title": "#ffffff", "body": "#e5cdc5", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Minimalist Clean":
        return {"bg": "#ffffff", "border": "1px solid #e0e0e0", "badge": "#0066cc", "title": "#111111", "body": "#444444", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Warm Editorial":
        return {"bg": "#fbf9f5", "border": "1px solid #e6dfd3", "badge": "#a85732", "title": "#2c221e", "body": "#5c4e47", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Neon Cyber/Tech":
        return {"bg": "#0b0f19", "border": "1px solid #1e293b", "badge": "#06b6d4", "title": "#f8fafc", "body": "#94a3b8", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Midnight Luxury":
        return {"bg": "#121212", "border": "1px solid #2a2415", "badge": "#d4af37", "title": "#f5e6c8", "body": "#d4c5a9", "font_family": "Inter", "title_weight": "600", "body_weight": "400"}
    elif style_theme == "Emerald Growth":
        return {"bg": "#0a1f1c", "border": "1px solid #133e38", "badge": "#10b981", "title": "#e6f4f1", "body": "#a3cbd0", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Nordic Slate":
        return {"bg": "#1e242b", "border": "1px solid #334155", "badge": "#38bdf8", "title": "#f1f5f9", "body": "#cbd5e1", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Bold Coral Pop":
        return {"bg": "#231818", "border": "1px solid #422929", "badge": "#ff6b6b", "title": "#fff0ed", "body": "#e2c4be", "font_family": "Inter", "title_weight": "700", "body_weight": "400"}
    elif style_theme == "Monochrome Obsidian":
        return {"bg": "#000000", "border": "1px solid #262626", "badge": "#ffffff", "title": "#ffffff", "body": "#a3a3a3", "font_family":