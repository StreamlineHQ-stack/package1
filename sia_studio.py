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
from sia_inspiration_template_module import build_inspiration_editorial_deck
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
    styled = []
    total = len(deck)
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", "SLIDE " + str(idx+1))).upper()
        title = str(slide.get("title", "Slide " + str(idx+1)))
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
    bg_hex = "#b0543c" if "Exact Inspiration Match" in style_mode else ("#a85732" if "Terracotta" in style_mode else "#0b0f19")
    img = Image.new("RGB", (width, height), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    title = ""
    body = ""
    category = ""
    
    preview_deck = st.session_state.get("sia_preview_deck", [])
    if preview_deck and len(preview_deck) >= slide_num:
        original_slide = preview_deck[slide_num - 1]
        if isinstance(original_slide, dict):
            category = str(original_slide.get("category", original_slide.get("tag", "SLIDE " + str(slide_num)))).upper()
            title = str(original_slide.get("title", original_slide.get("headline", "")))
            body = str(original_slide.get("content", original_slide.get("body", "")))
            
    if not title:
        title = str(slide_data.get("title", slide_data.get("headline", "Slide " + str(slide_num))))
    if not body:
        body = str(slide_data.get("content", slide_data.get("body", "")))
    if not category:
        raw_cat = slide_data.get("category") or slide_data.get("tag") or ("SLIDE " + str(slide_num))
        category = str(raw_cat).upper()
        
    if "Exact Inspiration Match" in style_mode:
        uploaded_files = st.session_state.get("sia_uploaded_files", None)
        try:
            badge_font = ImageFont.truetype("arialbd.ttf", 24)
            title_font = ImageFont.truetype("arialbd.ttf", 44)
            body_font = ImageFont.truetype("arialbd.ttf", 30)
            footer_font = ImageFont.truetype("arialbd.ttf", 20)
        except IOError:
            badge_font = title_font = body_font = footer_font = ImageFont.load_default()

        if uploaded_files:
            # Render with uploaded swipe as top banner image
            try:
                banner_bytes = uploaded_files[0].getvalue()
                banner_img = Image.open(io.BytesIO(banner_bytes)).convert("RGB").resize((880, 420))
                img.paste(banner_img, (100, 80))
            except Exception:
                pass

            current_y = 530
            badge_text = "SLIDE " + str(slide_num) + " OF " + str(total_slides) + " • " + category
            draw.text((100, current_y), badge_text, fill="#ffcc00", font=badge_font)
            current_y += 45

            for line in wrap_text_to_width(title, title_font, width - 200, draw):
                draw.text((100, current_y), line, fill="#ffffff", font=title_font)
                current_y += 50

            current_y += 15
            if body:
                for line in wrap_text_to_width(body, body_font, width - 200, draw):
                    draw.text((100, current_y), line, fill="#e5e7eb", font=body_font)
                    current_y += 38
        else:
            from sia_inspiration_template_module import fetch_inspiration_image
            flower_q = st.session_state.get("sia_insp_flower", "white rose")
            object_q = st.session_state.get("sia_insp_object", "ceramic vase")
            img1_url = fetch_inspiration_image(object_q)
            img2_url = fetch_inspiration_image(flower_q)
            img_urls = [img1_url, img2_url]
                
            current_y = 80
            badge_text = "SLIDE " + str(slide_num) + " OF " + str(total_slides) + " • " + category
            draw.text((100, current_y), badge_text, fill="#fde047", font=badge_font)
            current_y += 45
            
            for line in wrap_text_to_width(title, title_font, width - 200, draw):
                draw.text((100, current_y), line, fill="#ffffff", font=title_font)
                current_y += 52
                
            current_y += 20
            if body:
                for line in wrap_text_to_width(body, body_font, width - 200, draw):
                    draw.text((100, current_y), line, fill="#f3f4f6", font=body_font)
                    current_y += 38
                    
            if len(img_urls) >= 2:
                try:
                    resp1 = requests.get(img_urls[0], timeout=3)
                    resp2 = requests.get(img_urls[1], timeout=3)
                    size = 120
                    im1 = Image.open(io.BytesIO(resp1.content)).convert("RGB").resize((size, size))
                    im2 = Image.open(io.BytesIO(resp2.content)).convert("RGB").resize((size, size))
                    
                    mask = Image.new("L", (size, size), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.ellipse((0, 0, size, size), fill=255)
                    
                    im1_rgba = im1.convert("RGBA")
                    im2_rgba = im2.convert("RGBA")
                    im1_rgba.putalpha(mask)
                    im2_rgba.putalpha(mask)
                    
                    total_w = size * 2 + 24
                    start_x = (width - total_w) // 2
                    start_y = 730
                    
                    img.paste(im1_rgba, (start_x, start_y), im1_rgba)
                    img.paste(im2_rgba, (start_x + size + 24, start_y), im2_rgba)
                except Exception:
                    pass
                
        draw.text((100, 970), "OCT 8 • 2026", fill="#ffffff", font=footer_font)
        # draw.text((width // 2 - 80, 970), "EXACT INSPIRATION", fill="#ffffff", font=footer_font)
        draw.text((width - 320, 970), "NIKKI'S SALON", fill="#ffffff", font=footer_font)
        
    else:
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
                elif "Unified Editorial Motif" in style_mode:
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
        draw.text((100, current_y), "SLIDE " + str(slide_num) + " OF " + str(total_slides) + " • " + category, fill="#ffcc00", font=badge_font)
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
        st.markdown("<div style='text-align: center; font-weight: bold; padding-top: 8px;'>Slide " + str(current_idx + 1) + " of " + str(total_slides) + "</div>", unsafe_allow_html=True)
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
                        zip_file.writestr("slide_" + str(idx+1) + ".png", img_bytes)
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
                    title_text = slide.get("title", "Slide " + str(idx)) if isinstance(slide, dict) else str(slide)
                    st.markdown("**Slide " + str(idx) + ":** " + title_text)
            else:
                st.info("🔥 Rendered Kinetic Loop ready for Instagram! Download your MP4 or GIF below.")

            st.markdown("### Production Render Engine")
            render_btn = st.button("✨ Render Premium Kinetic Loop (Active Deck)", use_container_width=True, key="sia_local_render_btn")

            if render_btn:
                active_mode = st.session_state.get("sia_current_active_mode", "Terracotta")
                
                with st.spinner("Rendering animation frames from actual deck cards..."):
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
                    '<div style="width: 100%; display: flex; justify-content: center; background: #000; padding: 10px; border-radius: 12px; border: 2px solid #ffcc00; box-sizing: border-box; margin-bottom: 20px;">'
                    '<video width="100%" autoplay loop muted playsinline style="border-radius: 8px; display: block; max-width: 280px; height: auto;">'
                    '<source src="data:video/mp4;base64,' + b64_mp4 + '" type="video/mp4">'
                    'Your browser does not support the video tag.'
                    '</video>'
                    '</div>',
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
                    mime="video/mp4",
                    use_container_width=True,
                    key="sia_dl_mp4_btn"
                )

        with col_eng:
            st.markdown("### 💬 Viral Ready-to-Post Caption")
            first_title = (
                slides_to_render[0].get("title", "Check this out")
                if slides_to_render
                else "Check this out"
            )
            st.info("🔥 Rendered Kinetic Loop ready for Instagram! Download your MP4 or GIF below.")
        return

    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Upload inspiration swipes, generate content via Carousel Engine engines, and render modular styled decks.")
    
    downstream_payload = st.session_state.get("sia_downstream_payload", None)
    if downstream_payload:
        st.success("📦 **Downstream Feature Script Loaded & Ready!**")
        with st.expander("🔍 View Incoming Feature Script Content"):
            st.write(downstream_payload)
            
        if not st.session_state.get("sia_preview_deck"):
            if isinstance(downstream_payload, list):
                st.session_state["sia_preview_deck"] = downstream_payload
            elif isinstance(downstream_payload, str):
                st.session_state["sia_preview_deck"] = [
                    {"category": "HOOK", "title": "Feature Script Highlight", "content": downstream_payload[:120]},
                    {"category": "PROBLEM", "title": "The Core Challenge", "content": "Addressing the key pain points outlined in the incoming script."},
                    {"category": "SOLUTION", "title": "Strategic Execution", "content": downstream_payload[120:300] if len(downstream_payload) > 120 else "Executing the primary recommendations."},
                    {"category": "CTA", "title": "Take Action Today", "content": "Implement this framework to drive immediate results."}
                ]
        st.divider()

    if "sia_uploaded_files" not in st.session_state:
        st.session_state["sia_uploaded_files"] = None
    if "sia_preview_deck" not in st.session_state:
        st.session_state["sia_preview_deck"] = []
    if "sia_rendered_output" not in st.session_state:
        st.session_state["sia_rendered_output"] = None

    uploaded_slides = st.file_uploader("Upload Reference Swipe Slides", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="sia_file_uploader")
    if uploaded_slides != st.session_state.get("sia_uploaded_files", None):
        st.session_state["sia_uploaded_files"] = uploaded_slides
        st.session_state["sia_rendered_output"] = None
        st.session_state["sia_preview_deck"] = []
        st.success("🧹 New reference swipe detected! Cache completely purged & palette deconstructed.")
        st.rerun()
        
        st.markdown("#### 🖼️ Reference Swipe Image Previews")
        img_cols = st.columns(min(len(uploaded_slides), 4))
        for idx, img_file in enumerate(uploaded_slides):
            with img_cols[idx % len(img_cols)]:
                st.image(img_file, caption="Swipe " + str(idx+1), use_container_width=True)

    if uploaded_slides or downstream_payload:
        st.divider()
        st.markdown("## 📊 Deconstruction Report & Content Engine")
        
        slide_count = st.slider("Target Slide Count:", 4, 10, 6, key="sia_slide_count_slider")
        
        ACTIVE_FRAMEWORK_LIBRARY = FRAMEWORK_LIBRARY.copy()
        if NOVEMBER_FRAMEWORK_LIBRARY:
            ACTIVE_FRAMEWORK_LIBRARY.update(NOVEMBER_FRAMEWORK_LIBRARY)

        tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])

        with tab1:
            st.markdown("### ⚡ AI Auto-Pilot Content Engine")
            topic_prompt = st.text_input("Enter your core topic or audience pain point:", "Why is high-converting copywriting important", key="sia_autopilot_input")
            if st.button("Generate Auto-Pilot Carousel Deck", type="primary", key="sia_btn_gen_auto"):
                with st.spinner("Crafting direct-response carousel deck via AI Engine..."):
                    res, status_msg = generate_carousel_deck(topic_prompt, slide_count=slide_count, mode="autopilot")
                    if isinstance(res, str):
                        try:
                            st.session_state["sia_preview_deck"] = json.loads(res)
                        except Exception:
                            st.session_state["sia_preview_deck"] = []
                    elif isinstance(res, list):
                        st.session_state["sia_preview_deck"] = res
                    st.success("🎉 AI Content Deck generated successfully!")
                    st.rerun()

        with tab2:
            st.markdown("### 📝 Custom Expert Notes")
            custom_notes = st.text_area(
                "Paste your unstructured notes:", 
                height=130, 
                value="Hook: Conversion rate optimization is leverage.\nProblem: People lose visitors on mobile landing pages.\nCTA: Comment CRO to get the framework.", 
                key="sia_custom_notes_input"
            )
            if st.button("Format Custom Notes into Deck", type="primary", key="sia_btn_gen_notes"):
                with st.spinner("Structuring raw notes into slides..."):
                    res, status_msg = generate_carousel_deck(custom_notes, slide_count=slide_count, mode="custom")
                    if isinstance(res, str):
                        try:
                            st.session_state["sia_preview_deck"] = json.loads(res)
                        except Exception:
                            st.session_state["sia_preview_deck"] = []
                    elif isinstance(res, list):
                        st.session_state["sia_preview_deck"] = res
                    st.success("🎉 Custom notes formatted successfully!")
                    st.rerun()

        with tab3:
            st.markdown("### 🪄 Guided Framework Wizard")
            col_pillar, col_template = st.columns(2)
            with col_pillar:
                selected_pillar = st.selectbox("Choose Content Pillar:", list(ACTIVE_FRAMEWORK_LIBRARY.keys()), key="sia_pillar_select")
            templates_in_pillar = ACTIVE_FRAMEWORK_LIBRARY[selected_pillar]
            with col_template:
                selected_template_name = st.selectbox("Choose Direct-Response Blueprint:", list(templates_in_pillar.keys()), key="sia_template_select")
            
            template_data = templates_in_pillar[selected_template_name]
            st.divider()
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                hook_input = st.text_input("1. Hook / Core Headline", value=template_data["hook"], key="sia_hook_in")
                problem_input = st.text_input("2. Core Problem / Pain", value=template_data["problem"], key="sia_prob_in")
            with col_f2:
                solution_input = st.text_input("3. Solution / System Steps", value=template_data["solution"], key="sia_sol_in")
                cta_input = st.text_input("4. Call to Action (CTA)", value=template_data["cta"], key="sia_cta_in")
                
            if st.button("Format Framework Carousel Deck", type="primary", key="sia_btn_gen_frame"):
                raw_text = "Hook: " + hook_input + "\nProblem: " + problem_input + "\nSolution: " + solution_input + "\nCTA: " + cta_input
                with st.spinner("Building direct-response carousel deck..."):
                    res, status_msg = generate_carousel_deck(raw_text, slide_count=slide_count, mode="framework")
                    if isinstance(res, str):
                        try:
                            st.session_state["sia_preview_deck"] = json.loads(res)
                        except Exception:
                            st.session_state["sia_preview_deck"] = []
                    elif isinstance(res, list):
                        st.session_state["sia_preview_deck"] = res
                    st.success("🎉 Framework Carousel Deck generated successfully!")
                    st.rerun()

        if st.session_state.get("sia_preview_deck"):
            st.divider()
            st.markdown("### 📄 White Background Preview & Edit Deck")
            st.markdown("Review and refine your slide cards before applying the SIA visual style.")
            
            for idx, slide in enumerate(st.session_state["sia_preview_deck"]):
                with st.expander("White Card " + str(idx+1) + ": [" + slide.get('category', 'SLIDE') + "] " + slide.get('title', '')):
                    edited_cat = st.text_input("Category " + str(idx+1), slide.get('category', ''), key="sia_cat_" + str(idx))
                    edited_title = st.text_input("Title " + str(idx+1), slide.get('title', ''), key="sia_title_" + str(idx))
                    edited_content = st.text_area("Content " + str(idx+1), slide.get('content', ''), key="sia_cont_" + str(idx))
                    
                    st.session_state["sia_preview_deck"][idx] = {
                        "category": edited_cat,
                        "title": edited_title,
                        "content": edited_content
                    }

        st.markdown("---")
        if st.button("🎭 Call Art Director & Activate Style Engine", type="primary", use_container_width=True, key="sia_call_art_director"):
            st.session_state["sia_art_director_active"] = True
            st.success("🎉 Art Director online! Check your sidebar for the 5 isolated SIA Style Engine control modes.")
            st.rerun()

    if st.session_state.get("sia_art_director_active", False):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Enhanced Visual Style Engine")
            
            style_modes = [
                "☕ Terracotta Background & White Font",
                "⚡ Smart AI Contextual Match",
                "🎯 Exact Inspiration Match",
                "🏛️ Unified Editorial Motif",
                "📂 Custom User Images"
            ]
            
            if "sia_sidebar_mode_choice" not in st.session_state:
                st.session_state["sia_sidebar_mode_choice"] = style_modes[0]
                
            sia_mode = st.radio(
                "Select SIA Style Mode:",
                style_modes,
                key="sia_sidebar_mode_radio"
            )
            
            prev_mode = st.session_state.get("sia_current_active_mode", None)
            
            custom_img_base64 = ""
            if "Custom User Images" in sia_mode:
                st.markdown("#### 📂 Custom Asset Uploader")
                custom_file = st.file_uploader("Upload Brand/Banner Asset", type=["png", "jpg", "jpeg"], key="sia_custom_asset_upload")
                if custom_file:
                    bytes_data = custom_file.getvalue()
                    st.session_state["sia_custom_img_bytes"] = bytes_data
                    encoded = base64.b64encode(bytes_data).decode("utf-8")
                    custom_img_base64 = "data:image/png;base64," + encoded
                    st.session_state["sia_custom_img_b64"] = custom_img_base64
                    st.success("✅ Brand asset loaded successfully!")
                elif "sia_custom_img_b64" in st.session_state:
                    custom_img_base64 = st.session_state["sia_custom_img_b64"]
            elif "Unified Editorial Motif" in sia_mode:
                st.markdown("#### 🏛️ Thematic Motif Custom Input")
                st.text_input("Enter Theme (e.g. flower, rose, beach, happy people):", value="flower", key="sia_motif_theme_input")
            elif "Exact Inspiration Match" in sia_mode:
                st.markdown("#### 🎯 Terracotta Replicator Input")
                st.text_input("Main Headline (Leave blank to use slide title)", value="", key="sia_insp_headline")
                st.text_input("Flower / Botanical", value="white rose", key="sia_insp_flower")
                st.text_input("Inanimate Object", value="ceramic vase", key="sia_insp_object")
                st.text_input("Date Footer", value="OCT 8 • 2026", key="sia_insp_date")
            
            if prev_mode != sia_mode:
                st.session_state["sia_rendered_output"] = None
                st.session_state["sia_current_active_mode"] = sia_mode
                st.success("🧹 Workspace flushed! Switched to: " + sia_mode + ". Previous cache purged.")
            
            if st.button("🔄 Refresh Workspace & Purge Cache", type="secondary", use_container_width=True):
                st.session_state["sia_rendered_output"] = None
                st.success("⚡ Cache wiped and workspace refreshed.")
                st.rerun()

        st.divider()
        st.markdown("### 🚀 Module Execution")
        st.markdown("**Active Render Module:** `" + sia_mode + "`")
        
        active_selected_mode = st.session_state.get("sia_sidebar_mode_radio", sia_mode)
        
        if st.button("✨ Generate Deck via [" + active_selected_mode + "]", type="primary", use_container_width=True, key="sia_generate_module_deck"):
            deck = st.session_state.get("sia_preview_deck", [])
            
            if not deck:
                deck = [
                    {"category": "HOOK", "title": "The Secret to High-Converting Copy", "content": "Discover how the right words transform casual visitors into paying customers instantly."},
                    {"category": "PROBLEM", "title": "Why Most Landing Pages Fail", "content": "Without compelling copy, even the best products get ignored. Are you losing sales?"},
                    {"category": "SOLUTION", "title": "Crafting Irresistible Messages", "content": "Address pain points and deliver clear solutions that build immediate trust."},
                    {"category": "CTA", "title": "Ready to Transform Your Sales?", "content": "Partner with a professional copywriter today and watch your engagement soar."}
                ]
                st.session_state["sia_preview_deck"] = deck
            
            if "Terracotta Background & White Font" in active_selected_mode:
                st.session_state["sia_active_bg_hex"] = "#a85732"
                st.session_state["sia_rendered_output"] = build_terracotta_deck(deck)
                st.success("☕ [Module 1 Rendered]: Terracotta cards built successfully!")
                st.rerun()
            elif "Smart AI Contextual Match" in active_selected_mode:
                st.session_state["sia_active_bg_hex"] = "#111827"
                st.session_state["sia_rendered_output"] = build_ai_context_deck(deck)
                st.success("⚡ [Module 2 Rendered]: AI Contextual cards built successfully!")
                st.rerun()
            elif "Exact Inspiration Match" in active_selected_mode:
                st.session_state["sia_active_bg_hex"] = "#b0543c"
                headline = st.session_state.get("sia_insp_headline", "")
                flower = st.session_state.get("sia_insp_flower", "white rose")
                obj = st.session_state.get("sia_insp_object", "ceramic vase")
                dt = st.session_state.get("sia_insp_date", "OCT 8 • 2026")
                
                st.session_state["sia_rendered_output"] = build_inspiration_editorial_deck(
                    deck,
                    main_title=headline,
                    flower_query=flower,
                    object_query=obj,
                    date_str=dt
                )
                st.success("🎯 [Module 3 Rendered]: Exact Inspiration Match multi-slide deck built successfully!")
                st.rerun()
            elif "Unified Editorial Motif" in active_selected_mode:
                st.session_state["sia_active_bg_hex"] = "#111827"
                theme_val = st.session_state.get("sia_motif_theme_input", "flower")
                st.session_state["sia_rendered_output"] = build_unified_editorial_deck(deck, theme_val)
                st.success("🏛️ [Module 4 Rendered]: Unified Editorial Motif [" + theme_val + "] cards built successfully!")
                st.rerun()
            elif "Custom User Images" in active_selected_mode:
                st.session_state["sia_active_bg_hex"] = "#111827"
                b64_val = st.session_state.get("sia_custom_img_b64", "")
                st.session_state["sia_rendered_output"] = build_custom_user_deck(deck, b64_val)
                st.success("📂 [Module 5 Rendered]: Custom Brand Image cards built successfully!")
                st.rerun()
            else:
                st.info("🔥 Rendered Kinetic Loop ready for Instagram! Download your MP4 or GIF below.")

    render_visual_preview(st.session_state.get("sia_rendered_output"))
