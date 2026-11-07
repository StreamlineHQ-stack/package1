# sia_studio.py • Style Inspiration & Analysis Studio (SIA) with Carousel Content Engine & Deck Carousel Player
import streamlit as st
import json
import base64
import io
import os
import requests
import zipfile
from PIL import Image, ImageDraw, ImageFont
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from sia_terracotta_module import build_terracotta_deck
from sia_ai_context_module import build_ai_context_deck
from sia_editorial_motif_module import build_unified_editorial_deck
from background_engine import get_modular_background
from smart_ai_engine import get_smart_ai_background

try:
    from templates.november import NOVEMBER_FRAMEWORK_LIBRARY
except Exception:
    NOVEMBER_FRAMEWORK_LIBRARY = {}

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

def build_custom_user_deck(deck, custom_img_base64=""):
    """
    Builds a styled deck using a single custom user-uploaded image stamped across all slides (Option A).
    """
    styled = []
    total = len(deck)
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        img_src = custom_img_base64 if custom_img_base64 else "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1080&auto=format&fit=crop&q=80"
        
        html = f"""
        <div style="background: #0b0f19; padding: 40px; border-radius: 24px; border: 3px solid #1f2937; max-width: 680px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
            <div style="width: 100%; height: 240px; border-radius: 16px; overflow: hidden; margin-bottom: 24px; border: 2px solid #374151;">
                <img src="{img_src}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
            <div style="color: #ffcc00; font-size: 14px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px;">
                SLIDE {idx+1} OF {total} • {cat}
            </div>
            <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 16px;">
                {title}
            </h2>
            <p style="color: #9ca3af; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                {content}
            </p>
            <div style="text-align: right; color: #6b7280; font-size: 12px; font-weight: 600; border-top: 1px solid #1f2937; padding-top: 12px;">
                Nikki's Salon • ApexMorph
            </div>
        </div>
        """
        styled.append({
            "category": cat,
            "title": title,
            "content": content,
            "rendered_html": html
        })
    return styled

