import os
import streamlit as st
import json
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas

def render_sia_studio():
    st.markdown("## 🧠 OpenAI Vision Design Intent Analyzer")
    
    # Load API key cleanly from secrets or environment
    api_key = ""
    try:
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        elif "OPENROUTER_API_KEY" in st.secrets:
            api_key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))

    if api_key:
        st.success("🔑 OpenRouter / OpenAI API Key loaded successfully from secrets.")
    else:
        api_key = st.text_input("Enter OpenRouter / OpenAI API Key:", type="password", key="sia_manual_key")

    uploaded_file = st.file_uploader("Upload Swipe Image / Slide Reference", type=["png", "jpg", "jpeg"], key="sia_swipe_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Reference Swipe", width=400)
        
        user_focus = st.text_input("Design Focus / Custom Prompt:", value="Analyze overall design intent and typography.")
        
        if st.button("🔍 Run Vision Analysis on Swipe", key="run_sia_vision"):
            if not api_key:
                st.error("Please provide an API key.")
                return
            
            with st.spinner("Deconstructing visual DNA via OpenRouter..."):
                try:
                    data_url, _ = image_to_data_url(uploaded_file)
                    spec = analyze_image(api_key=api_key, model="openai/gpt-4o-mini", image_data_url=data_url, user_focus=user_focus)
                    st.success("Visual analysis completed successfully!")
                    st.session_state["last_sia_spec"] = spec
                    st.session_state["dna_approved"] = False # Reset approval on new analysis
                except Exception as e:
                    st.error(f"Error during analysis: {e}")

    # --- VISUAL DNA VERIFICATION GATE ---
    if "last_sia_spec" in st.session_state:
        st.divider()
        st.markdown("### 🧬 Visual DNA Verification Gate")
        st.markdown("Review the deconstructed elements below. Approve them to proceed, or reject to upload a new reference swipe.")
        
        spec = st.session_state["last_sia_spec"]
        
        col1, col2 = st.columns(2)
        with col1:
            use_style = st.checkbox(f"Design Style: **{spec.get('design_style', '')}** — Keep / Use this?", value=True, key="chk_style")
            use_mood = st.checkbox(f"Visual Mood: **{spec.get('visual_mood', '')}** — Keep / Use this?", value=True, key="chk_mood")
            use_palette = st.checkbox(f"Palette: **{spec.get('palette', '')}** — Keep / Use this?", value=True, key="chk_palette")
        with col2:
            use_comp = st.checkbox(f"Composition: **{spec.get('composition', '')}** — Keep / Use this?", value=True, key="chk_comp")
            use_brief = st.checkbox(f"Background Brief: **{spec.get('background_generation_brief', '')}** — Keep / Use this?", value=True, key="chk_brief")

        verified_intent = st.text_area("Design Intent (Verify or edit description):", value=spec.get("design_intent", ""), key="verified_intent_field")

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            if st.button("✅ YES - Approve Visual DNA & Open Content Engine", use_container_width=True):
                # Update spec with user verifications
                spec["design_intent"] = verified_intent
                spec["use_style"] = use_style
                spec["use_mood"] = use_mood
                st.session_state["dna_approved"] = True
                st.success("Visual DNA approved! Unlocking Carousel Content Engine below...")
        with d_col2:
            if st.button("❌ NO - Reject & Upload New Image", use_container_width=True):
                del st.session_state["last_sia_spec"]
                st.session_state["dna_approved"] = False
                st.warning("Deconstruction discarded. Please upload a new reference swipe above.")
                st.rerun()

    # --- RENDER CONTENT ENGINE IF APPROVED ---
    if st.session_state.get("dna_approved", False) and "last_sia_spec" in st.session_state:
        st.divider()
        slide_count = st.slider("Target Slide Count:", 3, 10, 6, key="verified_slide_count")
        render_universal_canvas(st.session_state["last_sia_spec"], slide_count)