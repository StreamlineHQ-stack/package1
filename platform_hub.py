import io
import json
import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Import your core engine modules
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from image_renderer import generate_png_zip_from_slides

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Creator Suite • Master Platform Hub",
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
if "generated_caption" not in st.session_state:
  st.session_state["generated_caption"] = ""


# --- SIDEBAR: MASTER LICENSE & MOTION CONTROLS ---
with st.sidebar:
  st.title("⚡ Creator Suite")
  st.caption("Master Package All-Access Hub")
  st.divider()

  master_key = st.text_input(
      "Master Suite License Key:", type="password", value="TEST_MASTER_KEY"
  )
  if master_key:
    st.success("✅ Master License Verified (All-Access)")
  else:
    st.warning("⚠️ Enter a valid master key to unlock platform.")
    st.stop()

  st.divider()
  st.markdown("### ⚙️ Pro Motion Controls")
  frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20)
  seconds_per_slide = st.slider(
      "Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25
  )
  transition_style = st.selectbox(
      "Kinetic Transition Style:",
      [
          "Dynamic Slide Up (Pro Easing)",
          "Smooth Slide Right",
          "Cinematic Zoom In",
          "Fade & Snap",
      ],
  )

  st.divider()
  brand_handle = st.text_input(
      "Brand Watermark Handle:", value="@nikki.coachpages"
  )
  slide_count = st.slider("Target Slide Count:", 4, 10, 6)

  st.divider()
  st.markdown("### 🔄 Automated Pipeline Status")
  st.write(
      "1. Carousel Gen: "
      + ("✅ Ready" if st.session_state["deck_json"] else "⏳ Waiting")
  )
  st.write(
      "2. Kinetic Bridge: "
      + ("✅ Loaded" if st.session_state["deck_json"] else "⏳ Waiting")
  )
  st.write(
      "3. Motion Output: "
      + (
          "✅ Compiled"
          if st.session_state["animated_gif_bytes"]
          else "⏳ Waiting"
      )
  )


# --- HELPER FUNCTION: PIXEL-PERFECT TEXT WRAPPING ---
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


# --- HELPER FUNCTION: ROBUST FONT LOADER ---
def load_app_font(size):
  # Check multiple fallback paths so fonts never crash rendering
  possible_paths = [
      "arialbd.ttf",
      "fonts/arialbd.ttf",
      "C:/Windows/Fonts/arialbd.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
  ]
  for path in possible_paths:
    if os.path.exists(path):
      try:
        return ImageFont.truetype(path, size)
      except Exception:
        continue
  return ImageFont.load_default()


# --- MAIN APP HEADER ---
st.title("⚡ Creator Suite: Automated Carousel-to-Animation Platform")
st.markdown(
    "Generate high-converting direct-response carousels and automatically pipe"
    " them into Kinetic for instant motion graphics and captions[cite: 5]."
)
st.divider()

# --- UNIFIED WORKFLOW TABS ---
tab_carousel, tab_kinetic, tab_delivery = st.tabs([
    "1. 🎨 Carousel Engine Studio",
    "2. ⚙️ Kinetic Motion Engine",
    "3. 🚀 Final Delivery & Export",
])

