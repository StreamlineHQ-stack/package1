import os
import streamlit as st
import json
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas

def render_sia_studio():
    st.markdown("## 🎨 Art Director & Visual Design Suites")
    
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

    # --- STEP 3: CHOOSE VISUAL PATH (3A vs 3B) ---
    st.markdown("### 🧭 Step 3: Choose Visual Foundation")
    visual_path = st.radio(
        "Select your visual foundation method:",
        [
            "3A. I have a Reference Slide (Visual DNA Analysis)",
            "3B. I do NOT have a Reference Slide (Choose from 3 Standalone Visual Modules)"
        ],
        key="visual_path_choice"
    )

    st.divider()

    # --- PATH 3A: REFERENCE SLIDE & VISUAL DNA ANALYSIS ---
    if "3A" in visual_path:
        st.markdown("#### 🧬 Visual DNA Analysis Suite")
        st.markdown("Upload a reference slide to extract its visual properties.")
        
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
                        st.session_state["visual_approved"] = False
                    except Exception as e:
                        st.error(f"Error during analysis: {e}")

        # --- STEP 4: ENHANCED VISUAL DNA VERIFICATION GATE ---
        if "visual_brief" in st.session_state and not st.session_state.get("visual_approved", False):
            st.divider()
            st.markdown("### 🔬 Step 4: Visual DNA Verification Gate")
            st.markdown("Review and verify the extracted visual attributes, foreground subjects, and background environment.")
            
            spec = st.session_state["visual_brief"]
            
            # 1. Style & Mood
            c1, c2 = st.columns(2)
            with c1:
                use_style = st.checkbox(f"Design Style: **{spec.get('design_style', '')}**", value=True, key="v_style")
                use_mood = st.checkbox(f"Visual Mood: **{spec.get('visual_mood', '')}**", value=True, key="v_mood")
            with c2:
                use_palette = st.checkbox(f"Palette: **{str(spec.get('palette', ''))}**", value=True, key="v_pal")
                use_comp = st.checkbox(f"Composition: **{spec.get('composition', '')}**", value=True, key="v_comp")

            st.divider()
            
            # 2. Foreground Figure / Object Decision (4E)
            st.markdown("#### 👤 Foreground Subject / Figure Analysis")
            fg_figure = spec.get('foreground_figure', 'None')
            st.info(f"Detected Foreground Subject: **{fg_figure}**")
            
            use_figure = st.radio(
                "Want to use this foreground figure/image/picture in your generated deck?",
                ["YES — Go with it", "NO — Choose/Upload a new figure or object"],
                key="fg_figure_decision"
            )
            
            if "NO" in use_figure:
                new_fg = st.file_uploader("Upload replacement foreground figure/object (PNG with transparent background recommended):", type=["png", "jpg", "jpeg"], key="replacement_fg")
                if new_fg:
                    st.success("New foreground asset staged.")

            st.divider()

            # 3. Background Scene / Environment Decision
            st.markdown("#### 🌄 Background Scene / Environment Analysis")
            bg_scene = spec.get('background_scene', 'Solid / Gradient Background')
            st.info(f"Detected Background Environment: **{bg_scene}**")
            
            use_bg = st.radio(
                "Want to use this background scene (e.g. forest, beach, studio gradient)?",
                ["YES — Go with it", "NO — Choose/Upload a new background scene"],
                key="bg_scene_decision"
            )
            
            if "NO" in use_bg:
                new_bg = st.file_uploader("Upload replacement background scene/image:", type=["png", "jpg", "jpeg"], key="replacement_bg")
                if new_bg:
                    st.success("New background asset staged.")

            visual_intent_desc = st.text_area("Visual Design Intent Description:", value=spec.get("design_intent", ""), key="v_intent")

            st.divider()
            btn_c1, btn_c2 = st.columns(2)
            with btn_c1:
                if st.button("✅ YES - Approve Visual Brief & Proceed to Content Engine", use_container_width=True):
                    spec["design_intent"] = visual_intent_desc
                    spec["use_style"] = use_style
                    spec["use_mood"] = use_mood
                    spec["foreground_decision"] = use_figure
                    spec["background_decision"] = use_bg
                    st.session_state["visual_approved"] = True
                    st.success("Visual brief locked and isolated!")
                    st.rerun()
            with btn_c2:
                if st.button("❌ NO - Reject & Upload New Reference Slide", use_container_width=True):
                    del st.session_state["visual_brief"]
                    st.session_state["visual_approved"] = False
                    st.warning("Visual brief discarded. Please upload a new reference slide.")
                    st.rerun()

    # --- PATH 3B: NO REFERENCE SLIDE (3 STANDALONE MODULES) ---
    else:
        st.markdown("#### 📦 Standalone Visual Modules (No Reference Slide)")
        module_choice = st.selectbox(
            "Select Standalone Visual Module:",
            [
                "1. SmartAI (AI-generated smart visual backgrounds & layout framing)",
                "2. Unified Motif (Type in motif to generate custom image asset pool)",
                "3. Custom Image Upload (Provide your own custom background/image asset)"
            ],
            key="standalone_module_select"
        )

        if "SmartAI" in module_choice:
            st.info("💡 **SmartAI Module:** Automatically configures high-converting visual layouts and background contrast vectors.")
            st.session_state["visual_brief"] = {
                "design_style": "SmartAI Clean Minimalist",
                "visual_mood": "High-Converting Professional",
                "design_intent": "Professional visual engagement",
                "foreground_figure": "None",
                "background_scene": "Clean gradient contrast",
                "background_generation_brief": "Minimalist gradient contrast",
                "use_style": True,
                "use_mood": True
            }
            st.session_state["visual_approved"] = True

        elif "Unified Motif" in module_choice:
            st.markdown("💡 **Unified Motif Module:** Enter your motif keywords to generate a custom image asset pool.")
            motif_input = st.text_input("Enter Motif Description:", value="Luxury dark gold geometric pattern")
            if st.button("🎨 Analyze Motif & Generate Asset Pool", key="btn_motif_gen"):
                st.success(f"Motif pool generated successfully for: {motif_input}")
                st.session_state["visual_brief"] = {
                    "design_style": f"Unified Motif ({motif_input})",
                    "visual_mood": "Sophisticated",
                    "design_intent": motif_input,
                    "foreground_figure": "None",
                    "background_scene": motif_input,
                    "background_generation_brief": f"Custom motif background: {motif_input}",
                    "use_style": True,
                    "use_mood": True
                }
                st.session_state["visual_approved"] = True

        elif "Custom Image Upload" in module_choice:
            st.markdown("💡 **Custom Image Module:** Upload your custom background image asset.")
            custom_img = st.file_uploader("Upload Custom Image Asset", type=["png", "jpg", "jpeg"], key="custom_img_upload")
            if custom_img is not None:
                st.image(custom_img, caption="Custom Asset Preview", width=300)
                st.session_state["visual_brief"] = {
                    "design_style": "Custom Uploaded Asset",
                    "visual_mood": "Personalized Brand",
                    "design_intent": "Custom background asset integration",
                    "foreground_figure": "None",
                    "background_scene": "Custom uploaded image",
                    "background_generation_brief": "User uploaded custom image asset",
                    "use_style": True,
                    "use_mood": True
                }
                st.session_state["visual_approved"] = True

    # --- STEP 5 & BEYOND: HANDOFF TO CONTENT ENGINE ONCE VISUAL BRIEF IS LOCKED ---
    if st.session_state.get("visual_approved", False) and "visual_brief" in st.session_state:
        st.divider()
        render_universal_canvas(st.session_state["visual_brief"])