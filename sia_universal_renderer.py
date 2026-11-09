import streamlit as st
import json
import os
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

def render_universal_canvas(spec, slide_count=4):
    st.markdown("## ✨ Content Engine (SIA Art Director Mode)")
    st.markdown("Generate high-converting carousels via asset-preserving routing and direct-response blueprints.")
    
    palette = spec.get("palette", ["Red", "Black", "Yellow", "White"])
    visual_mood = spec.get("visual_mood", "Bold and Energetic")
    fg_subject = spec.get("foreground_subject", spec.get("foreground_figure", "Person with braided hair, wearing a black t-shirt."))
    
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

    st.info(f"🎨 **Active Visual Brief:** Mood: `{visual_mood}` | Palette: `{palette}`")
    
    exact_bg = "#dc2626"
    exact_text = "#ffffff"
    exact_body = "#fef08a"
    exact_tag = "#facc15"
    exact_border = "2px solid #000000"
    
    if "sia_slide_contents" not in st.session_state or not st.session_state["sia_slide_contents"]:
        st.session_state["sia_slide_contents"] = [
            {"category": f"STEP {i+1}", "title": f"Slide {i+1}: Hook & Core Angle", "content": f"Core angle addressing your topic for slide {i+1}."} for i in range(slide_count)
        ]
    
    tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
    
    with tab1:
        st.markdown("### ⚡ AI Auto-Pilot")
        topic_prompt = st.text_input("Enter your core topic or audience pain point:", value="Why time management matters", key="sia_autopilot_input")
        if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
            with st.spinner("Crafting direct-response carousel deck..."):
                new_slides = [
                    {"category": "HOOK", "title": f"Why {topic_prompt} Is Costing You Clients", "content": f"Most creators struggle with {topic_prompt} because they lack a systematic framework."}, 
                    {"category": "PROBLEM", "title": "The Hidden Cost of Inefficiency", "content": "Working harder without leverage burns you out and leaves revenue on the table."}, 
                    {"category": "SOLUTION", "title": "The 3-Step Execution Model", "content": "1. Audit your time blocks.\n2. Eliminate friction points.\n3. Automate repetitive workflows."},
                    {"category": "CTA", "title": "Want the Exact System?", "content": f"Comment SYSTEM below to get our complete {topic_prompt} toolkit today!"}
                ][:slide_count]
                st.session_state["sia_slide_contents"] = new_slides
                # Clear widget state keys so Streamlit updates fields on rerun
                for idx, s in enumerate(new_slides):
                    st.session_state[f"sia_content_t_{idx}"] = s["title"]
                    st.session_state[f"sia_content_b_{idx}"] = s["content"]
                    st.session_state[f"sia_content_c_{idx}"] = s["category"]
                st.success("Auto-pilot generated successfully!")
                st.rerun()
    
    with tab2:
        st.markdown("### 📝 Custom Expert Notes")
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
        st.markdown("### 🪄 Guided Framework Wizard")
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
    st.markdown("### 🧬 Art Director Rendering Mode Gate")
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
    st.markdown("### 🎨 Step 6: Review Dummy Slide Section")
    
    current_first_slide = updated_slides[0] if updated_slides else st.session_state["sia_slide_contents"][0]
    f_title = current_first_slide.get("title", "")
    f_body = current_first_slide.get("content", "")
    f_cat = current_first_slide.get("category", "SLIDE 1").upper()
    
    if "sia_dummy_approved" not in st.session_state:
        st.session_state["sia_dummy_approved"] = False
    
    if not st.session_state["sia_dummy_approved"]:
        st.markdown(
            f"""
            <div style="background-color: {exact_bg}; color: {exact_text}; padding: 40px; border-radius: 16px; min-height: 420px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 20px;">
                        <span style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase;">SLIDE 1 OF {total_slides} • {f_cat}</span>
                        <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 6px 12px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 {palette}</span>
                    </div>
                    <h2 style="color: {exact_text}; font-size: 30px; font-weight: 900; margin-top: 0; margin-bottom: 20px; line-height: 1.2;">{f_title}</h2>
                    <p style="color: {exact_body}; font-size: 16px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{f_body}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if active_foreground_bytes is not None:
            st.markdown("### 🖼️ Compositor Asset Injection:")
            st.image(active_foreground_bytes, caption=f"Routed Asset (Mode: {render_mode[:6]})", width=300)
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("✅ YES — Like it! Compile full deck", key="sia_btn_approve_dummy", use_container_width=True):
                st.session_state["sia_dummy_approved"] = True
                st.success("Dummy slide approved!")
                st.rerun()
        with col_d2:
            if st.button("❌ NO — Reset", key="sia_btn_reject_dummy", use_container_width=True):
                st.session_state["sia_dummy_approved"] = False
                st.rerun()
    else:
        st.success("✨ Full carousel deck compiled successfully!")
        st.divider()
        st.markdown("### 📊 Final Rendered Carousel Deck")
        for i, slide in enumerate(st.session_state["sia_slide_contents"]):
            s_title = slide.get("title", "")
            s_body = slide.get("content", "")
            s_cat = slide.get("category", f"SLIDE {i+1}").upper()
            st.markdown(
                f"""
                <div style="background-color: {exact_bg}; color: {exact_text}; padding: 40px; border-radius: 16px; min-height: 420px; border: {exact_border}; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: 'Inter', sans-serif; margin-top: 15px; margin-bottom: 25px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 20px;">
                            <span style="color: {exact_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase;">SLIDE {i+1} OF {total_slides} • {s_cat}</span>
                            <span style="background: #000000; color: {exact_tag}; font-weight: 800; font-size: 11px; padding: 6px 12px; border-radius: 6px; border: 1px solid {exact_tag};">🎨 {palette}</span>
                        </div>
                        <h2 style="color: {exact_text}; font-size: 30px; font-weight: 900; margin-top: 0; margin-bottom: 20px; line-height: 1.2;">{s_title}</h2>
                        <p style="color: {exact_body}; font-size: 16px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{s_body}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if active_foreground_bytes is not None:
                st.image(active_foreground_bytes, width=300)
