import os
import streamlit as st
import json
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas

def render_sia_studio():
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

    # --- GLOBAL SLIDE COUNT CONFIGURATION GATE ---
    col_cfg1, col_cfg2 = st.columns([2, 1])
    with col_cfg1:
        st.markdown("### ⚙️ Carousel Configuration")
    with col_cfg2:
        dynamic_slide_count = st.slider("Select Number of Slides:", min_value=3, max_value=10, value=st.session_state.get("sia_global_slide_count", 4), key="sia_global_slide_count")

    st.divider()

    # --- WORKFLOW STEP NAVIGATION ---
    if "sia_workflow_step" not in st.session_state:
        st.session_state["sia_workflow_step"] = "step1_content"

    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("📝 Step 1: Content Engine", use_container_width=True):
            st.session_state["sia_workflow_step"] = "step1_content"
            st.rerun()
    with nav_col2:
        if st.button("🎨 Step 2: Visual Foundation & Engine", use_container_width=True):
            st.session_state["sia_workflow_step"] = "step2_visual"
            st.rerun()

    st.divider()

    # ==========================================
    # STEP 1: CONTENT ENGINE ONLY
    # ==========================================
    if st.session_state["sia_workflow_step"] == "step1_content":
        render_universal_canvas(spec={}, slide_count=dynamic_slide_count, content_only_mode=True)

    # ==========================================
    # STEP 2: CHOOSE VISUAL FOUNDATION (3A vs 3B)
    # ==========================================
    elif st.session_state["sia_workflow_step"] == "step2_visual":
        st.markdown("### 🧭 Step 3: Choose Visual Foundation")
        visual_path = st.radio(
            "Select your visual foundation method:",
            [
                "3A. Reference Slide (Visual DNA Analysis)",
                "3B. Standalone Visual Modules (No Reference Slide)"
            ],
            key="visual_path_choice"
        )

        st.divider()

        # ==========================================
        # WORKFLOW 2: PATH 3A (Reference Slide & Art Director Routing)
        # ==========================================
        if "3A" in visual_path:
            st.session_state["is_standalone_mode"] = False
            
            st.markdown("#### 🧬 Visual DNA Analysis Suite")
            uploaded_file = st.file_uploader("Upload Inspiration Slide", type=["png", "jpg", "jpeg"], key="sia_swipe_upload")
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Reference Swipe Preview", width=300)
                st.session_state["sia_persisted_image"] = uploaded_file.getvalue()
                
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

            if st.session_state.get("visual_approved", False) and "visual_brief" in st.session_state:
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=dynamic_slide_count, content_only_mode=False, standalone_mode=False)

        # ==========================================
        # WORKFLOW 1: PATH 3B (3 Standalone Models)
        # ==========================================
        else:
            st.markdown("#### 📦 Standalone Visual Modules")
            standalone_choice = st.radio(
                "Choose Standalone Model:",
                [
                    "Smart AI Background",
                    "Unified Motif",
                    "Custom Image"
                ],
                key="standalone_model_radio"
            )

            standalone_payload = {"type": standalone_choice}

            if "Smart AI Background" in standalone_choice:
                st.info("💡 **Smart AI Background Module:** Dynamically queries live Unsplash context streams for professional background photography across your deck.")
            elif "Unified Motif" in standalone_choice:
                motif_val = st.text_input("Enter Motif Description (e.g. floral, luxury, minimal):", value="floral")
                standalone_payload["motif"] = motif_val
            elif "Custom Image" in standalone_choice:
                custom_file = st.file_uploader("Upload Custom Background Image (Applied across the deck)", type=["png", "jpg", "jpeg"], key="custom_standalone_img")
                if custom_file is not None:
                    st.image(custom_file, caption="Custom Background Asset", width=250)
                    standalone_payload["custom_image_bytes"] = custom_file.getvalue()

            if st.button("🚀 Generate Full Dummy Deck", type="primary", key="btn_gen_standalone_deck"):
                st.session_state["is_standalone_mode"] = True
                st.session_state["visual_brief"] = {
                    "design_style": standalone_choice,
                    "standalone_payload": standalone_payload,
                    "palette": ["Red", "Black", "Yellow", "White"],
                    "visual_mood": "High-Converting Professional"
                }
                st.success(f"{standalone_choice} module applied successfully!")
                st.rerun()

            if st.session_state.get("is_standalone_mode", False) and "visual_brief" in st.session_state:
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=dynamic_slide_count, content_only_mode=False, standalone_mode=True)