import os
import streamlit as st
import json
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas

def render_sia_studio():
    st.markdown("## 🧠 OpenAI Vision Design Intent Analyzer")
    
    # Debug and load secrets safely
    secret_key = ""
    try:
        available_secrets = list(st.secrets.keys())
        # Check common naming conventions in secrets
        for k in ["OPENROUTER_API_KEY", "OPENAI_API_KEY", "OPENROUTER", "OPENAI", "API_KEY"]:
            if k in st.secrets:
                secret_key = st.secrets[k]
                break
        # If nested under a section like [api] or [openrouter]
        if not secret_key:
            for section in available_secrets:
                if isinstance(st.secrets[section], dict):
                    for subk in ["OPENROUTER_API_KEY", "OPENAI_API_KEY", "key", "api_key"]:
                        if subk in st.secrets[section]:
                            secret_key = st.secrets[section][subk]
                            break
    except Exception as e:
        secret_key = os.getenv("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))

    if "sia_openai_key_input" not in st.session_state or not st.session_state["sia_openai_key_input"]:
        st.session_state["sia_openai_key_input"] = secret_key

    api_key_input = st.text_input("OpenAI / OpenRouter API Key:", type="password", key="sia_openai_key_input")
    
    if not api_key_input:
        try:
            st.warning(f"⚠️ API key not detected in st.secrets. Available secret sections/keys: {list(st.secrets.keys())}. Please paste your OpenRouter key below or add it to Streamlit secrets.")
        except Exception:
            st.warning("⚠️ API key not detected. Please paste your OpenRouter key below.")

    uploaded_file = st.file_uploader("Upload Swipe Image / Slide Reference", type=["png", "jpg", "jpeg"], key="sia_swipe_upload")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Reference Swipe", width=400)
        
        user_focus = st.text_input("Design Focus / Custom Prompt:", value="Analyze overall design intent and typography.")
        
        if st.button("🔍 Run Vision Analysis on Swipe", key="run_sia_vision"):
            key_to_use = api_key_input or st.session_state.get("sia_openai_key_input", "")
            if not key_to_use:
                st.error("Please provide an API key.")
                return
            
            with st.spinner("Deconstructing visual DNA via OpenRouter..."):
                try:
                    data_url, _ = image_to_data_url(uploaded_file)
                    spec = analyze_image(api_key=key_to_use, model="openai/gpt-4o-mini", image_data_url=data_url, user_focus=user_focus)
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