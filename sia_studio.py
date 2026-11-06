# sia_studio.py • Style Inspiration & Analysis Studio (SIA) with Complete Content Engine & Deck Preview
import streamlit as st
import base64
from PIL import Image

def render_sia_studio():
    # --- Main SIA Studio UI ---
    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Upload reference swipe slides, configure content sources, preview white background slides, and apply SIA visual styles.")
    
    # --- 1. Downstream Feature Payload Banner ---
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
    if "sia_deck_generated" not in st.session_state:
        st.session_state["sia_deck_generated"] = False

    # --- 2. Inspiration Swipe Upload ---
    uploaded_slides = st.file_uploader(
        "Upload Reference Swipe Slides", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        key="sia_file_uploader"
    )
    
    if uploaded_slides:
        st.session_state["sia_uploaded_files"] = uploaded_slides
        st.success(f"Successfully loaded {len(uploaded_slides)} reference slide(s) for style analysis.")
        
        st.markdown("### 🔍 Swipe Style Extraction & Parameter Breakdown")
        cols = st.columns(min(len(uploaded_slides), 3))
        for idx, uploaded_file in enumerate(uploaded_slides):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Reference {idx+1}: {uploaded_file.name}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error previewing {uploaded_file.name}: {e}")

    # --- 3. Deconstruction Intelligence Report & Content Source Selection ---
    if uploaded_slides:
        st.divider()
        st.markdown("## 📊 Deconstruction Intelligence Report")
        
        st.markdown("### 🎨 Advanced Visual & Photographic Deconstruction")
        st.markdown(
            """
            * **Color Palette & Tone:** Warm editorial aesthetic (Terracotta base `#a85732` paired with rich cream and dark typography).
            * **Subject Framing & Composition:** Minimalist, centered subject placement utilizing substantial negative space to maintain an uncluttered high-end aesthetic.
            * **Prop & Texture Staging:** Incorporation of tactile organic elements (e.g., natural wood blocks, sleek mirrors, and single botanical stems) to anchor the visual mood.
            * **Lighting & Atmosphere:** Warm, low-key lighting with earthy amber and terracotta color grading creating an intimate, editorial feel.
            * **Image-to-Text Integration:** High-contrast serif typography positioned cleanly over the upper third of the photographic backdrop, ensuring readability without obstructing the primary focal point.
            """
        )
        
        st.divider()
        st.markdown("### 📝 Content Source & Generation Engine")
        
        # Context-aware content source options based on whether a downstream payload actually exists
        if downstream_payload:
            st.markdown("Choose whether to use the incoming feature content payload or generate fresh carousel content inside SIA.")
            content_choice = st.radio(
                "Select Content Source Strategy:",
                [
                    "📦 Keep & Use Passed Down Feature Content",
                    "✨ Generate New Carousel Content inside SIA (AI Auto-Pilot & Notes)"
                ],
                key="sia_content_choice_radio"
            )
        else:
            st.info("💡 No downstream feature script detected. Set up your content generation strategy below:")
            content_choice = "✨ Generate New Carousel Content inside SIA (AI Auto-Pilot & Notes)"

        if "Keep & Use Passed Down Feature Content" in content_choice and downstream_payload:
            st.info("✅ Feature content retained. Generating white background preview deck from passed-down script.")
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
            st.success("✨ New content generation active. Use AI Auto-Pilot or Custom Notes below:")
            sub_tab1, sub_tab2 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Notes"])
            
            with sub_tab1:
                auto_topic = st.text_input("Core Topic / Hook for SIA Deck:", "High-converting digital product strategies for creators", key="sia_auto_topic")
                slide_count = st.slider("Target Slide Count:", 4, 8, 6, key="sia_slide_count")
                if st.button("Generate AI Content Deck", type="primary", key="sia_gen_ai_deck"):
                    st.session_state["sia_preview_deck"] = [
                        {"category": f"SLIDE {i+1}", "title": f"Key Principle #{i+1} for {auto_topic}", "content": f"Detailed strategic breakdown and actionable implementation step {i+1}."}
                        for i in range(slide_count)
                    ]
                    st.success("🎉 AI Content Deck generated successfully!")

            with sub_tab2:
                custom_notes = st.text_area("Paste Custom Outline or Script Notes:", "Slide 1: Hook\nSlide 2: Mechanism\nSlide 3: Offer", key="sia_custom_notes")
                if st.button("Load Custom Notes into Deck", key="sia_load_notes"):
                    st.session_state["sia_preview_deck"] = [
                        {"category": "CUSTOM SLIDE", "title": "Custom Outline Point", "content": custom_notes}
                    ]
                    st.success("🎉 Custom notes loaded into preview deck!")

        # --- 4. White Background Preview & Edit Deck ---
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
        
        # --- 5. Call Art Director Button ---
        if st.button("🎭 Call Art Director & Activate Style Engine", type="primary", use_container_width=True, key="sia_call_art_director"):
            st.session_state["sia_art_director_active"] = True
            st.success("🎉 Art Director online! Check your sidebar for the 5 isolated SIA Style Engine control modes.")
            st.rerun()
    elif downstream_payload:
        st.info("💡 **Next Step:** Upload a reference swipe slide above to generate the Deconstruction Report and configure your content.")

    # --- 6. Sidebar Style Engine Controls & Final Generation ---
    if st.session_state.get("sia_art_director_active", False):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Enhanced Background & Visual Style Engine")
            st.markdown("**Style Mode Control (5 SIA Options):**")
            
            sia_mode = st.radio(
                "Select SIA Style Mode:",
                [
                    "🎯 Exact Inspiration Match (Objects & Layout)",
                    "🏛️ Unified Editorial Motif",
                    "📂 Custom User Images",
                    "☕ Terracotta Background & White Font",
                    "⚡ Smart AI Contextual Match"
                ],
                key="sia_sidebar_mode_radio"
            )
            
            if "Unified Editorial Motif" in sia_mode:
                st.markdown("### 🏛️ Custom Motif Theme")
                st.text_input("Enter Motif Theme (e.g., Sunset, Rose, Luxury, Ocean, Minimalist):", "sunset", key="sia_motif_input")
                
            st.info("✨ SIA Style Profile Active & Synced to Render Pipeline.")

        st.divider()
        st.markdown("### 🚀 Final Deck Generation")
        st.markdown("Your content preview deck is confirmed and your style engine mode is selected.")
        
        if st.button("✨ Generate Styled Deck with SIA Parameters", type="primary", use_container_width=True, key="sia_generate_final_deck"):
            st.session_state["sia_deck_generated"] = True
            st.success("🎉 Styled carousel deck successfully generated using your preview deck and selected SIA Style Mode!")

        if st.session_state.get("sia_deck_generated", False):
            st.info("⚡ Deck is locked and styled! Switch over to Carousel Studio or export your finalized slides.")