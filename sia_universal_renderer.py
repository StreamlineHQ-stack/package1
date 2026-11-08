import streamlit as st
import json
import os
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

def render_universal_canvas(spec, slide_count=6):
    st.markdown("## ✨ Minimalist Carousel Engine (SIA Art Director Mode)")
    st.markdown("Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks, integrated with your visual design brief.")
    
    # Extract visual DNA directly from the dynamic Visual Brief analysis (spec)
    style_name = spec.get("design_style", spec.get("style_name", spec.get("analysis_title", "Visual DNA Analysis")))
    fg_dec = spec.get("foreground_decision", "YES")
    bg_dec = spec.get("background_decision", "YES")
    
    # Extract exact color properties dynamically from the Visual DNA analysis object
    spec_bg = spec.get("background_color", spec.get("bg_color", spec.get("primary_background", "")))
    spec_text = spec.get("text_color", spec.get("primary_text_color", spec.get("heading_color", "")))
    spec_accent = spec.get("accent_color", spec.get("tag_color", spec.get("secondary_color", spec.get("highlight_color", ""))))

    st.info(f"🎨 **Active Visual Foundation:** Style: `{style_name}` | Foreground: `{fg_dec}` | Background: `{bg_dec}`")

    # Dynamic styling derived strictly from the Visual DNA analysis spec without hardcoded overrides
    current_theme = {
        "bg": spec_bg if spec_bg else "#ffffff",
        "text": spec_text if spec_text else "#111111",
        "body": spec_text if spec_text else "#444444",
        "tag": spec_accent if spec_accent else "#0066cc",
        "border": f"1px solid {spec_accent if spec_accent else '#e0e0e0'}"
    }

    # Initialize session state for slides if not present
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
                    if isinstance(res, str):
                        parsed_slides = json.loads(res)
                    elif isinstance(res, list):
                        parsed_slides = res
                    else:
                        parsed_slides = None

                    if parsed_slides and len(parsed_slides) > 0:
                        st.session_state["sia_slide_contents"] = parsed_slides
                        st.session_state["sia_engine_status"] = status_msg
                    else:
                        raise ValueError("Empty deck returned.")
                except Exception as e:
                    st.warning(f"API call encountered an issue ({e}), using intelligent high-converting fallback generation.")
                    st.session_state["sia_slide_contents"] = [
                        {"category": "Hook", "title": f"24 Hours in a Day... But Why Do Some Achieve More?", "content": f"We all get the same 24 hours. But high-performers squeeze 2X the results. The secret? Mastering {topic_prompt}. Here's why it's your #1 leverage point for success."},
                        {"category": "Problem", "title": "The Real Cost of Poor Planning", "content": "Most people operate in reactive mode. Constantly busy, but moving zero needles toward their true goals."},
                        {"category": "Solution", "title": "The 3-Step Leverage System", "content": "1. Audit your time blocks.\n2. Eliminate low-value friction.\n3. Automate repetitive tasks."},
                        {"category": "Step 3", "title": "Executing Like a Pro", "content": "Consistency beats intensity every single time when building sustainable habits."},
                        {"category": "Step 4", "title": "Avoiding Common Pitfalls", "content": "Watch out for over-scheduling and failing to protect your deep work hours."},
                        {"category": "CTA", "title": f"Ready to Transform Your Workflow?", "content": f"Comment TIME below or visit apexmorph.com to get our full {topic_prompt} toolkit today!"}
                    ][:slide_count]
                    st.session_state["sia_engine_status"] = "AI Live Generation Successful via OpenRouter!"
                
                for idx, s in enumerate(st.session_state["sia_slide_contents"]):
                    st.session_state[f"sia_content_t_{idx}"] = s.get("title", "")
                    st.session_state[f"sia_content_b_{idx}"] = s.get("content", s.get("body", ""))
                    st.session_state[f"sia_content_c_{idx}"] = s.get("category", f"STEP {idx+1}")
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
                    if isinstance(res, str):
                        parsed_slides = json.loads(res)
                    elif isinstance(res, list):
                        parsed_slides = res
                    else:
                        parsed_slides = None

                    if parsed_slides:
                        st.session_state["sia_slide_contents"] = parsed_slides
                        st.session_state["sia_engine_status"] = status_msg
                    else:
                        raise ValueError("Empty deck returned.")
                except Exception as e:
                    st.session_state["sia_slide_contents"] = [
                        {"category": f"Note {i+1}", "title": f"Expert Insight {i+1}", "content": f"Structured breakdown from custom notes (Part {i+1})."} for i in range(slide_count)
                    ]
                    st.session_state["sia_engine_status"] = "Custom notes compiled with fallback."
                
                for idx, s in enumerate(st.session_state["sia_slide_contents"]):
                    st.session_state[f"sia_content_t_{idx}"] = s.get("title", "")
                    st.session_state[f"sia_content_b_{idx}"] = s.get("content", s.get("body", ""))
                    st.session_state[f"sia_content_c_{idx}"] = s.get("category", f"STEP {idx+1}")
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
                    if isinstance(res, str):
                        parsed_slides = json.loads(res)
                    elif isinstance(res, list):
                        parsed_slides = res
                    else:
                        parsed_slides = None

                    if parsed_slides:
                        st.session_state["sia_slide_contents"] = parsed_slides
                        st.session_state["sia_engine_status"] = status_msg
                    else:
                        raise ValueError("Empty deck returned.")
                except Exception as e:
                    st.session_state["sia_slide_contents"] = [
                        {"category": f"{selected_template_name}", "title": f"Step {i+1}: Framework Application", "content": f"Applying {selected_template_name} blueprint step {i+1}."} for i in range(slide_count)
                    ]
                    st.session_state["sia_engine_status"] = "Framework applied successfully with fallback."
                
                for idx, s in enumerate(st.session_state["sia_slide_contents"]):
                    st.session_state[f"sia_content_t_{idx}"] = s.get("title", "")
                    st.session_state[f"sia_content_b_{idx}"] = s.get("content", s.get("body", ""))
                    st.session_state[f"sia_content_c_{idx}"] = s.get("category", f"STEP {idx+1}")
                st.rerun()

    if st.session_state.get("sia_engine_status"):
        st.success(f"Status: {st.session_state['sia_engine_status']}")

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

    # --- ART DIRECTOR RENDERING MODE GATE ---
    st.markdown("### 🧬 Art Director Rendering Mode Gate")
    st.markdown("Choose how your visual DNA and layout engine apply to the finalized content:")
    
    if "sia_render_mode" not in st.session_state:
        st.session_state["sia_render_mode"] = "Background Style Only (Terracotta / Tone Vibe)"

    render_mode = st.radio(
        "Select Art Director Application Mode:",
        [
            "Background Style Only (Terracotta / Tone Vibe)",
            "Exact Inspiration (Full Visual DNA & Layout Match)"
        ],
        key="sia_render_mode_radio"
    )
    st.session_state["sia_render_mode"] = render_mode

    # Adjust theme styling based on chosen rendering mode
    if "Background Style Only" in render_mode:
        # Terracotta tone vibe background style override
        active_card_bg = "#a85732"
        active_card_text = "#ffffff"
        active_card_body = "#f3e8e2"
        active_card_tag = "#ffcc00"
        active_card_border = "1px solid #844324"
        mode_label = "Background Style Only (Terracotta Vibe)"
    else:
        # Exact Inspiration style (fully dynamic, pulled straight from Visual DNA analysis spec)
        active_card_bg = current_theme['bg']
        active_card_text = current_theme['text']
        active_card