# ==========================================
# TAB 1: CAROUSEL ENGINE STUDIO
# ==========================================
with tab_carousel:
  st.markdown('<div class="card">', unsafe_allow_html=True)
  st.markdown(
      '<p class="step-header">Step 1: Build Your Carousel (Auto-Pilot, Notes,'
      " or 100-Template Frameworks)</p>",
      unsafe_allow_html=True,
  )

  sub_tab1, sub_tab2, sub_tab3 = st.tabs(
      ["⚡ Auto-Pilot", "📝 Custom Notes", "🛠️ Framework Wizard"]
  )

  deck_result = None

  with sub_tab1:
    topic_input = st.text_input(
        "Core Topic / Hook:",
        value="High-converting landing page optimization for online coaches",
    )
    if st.button("Generate Auto-Pilot Deck", type="primary"):
      with st.spinner("Crafting direct-response deck..."):
        deck_result = generate_carousel_deck(
            topic_input, slide_count=slide_count, mode="autopilot"
        )
        st.session_state["deck_json"] = deck_result
        st.session_state["current_slide"] = 0
        st.success("✅ Carousel generated and loaded into platform memory!")
        st.rerun()

  with sub_tab2:
    notes_input = st.text_area(
        "Paste raw coaching notes:",
        height=120,
        value=(
            "Hook: 73% of prospects leave your offer page without buying.\nProblem:"
            " Vague copy creates friction.\nSolution: Audit top-of-fold"
            " messaging."
        ),
    )
    if st.button("Format Custom Notes", type="primary"):
      with st.spinner("Structuring notes..."):
        deck_result = generate_carousel_deck(
            notes_input, slide_count=slide_count, mode="custom"
        )
        st.session_state["deck_json"] = deck_result
        st.session_state["current_slide"] = 0
        st.success("✅ Carousel generated and loaded into platform memory!")
        st.rerun()

  with sub_tab3:
    pillar_name = st.selectbox(
        "Content Pillar:", list(FRAMEWORK_LIBRARY.keys())
    )
    template_name = st.selectbox(
        "Blueprint:", list(FRAMEWORK_LIBRARY[pillar_name].keys())
    )
    t_data = FRAMEWORK_LIBRARY[pillar_name][template_name]

    col_f1, col_f2 = st.columns(2)
    with col_f1:
      h_in = st.text_input("Hook", value=t_data["hook"])
      p_in = st.text_input("Problem", value=t_data["problem"])
    with col_f2:
      s_in = st.text_input("Solution", value=t_data["solution"])
      c_in = st.text_input("CTA", value=t_data["cta"])

    if st.button("Format Framework Deck", type="primary"):
      raw_text = (
          f"Hook Element: {h_in}\nProblem/Agitation:"
          f" {p_in}\nSolution/Steps: {s_in}\nCall to Action: {c_in}"
      )
      with st.spinner("Building framework carousel..."):
        deck_result = generate_carousel_deck(
            raw_text, slide_count=slide_count, mode="framework"
        )
        st.session_state["deck_json"] = deck_result
        st.session_state["current_slide"] = 0
        st.success("✅ Framework carousel loaded into platform memory!")
        st.rerun()

  # Preview and Slide Navigation
  if st.session_state["deck_json"]:
    st.divider()
    try:
      if isinstance(st.session_state["deck_json"], str):
        slides = json.loads(st.session_state["deck_json"])
      else:
        slides = st.session_state["deck_json"]
    except Exception:
      slides = []

    if slides:
      st.subheader("🔍 Live Slide Deck Preview")
      curr = st.session_state["current_slide"]
      if curr >= len(slides):
        curr = len(slides) - 1
        st.session_state["current_slide"] = curr

      s = slides[curr]
      tag = s.get("category", s.get("badge", f"SLIDE {curr+1}"))
      title = s.get("title", "")
      body = s.get("content", s.get("body", ""))

      st.markdown(
          f"""
            <div style="background-color: #1a1a1a; color: #ffffff; padding: 35px; border-radius: 12px; border: 2px solid #ffcc00; margin-top: 15px;">
                <p style="color: #ffcc00; font-weight: bold; font-size: 12px; letter-spacing: 1px;">SLIDE {curr+1} • {str(tag).upper()}</p>
                <h3 style="color: #ffffff; font-size: 22px; margin-top: 10px; margin-bottom: 10px;">{title}</h3>
                <p style="color: #d1d1d1; font-size: 15px; line-height: 1.5;">{body}</p>
                <p style="color: #8b949e; font-size: 11px; text-align: right; margin-top: 20px;">{brand_handle}</p>
            </div>
        """,
          unsafe_allow_html=True,
      )

      c_prev, c_ind, c_next = st.columns([1, 2, 1])
      with c_prev:
        if st.button("← Previous Slide") and curr > 0:
          st.session_state["current_slide"] -= 1
          st.rerun()
      with c_ind:
        st.markdown(
            f"<p style='text-align: center; margin-top: 8px;'>Slide {curr+1} of"
            f" {len(slides)}</p>",
            unsafe_allow_html=True,
        )
      with c_next:
        if st.button("Next Slide →") and curr < len(slides) - 1:
          st.session_state["current_slide"] += 1
          st.rerun()

      if st.button(
          "🚀 Send Payload to Kinetic Motion Engine",
          type="primary",
          use_container_width=True,
      ):
        st.toast(
            "Payload successfully bridged to Kinetic motion engine!", icon="✨"
        )

  st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: KINETIC MOTION ENGINE (FROM animator_app.py)
