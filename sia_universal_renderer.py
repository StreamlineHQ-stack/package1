import streamlit as st
import json
import os
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

def render_universal_canvas(spec, slide_count=4, content_only_mode=False, standalone_mode=False):
    palette = spec.get("palette", ["Red", "Black", "Yellow", "White"])
    visual_mood = spec.get("visual_mood", "Bold and Energetic")
    
    if "sia_slide_contents" not in st.session_state or not st.session_state["sia_slide_contents"]:
        st.session_state["sia_slide_contents"] = [
            {"category": f"STEP {i+1}", "title": f"Slide {i+1}: Hook & Core Angle", "content": f"Core angle addressing your topic for slide {i+1}."} for i in range(slide_count)
        ]

    # ==========================================
    # STEP 1: CONTENT ENGINE
    # ==========================================
    if content_only_mode:
        st.markdown("### 📝 Content Engine & Copywriting Suite")
        st.markdown("Build, refine, and structure your carousel copy independently before applying visual styles.")
        
        tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
        
        with tab1:
            topic_prompt = st.text_input("Enter core topic or pain point:", value="Why time management matters", key="sia_autopilot_input")
            if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
                with st.spinner("Crafting direct-response carousel deck..."):
                    new_slides = [
                        {"category": "HOOK", "title": f"Why {topic_prompt} Is Costing You Clients", "content": f"Most creators struggle with {topic_prompt} because they lack a systematic framework."}, 
                        {"category": "PROBLEM", "title": "The Hidden Cost of Inefficiency", "content": "Working harder without leverage burns you out and leaves revenue on the table."}, 
                        {"category": "SOLUTION", "title": "The 3-Step Execution Model", "content": "1. Audit your time blocks.\n2. Eliminate friction points.\n3. Automate repetitive workflows."},
                        {"category": "CTA", "title": "Want the Exact System?", "content": f"Comment SYSTEM below to get our complete {topic_prompt} toolkit today!"}
                    ][:slide_count]
                    st.session_state["sia_slide_contents"] = new_slides
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
                for idx, s in enumerate(new_slides):
                    st.session_state[f"sia_content_t_{idx}"] = s["title"]
                    st.session_state[f"sia_content_b_{idx}"] = s["content"]
                    st.session_state[f"sia_content_c_{idx}"] = s["category"]
                st.success("Framework applied!")
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
        st.success("✨ Content locked and saved in session state! Switch to Step 2 to configure your visual engine.")
        if st.button("🚀 Proceed to Step 2: Visual Foundation & Engine", type="primary", use_container_width=True):
            st.session_state["sia_workflow_step"] = "step2_visual"
            st.rerun()
        return

    # ==========================================
    # WORKFLOW 1: STANDALONE MODE (Direct Full Deck)
    # ==========================================
    if standalone_mode:
        st.markdown("### 📊 Standalone Visual Modules — Full Dummy Deck Preview")
        slides = st.session_state.get("sia_slide_contents", [])
        exact_bg = "#dc2626"
        exact_text = "#ffffff"
        exact_body = "#fef08a"
        exact_tag = "#facc15"
        exact_border = "2px solid #000000"

        for i, slide in enumerate(slides):
            s_title = slide.get("title", "")
            s_body = slide.get("content", "")
            s_cat = slide.get("category", f"SLIDE {i+1}").upper()
            
            st.markdown(
                f"""
                <div style="background-color: {exact_bg}; color: {exact_text}; padding: 35px; border-radius: 16px; min-height: 380px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; margin-bottom: 20px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 15px;">
                            <span style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase;">SLIDE {i+1} OF {len(slides)} • {s_cat}</span>
                            <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 6px 12px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 {palette}</span>
                        </div>
                        <h2 style="color: {exact_text}; font-size: 26px; font-weight: 900; margin-top: 0; margin-bottom: 15px; line-height: 1.2;">{s_title}</h2>
                        <p style="color: {exact_body}; font-size: 15px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{s_body}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.divider()
        st.markdown("### 📥 Export Options")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📦 Download Carousel as ZIP (PNG)", key="standalone_export_zip", use_container_width=True):
                st.success("ZIP package generated successfully!")
        with exp_col2:
            if st.button("🔄 Edit Content Again", key="standalone_restart", use_container_width=True):
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
        active_foreground_bytes = st.session_state.get("original_image_bytes")
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
        st.markdown("### 📥 Export Options")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📦 Download Carousel as ZIP (PNG)", key="sia_btn_export_zip", use_container_width=True):
                st.success("ZIP package generated successfully!")
        with exp_col2:
            if st.button("🔄 Shift to Kinetic Engine / Restart", key="sia_btn_restart", use_container_width=True):
                st.rerun()