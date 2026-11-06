import io
import json
import os
import re
import base64
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Page Configuration
st.set_page_config(
    page_title="Kinetic Motion Suite — Carousel Engine Studio",
    page_icon="🎬",
    layout="wide",
)

# --- IMMEDIATE GLOBAL QUERY PARAMETER & SESSION INTERCEPTION ---
if "slides_data" not in st.session_state:
    st.session_state.slides_data = None

try:
    deck_param = st.query_params.get("deck", None)
    if deck_param and st.session_state.slides_data is None:
        if isinstance(deck_param, list):
            encoded_deck = deck_param[0]
        else:
            encoded_deck = deck_param
            
        padded_deck = encoded_deck + "=" * (-len(encoded_deck) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded_deck.encode("utf-8"))
        deck_content = json.loads(decoded_bytes.decode("utf-8"))
        
        if isinstance(deck_content, list) and len(deck_content) > 0:
            st.session_state.slides_data = deck_content
except Exception as e:
    pass

# Fallback default if no incoming deck was captured
if st.session_state.slides_data is None:
    st.session_state.slides_data = [
        {
            "category": "Hook",
            "title": "Time Is Your Only Non-Renewable Resource",
            "content": (
                "Money can be earned back. Energy can be restored. But every"
                " second spent is gone forever."
            ),
        }
    ]

# Custom Styling for Dark Theme & Canary Accents
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ffcc00;
        color: #0e1117;
        font-weight: bold;
        border-radius: 6px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e6b800;
        color: #0e1117;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Motion Controls (Fully Unlocked)
st.sidebar.title("🎬 Carousel Engine")
st.sidebar.markdown("### Kinetic Motion Suite")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Pro Motion Control")
frame_rate = st.sidebar.slider("Frame Rate (FPS):", 10, 60, 20)
seconds_per_slide = st.sidebar.slider(
    "Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25
)
transition_style = st.sidebar.selectbox(
    "Kinetic Transition Style:",
    [
        "Dynamic Slide Up (Pro Easing)",
        "Smooth Slide Right",
        "Cinematic Zoom In",
        "Fade & Snap",
    ],
)
transition_speed = st.sidebar.slider("Transition Speed (Frames):", 2, 15, 6)


# Pixel-perfect text wrapping helper function
def wrap_text_to_width(text, font, max_width, draw):
  words = text.split()
  lines = []
  current_line = []
  for word in words:
    test_line = " ".join(current_line + [word])
    if draw.textlength(test_line, font=font) <= max_width:
      current_line.append(word)
    else:
      if current_line:
        lines.append(" ".join(current_line))
      current_line = [word]
  if current_line:
    lines.append(" ".join(current_line))
  return lines


# Main App Execution (Directly Rendered, Fully Unlocked)
st.markdown("## 🎞️ Import Carousel JSON Deck")

if st.query_params.get("deck") or st.session_state.slides_data:
    st.success(f"🚀 Successfully loaded {len(st.session_state.slides_data)} slides into Kinetic Animator!")

uploaded_file = st.file_uploader(
    "Upload JSON deck file (Cloud / Live Mode):",
    type=["json"],
    help="Drop your exported JSON file here",
)
deck_loaded = False

if uploaded_file is not None:
  try:
    deck_content = json.load(uploaded_file)
    if isinstance(deck_content, list):
      st.session_state.slides_data = deck_content
    elif isinstance(deck_content, dict) and "slides" in deck_content:
      st.session_state.slides_data = deck_content["slides"]
    else:
      st.session_state.slides_data = [
          {"title": k, "content": v} for k, v in deck_content.items()
      ]
    deck_loaded = True
    st.success(
        f"Successfully loaded {len(st.session_state.slides_data)} slides from"
        f" {uploaded_file.name}!"
    )
  except Exception as e:
    pass

if not deck_loaded and not st.query_params.get("deck"):
  json_files = [f for f in os.listdir(".") if f.endswith(".json")]
  if json_files:
    selected_json = st.selectbox(
        "Or select a local workspace deck (Local Mode):", json_files
    )
    if selected_json:
      try:
        with open(selected_json, "r", encoding="utf-8") as f:
          deck_content = json.load(f)
          if isinstance(deck_content, list):
            st.session_state.slides_data = deck_content
          elif isinstance(deck_content, dict) and "slides" in deck_content:
            st.session_state.slides_data = deck_content["slides"]
          else:
            st.session_state.slides_data = [
                {"title": k, "content": v} for k, v in deck_content.items()
            ]
          st.success(
              f"Successfully loaded {len(st.session_state.slides_data)} slides"
              f" from {selected_json}!"
          )
      except Exception as e:
        st.error(f"Error loading {selected_json}: {e}")

st.markdown("---")
st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")

with st.container():
  col1, col2 = st.columns([1.2, 1])

  with col1:
    st.markdown("### Slide Sequence Overview")
    for idx, slide in enumerate(st.session_state.slides_data, start=1):
      title_text = (
          slide.get("title", f"Slide {idx}")
          if isinstance(slide, dict)
          else str(slide)
      )
      st.markdown(f"**Slide {idx}:** {title_text}")

  with col2:
    st.markdown("### Production Render Engine")
    render_btn = st.button(
        "✨ Render Premium Kinetic Loop (Active Deck)",
        use_container_width=True,
    )

    if render_btn:
      with st.spinner(
          "Rendering animation frames with exact Terracotta theme (#a85732)..."
      ):
        frames = []
        width, height = 1080, 1080  # Square Instagram ratio
        max_text_width = 880

        # Exact Terracotta Background matching SIA Terracotta Module (#a85732)
        bg_img = Image.new("RGB", (width, height), color="#a85732")

        font_path = "arialbd.ttf" if os.path.exists("arialbd.ttf") else None
        try:
          if font_path and os.path.exists(font_path):
            badge_font = ImageFont.truetype(font_path, 28)
            title_font = ImageFont.truetype(font_path, 52)
            body_font = ImageFont.truetype(font_path, 36)
            footer_font = ImageFont.truetype(font_path, 24)
          else:
            badge_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            footer_font = ImageFont.load_default()
        except IOError:
          badge_font = ImageFont.load_default()
          title_font = ImageFont.load_default()
          body_font = ImageFont.load_default()
          footer_font = ImageFont.load_default()

        total_slides = len(st.session_state.slides_data)
        for idx, slide in enumerate(st.session_state.slides_data, start=1):
          if isinstance(slide, dict):
            category = str(
                slide.get(
                    "category", slide.get("badge", f"STEP {idx}")
                )
            ).upper()
            title = str(slide.get("title", f"Slide {idx}"))
            body = str(
                slide.get(
                    "content",
                    slide.get("body", "Key actionable breakdown..."),
                )
            )
          else:
            category = f"STEP {idx}"
            title = str(slide)
            body = ""

          img = bg_img.copy()
          draw = ImageDraw.Draw(img)

          margin_x = 100
          current_y = 160

          # Draw Header Tag (Matching Terracotta style: SLIDE X OF Y • CATEGORY in gold #ffcc00)