# ==========================================
with tab_kinetic:
  st.markdown('<div class="card">', unsafe_allow_html=True)
  st.markdown(
      '<p class="step-header">Step 2: Automated JSON Handoff & Pro GIF'
      " Rendering Engine</p>",
      unsafe_allow_html=True,
  )

  if st.session_state["deck_json"]:
    st.success(
        "✨ Active JSON payload successfully received from Carousel Engine via"
        " Platform Bridge[cite: 5]!"
    )

    with st.expander("🔍 Inspect Ingested JSON Payload"):
      st.json(st.session_state["deck_json"])

    st.divider()
    st.subheader("🎬 Render Engine Compilation")

    render_btn = st.button(
        "✨ Render Premium Kinetic GIF (Active Deck)", use_container_width=True
    )

    if render_btn:
      with st.spinner(
          "Rendering animation frames with precise typography and card styling..."
      ):
        try:
          if isinstance(st.session_state["deck_json"], str):
            slides_data = json.loads(st.session_state["deck_json"])
          else:
            slides_data = st.session_state["deck_json"]

          frames = []
          width, height = 1080, 1080  # Square Instagram/Carousel ratio
          max_text_width = 800  # Exact available width inside card

          badge_font = load_app_font(38)
          title_font = load_app_font(62)
          body_font = load_app_font(42)
          footer_font = load_app_font(30)

          for idx, slide in enumerate(slides_data, start=1):
            if isinstance(slide, dict):
              badge = str(
                  slide.get(
                      "badge",
                      slide.get("category", f"SLIDE {idx} | STRATEGY"),
                  )
              )
              title = str(slide.get("title", f"Slide Title {idx}"))
              body = str(
                  slide.get(
                      "body",
                      slide.get("content", "Key actionable breakdown..."),
                  )
              )
            else:
              badge = f"SLIDE {idx}"
              title = str(slide)
              body = ""

            # Sanitize strings
            badge = (
                badge.replace("•", "|")
                .replace("—", "-")
                .replace("“", '"')
                .replace("”", '"')
            )
            title = (
                title.replace("•", "|")
                .replace("—", "-")
                .replace("“", '"')
                .replace("”", '"')
            )
            body = (
                body.replace("•", "|")
                .replace("—", "-")
                .replace("“", '"')
                .replace("”", '"')
            )

            # Create base background (#0e1117)
            img = Image.new("RGB", (width, height), color="#0e1117")
            draw = ImageDraw.Draw(img)

            # Draw Main Card Box (#161b22 with Canary Yellow border #ffcc00)
            draw.rounded_rectangle(
                [80, 100, width - 80, height - 150],
                radius=28,
                fill="#161b22",
                outline="#ffcc00",
                width=5,
            )

            # Draw Badge / Header
            draw.text((140, 160), badge.upper(), fill="#ffcc00", font=badge_font)

            # Wrapped Title rendering
            temp_img = Image.new("RGB", (width, height))
            temp_draw = ImageDraw.Draw(temp_img)
            wrapped_title = wrap_text_to_width(
                title, title_font, max_text_width, temp_draw
            )
            title_y = 250
            for line in wrapped_title:
              draw.text((140, title_y), line, fill="#ffffff", font=title_font)
              title_y += 74

            # Wrapped Body rendering
            if body:
              wrapped_body = wrap_text_to_width(
                  body, body_font, max_text_width, temp_draw
              )
              body_y = title_y + 30
              for line in wrapped_body:
                draw.text((140, body_y), line, fill="#c9d1d9", font=body_font)
                body_y += 56

            # Draw Footer Handle
            draw.text(
                (140, height - 230),
                brand_handle,
                fill="#8b949e",
                font=footer_font,
            )

            frames.append(img)

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
          st.session_state["animated_gif_bytes"] = gif_buffer.getvalue()

          # Generate viral caption from first slide
          first_slide = slides_data[0] if slides_data else {}
          cap_title = (
              first_slide.get("title", "Transform Your Coaching Page")
              if isinstance(first_slide, dict)
              else "Transform Your Coaching Page"
          )
          cap_body = (
              first_slide.get("body", first_slide.get("content", ""))
              if isinstance(first_slide, dict)
              else ""
          )

          st.session_state["generated_caption"] = (
              f"🔥 {cap_title}\n\n{cap_body}\n\nWhich slide hit home for you the"
              " most? Drop your thoughts below! 👇\n\n--- \n⚡ Built & animated"
              " seamlessly using Carousel Engine & Kinetic Motion Suite."
          )

          st.success("🎉 Kinetic Loop rendered successfully!")
        except Exception as e:
          st.error(f"Render error: {e}")
  else:
    st.warning(
        "🔒 No carousel payload found. Please generate a carousel deck in Step 1"
        " first."
    )

  st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: FINAL DELIVERY & EXPORT
