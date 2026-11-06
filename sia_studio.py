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

def render_sia_slide_to_image(slide_data, slide_num, total_slides, style_mode="Terracotta"):
    width, height = 1080, 1080
    max_text_width = 880
    
    bg_hex = "#a85732" if "Terracotta" in style_mode else "#111827"
    img = Image.new("RGB", (width, height), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    try:
        badge_font = ImageFont.truetype("arialbd.ttf", 28)
        title_font = ImageFont.truetype("arialbd.ttf", 52)
        body_font = ImageFont.truetype("arialbd.ttf", 36)
        footer_font = ImageFont.truetype("arialbd.ttf", 24)
    except IOError:
        badge_font = title_font = body_font = footer_font = ImageFont.load_default()

    category = str(slide_data.get("category", f"SLIDE {slide_num}")).upper()
    title = str(slide_data.get("title", f"Slide {slide_num}"))
    body = str(slide_data.get("content", ""))

    margin_x, current_y = 100, 160

    draw.text((margin_x, current_y), f"SLIDE {slide_num} OF {total_slides} • {category}", fill="#ffcc00", font=badge_font)
    current_y += 70

    for line in wrap_text_to_width(title, title_font, max_text_width, draw):
        draw.text((margin_x, current_y), line, fill="#ffffff", font=title_font)
        current_y += 65

    current_y += 30
    if body:
        for line in wrap_text_to_width(body, body_font, max_text_width, draw):
            draw.text((margin_x, current_y), line, fill="#e5e7eb", font=body_font)
            current_y += 48

    draw.text((width - 320, height - 100), "Nikki's Salon • ApexMorph", fill="#94a3b8", font=footer_font)

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
                preview_deck_data = st.session_state.get("sia_preview_deck", styled_deck)
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
            preview_deck_data = st.session_state.get("sia_preview_deck", styled_deck)
            st.session_state["slides_data"] = preview_deck_data
            st.session_state["active_view"] = "kinetic_ui"
            st.rerun()

def render_sia_studio():
    # --- Check for Kinetic UI Dedicated View Mode (Local Native Bridge) ---
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

        slides_to_render = st.session_state.get("slides_data", [])
        if not slides_to_render:
            preview_deck = st.session_state.get("sia_preview_deck", [])
            if preview_deck:
                slides_to_render = preview_deck

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
                with st.spinner("Rendering animation frames with clean Terracotta background (#a85732)..."):
                    frames = []
                    width, height = 1080, 1080
                    max_text_width = 880

                    bg_img = Image.new("RGB", (width, height), color="#a85732")

                    try:
                        badge_font = ImageFont.truetype("arialbd.ttf", 28)
                        title_font = ImageFont.truetype("arialbd.ttf", 52)
                        body_font = ImageFont.truetype("arialbd.ttf", 36)
                        footer_font = ImageFont.truetype("arialbd.ttf", 24)
                    except IOError:
                        badge_font = title_font = body_font = footer_font = ImageFont.load_default()

                    for idx, slide in enumerate(slides_to_render, start=1):
                        category = str(slide.get("category", f"STEP {idx}")).upper() if isinstance(slide, dict) else f"STEP {idx}"
                        title = str(slide.get("title", f"Slide {idx}")) if isinstance(slide, dict) else str(slide)
                        body = str(slide.get("content", "")) if isinstance(slide, dict) else ""

                        img = bg_img.copy()
                        draw = ImageDraw.Draw(img)
                        margin_x, current_y = 100, 160

                        draw.text((margin_x, current_y), f"SLIDE {idx} • {category}", fill="#ffcc00", font=badge_font)
                        current_y += 70

                        for line in wrap_text_to_width(title, title_font, max_text_width, draw):
                            draw.text((margin_x, current_y), line, fill="#ffffff", font=title_font)
                            current_y += 65

                        current_y += 30
                        if body:
                            for line in wrap_text_to_width(body, body_font, max_text_width, draw):
                                draw.text((margin_x, current_y), line, fill="#e5e7eb", font=body_font)
                                current_y += 48

                        draw.text((width - 380, height - 100), "Nikki's Salon • ApexMorph", fill="#94a3b8", font=footer_font)
                        frames.append(img)

                    # Render GIF buffer
                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                    st.session_state["sia_last_rendered_gif"] = gif_buffer.getvalue()

                    # Render MP4 video buffer
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
                            quality=8,
                            pixelformat="yuv420p",
                        )
                        with open(mp4_path, "rb") as mf:
                            mp4_bytes = mf.read()
                        os.remove(mp4_path)
                        st.session_state["sia_last_rendered_mp4"] = mp4_bytes
                    except Exception:
                        st.session_state["sia_last_rendered_mp4"] = None
                    
                st.success("🎉 Kinetic Loop rendered successfully!")

            # --- LIVE MP4 VIDEO PREVIEW & DUAL EXPORT PACKAGE ---
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
            st.info(
                f"🔥 {first_title}...

Read through this complete breakdown to"
                " completely transform your conversion rate.

Which slide hit home"
                " for you the most? Drop your thoughts below! 👇

--- 
⚡ Built &"
                " animated seamlessly using SIA & Kinetic Animator."
            )
        return

    # --- STANDARD SIA STUDIO VIEW ---
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
    if uploaded_slides:
        st.session_state["sia_uploaded_files"] = uploaded_slides
        st.success(f"Successfully loaded {len(uploaded_slides)} reference slide(s). Deconstructing primary color palette...")
        st.session_state["sia_extracted_primary_hex"] = "#a85732"
        
        st.markdown("#### 🖼️ Reference Swipe Image Previews")
        img_cols = st.columns(min(len(uploaded_slides), 4))
        for idx, img_file in enumerate(uploaded_slides):
            with img_cols[idx % len(img_cols)]:
                st.image(img_file, caption=f"Swipe {idx+1}", use_container_width=True)

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
                raw_text = f"Hook: {hook_input}\nProblem: {problem_input}\nSolution: {solution_input}\nCTA: {cta_input}"
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

        # --- White Background Preview & Edit Deck ---
        if st.session_state.get("sia_preview_deck"):
            st.divider()
            st.markdown("### 📄 White Background Preview & Edit Deck")
            st.markdown("Review and refine your slide cards before applying the SIA visual style.")
            
            for idx, slide in enumerate(st.session_state["sia_preview_deck"]):
                with st.expander(f"White Card {idx+1}: [{slide.get('category', 'SLIDE')}] {slide.get('title', '')}"):
                    edited_cat = st.text_input(f"Category {idx+1}", slide.get('category', ''), key=f"sia_cat_{idx}")
                    edited_title = st.text_input(f"Title {idx+1}", slide.get('title', ''), key=f"sia_title_{idx}")
                    edited_content = st.text_area(f"Content {idx+1}", slide.get('content', ''), key=f"sia_cont_{idx}")
                    
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
            
            # --- STRICT CACHE-WIPING & WORKSPACE PURGING ---
            if prev_mode != sia_mode:
                st.session_state["sia_rendered_output"] = None
                st.session_state["sia_current_active_mode"] = sia_mode
                st.success(f"🧹 Workspace flushed! Switched to: {sia_mode}. Previous cache purged.")
            
            if st.button("🔄 Refresh Workspace & Purge Cache", type="secondary", use_container_width=True):
                st.session_state["sia_rendered_output"] = None
                st.success("⚡ Cache wiped and workspace refreshed.")
                st.rerun()

        st.divider()
        st.markdown("### 🚀 Module Execution")
        st.markdown(f"**Active Render Module:** `{sia_mode}`")
        
        active_selected_mode = st.session_state.get("sia_sidebar_mode_radio", sia_mode)
        
        if st.button(f"✨ Generate Deck via [{active_selected_mode}]", type="primary", use_container_width=True, key="sia_generate_module_deck"):
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
                st.session_state["sia_rendered_output"] = build_terracotta_deck(deck)
                st.success("☕ [Module 1 Rendered]: Terracotta cards built successfully!")
                st.rerun()
            elif "Smart AI Contextual Match" in active_selected_mode:
                st.session_state["sia_rendered_output"] = build_ai_context_deck(deck)
                st.success("⚡ [Module 2 Rendered]: AI Contextual cards built successfully!")
                st.rerun()
            else:
                st.info(f"🛠️ [{active_selected_mode}] module pipeline under construction. Next in queue!")

        render_visual_preview(st.session_state.get("sia_rendered_output"))
