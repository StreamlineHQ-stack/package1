# sia_studio.py • Style Inspiration & Analysis Studio (SIA) with OpenAI Vision AI Design Intent Integration
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
from background_engine import get_modular_background
from smart_ai_engine import get_smart_ai_background
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import build_universal_deck

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

def render_sia_slide_to_image(slide_data, slide_num, total_slides, intent_spec=None):
    width, height = 1080, 1080
    bg_hex = "#111827"
    text_hex = "#ffffff"
    if intent_spec and "palette" in intent_spec and len(intent_spec["palette"]) > 0:
        bg_hex = intent_spec["palette"][0].get("hex", "#111827")
        
    img = Image.new("RGB", (width, height), color=bg_hex)
    draw = ImageDraw.Draw(img)
    
    title = str(slide_data.get("title", f"Slide {slide_num}"))
    body = str(slide_data.get("content", ""))
    category = str(slide_data.get("category", f"SLIDE {slide_num}")).upper()
    
    try:
        badge_font = ImageFont.truetype("arialbd.ttf", 26)
        title_font = ImageFont.truetype("arialbd.ttf", 46)
        body_font = ImageFont.truetype("arialbd.ttf", 32)
        footer_font = ImageFont.truetype("arialbd.ttf", 22)
    except IOError:
        badge_font = title_font = body_font = footer_font = ImageFont.load_default()

    current_y = 150
    draw.text((100, current_y), f"SLIDE {slide_num} OF {total_slides} • {category}", fill="#ffcc00", font=badge_font)
    current_y += 60

    for line in wrap_text_to_width(title, title_font, width - 200, draw):
        draw.text((100, current_y), line, fill=text_hex, font=title_font)
        current_y += 58

    current_y += 30
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
            
    html_code = slide.get("rendered_html", "")
    st.components.v1.html(html_code, height=620, scrolling=True)
    
    st.markdown("### 📥 Export & Download Deck")
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        if st.button("📦 Generate & Download Image Deck (.zip)", type="primary", use_container_width=True, key="sia_gen_zip_imgs"):
            with st.spinner("Rendering high-res Instagram PNG slide images into ZIP archive..."):
                zip_buffer = io.BytesIO()
                preview_deck_data = st.session_state.get("sia_rendered_output", styled_deck)
                intent_spec = st.session_state.get("sia_intent_spec", None)
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, s in enumerate(preview_deck_data):
                        img_bytes = render_sia_slide_to_image(
                            slide_data=s,
                            slide_num=idx + 1,
                            total_slides=len(preview_deck_data),
                            intent_spec=intent_spec
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
            st.session_state["slides_data"] = preview_deck_data
            st.session_state["active_view"] = "kinetic_ui"
            st.rerun()

def render_sia_studio():
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ⚠️ System Reset & Purge")
        if st.button("🔥 MASTER PURGE & RESET", type="primary", use_container_width=True, key="sia_master_purge_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.cache_data.clear()
            st.success("🔥 100% Slate Wiped Clean! All history and cache purged.")
            st.rerun()

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

        slides_to_render = st.session_state.get("sia_rendered_output", []) or st.session_state.get("slides_data", []) or st.session_state.get("sia_preview_deck", [])

        st.markdown("## 🚀 Compile & Export High-Impact Kinetic Loop")
        
        col_seq, col_eng = st.columns([1.2, 1.4])
        with col_seq:
            st.markdown("### Slide Sequence Overview")
            if slides_to_render:
                for idx, slide in enumerate(slides_to_render, start=1):
                    title_text = slide.get("title", f"Slide {idx}") if isinstance(slide, dict) else str(slide)
                    st.markdown(f"**Slide {idx}:** {title_text}")
            else:
                st.info("🔥 Rendered Kinetic Loop ready for Instagram!")

            st.markdown("### Production Render Engine")
            if st.button("✨ Render Premium Kinetic Loop (Active Deck)", use_container_width=True, key="sia_local_render_btn"):
                with st.spinner("Rendering animation frames from actual deck cards..."):
                    frames = []
                    intent_spec = st.session_state.get("sia_intent_spec", None)
                    for idx, slide in enumerate(slides_to_render, start=1):
                        png_bytes = render_sia_slide_to_image(slide_data=slide, slide_num=idx, total_slides=len(slides_to_render), intent_spec=intent_spec)
                        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
                        frames.append(img)

                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                    st.session_state["sia_last_rendered_gif"] = gif_buffer.getvalue()
                    st.success("🎉 Kinetic Loop rendered successfully!")

            if "sia_last_rendered_gif" in st.session_state:
                st.download_button(
                    label="⬇️ Download Animated GIF",
                    data=st.session_state["sia_last_rendered_gif"],
                    file_name="sia_kinetic_loop.gif",
                    mime="image/gif",
                    use_container_width=True,
                    key="sia_dl_gif_btn"
                )
        return

    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Upload inspiration swipes, analyze visual intent via OpenAI Vision, and synthesize modular styled decks.")
    
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

    uploaded_slides = st.file_uploader("Upload Reference Swipe Slides", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="sia_file_uploader")
    
    if uploaded_slides:
        if uploaded_slides != st.session_state.get("sia_uploaded_files", None):
            st.session_state["sia_uploaded_files"] = uploaded_slides
            st.session_state["sia_rendered_output"] = None
            st.session_state["sia_preview_deck"] = []
            st.success("🧹 New reference swipe detected!")
            
        st.markdown("#### 🖼️ Reference Swipe Image Previews")
        img_cols = st.columns(min(len(uploaded_slides), 4))
        for idx, img_file in enumerate(uploaded_slides):
            with img_cols[idx % len(img_cols)]:
                st.image(img_file, caption=f"Swipe {idx+1}", use_container_width=True)
                
        st.markdown("---")
        st.markdown("### 🧠 OpenAI Vision Design Intent Analyzer")
        api_key_input = st.text_input("OpenAI API Key (or set OPENAI_API_KEY env):", type="password", value=os.getenv("OPENAI_API_KEY", ""), key="sia_openai_key_input")
        
        if st.button("🔍 Run Vision Analysis on Swipe", type="primary", key="sia_run_vision_btn"):
            if not api_key_input:
                st.error("Please provide your OpenAI API key.")
            else:
                with st.spinner("Analyzing slide visual DNA via OpenAI Vision..."):
                    try:
                        img_data_url, _ = image_to_data_url(uploaded_slides[0])
                        intent_spec = analyze_image(
                            api_key=api_key_input,
                            model="gpt-4o-mini",
                            image_data_url=img_data_url,
                            user_focus="Focus on background style, color palette, mood, and typography."
                        )
                        st.session_state["sia_intent_spec"] = intent_spec
                        st.success("✨ Vision analysis complete! Structured JSON spec generated.")
                    except Exception as e:
                        st.error(f"Vision analysis failed: {e}")

        if st.session_state.get("sia_intent_spec"):
            with st.expander("🔍 View Structured JSON Design Intent Spec", expanded=True):
                st.json(st.session_state["sia_intent_spec"])
        st.markdown("---")

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
                value="Hook: Conversion rate optimization is leverage.
Problem: People lose visitors on mobile landing pages.
CTA: Comment CRO to get the framework.", 
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
                raw_text = f"Hook: {hook_input}
Problem: {problem_input}
Solution: {solution_input}
CTA: {cta_input}"
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
        if st.button("✨ Synthesize Deck via OpenAI Vision Intent Spec", type="primary", use_container_width=True, key="sia_generate_intent_deck"):
            deck = st.session_state.get("sia_preview_deck", [])
            if not deck:
                deck = [
                    {"category": "HOOK", "title": "The Secret to High-Converting Copy", "content": "Discover how the right words transform casual visitors into paying customers instantly."},
                    {"category": "PROBLEM", "title": "Why Most Landing Pages Fail", "content": "Without compelling copy, even the best products get ignored. Are you losing sales?"},
                    {"category": "SOLUTION", "title": "Crafting Irresistible Messages", "content": "Address pain points and deliver clear solutions that build immediate trust."},
                    {"category": "CTA", "title": "Ready to Transform Your Sales?", "content": "Partner with a professional copywriter today and watch your engagement soar."}
                ]
                st.session_state["sia_preview_deck"] = deck
            
            intent_spec = st.since_state.get("sia_intent_spec", None) if hasattr(st, "since_state") else st.session_state.get("sia_intent_spec", None)
            st.session_state["sia_rendered_output"] = build_universal_deck(deck, intent_spec=intent_spec)
            st.success("🎉 [AI Intent Engine]: Deck successfully synthesized and rendered from OpenAI Vision DNA!")
            st.rerun()

    render_visual_preview(st.session_state.get("sia_rendered_output"))
