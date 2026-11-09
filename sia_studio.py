import os
import streamlit as st
import json
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas

def render_sia_studio():
    st.markdown("## 🎨 Art Director & Content Engine Suite")
    
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

    if not api_key:
        api_key = st.text_input("Enter OpenRouter / OpenAI API Key:", type="password", key="sia_manual_key")

    st.divider()

    # --- INITIALIZE WIZARD STEP ---
    if "sia_main_step" not in st.session_state:
        st.session_state["sia_main_step"] = "content_first"

    # Top-level workflow switcher for total modular separation
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("📝 Step 1: Content Engine (Copy & Frameworks)", use_container_width=True):
            st.session_state["sia_main_step"] = "content_first"
            st.rerun()
    with nav_col2:
        if st.button("🎨 Step 2: Visual Foundation & Art Director", use_container_width=True):
            st.session_state["sia_main_step"] = "visual_foundation"
            st.rerun()

    st.divider()

    # ==========================================
    # STEP 1: CONTENT ENGINE FIRST (Completely Separated)
    # ==========================================
    if st.session_state["sia_main_step"] == "content_first":
        st.markdown("### 📝 Step 1: Content Engine & Copywriting Suite")
        st.markdown("Build and structure your direct-response carousel copy first, independently of any visual design brief.")
        
        # Render the universal canvas in content-editing mode
        render_universal_canvas(spec=st.session_state.get("visual_brief", {}), content_only_mode=True)

    # ==========================================
    # STEP 2: VISUAL FOUNDATION & ART DIRECTOR
    # ==========================================
    elif st.session_state["sia_main_step"] == "visual_foundation":
        st.markdown("### 🧭 Step 2: Visual Foundation & Art Director Suite")
        
        visual_path = st.radio(
            "Select your visual foundation method:",
            [
                "3A. Reference Slide (Visual DNA Analysis)",
                "3B. Standalone Visual Modules (No Reference Slide)"
            ],
            key="visual_path_choice"
        )

        st.divider()

        if "3A" in visual_path:
            st.markdown("#### 🧬 Visual DNA Analysis Suite")
            uploaded_file = st.file_uploader("Upload Reference Slide", type=["png", "jpg", "jpeg"], key="sia_swipe_upload")
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Reference Swipe Preview", width=400)
                user_focus = st.text_input("Design Focus / Custom Prompt:", value="Analyze overall design intent and typography.")
                
                if st.button("🔍 Run Visual DNA Analysis", key="run_sia_vision"):
                    if not api_key:
                        st.error("Please provide an API key.")
                        return
                    
                    with st.spinner("Deconstructing visual DNA strictly as visual brief..."):
                        try:
                            data_url, _ = image_to_data_url(uploaded_file)
                            spec = analyze_image(api_key=api_key, model="openai/gpt-4o-mini", image_data_url=data_url, user_focus=user_focus)
                            st.success("Visual DNA extracted successfully!")
                            st.session_state["visual_brief"] = spec
                            st.session_state["visual_approved"] = True
                        except Exception as e:
                            st.error(f"Error during analysis: {e}")
        else:
            module_choice = st.selectbox(
                "Select Standalone Visual Module:",
                ["SmartAI Backgrounds", "Unified Motif", "Custom Image Upload"],
                key="standalone_module_select"
            )
            if st.button("Apply Standalone Visual Module", key="btn_apply_mod"):
                st.session_state["visual_brief"] = {"design_style": module_choice, "palette": ["Red", "Black", "Yellow", "White"]}
                st.session_state["visual_approved"] = True
                st.success("Visual module applied!")

        # Once visual brief is ready, hand off to the Art Director Renderer
        if st.session_state.get("visual_approved", False):
            st.divider()
            st.markdown("### 🧬 Art Director Asset Routing & Preview")
            render_universal_canvas(spec=st.session_state["visual_brief"], content_only_mode=False)