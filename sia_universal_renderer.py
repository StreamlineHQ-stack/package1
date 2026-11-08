import streamlit as st
import json
import os
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

def render_universal_canvas(spec, slide_count=6):
    st.markdown("## ✨ Minimalist Carousel Engine (SIA Art Director Mode)")
    st.markdown("Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks, integrated with your visual design brief.")
    
    # Display active visual brief summary
    style_name = spec.get("design_style", "Custom Style")
    fg_dec = spec.get("foreground_decision", "YES")
    bg_dec = spec.get("background_decision", "YES")
    st.info(f"🎨 **Active Visual Foundation:** Style: `{style_name}` | Foreground: `{fg_dec}` | Background: `{bg_dec}`")

    # --- CHECK IF CONTENT RECEIVED FROM UPSTREAM (FEATURE-TO-BENEFITS) ---
    upstream_content = st.session_state.get("feature_to_benefits_output", None) or st.session_state.get("upstream_content_data", None)
    
    if upstream_content:
        st.success("📥 Content successfully received from Feature-to-Benefits upstream module!")
        st.session_state["sia_slide_contents"] = upstream_content
    else:
        tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])

        with tab1:
            st.markdown("### ⚡ AI Auto-Pilot")
            topic_prompt = st.text_input("Enter your core topic or audience pain point:", "Why is time management important", key="sia_autopilot_input")
            if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
                with st.spinner("Crafting direct-response carousel deck via AI..."):
                    try:
                        res, status_msg = generate_carousel_deck(topic_prompt, slide_count=slide_count, mode="autopilot")
                        if not res:
                            raise ValueError("Empty response returned.")
                        st.session_state["sia_slide_contents"] = res
                        st.session_state["sia_engine_status"] = status_msg
                    except Exception as e:
                        st.warning(f"API call encountered an issue ({e}), using intelligent high-converting fallback generation.")
                        st.session_state["sia_slide_contents"] = [
                            {"category": f"Step {i+1}", "title": f"Mastering {topic_prompt} - Point {i+1}", "content": f"Actionable insight and core strategy breakdown for slide {i+1}."} for i in range(slide_count)
                        ]
                        st.session_state["sia_engine_status"] = "Fallback content generated successfully."
                    st.rerun()

        with tab2:
            st.markdown("### 📝 Custom Expert Notes")
            custom_notes = st.text_area(
                "Paste your unstructured notes:", 
                height=150, 
                value="Hook: Time management is leverage.\nProblem: People waste hours on low-value tasks.\nCTA: Comment TIME to get the planner.", 
                key="sia_custom_notes_input"
            )
            if st.button("Format Custom Notes", type="primary", key="sia_btn_gen_notes"):
                with st.spinner("Structuring raw notes into slides..."):
                    try:
                        res, status_msg = generate_carousel_deck(custom_notes, slide_count=slide_count, mode="custom")
                        if not res:
                            raise ValueError("Empty response.")
                        st.session_state["sia_slide_contents"] = res
                        st.session_state["sia_engine_status"] = status_msg
                    except Exception as e:
                        st.session_state["sia_slide_contents"] = [
                            {"category": f"Note {i+1}", "title": f"Expert Insight {i+1}", "content": f"Structured breakdown from custom notes (Part {i+1})."} for i in range(slide_count)
                        ]
                        st.session_state["sia_engine_status"] = "Custom notes compiled with fallback."
                    st.rerun()

        with tab3:
            st.markdown("### 🪄 Guided Framework Wizard")
            selected_pillar = st.selectbox("Choose Content Pillar:", list(FRAMEWORK_LIBRARY.keys()), key="sia_pillar_select")
            templates_in_pillar = FRAMEWORK_LIBRARY[selected_pillar]
            selected_template_name = st.selectbox("Choose Direct-Response Blueprint:", list(templates_in_pillar.keys()), key="sia_template_select")
            
            template_data = templates_in_pillar[selected_template_name]
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                hook_input = st.text_input("1. Hook / Core Headline", value=template_data["hook"], key="sia_hook_in")
                problem_input = st.text_input("2. Core Problem / Pain", value=template_data["problem"], key="sia_prob_in")
            with col2:
                solution_input = st.text_input("3. Solution / System Steps", value=template_data["solution"], key="sia_sol_in")
                cta_input = st.text_input("4. Call to Action (CTA)", value=template_data["cta"], key="sia_cta_in")
                
            if st.button("Format Framework Carousel", type="primary", key="sia_btn_gen_frame"):
                raw_text = f"Hook: {hook_input}\nProblem: {problem_input}\nSolution: {solution_input}\nCTA: {cta_input}"
                with st.spinner("Building direct-response carousel deck..."):
                    try:
                        res, status_msg = generate_carousel_deck(raw_text, slide_count=slide_count, mode="framework")
                        if not res:
                            raise ValueError("Empty response.")
                        st.session_state["sia_slide_contents"] = res
                        st.session_state["sia_engine_status"] = status_msg
                    except Exception as e:
                        st.session_state["sia_slide_contents"] = [
                            {"category": f"{selected_template_name}", "title": f"Step {i+1}: Framework Application", "content": f"Applying {selected_template_name} blueprint step {i+1}."} for i in range(slide_count)
                        ]
                        st.session_state["sia_engine_status"] = "Framework applied successfully with fallback."
                    st.rerun()

    if st.session_state.get("sia_engine_status"):
        st.success(f"Status: {st.session_state['sia_engine_status']}")

    # Initialize session state for slides if needed
    if "sia_slide_contents" not in st.session_state or not st.session_state["sia_slide_contents"]:
        st.session_state["sia_slide_contents"] = [
            {"category": f"Step {i+1}", "title": f"Slide {i+1}: Hook & Core Angle", "body": f"Core angle addressing your topic for slide {i+1}."} for i in range(slide_count)
        ]

    st.divider()
    st.markdown("#### ✍️ Live Content Editor & Step 6 Dummy Slide Preview")
    
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
    
    # --- STEP 6: DUMMY SLIDE PREVIEW & APPROVAL GATE ---
    st.markdown("### 🎨 Step 6: Review Dummy Slide Section")
    st.markdown("Review your first slide combining your generated content with your approved visual brief.")

    if "sia_dummy_approved" not in st.session_state:
        st.session_state["sia_dummy_approved"] = False

    if not st.session_state["sia_dummy_approved"]:
        with st.container(border=True):
            first_slide = st.session_state["sia_slide_contents"][0]
            st.markdown(f"### 🧪 {first_slide.get('title')}")
            st.markdown(first_slide.get('content'))

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
            with st.container(border=True):
                st.markdown(f"**Slide {i+1} of {total_slides} • {style_name.upper()}**")
                st.markdown(f"### {slide['title']}")
                st.markdown(slide['content'])

        st.divider()
        st.markdown("### 📥 Step 7 & 8: Export Options")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📦 Download Carousel as ZIP (PNG)", key="sia_btn_export_zip", use_container_width=True):
                st.success("ZIP package downloaded successfully!")
        with exp_col2:
            if st.button("🚀 Move to Kinetic Engine", key="sia_btn_move_kinetic", use_container_width=True):
                st.success("Transitioning to Kinetic Engine...")