# sia_studio.py • Style Inspiration & Analysis Studio (SIA) with Style Modules & Cache Purge Switch
import streamlit as st
import base64
from PIL import Image

def render_sia_studio():
    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Configure your content, activate style modes, and render specialized module outputs.")
    
    # --- Downstream Feature Payload Banner ---
    downstream_payload = st.session_state.get("sia_downstream_payload", None)
    if downstream_payload:
        st.success("📦 **Downstream Feature Script Loaded & Ready for Style Analysis!**")
        with st.expander("🔍 View Incoming Feature Script Content"):
            st.write(downstream_payload)
        st.divider()

    # Isolated state variables for SIA
    if "sia_uploaded_files" not in st.session_state:
        st.session_state["sia_uploaded_files"] = None
    if "sia_preview_deck" not in st.session_state:
        st.session_state["sia_preview_deck"] = []
    if "sia_rendered_output" not in st.session_state:
        st.session_state["sia_rendered_output"] = None

    # --- 1. Inspiration Swipe Upload ---
    uploaded_slides = st.file_uploader(
        "Upload Reference Swipe Slides", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        key="sia_file_uploader"
    )
    
    if uploaded_slides:
        st.session_state["sia_uploaded_files"] = uploaded_slides
        st.success(f"Successfully loaded {len(uploaded_slides)} reference slide(s) for style analysis.")

    # --- 2. Deconstruction Report & Content Generation ---
    if uploaded_slides or downstream_payload:
        st.divider()
        st.markdown("## 📊 Deconstruction Intelligence Report & Content Engine")
        
        if downstream_payload:
            content_choice = st.radio(
                "Select Content Source Strategy:",
                [
                    "📦 Keep & Use Passed Down Feature Content",
                    "✨ Generate New Carousel Content inside SIA"
                ],
                key="sia_content_choice_radio"
            )
        else:
            content_choice = "✨ Generate New Carousel Content inside SIA"

        if "Keep & Use Passed Down Feature Content" in content_choice and downstream_payload:
            if isinstance(downstream_payload, list):
                st.session_state["sia_preview_deck"] = downstream_payload
            else:
                st.session_state["sia_preview_deck"] = [
                    {"category": "HOOK", "title": "Tired of aching joints?", "content": "Meet the Ergonomic Garden Kneeler."},
                    {"category": "PROBLEM", "title": "Traditional gardening causes pain.", "content": "Hard earth causes severe strain."},
                    {"category": "SOLUTION", "title": "Protect your knees with EVA padding.", "content": "Thick foam cushions joints."},
                    {"category": "CTA", "title": "Ready to garden in comfort?", "content": "Comment GARDEN today!"}
                ]
        else:
            sub_tab1, sub_tab2 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Notes"])
            with sub_tab1:
                auto_topic = st.text_input("Core Topic / Hook for SIA Deck:", "High-converting digital product strategies", key="sia_auto_topic")
                slide_count = st.slider("Target Slide Count:", 4, 8, 6, key="sia_slide_count")
                if st.button("Generate AI Content Deck", type="primary", key="sia_gen_ai_deck"):
                    st.session_state["sia_preview_deck"] = [
                        {"category": f"SLIDE {i+1}", "title": f"Key Principle #{i+1} for {auto_topic}", "content": f"Actionable implementation step {i+1}."}
                        for i in range(slide_count)
                    ]
                    st.success("🎉 AI Content Deck generated successfully!")

            with sub_tab2:
                custom_notes = st.text_area("Paste Custom Outline Notes:", "Slide 1: Hook\nSlide 2: Value", key="sia_custom_notes")
                if st.button("Load Custom Notes", key="sia_load_notes"):
                    st.session_state["sia_preview_deck"] = [
                        {"category": "CUSTOM SLIDE", "title": "Custom Outline", "content": custom_notes}
                    ]
                    st.success("🎉 Custom notes loaded!")

        # --- White Background Preview Deck ---
        if st.session_state.get("sia_preview_deck"):
            st.divider()
            st.markdown("### 📄 White Background Preview & Edit Deck")
            for idx, slide in enumerate(st.session_state["sia_preview_deck"]):
                with st.expander(f"White Card {idx+1}: [{slide.get('category', 'SLIDE')}] {slide.get('title', '')}"):
                    edited_cat = st.text_input(f"Category {idx+1}", slide.get('category', ''), key=f"sia_cat_{idx}")
                    edited_title = st.text_input(f"Title {idx+1}", slide.get('title', ''), key=f"sia_title_{idx}")
                    edited_content = st.text_area(f"Content {idx+1}", slide.get('content', ''), key=f"sia_cont_{idx}")
                    st.session_state["sia_preview_deck"][idx] = {"category": edited_cat, "title": edited_title, "content": edited_content}

        st.markdown("---")
        if st.button("🎭 Call Art Director & Activate Style Engine", type="primary", use_container_width=True, key="sia_call_art_director"):
            st.session_state["sia_art_director_active"] = True
            st.rerun()

    # --- 3. Sidebar Style Engine Controls & Mode Switching with Cache Purge ---
    if st.session_state.get("sia_art_director_active", False):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Enhanced Background & Visual Style Engine")
            
            previous_mode = st.session_state.get("sia_current_active_mode", None)
            
            sia_mode = st.radio(
                "Select SIA Style Mode:",
                [
                    "☕ Terracotta Background & White Font",
                    "⚡ Smart AI Contextual Match",
                    "🎯 Exact Inspiration Match (Objects & Layout)",
                    "🏛️ Unified Editorial Motif",
                    "📂 Custom User Images"
                ],
                key="sia_sidebar_mode_radio"
            )
            
            # --- STRICT CACHE PURGE ON MODE SWITCH ---
            if previous_mode != sia_mode:
                st.session_state["sia_rendered_output"] = None
                st.session_state["sia_current_active_mode"] = sia_mode
                st.success(f"🧹 Workspace flushed! Switched mode to: {sia_mode}. Previous cache purged to prevent contamination.")
            
            if st.button("🔄 Refresh Workspace & Purge Cache", type="secondary", use_container_width=True):
                st.session_state["sia_rendered_output"] = None
                st.success("⚡ Workspace refreshed and cache completely wiped.")
                st.rerun()

        st.divider()
        st.markdown("### 🚀 Module Execution & Deck Generation")
        st.markdown(f"**Active Render Module:** `{sia_mode}`")
        
        if st.button(f"✨ Generate Deck via [{sia_mode}]", type="primary", use_container_width=True, key="sia_generate_module_deck"):
            deck = st.session_state.get("sia_preview_deck", [])
            
            # --- MODULE 1: Terracotta Background & White Font ---
            if "Terracotta Background & White Font" in sia_mode:
                rendered_slides = []
                for idx, s in enumerate(deck):
                    rendered_slides.append({
                        "card_num": idx + 1,
                        "style": "Terracotta Editorial (#a85732)",
                        "bg_color": "#a85732",
                        "font_color": "#FFFFFF",
                        "typography": "Clean Serif High-Contrast",
                        "spacing": "Generous Negative Space",
                        "category": s.get("category"),
                        "title": s.get("title"),
                        "content": s.get("content"),
                        "imagery": "Solid Terracotta Editorial Backdrop"
                    })
                st.session_state["sia_rendered_output"] = rendered_slides
                st.success("☕ [Module 1 Rendered]: Terracotta Background & White Font applied successfully!")

            # --- MODULE 2: Smart AI Contextual Match ---
            elif "Smart AI Contextual Match" in sia_mode:
                context_keywords = {
                    "focus": "🎯 Bulls-eye Precision Target Graphic",
                    "long way": "🌉 Winding Bridge & Horizon Road",
                    "growth": "📈 Upward Escalation Vector",
                    "joint": "🛡️ Ergonomic Shield & Protection Icon",
                    "goal": "🏁 Finish Line Banner & Milestone Marker"
                }
                
                rendered_slides = []
                for idx, s in enumerate(deck):
                    text_blob = (s.get("title", "") + " " + s.get("content", "")).lower()
                    matched_img = "🖼️ Clean Minimalist Abstract Gradient Backdrop"
                    for kw, img_desc in context_keywords.items():
                        if kw in text_blob:
                            matched_img = img_desc
                            break
                    
                    rendered_slides.append({
                        "card_num": idx + 1,
                        "style": "Smart AI Contextual Match",
                        "category": s.get("category"),
                        "title": s.get("title"),
                        "content": s.get("content"),
                        "imagery": matched_img
                    })
                st.session_state["sia_rendered_output"] = rendered_slides
                st.success("⚡ [Module 2 Rendered]: Smart AI Contextual Match applied unique context imagery per slide!")

        # --- Render Output Display ---
        if st.session_state.get("sia_rendered_output"):
            st.divider()
            st.markdown("### 👁️ Rendered Module Output Preview")
            for slide in st.session_state["sia_rendered_output"]:
                with st.container():
                    st.info(f"**Slide {slide['card_num']} [{slide['category']}]** — *Style: {slide.get('style')}*\n\n"
                            f"🎨 **Visual Asset / Imagery:** {slide.get('imagery')}\n\n"
                            f"📌 **Title:** {slide['title']}\n\n"
                            f"📝 **Content:** {slide['content']}")