def render_sia_slide_to_image(slide_data, slide_num, total_slides, style_mode="Terracotta"):
    width, height = 1080, 1080
    max_text_width = 880
    
    bg_hex = "#a85732" if "Terracotta" in style_mode else "#0b0f19"
    img = Image.new("RGB", (width, height), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    title = ""
    body = ""
    category = ""
    
    preview_deck = st.session_state.get("sia_preview_deck", [])
    if preview_deck and len(preview_deck) >= slide_num:
        original_slide = preview_deck[slide_num - 1]
        if isinstance(original_slide, dict):
            category = str(original_slide.get("category", original_slide.get("tag", f"SLIDE {slide_num}"))).upper()
            title = str(original_slide.get("title", original_slide.get("headline", "")))
            body = str(original_slide.get("content", original_slide.get("body", "")))
            
    if not title:
        title = str(slide_data.get("title", slide_data.get("headline", f"Slide {slide_num}")))
    if not body:
        body = str(slide_data.get("content", slide_data.get("body", "")))
    if not category:
        raw_cat = slide_data.get("category") or slide_data.get("tag") or f"SLIDE {slide_num}"
        category = str(raw_cat).upper()
        
    bg_url = ""
    if "Custom User Images" in style_mode and st.session_state.get("sia_custom_img_bytes"):
        pass
    else:
        html_content = slide_data.get("rendered_html", "")
        if html_content:
            import re
            match = re.search(r'img[^>]+src="([^">]+)"', html_content)
            if match:
                bg_url = match.group(1)
                
        if not bg_url:
            if "Smart AI Contextual Match" in style_mode or "Smart AI" in style_mode:
                bg_url = get_smart_ai_background(category, slide_num - 1, title + " " + body)
            elif "Unified Editorial Motif" in style_mode or "Exact Inspiration Match" in style_mode:
                bg_url = get_modular_background(style_mode, st.session_state.get("sia_motif_choice", "editorial"), slide_num - 1)
                
    try:
        if "Custom User Images" in style_mode and st.session_state.get("sia_custom_img_bytes"):
            banner_img = Image.open(io.BytesIO(st.session_state["sia_custom_img_bytes"])).convert("RGB").resize((960, 380))
            img.paste(banner_img, (60, 100))
        elif bg_url and bg_url.startswith("data:image"):
            header, encoded = bg_url.split(",", 1)
            img_bytes = base64.b64decode(encoded)
            banner_img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((960, 380))
            img.paste(banner_img, (60, 100))
        elif bg_url:
            resp = requests.get(bg_url, timeout=3)
            banner_img = Image.open(io.BytesIO(resp.content)).convert("RGB").resize((960, 380))
            img.paste(banner_img, (60, 100))
    except Exception:
        pass
        
    draw = ImageDraw.Draw(img)
    
    try:
        badge_font = ImageFont.truetype("arialbd.ttf", 26)
        title_font = ImageFont.truetype("arialbd.ttf", 46)
        body_font = ImageFont.truetype("arialbd.ttf", 32)
        footer_font = ImageFont.truetype("arialbd.ttf", 22)
    except IOError:
        badge_font = title_font = body_font = footer_font = ImageFont.load_default()

    current_y = 510
    draw.text((100, current_y), f"SLIDE {slide_num} OF {total_slides} • {category}", fill="#ffcc00", font=badge_font)
    current_y += 50

    for line in wrap_text_to_width(title, title_font, width - 200, draw):
        draw.text((100, current_y), line, fill="#ffffff", font=title_font)
        current_y += 58

    current_y += 20
    if body:
        for line in wrap_text_to_width(body, body_font, width - 200, draw):
            draw.text((100, current_y), line, fill="#e5e7eb", font=body_font)
            current_y += 42

    draw.text((width - 340, height - 100), "Nikki's Salon • ApexMorph", fill="#94a3b8", font=footer_font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def render_visual_preview(styled_deck):
    if not styled_deck:
        return
    st.divider()
    st.markdown("### 👁️ Rendered Module Visual Deck Presenter")
    
    if "sia_current_slide_idx" not in st.session_state:
        st.session_state["sia_current_slide_idx"] = 0
        
    total_slides = len(styled_deck)
    if st.session_state["sia_current_slide_idx"] >= total_slides:
        st.session_state["sia_current_slide_idx"] = max(0, total_slides - 1)
        
    current_idx = st.session_state["sia_current_slide_idx"]
    slide = styled_deck[current_idx]
    
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        if st.button("◀ Previous Slide", use_container_width=True, key="sia_prev_slide_btn", disabled=(current_idx == 0)):
            st.session_state["sia_current_slide_idx"] = max(0, current_idx - 1)
            st.rerun()
    with nav_col2:
        st.markdown(f"<div style='text-align: center; font-weight: bold; padding-top: 8px;'>Slide {current_idx + 1} of {total_slides}</div>", unsafe_allow_html=True)
    with nav_col3:
        if st.button("Next Slide ▶", use_container_width=True, key="sia_next_slide_btn", disabled=(current_idx == total_slides - 1)):
            st.session_state["sia_current_slide_idx"] = min(total_slides - 1, current_idx + 1)
            st.rerun()
            
    st.markdown(slide.get("rendered_html", ""), unsafe_allow_html=True)
    
    st.markdown("### 📥 Export & Download Deck")
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        if st.button("📦 Generate & Download Image Deck (.zip)", type="primary", use_container_width=True, key="sia_gen_zip_imgs"):
            active_mode_name = st.session_state.get("sia_current_active_mode", "Terracotta")
            with st.spinner("Rendering high-res Instagram PNG slide images into ZIP archive..."):
                zip_buffer = io.BytesIO()
                preview_deck_data = st.session_state.get("sia_rendered_output", styled_deck)
                if not preview_deck_data:
                    preview_deck_data = styled_deck
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, s in enumerate(preview_deck_data):
                        img_bytes = render_sia_slide_to_image(
                            slide_data=s,
                            slide_num=idx + 1,
                            total_slides=len(preview_deck_data),
                            style_mode=active_mode_name
                        )
                        zip_file.writestr(f"slide_{idx+1}.png", img_bytes)
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📥 Click Here to Download .zip Archive",
                    data=zip_buffer,
                    file_name="instagram_carousel_images.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="sia_actual_download_btn"
                )
                
    with col_dl2:
        if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="sia_send_animator_btn"):
            preview_deck_data = st.session_state.get("sia_rendered_output", styled_deck)
            if not preview_deck_data:
                preview_deck_data = styled_deck
            st.session_state["slides_data"] = preview_deck_data
            st.session_state["active_view"] = "kinetic_ui"
            st.rerun()

