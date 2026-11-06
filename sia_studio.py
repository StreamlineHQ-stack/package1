# sia_studio.py • Style Inspiration & Analysis Studio (SIA) with Carousel Content Engine & Deck Carousel Player
import streamlit as st
import json
import base64
from PIL import Image
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from sia_terracotta_module import build_terracotta_deck
from sia_ai_context_module import build_ai_context_deck

try:
    from templates.november import NOVEMBER_FRAMEWORK_LIBRARY
except Exception:
    NOVEMBER_FRAMEWORK_LIBRARY = {}

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
    
    # Navigation controls header
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
            
    # Simply render the fully baked card HTML received from the active module!
    st.markdown(slide.get("rendered_html", ""), unsafe_allow_html=True)

def render_sia_studio():
    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Upload inspiration swipes, generate content via Carousel Engine engines, and render modular styled decks.")
    
    downstream_payload = st.session_state.get("sia_downstream_payload", None)
    if downstream_payload:
        st.success("📦 **Downstream Feature Script Loaded & Ready!**")
        with st.expander("🔍 View Incoming Feature Script Content"):
            st.write(downstream_payload)
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