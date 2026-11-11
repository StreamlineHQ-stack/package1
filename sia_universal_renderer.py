import streamlit as st
import json
import os
import io
import zipfile
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from sia_ai_context_module import build_ai_context_deck
from sia_editorial_motif_module import build_unified_editorial_deck

def render_carousel_slide_to_image(slide_data, slide_num, total_slides, bg_color="#0b0f19", text_color="#ffffff", body_color="#d1d5db", tag_color="#34d399"):
    # Fallback helper for rendering images if PIL is used
    return b""

def render_universal_canvas(spec, slide_count=4, content_only_mode=False, standalone_mode=False):
    palette = spec.get("palette", ["Red", "Black", "Yellow", "White"])
    visual_mood = spec.get("visual_mood", "Bold and Energetic")
    
    # --- CROSS-MODULE BRIDGE FOR FEATURE-TO-BENEFITS ---
    external_payload = (
        st.session_state.get("sia_slide_contents") or 
        st.session_state.get("feature_benefits_slides") or 
        st.session_state.get("imported_carousel_content")
    )
    
    incoming_flag = False
    if external_payload and isinstance(external_payload, list) and len(external_payload) > 0:
        is_default = len(external_payload) == 4 and "Hook & Core Angle" in str(external_payload[0])
        if not is_default or "sia_content_received_banner" not in st.session_state:
            st.session_state["sia_slide_contents"] = external_payload
            st.session_state["sia_content_received_banner"] = True
            incoming_flag = True

    if "sia_slide_contents" not in st.session_state or len(st.session_state["sia_slide_contents"]) != slide_count:
        if not incoming_flag and not st.session_state.get("sia_slide_contents"):
            st.session_state["sia_slide_contents"] = [
                {"category": f"STEP {i+1}", "title": f"Slide {i+1}: Hook & Core Angle", "content": f"Core angle addressing your topic for slide {i+1}."} for i in range(slide_count)
            ]

    # ==========================================
    # STEP 1: CONTENT ENGINE & COPYWRITING SUITE
    # ==========================================
    if content_only_mode:
        st.markdown("### 📝 Content Engine & Copywriting Suite")
        
        if st.session_state.get("sia_content_received_banner", False):
            st.success("✨ Content successfully received from Feature-to-Benefits! Loaded into Live Content Editor below for review and approval.")
        
        st.markdown(f"Building custom carousel with **{slide_count} slides**. Refine and structure your copy below.")
        
        tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
        
        with tab1:
            topic_prompt = st.text_input("Enter core topic or pain point:", value="Why time management matters", key="sia_autopilot_input")
            if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
                with st.spinner(f"Crafting direct-response {slide_count}-slide carousel deck..."):
                    default_titles = [
                        f"Why {topic_prompt} Is Costing You Clients",
                        "The Hidden Cost of Inefficiency",
                        "The 3-Step Execution Model",
                        "Step 1: Audit Your Time Blocks",
                        "Step 2: Eliminate Friction Points",
                        "Step 3: Automate Workflows",
                        "Overcoming Common Bottlenecks",
                        "Scaling Your Daily Output",
                        "Measuring Your Time Leverage",
                        "Want the Exact System?"
                    ]
                    new_slides = []
                    for i in range(slide_count):
                        cat = "HOOK" if i == 0 else ("CTA" if i == slide_count - 1 else f"STEP {i+1}")
                        t = default_titles[i % len(default_titles)]
                        c = f"Detailed breakdown and actionable execution strategy for slide {i+1} addressing {topic_prompt}."
                        new_slides.append({"category": cat, "title": t, "content": c})
                        
                    st.session_state["sia_slide_contents"] = new_slides
                    st.session_state["sia_content_received_banner"] = False
                    for idx, s in enumerate(new_slides):
                        st.session_state[f"sia_content_t_{idx}"] = s["title"]
                        st.session_state[f"sia_content_b_{idx}"] = s["content"]
                        st.session_state[f"sia_content_c_{idx}"] = s["category"]
                    st.success("Auto-pilot generated successfully!")
                    st.rerun()
        
        with tab2:
            custom_notes = st.text_area("Paste notes:", value="Hook: Time management is leverage.", key="sia_custom_notes_input")
            if st.button("Format Custom Notes", type="primary", key="sia_btn_gen_notes"):
                new_slides = [
                    {"category": f"INSIGHT {i+1}", "title": f"Expert Breakdown {i+1}", "content": f"Structured insights based on notes: {custom_notes[:30]}..."}
                    for i in range(slide_count)
                ]
                st.session_state["sia_slide_contents"] = new_slides
                st.session_state["sia_content_received_banner"] = False
                for idx, s in enumerate(new_slides):
                    st.session_state[f"sia_content_t_{idx}"] = s["title"]
                    st.session_state[f"sia_content_b_{idx}"] = s["content"]
                    st.session_state[f"sia_content_c_{idx}"] = s["category"]
                st.success("Custom notes compiled!")
                st.rerun()
                
        with tab3:
            selected_pillar = st.selectbox("Choose Content Pillar:", list(FRAMEWORK_LIBRARY.keys()), key="sia_pillar_select")
            templates_in_pillar = FRAMEWORK_LIBRARY[selected_pillar]
            selected_template_name = st.selectbox("Choose Blueprint:", list(templates_in_pillar.keys()), key="sia_template_select")
            if st.button("Format Framework Carousel", type="primary", key="sia_btn_gen_frame"):
                new_slides = [
                    {"category": selected_template_name.upper(), "title": f"Step {i+1}: Framework execution", "content": f"Executing blueprint step {i+1} for maximum engagement."}
                    for i in range(slide_count)
                ]
                st.session_state["sia_slide_contents"] = new_slides
                st.session_state["sia_content_received_banner"] = False
                for idx, s in enumerate(new_slides):
                    st.session_state[f"sia_content_t_{idx}"] = s["title"]
                    st.session_state[f"sia_content_b_{idx}"] = s["content"]
                    st.session_state[f"sia_content_c_{idx}"] = s["category"]
                st.success("Framework applied!")
                st.rerun()

        st.divider()
        st.markdown(f"#### ✍️ Live Content Editor ({slide_count} Slides Active)")
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
        if st.button("🚀 Lock Content & Proceed to Step 2: Visual Engine", type="primary", use_container_width=True):
            st.session_state["sia_content_locked"] = True
            st.success("✨ Content locked and saved in session state! Switch to Step 2 above to configure your visual engine.")
            st.session_state["sia_workflow_step"] = "step2_visual"
            st.rerun()
        return

    # ==========================================
    # WORKFLOW 1: STANDALONE MODE (3B Modules)
    # ==========================================
    if standalone_mode:
        payload = spec.get("standalone_payload", {})
        mod_type = payload.get("type", "Smart AI Background")
        slides = st.session_state.get("sia_slide_contents", [])
        
        st.markdown(f"### 📊 Standalone Visual Modules — Full Deck Preview (`{mod_type}`)")
        
        rendered_deck = []
        if "Smart AI Background" in mod_type:
            rendered_deck = build_ai_context_deck(slides)
        elif "Unified Motif" in mod_type:
            motif_theme = payload.get("motif", "floral")
            rendered_deck = build_unified_editorial_deck(slides, motif_theme=motif_theme)
        else:
            custom_bytes = payload.get("custom_image_bytes")
            import base64
            img_data_uri = ""
            if custom_bytes:
                encoded = base64.b64encode(custom_bytes).decode("utf-8")
                img_data_uri = f"data:image/png;base64,{encoded}"
                
            for idx, slide in enumerate(slides):
                cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
                title = str(slide.get("title", f"Slide {idx+1}"))
                content = str(slide.get("content", ""))
                
                html = f"""
                <div style="background: #0b0f19; padding: 40px; border-radius: 24px; border: 3px solid #3b82f6; max-width: 680px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
                    <div style="width: 100%; height: 240px; border-radius: 16px; overflow: hidden; margin-bottom: 24px; border: 2px solid #60a5fa;">
                        {f'<img src="{img_data_uri}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />' if img_data_uri else '<div style="background:#1e293b; width:100%; height:100%; display:flex; align-items:center; justify-content:center; color:#94a3b8;">No Custom Image Uploaded</div>'}
                    </div>
                    <div style="color: #60a5fa; font-size: 14px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 12px; text-transform: uppercase;">
                        CUSTOM IMAGE • SLIDE {idx+1} OF {len(slides)} • {cat}
                    </div>
                    <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 16px;">
                        {title}
                    </h2>
                    <p style="color: #d1d5db; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                        {content}
                    </p>
                </div>
                """
                rendered_deck.append({"rendered_html": html})

        for item in rendered_deck:
            st.markdown(item["rendered_html"], unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📥 Export Options & Kinetic Handoff")
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="standalone_kinetic_btn"):
                st.session_state["slides_data"] = slides
                st.session_state["deck_json"] = slides
                st.session_state["active_view"] = "kinetic_ui"
                st.rerun()

        with exp_col2:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, s in enumerate(slides):
                    zip_file.writestr(f"carousel_slide_{idx+1}.json", json.dumps(s, indent=2))
            zip_buffer.seek(0)
            st.download_button(
                label="📦 Download Deck (.zip)",
                data=zip_buffer,
                file_name="carousel_deck_package.zip",
                mime="application/zip",
                use_container_width=True,
                key="standalone_download_zip"
            )

        with exp_col3:
            if st.button("🔄 Edit Content Again", key="standalone_restart", use_container_width=True):
                st.session_state["sia_workflow_step"] = "step1_content"
                st.rerun()
        return

    # ==========================================
    # WORKFLOW 2: REFERENCE SLIDE ART DIRECTOR ROUTING (3A)
    # ==========================================
    st.markdown("### 🎨 Visual Engine & Art Director Asset Routing")
    
    render_mode = st.radio(
        "Select Asset Preservation Mode:", 
        [
            "Mode A — Preserve Original Foreground Image (YES)", 
            "Mode B — Replace with User-Supplied Image (NO + Upload)", 
            "Mode C — Background Only / No Asset"
        ], 
        key="sia_render_mode_radio"
    )
    
    active_foreground_bytes = None
    if "Mode A" in render_mode:
        active_foreground_bytes = st.session_state.get("original_image_bytes", st.session_state.get("sia_persisted_image"))
        if active_foreground_bytes is None:
            re_up = st.file_uploader("Upload Inspiration Asset:", type=["png", "jpg", "jpeg"], key="mode_a_reup")
            if re_up is not None:
                active_foreground_bytes = re_up.getvalue()
                st.session_state["original_image_bytes"] = active_foreground_bytes
                st.rerun()
    elif "Mode B" in render_mode:
        replacement_file = st.file_uploader("Upload Replacement Asset:", type=["png", "jpg", "jpeg"], key="mode_b_upload")
        if replacement_file is not None:
            active_foreground_bytes = replacement_file.getvalue()

    st.divider()
    st.markdown("### 🎨 Review Single Dummy Slide Preview")
    
    slides = st.session_state.get("sia_slide_contents", [])
    current_first_slide = slides[0] if slides else {"title": "Sample Title", "content": "Sample Content", "category": "HOOK"}
    f_title = current_first_slide.get("title", "")
    f_body = current_first_slide.get("content", "")
    f_cat = current_first_slide.get("category", "SLIDE 1").upper()
    total_slides = len(slides)
    
    has_asset = bool(active_foreground_bytes is not None and "Mode C" not in render_mode)
    col_prev1, col_prev2 = st.columns([1.2, 1] if has_asset else [1])
    
    exact_bg = "#dc2626"
    exact_text = "#ffffff"
    exact_body = "#fef08a"
    exact_tag = "#facc15"
    exact_border = "2px solid #000000"

    with col_prev1:
        st.markdown(
            f"""
            <div style="background-color: {exact_bg}; color: {exact_text}; padding: 40px; border-radius: 16px; min-height: 400px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 20px;">
                        <span style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase;">SLIDE 1 OF {total_slides} • {f_cat}</span>
                        <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 6px 12px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 {palette}</span>
                    </div>
                    <h2 style="color: {exact_text}; font-size: 28px; font-weight: 900; margin-top: 0; margin-bottom: 15px; line-height: 1.2;">{f_title}</h2>
                    <p style="color: {exact_body}; font-size: 16px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{f_body}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if has_asset:
        with col_prev2:
            st.markdown("#### 🖼️ Routed Asset Match")
            st.image(active_foreground_bytes, caption=f"Asset (Mode: {render_mode[:6]})", width=280)
    
    st.divider()
    if st.button("✅ Approve Dummy & Render Complete Deck", type="primary", key="sia_btn_approve_dummy", use_container_width=True):
        st.success("✨ Full carousel deck compiled successfully!")
        st.markdown("### 📊 Final Rendered Carousel Deck")
        for i, slide in enumerate(slides):
            s_title = slide.get("title", "")
            s_body = slide.get("content", "")
            s_cat = slide.get("category", f"SLIDE {i+1}").upper()
            
            c_col1, c_col2 = st.columns([1.2, 1] if has_asset else [1])
            with c_col1:
                st.markdown(
                    f"""
                    <div style="background-color: {exact_bg}; color: {exact_text}; padding: 35px; border-radius: 16px; min-height: 380px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; margin-bottom: 20px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 15px;">
                                <span style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase;">SLIDE {i+1} OF {total_slides} • {s_cat}</span>
                                <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 6px 12px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 {palette}</span>
                            </div>
                            <h2 style="color: {exact_text}; font-size: 26px; font-weight: 900; margin-top: 0; margin-bottom: 15px; line-height: 1.2;">{s_title}</h2>
                            <p style="color: {exact_body}; font-size: 15px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{s_body}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            if has_asset:
                with c_col2:
                    st.image(active_foreground_bytes, width=240)
        
        st.divider()
        st.markdown("### 📥 Export Options & Kinetic Handoff")
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="workflow2_kinetic_btn"):
                st.session_state["slides_data"] = slides
                st.session_state["deck_json"] = slides
                st.session_state["active_view"] = "kinetic_ui"
                st.rerun()

        with exp_col2:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, s in enumerate(slides):
                    zip_file.writestr(f"carousel_slide_{idx+1}.json", json.dumps(s, indent=2))
            zip_buffer.seek(0)
            st.download_button(
                label="📦 Download Deck (.zip)",
                data=zip_buffer,
                file_name="carousel_deck_package.zip",
                mime="application/zip",
                use_container_width=True,
                key="workflow2_download_zip"
            )

        with exp_col3:
            if st.button("🔄 Edit Content Again", key="workflow2_restart", use_container_width=True):
                st.session_state["sia_workflow_step"] = "step1_content"
                st.rerun()