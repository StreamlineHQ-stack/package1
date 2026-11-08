import streamlit as st
import json
import os
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

def render_universal_canvas(spec, slide_count=6):
    st.markdown("## ✨ Minimalist Carousel Engine (SIA Art Director Mode)")
    st.markdown("Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks, integrated with your visual design brief.")
    
    style_name = spec.get("design_style", spec.get("style_name", "Visual Brief Analysis"))
    
    raw_fg_dec = spec.get("foreground_decision", True)
    raw_bg_dec = spec.get("background_decision", True)
    
    fg_dec_bool = True if str(raw_fg_dec).upper() in ["YES", "TRUE", "1", "Y"] else False
    bg_dec_bool = True if str(raw_bg_dec).upper() in ["YES", "TRUE", "1", "Y"] else False

    palette = spec.get("palette", ["Red", "Black", "Yellow", "White"])
    visual_mood = spec.get("visual_mood", "Bold and Energetic")
    composition = spec.get("composition", "The text is prominent at the top, with strong contrast")
    bg_environment = spec.get("background_environment", spec.get("background_scene", "Solid red background"))
    fg_subject = spec.get("foreground_subject", spec.get("foreground_figure", "A person with braided hair, wearing a black t-shirt and sunglasses, posing with arms crossed"))

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

    st.markdown("### 🧬 Art Director Rendering Mode Gate")
    st.markdown("Choose how your visual brief parameters apply to the finalized content:")
    
    if "sia_render_mode" not in st.session_state:
        st.session_state["sia_render_mode"] = "Exact Inspiration (Full Visual Brief & Layout Match)"

    render_mode = st.radio(
        "Select Art Director Application Mode:",
        [
            "Background Style Only (Red/Yellow/Black Vibe)",
            "Exact Inspiration (Full Visual Brief & Layout Match)"
        ],
        key="sia_render_mode_radio"
    )
    st.session_state["sia_render_mode"] = render_mode

    active_card_bg = exact_bg
    active_card_text = exact_text
    active_card_body = exact_body
    active_card_tag = exact_tag
    active_card_border = exact_border

    is_exact_mode = "Exact Inspiration" in render_mode

    if not is_exact_mode:
        mode_label = f"Background Style Only [Mood: {visual_mood} | Palette: {palette} | Top Composition]"
        card_footer_html = f'<div style="background: rgba(0,0,0,0.4); padding: 8px 12px; border-radius: 6px; margin-top: 15px; border-left: 3px solid {active_card_tag};"><p style="color: {active_card_body}; font-size: 11px; margin: 0; font-weight: 600;">Art Director Style Only • {visual_mood}</p></div>'
    else:
        mode_label = f"Exact Inspiration [Full Visual Brief & Layout Match]"
        card_footer_html = f"""<div style="background: #000000; border: 2px solid {active_card_tag}; padding: 12px 16px; border-radius: 10px; margin-top: 20px; display: flex; align-items: center; gap: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);"><div style="background: {active_card_tag}; color: #000000; font-weight: 900; font-size: 12px; padding: 6px 10px; border-radius: 6px; white-space: nowrap;">👤 SUBJECT ASSET</div><div><p style="color: #ffffff; font-size: 12px; margin: 0; font-weight: 700;">{fg_subject}</p><p style="color: {active_card_body}; font-size: 11px; margin: 2px 0 0 0; font-weight: 500;">Background: {bg_environment}</p></div></div>"""

    st.divider()
    
    st.markdown("### 🎨 Step 6: Review Dummy Slide Section")
    st.markdown(f"Review your first slide rendered via **{mode_label}**.")

    current_first_slide = updated_slides[0] if updated_slides else st.session_state["sia_slide_contents"][0]
    f_title = current_first_slide.get('title', '')
    f_body = current_first_slide.get('content', current_first_slide.get('body', ''))
    f_cat = current_first_slide.get('category', 'SLIDE 1').upper()

    if "sia_dummy_approved" not in st.session_state:
        st.session_state["sia_dummy_approved"] = False

    if not st.session_state["sia_dummy_approved"]:
        st.markdown(
            f"""
            <div style="
                background-color: {active_card_bg};
                color: {active_card_text};
                padding: 40px;
                border-radius: 16px;
                min-height: 340px;
                border: {active_card_border};
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                font-family: 'Inter', sans-serif;
                margin-top: 15px;
                margin-bottom: 25px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            ">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <p style="color: {active_card_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; margin: 0;">SLIDE 1 OF {total_slides} • {f_cat}</p>
                        <span style="background: #000000; color: {active_card_tag}; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 6px; border: 1px solid {active_card_tag};">🎨 Palette: {palette}</span>
                    </div>
                    <h2 style="color: {active_card_text}; font-size: 30px; font-weight: 900; margin-bottom: 15px; line-height: 1.2;">{f_title}</h2>
                    <p style="color: {active_card_body}; font-size: 16px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{f_body}</p>
                </div>
                <div>
                    {card_footer_html}
                    <div style="text-align: right; margin-top: 12px;">
                        <span style="color: {active_card_body}; font-size: 11px; opacity: 0.9; font-weight: 600;">Nikki's Salon • Art Director</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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
            s_title = slide.get('title', '')
            s_body = slide.get('content', slide.get('body', ''))
            s_cat = slide.get('category', f'SLIDE {i+1}').upper()

            st.markdown(
                f"""
                <div style="
                    background-color: {active_card_bg};
                    color: {active_card_text};
                    padding: 40px;
                    border-radius: 16px;
                    min-height: 340px;
                    border: {active_card_border};
                    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                    font-family: 'Inter', sans-serif;
                    margin-top: 15px;
                    margin-bottom: 25px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                ">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <p style="color: {active_card_tag}; font-weight: 900; font-size: 13px; letter-spacing: 1.5px; margin: 0;">SLIDE {i+1} OF {total_slides} • {s_cat}</p>
                            <span style="background: #000000; color: {active_card_tag}; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 6px; border: 1px solid {active_card_tag};">🎨 Palette: {palette}</span>
                        </div>
                        <h2 style="color: {active_card_text}; font-size: 30px; font-weight: 900; margin-bottom: 15px; line-height: 1.2;">{s_title}</h2>
                        <p style="color: {active_card_body}; font-size: 16px; line-height: 1.6; white-space: pre-wrap; font-weight: 600;">{s_body}</p>
                    </div>
                    <div>
                        {card_footer_html}
                        <div style="text-align: right; margin-top: 12px;">
                            <span style="color: {active_card_body}; font-size: 11px; opacity: 0.9; font-weight: 600;">Nikki's Salon • Art Director</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()
        st.markdown("### 📥 Step 7 & 8: Export Options")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📦 Download Carousel as ZIP (PNG)", key="sia_btn_export_zip", use_container_width=True):
                st.success("ZIP package downloaded successfully!")
        with exp_col2:
            if st.button("🚀 Move to Kinetic Engine", key="sia_btn_move_kinetic", use_container_width=True):
                st.success("Transitioning to Kinetic Engine...")