def render_sia_studio():
    if st.session_state.get("active_view") == "kinetic_ui":
        st.markdown("<h1 style='text-align: center;'>🧬 Kinetic UI Workspace (Local Suite)</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>High-performance local motion rendering engine running natively inside SIA.</p>", unsafe_allow_html=True)
        st.divider()
        
        if st.button("← Back to Style Inspiration Studio", type="secondary", key="sia_back_to_studio"):
            st.session_state["active_view"] = "studio"
            st.rerun()
            
        st.divider()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### ⚙️ Pro Motion Control")
            frame_rate = st.slider("Frame Rate (FPS):", 10, 60, 20, key="sia_local_fps")
            seconds_per_slide = st.slider("Seconds per Slide:", 1.0, 5.0, 2.5, step=0.25, key="sia_local_sps")
            transition_style = st.selectbox(
                "Kinetic Transition Style:",
                [
                    "Dynamic Slide Up (Pro Easing)",
                    "Smooth Slide Right",
                    "Cinematic Zoom In",
                    "Fade & Snap",
                ],
                key="sia_local_transition"
            )
            transition_speed = st.slider("Transition Speed (Frames):", 2, 15, 6, key="sia_local_trans_speed")

        slides_to_render = st.session_state.get("sia_rendered_output", [])
        if not slides_to_render:
            slides_to_render = st.session_state.get("slides_data", [])
        if not slides_to_render:
            slides_to_render = st.session_state.get("sia_preview_deck", [])

        st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")
        
        col_seq, col_eng = st.columns([1.2, 1.4])
        with col_seq:
            st.markdown("### Slide Sequence Overview")
            if slides_to_render:
                for idx, slide in enumerate(slides_to_render, start=1):
                    title_text = slide.get("title", f"Slide {idx}") if isinstance(slide, dict) else str(slide)
                    st.markdown(f"**Slide {idx}:** {title_text}")
            else:
                st.info("No active slides found. Generate a carousel first.")

            st.markdown("### Production Render Engine")
            render_btn = st.button("✨ Render Premium Kinetic Loop (Active Deck)", use_container_width=True, key="sia_local_render_btn")

            if render_btn:
                active_mode = st.session_state.get("sia_current_active_mode", "Terracotta")
                
                with st.spinner(f"Rendering animation frames from actual deck cards [{active_mode}]..."):
                    frames = []
                    
                    for idx, slide in enumerate(slides_to_render, start=1):
                        png_bytes = render_sia_slide_to_image(
                            slide_data=slide,
                            slide_num=idx,
                            total_slides=len(slides_to_render),
                            style_mode=active_mode
                        )
                        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
                        frames.append(img)

                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                    st.session_state["sia_last_rendered_gif"] = gif_buffer.getvalue()

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

                        mp4_path = "temp_kinetic_deck_sia.mp4"
                        imageio.mimwrite(
                            mp4_path,
                            paced_frames,
                            fps=fps,
                            codec="libx264",
                            pixelformat="yuv420p",
                            output_params=['-crf', '10', '-preset', 'slow']
                        )
                        with open(mp4_path, "rb") as mf:
                            mp4_bytes = mf.read()
                        os.remove(mp4_path)
                        st.session_state["sia_last_rendered_mp4"] = mp4_bytes
                    except Exception:
                        st.session_state["sia_last_rendered_mp4"] = None
                    
                st.success("🎉 Kinetic Loop rendered successfully from your actual deck cards!")

            if "sia_last_rendered_mp4" in st.session_state and st.session_state["sia_last_rendered_mp4"]:
                st.markdown("---")
                st.markdown("#### 👁️ Live Loop Preview")
                mp4_bytes = st.session_state["sia_last_rendered_mp4"]
                b64_mp4 = base64.b64encode(mp4_bytes).decode("utf-8")
                st.markdown(
                    f'<div style="width: 100%; display: flex; justify-content: center; background: #000; padding: 10px; border-radius: 12px; border: 2px solid #ffcc00; box-sizing: border-box; margin-bottom: 20px;">'
                    f'<video width="100%" autoplay loop muted playsinline style="border-radius: 8px; display: block; max-width: 280px; height: auto;">'
                    f'<source src="data:video/mp4;base64,{b64_mp4}" type="video/mp4">'
                    f'Your browser does not support the video tag.'
                    f'</video>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                st.markdown("#### 📥 Download Package")
                if "sia_last_rendered_gif" in st.session_state:
                    st.download_button(
                        label="⬇️ Download Animated GIF",
                        data=st.session_state["sia_last_rendered_gif"],
                        file_name="sia_kinetic_loop.gif",
                        mime="image/gif",
                        use_container_width=True,
                        key="sia_dl_gif_btn"
                    )
                st.download_button(
                    label="🎬 Download Instagram MP4",
                    data=mp4_bytes,
                    file_name="sia_kinetic_loop.mp4",
                    mime="video/mp4