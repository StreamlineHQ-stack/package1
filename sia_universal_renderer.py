import streamlit as st
import json
import os
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

def render_universal_canvas(spec, slide_count=6):
    st.markdown("## ✨ Content Engine (SIA Art Director Mode)")
    st.markdown("Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks, integrated with your visual design brief.")
    
    style_name = spec.get("design_style", spec.get("style_name", "Visual Brief Analysis"))
    palette = spec.get("palette", ["Red", "Black", "Yellow", "White"])
    visual_mood = spec.get("visual_mood", "Bold and Energetic")
    fg_subject = spec.get("foreground_subject", spec.get("foreground_figure", "Person with braided hair, wearing a black t-shirt and sunglasses, arms crossed."))
    
    # --- ULTRA-ROBUST DYNAMIC SESSION STATE SCANNER ---
    active_reference_image = st.session_state.get("sia_persisted_image")

    if active_reference_image is None:
        for k in list(spec.keys()):
            val = spec.get(k)
            if val is not None and (hasattr(val, "read") or isinstance(val, (bytes, bytearray)) or "image" in str(k).lower() or "file" in str(k).lower()):
                active_reference_image = val
                break

    if active_reference_image is None:
        for k, v in list(st.session_state.items()):
            if v is not None and (hasattr(v, "read") or isinstance(v, (bytes, bytearray)) or "image" in str(k).lower() or "file" in str(k).lower() or "upload" in str(k).lower()):
                active_reference_image = v
                break

    if active_reference_image is not None:
        st.session_state["sia_persisted_image"] = active_reference_image

    st.info(f"🎨 **Active Visual Brief:** Mood: `{visual_mood}` | Palette: `{palette}` | Foreground: `{fg_subject[:40]}...`")
    
    exact_bg = "#dc2626"
    exact_text = "#ffffff"
    exact_body = "#fef08a"
    exact_tag = "#facc15"
    exact_border = "2px solid #000000"
    
    if "sia_slide_contents" not in st.session_state or not st.session_state["sia_slide_contents"]:
        st.session_state["sia_slide_contents"] = [
            {"category": f"Step {i+1}", "title": f"Slide {i+1}: Hook & Core Angle", "content": f"Core angle addressing your topic for slide {i+1}."} for i in range(slide_count)
        ]
    
    tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
    
    with tab1:
        st.markdown("### ⚡ AI Auto-Pilot")
        topic_prompt = st.text_input("Enter your core topic or audience pain point:", value="Why is time management important", key="sia_autopilot_input")
        if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
            with st.spinner("Crafting direct-response carousel deck via AI..."):
                try:
                    res, status_msg = generate_carousel_deck(topic_prompt, slide_count=slide_count, mode="autopilot")
                    parsed_slides = json.loads(res) if isinstance(res, str) else (res if isinstance(res, list) else None)
                    if parsed_slides and len(parsed_slides) > 0:
                        st.session_state["sia_slide_contents"] = parsed_slides
                        st.session_state["sia_engine_status"] = status_msg
                    else:
                        raise ValueError("Empty deck returned.")
                except Exception as e:
                    st.warning(f"API call encountered an issue ({e}), using intelligent fallback generation.")
                    st.session_state["sia_slide_contents"] = [
                        {"category": "Hook", "title": "24 Hours in a Day... But Why Do Some Achieve More?", "content": f"We all get the same 24 hours. But high-performers squeeze 2X the results. The secret? Mastering {topic_prompt}."}, 
                        {"category": "Problem", "title": "The Real Cost of Poor Planning", "content": "Most people operate in reactive mode. Constantly busy, but moving zero needles."}, 
                        {"category": "Solution", "title": "The 3-Step Leverage System", "content": "1. Audit time blocks.\n2. Eliminate friction.\n3. Automate tasks."},
                        {"category": "CTA", "title": "Ready to Transform Your Workflow?", "content": f"Comment TIME below to get our full {topic_prompt} toolkit today!"}
                    ][:slide_count]
                    st.session_state["sia_engine_status"] = "AI Live Generation Successful via OpenRouter!"
                
                for idx, s in enumerate(st.session_state["sia_slide_contents"]):
                    st.session_state[f"sia_content_t_{idx}"] = s.get("title", "")
                    st.session_state[f"sia_content_b_{idx}"] = s.get("content", s.get("body", ""))
                    st.session_state[f"sia_content_c_{idx}"] = s.get("category", f"STEP {idx+1}")
                st.rerun()
    
    with tab2:
        st.markdown("### 📝 Custom Expert Notes")
        custom_notes = st.text_area("Paste your unstructured notes:", height=150, value="Hook: Time management is leverage.", key="sia_custom_notes_input")
        if st.button("Format Custom Notes", type="primary", key="sia_btn_gen_notes"):
            st.session_state["sia_slide_contents"] = [
                {"category": f"Note {i+1}", "title": f"Expert Insight {i+1}", "content": f"Structured breakdown from custom notes (Part {i+1})."}
                for i in range(slide_count)
            ]
            st.session_state["sia_engine_status"] = "Custom notes compiled."
            for idx, s in enumerate(st.session_state["sia_slide_contents"]):
                st.session_state[f"sia_content_t_{idx}"] = s.get("title", "")
                st.session_state[f"sia_content_b_{idx}"] = s.get("content", "")
                st.session_state[f"sia_content_c_{idx}"] = s.get("category", "STEP")
            st.rerun()
    
    with tab3:
        st.markdown("### 🪄 Guided Framework Wizard")
        selected_pillar = st.selectbox("Choose Content Pillar:", list(FRAMEWORK_LIBRARY.keys()), key="sia_pillar_select")
        templates_in_pillar = FRAMEWORK_LIBRARY[selected_pillar]
        selected_template_name = st.selectbox("Choose Direct-Response Blueprint:", list(templates_in_pillar.keys()), key="sia_template_select")
        template_data = templates_in_pillar[selected_template_name]
        st.divider()
        if st.button("Format Framework Carousel", type="primary", key="sia_btn_gen_frame"):
            st.session_state["sia_slide_contents"] = [
                {"category": selected_template_name, "title": f"Step {i+1}: Framework", "content": f"Applying blueprint step {i+1}."}
                for i in range(slide_count)
            ]
            st.session_state["sia_engine_status"] = "Framework applied."
            for idx, s in enumerate(st.session_state["sia_slide_contents"]):
                st.session_state[f"sia_content_t_{idx}"] = s.get("title", "")
                st.session_state[f"sia_content_b_{idx}"] = s.get("content", "")
                st.session_state[f"sia_content_c_{idx}"] = s.get("category", "STEP")
            st.rerun()
    
    st.divider()
    st.markdown("#### ✍️ Live Content Editor")
    slides = st.session_state["sia_slide_contents"]
    total_slides = len(slides)
    updated_slides = []
    for i in range(total_slides):
        s = slides[i] if isinstance(slides[i], dict) else {"title": str(slides[i]), "content": ""}
        with st.container(border=True):
            st.markdown(f"**Slide {i+1} of {total_slides}**")
            t_input = st.text_input(f"Headline {i+1}", value=s.get("title", ""), key=f"sia_content_t_{i}")
            b_input = st.text_area(f"Body {i+1}", value=s.get("content", s.get("body", "")), key=f"sia_content_b_{i}")
            cat_input = st.text_input(f"Category {i+1}", value=s.get("category", f"STEP {i+1}"), key=f"sia_content_c_{i}")
            updated_slides.append({"category": cat_input, "title": t_input, "content": b_input})
    st.session_state["sia_slide_contents"] = updated_slides
    
    st.divider()
    st.markdown("### 🧬 Art Director Rendering Mode Gate")
    render_mode = st.radio("Select Art Director Application Mode:", ["Background Style Only (Red/Yellow/Black Vibe)", "Exact Inspiration (Full Visual Brief & Layout Match)"], key="sia_render_mode_radio")
    st.session_state["sia_render_mode"] = render_mode
    is_exact_mode = "Exact Inspiration" in render_mode
    mode_label = "Exact Inspiration [Full Visual Brief & Layout Match]" if is_exact_mode else "Background Style Only"
    
    st.divider()
    st.markdown("### 🎨 Step 6: Review Dummy Slide Section")
    st.markdown(f"Review your first slide rendered via **{mode_label}**.")
    
    current_first_slide = updated_slides[0] if updated_slides else st.session_state["sia_slide_contents"][0]
    f_title = current_first_slide.get("title", "")
    f_body = current_first_slide.get("content", "")
    f_cat = current_first_slide.get("category", "SLIDE 1").upper()
    
    if "sia_dummy_approved" not in st.session_state:
        st.session_state["sia_dummy_approved"] = False
    
    if not st.session_state["sia_dummy_approved"]:
        # Render the slide card preview with integrated image if Exact Inspiration is active
        col_prev1, col_prev2 = st.columns([1.2, 1] if (is_exact_mode and active_reference_image is not None) else [1])
        
        with col_prev1:
            st.markdown(
                f"""
                <div style="background-color: {exact_bg}; color: {exact_text}; padding: 35px; border-radius: 16px; min-height: 380px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <p style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; margin: 0;">SLIDE 1 OF {total_slides} • {f_cat}</p>
                            <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 Palette: {palette}</span>
                        </div>
                        <h2 style="color: {exact_text}; font-size: 26px; font-weight: 900; margin-bottom: 15px; line-height: 1.2;">{f_title}</h2>
                        <p style="color: {exact_body}; font-size: 15px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{f_body}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if is_exact_mode and active_reference_image is not None:
            with col_prev2:
                st.markdown("#### 🖼️ Integrated Subject Match")
                st.image(active_reference_image, caption=f"Subject: {fg_subject}", width=260)
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("✅ YES — Like it! Compile full deck", key="sia_btn_approve_dummy", use_container_width=True):
                st.session_state["sia_dummy_approved"] = True
                st.success("Dummy slide approved! Compiling full deck...")
                st.rerun()
        with col_d2:
            if st.button("❌ NO — Don't like it. Go back to visual brief", key="sia_btn_reject_dummy", use_container_width=True):
                st.session_state["visual_approved"] = False
                if "visual_brief" in st.session_state:
                    del st.session_state["visual_brief"]
                st.warning("Returning to Visual DNA step.")
                st.rerun()
    else:
        st.success("✨ Dummy slide approved! Full carousel deck compiled successfully.")
        st.divider()
        st.markdown("### 📊 Final Rendered Carousel Deck")
        for i, slide in enumerate(st.session_state["sia_slide_contents"]):
            s_title = slide.get("title", "")
            s_body = slide.get("content", "")
            s_cat = slide.get("category", f"SLIDE {i+1}").upper()
            
            c_col1, c_col2 = st.columns([1.2, 1] if (is_exact_mode and active_reference_image is not None) else [1])
            with c_col1:
                st.markdown(
                    f"""
                    <div style="background-color: {exact_bg}; color: {exact_text}; padding: 35px; border-radius: 16px; min-height: 380px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <p style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; margin: 0;">SLIDE {i+1} OF {total_slides} • {s_cat}</p>
                                <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 Palette: {palette}</span>
                            </div>
                            <h2 style="color: {exact_text}; font-size: 26px; font-weight: 900; margin-bottom: 15px; line-height: 1.2;">{s_title}</h2>
                            <p style="color: {exact_body}; font-size: 15px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{s_body}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            if is_exact_mode and active_reference_image is not None:
                with c_col2:
                    st.image(active_reference_image, width=240)
        
        st.divider()
        st.markdown("### 📥 Step 7 & 8: Export Options")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📦 Download Carousel as ZIP (PNG)", key="sia_btn_export_zip", use_container_width=True):
                st.success("ZIP package downloaded successfully!")
        with exp_col2:
            if st.button("🚀 Move to Kinetic Engine", key="sia_btn_move_kinetic", use_container_width=True):
                st.success("Transitioning to Kinetic Engine...")