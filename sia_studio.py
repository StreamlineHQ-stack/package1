# sia_studio.py • Orchestrator Router for SIA Studio
import streamlit as st
import base64
from PIL import Image
from sia_terracotta_module import build_terracotta_deck
from sia_ai_context_module import build_ai_context_deck

def render_visual_preview(styled_deck):
    if not styled_deck:
        return
    st.divider()
    st.markdown("### 👁️ Rendered Module Visual Deck Preview")
    
    for slide in styled_deck:
        card_html = f"""
        <div style="background-color: {slide['bg_color']}; color: {slide['font_color']}; padding: 35px; border-radius: 14px; margin-bottom: 24px; box-shadow: 0 6px 16px rgba(0,0,0,0.18); font-family: Arial, sans-serif;">
            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; margin-bottom: 8px;">
                Slide {slide['card_num']} • {slide['category']} • [{slide['style']}]
            </div>
            <div style="font-size: 13px; font-weight: bold; opacity: 0.95; margin-bottom: 14px; background: {slide['accent_bg']}; padding: 6px 12px; border-radius: 6px; display: inline-block;">
                {slide['imagery']}
            </div>
            <div style="font-size: 24px; font-weight: bold; margin-bottom: 14px; line-height: 1.3;">
                {slide['title']}
            </div>
            <div style="font-size: 15px; opacity: 0.95; line-height: 1.5;">
                {slide['content']}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

def render_sia_studio():
    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Modular style orchestrator with isolated rendering pipelines.")
    
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
        st.success(f"Successfully loaded {len(uploaded_slides)} reference slide(s).")

    if uploaded_slides or downstream_payload:
        st.divider()
        st.markdown("## 📊 Deconstruction Report & Content Engine")
        
        if downstream_payload:
            content_choice = st.radio("Select Content Source:", ["📦 Keep Passed Down Feature Content", "✨ Generate New Carousel Content inside SIA"], key="sia_content_choice_radio")
        else:
            content_choice = "✨ Generate New Carousel Content inside SIA"

        if "Keep Passed Down Feature Content" in content_choice and downstream_payload:
            st.session_state["sia_preview_deck"] = downstream_payload if isinstance(downstream_payload, list) else [
                {"category": "HOOK", "title": "Tired of aching joints?", "content": "Meet the Ergonomic Garden Kneeler."},
                {"category": "PROBLEM", "title": "Traditional gardening causes pain.", "content": "Hard earth causes severe strain."},
                {"category": "SOLUTION", "title": "Protect your knees with EVA padding.", "content": "Thick foam cushions joints."},
                {"category": "CTA", "title": "Ready to garden in comfort?", "content": "Comment GARDEN today!"}
            ]
        else:
            sub_tab1, sub_tab2 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Notes"])
            with sub_tab1:
                auto_topic = st.text_input("Core Topic / Hook:", "High-converting digital product strategies", key="sia_auto_topic")
                slide_count = st.slider("Target Slide Count:", 4, 8, 6, key="sia_slide_count")
                if st.button("Generate AI Content Deck", type="primary", key="sia_gen_ai_deck"):
                    st.session_state["sia_preview_deck"] = [{"category": f"SLIDE {i+1}", "title": f"Key Principle #{i+1} for {auto_topic}", "content": f"Actionable step {i+1}."} for i in range(slide_count)]
                    st.success("🎉 AI Content Deck generated!")
            with sub_tab2:
                custom_notes = st.text_area("Custom Outline Notes:", "Slide 1: Hook\nSlide 2: Value", key="sia_custom_notes")
                if st.button("Load Custom Notes", key="sia_load_notes"):
                    st.session_state["sia_preview_deck"] = [{"category": "CUSTOM", "title": "Custom Outline", "content": custom_notes}]
                    st.success("🎉 Custom notes loaded!")

        if st.session_state.get("sia_preview_deck"):
            st.divider()
            st.markdown("### 📄 White Background Preview & Edit Deck")
            for idx, slide in enumerate(st.session_state["sia_preview_deck"]):
                with st.expander(f"White Card {idx+1}: [{slide.get('category', 'SLIDE')}] {slide.get('title', '')}"):
                    c = st.text_input(f"Cat {idx}", slide.get('category', ''), key=f"s_cat_{idx}")
                    t = st.text_input(f"Title {idx}", slide.get('title', ''), key=f"s_tit_{idx}")
                    cnt = st.text_area(f"Content {idx}", slide.get('content', ''), key=f"s_cnt_{idx}")
                    st.session_state["sia_preview_deck"][idx] = {"category": c, "title": t, "content": cnt}

        st.markdown("---")
        if st.button("🎭 Call Art Director & Activate Style Engine", type="primary", use_container_width=True, key="sia_call_art_director"):
            st.session_state["sia_art_director_active"] = True
            st.rerun()

    if st.session_state.get("sia_art_director_active", False):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Enhanced Visual Style Engine")
            
            prev_mode = st.session_state.get("sia_current_active_mode", None)
            sia_mode = st.radio("Select SIA Style Mode:", [
                "☕ Terracotta Background & White Font",
                "⚡ Smart AI Contextual Match",
                "🎯 Exact Inspiration Match",
                "🏛️ Unified Editorial Motif",
                "📂 Custom User Images"
            ], key="sia_sidebar_mode_radio")
            
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
        
        if st.button(f"✨ Generate Deck via [{sia_mode}]", type="primary", use_container_width=True, key="sia_generate_module_deck"):
            deck = st.session_state.get("sia_preview_deck", [])
            
            if "Terracotta Background & White Font" in sia_mode:
                st.session_state["sia_rendered_output"] = build_terracotta_deck(deck)
                st.success("☕ [Module 1 Rendered]: Terracotta cards built successfully!")
            elif "Smart AI Contextual Match" in sia_mode:
                st.session_state["sia_rendered_output"] = build_ai_context_deck(deck)
                st.success("⚡ [Module 2 Rendered]: AI Contextual cards built successfully!")
            else:
                st.info(f"🛠️ [{sia_mode}] module pipeline under construction. Next in queue!")

        render_visual_preview(st.session_state.get("sia_rendered_output"))