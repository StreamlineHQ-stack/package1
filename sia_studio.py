import os
import streamlit as st
import json
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas

def render_sia_studio():
    st.markdown("## 🧠 OpenAI Vision Design Intent Analyzer")
    
    # Retrieve API key cleanly from secrets or environment
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

    # If key is found in secrets/env, show a success badge instead of forcing a blank input box
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
                st.error("Please provide an API key or configure it in Streamlit secrets.")
                return
            
            with st.spinner("Deconstructing visual DNA via OpenRouter..."):
                try:
                    data_url, _ = image_to_data_url(uploaded_file)
                    spec = analyze_image(api_key=api_key, model="openai/gpt-4o-mini", image_data_url=data_url, user_focus=user_focus)
                    st.success("Visual analysis completed successfully!")
                    st.json(spec)
                    st.session_state["last_sia_spec"] = spec
                except Exception as e:
                    st.error(f"Error during analysis: {e}")

    st.divider()
    st.markdown("### 📊 Deconstruction Report & Content Engine")
    slide_count = st.slider("Target Slide Count:", 3, 10, 6)
    
    tab_autopilot, tab_notes, tab_wizard = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
    with tab_autopilot:
        st.write("Ready to generate slides based on deconstructed spec.")
        if "last_sia_spec" in st.session_state:
            render_universal_canvas(st.session_state["last_sia_spec"], slide_count)
        else:
            st.info("Upload and analyze a reference swipe above to activate auto-pilot generation.")
    with tab_notes:
        st.text_area("Add custom guidance notes for copy generation:", placeholder="Focus on high-ticket coaching transformation...")
    with tab_wizard:
        st.write("Configure framework parameters and style constraints.")