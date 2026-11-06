import io
import json
import os
import requests
import re
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from license_verifier import verify_license_sidebar

# Page Configuration
st.set_page_config(
    page_title="Kinetic Motion Suite — Carousel Engine Studio",
    page_icon="🎬",
    layout="wide",
)

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

# Sidebar License Verification Gate
is_licensed = verify_license_sidebar()

# Sidebar Motion Controls (Available when licensed)
if is_licensed:
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
else:
  frame_rate, seconds_per_slide, transition_style, transition_speed = (
      20,
      2.5,
      "Dynamic Slide Up (Pro Easing)",
      6,
  )


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


# Main App Execution
if is_licensed:
  st.sidebar.title("🎬 Carousel Engine")
  st.sidebar.markdown("### Kinetic Motion Suite")

  st.markdown("## 🎞️ Import Carousel JSON Deck")

  if "slides_data" not in st.session_state:
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

  if not deck_loaded:
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
    else:
      st.info(
          "📁 Using active preview deck. Upload or place a JSON deck in your"
          " workspace anytime."
      )

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
            "Rendering animation frames matching exact November Fall theme"
            " & typography..."
        ):
          frames = []
          width, height = 1080, 1080  # Square Instagram ratio
          max_text_width = 880

          # Load exact November Fall theme forest background texture matching main app
          bg_img = None
          november_texture_url = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=1080&q=80"
          try:
            res = requests.get(november_texture_url, timeout=5)
            if res.status_code == 200:
              tex = Image.open(io.BytesIO(res.content)).convert("RGB")
              tex = tex.resize((width, height), Image.Resampling.LANCZOS)
              overlay = Image.new("RGB", (width, height), color="#120c08")
              bg_img = Image.blend(tex, overlay, alpha=0.82)
          except Exception:
            pass

          if not bg_img:
            bg_img = Image.new("RGB", (width, height), color="#1a120b")

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

            # Start directly from exact November Fall background canvas
            img = bg_img.copy()
            draw = ImageDraw.Draw(img)

            margin_x = 100
            current_y = 160

            # Draw Header Tag (Matching main app: SLIDE X • CATEGORY in gold #ffcc00)
            header_text = f"SLIDE {idx} • {category}"
            draw.text(
                (margin_x, current_y), header_text, fill="#ffcc00", font=badge_font
            )
            current_y += 70

            # Draw Title (Wrapped, crisp white #ffffff)
            wrapped_title = wrap_text_to_width(
                title, title_font, max_text_width, draw
            )
            for line in wrapped_title:
              draw.text(
                  (margin_x, current_y), line, fill="#ffffff", font=title_font
              )
              current_y += 65

            current_y += 30

            # Draw Body Content (Wrapped, soft light gray #c9d1d9)
            if body:
              wrapped_body = wrap_text_to_width(
                  body, body_font, max_text_width, draw
              )
              for line in wrapped_body:
                draw.text(
                    (margin_x, current_y),
                    line,
                    fill="#c9d1d9",
                    font=body_font,
                )
                current_y += 48

            # Draw Footer Watermark (Matching main app preview exactly: "Nikki's Salon")
            draw.text(
                (width - 320, height - 100),
                "Nikki's Salon",
                fill="#c9d1d9",
                font=footer_font,
            )

            frames.append(img)

          # Render GIF buffer
          gif_buffer = io.BytesIO()
          if frames:
            frames[0].save(
                gif_buffer,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                duration=int(seconds_per_slide * 1000),
                loop=0,
            )
          gif_bytes = gif_buffer.getvalue()

          # Render MP4 video buffer with correct frame pacing
          mp4_bytes = None
          try:
            import imageio
            import numpy as np

            fps = int(frame_rate)
            frames_per_slide = int(fps * seconds_per_slide)

            paced_frames = []
            for f in frames:
              np_f = np.array(f)
              for _ in range(frames_per_slide):
                paced_frames.append(np_f)

            mp4_path = "temp_kinetic_deck.mp4"
            imageio.mimwrite(
                mp4_path,
                paced_frames,
                fps=fps,
                codec="libx264",
                quality=8,
                pixelformat="yuv420p",
            )
            with open(mp4_path, "rb") as mf:
              mp4_bytes = mf.read()
            os.remove(mp4_path)
          except Exception:
            mp4_bytes = None

        st.success("🎉 Kinetic Loop rendered successfully!")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
          st.download_button(
              label="⬇️ Download Animated GIF",
              data=gif_bytes,
              file_name="kinetic_carousel_loop.gif",
              mime="image/gif",
              use_container_width=True,
          )

        with col_d2:
          if mp4_bytes:
            st.download_button(
                label="🎬 Download Instagram MP4",
                data=mp4_bytes,
                file_name="kinetic_carousel_loop.mp4",
                mime="video/mp4",
                use_container_width=True,
            )
          else:
            st.info(
                "💡 Add `imageio-ffmpeg` to requirements.txt to enable MP4"
                " export."
            )

      st.markdown("---")
      st.markdown("### 💬 Viral Ready-to-Post Caption:")

      first_slide = (
          st.session_state.slides_data[0]
          if st.session_state.slides_data
          else {}
      )
      caption_title = (
          first_slide.get("title", "Transform Your Coaching Page")
          if isinstance(first_slide, dict)
          else "Transform Your Coaching Page"
      )
      caption_body = (
          first_slide.get("content", first_slide.get("body", ""))
          if isinstance(first_slide, dict)
          else ""
      )

      st.info(
          f"🔥 {caption_title}\n\n{caption_body}\n\nWhich slide hit home for you"
          " the most? Drop your thoughts below! 👇\n\n--- \n⚡ Built & animated"
          " seamlessly using Carousel Engine & Kinetic Animator."
      )
else:
  st.title("🎬 Kinetic Motion Suite — Restricted Access")
  st.warning(
      "🔒 Please enter a valid license key in the sidebar to unlock the Kinetic"
      " Animator Studio."
  )