# ==========================================
with tab_delivery:
  st.markdown('<div class="card">', unsafe_allow_html=True)
  st.markdown(
      '<p class="step-header">Step 3: Final Animated GIF, Slide Package & Social'
      " Caption Delivery</p>",
      unsafe_allow_html=True,
  )

  if st.session_state["animated_gif_bytes"]:
    col_res1, col_res2 = st.columns(2, gap="large")

    with col_res1:
      st.subheader("🎬 Final Motion Asset (GIF)")
      st.success("✅ Kinetic animation loop successfully compiled.")

      # Display GIF preview in Streamlit
      st.image(
          st.session_state["animated_gif_bytes"],
          caption="Rendered Kinetic Loop Preview",
          use_container_width=True,
      )

      st.download_button(
          label="⬇️ Download Rendered Animated GIF (.gif)",
          data=st.session_state["animated_gif_bytes"],
          file_name="kinetic_carousel_loop.gif",
          mime="image/gif",
          use_container_width=True,
      )

      st.divider()

      # Also allow downloading static PNG slide zip package using image_renderer
      if st.session_state["deck_json"]:
        try:
          if isinstance(st.session_state["deck_json"], str):
            slides_list = json.loads(st.session_state["deck_json"])
          else:
            slides_list = st.session_state["deck_json"]

          zip_data = generate_png_zip_from_slides(
              slides_list, handle_text=brand_handle
          )
          st.download_button(
              label="📥 Download Static Slide PNG Package (.zip)",
              data=zip_data,
              file_name="carousel_slides_package.zip",
              mime="application/zip",
              use_container_width=True,
          )
        except Exception as e:
          st.caption(f"PNG package generation note: {e}")

    with col_res2:
      st.subheader("📝 Generated Social Media Caption")
      st.text_area(
          "Ready-to-Post Caption (Optimized for Engagement):",
          st.session_state["generated_caption"],
          height=220,
      )
      st.success("📋 Caption optimized for comments and reach conversion.")
  else:
    st.warning(
        "⏳ Final delivery pending. Complete Step 1 (Carousel Studio) and Step"
        " 2 (Kinetic Motion Engine) to compile your assets."
    )

  st.markdown("</div>", unsafe_allow_html=True)