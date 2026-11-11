# sia_studio.py • Updated Studio with 3 Asset Modes & Unique Widget Keys
import os
import streamlit as st
import json
import io
import zipfile
from PIL import Image
from sia_vision_parser import image_to_data_url, analyze_image
from sia_universal_renderer import render_universal_canvas
from slide_visual_asset_extractor import SlideVisualAssetExtractor

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

    # --- CROSS-MODULE BRIDGE CHECK ---
    downstream_payload = st.session_state.get("sia_downstream_payload") or st.session_state.get("external_imported_slides")
    if downstream_payload and isinstance(downstream_payload, list) and len(downstream_payload) > 0:
        st.session_state["sia_slide_contents"] = downstream_payload
        st.session_state["sia_content_received_banner"] = True
        if "sia_downstream_payload" in st.session_state:
            del st.session_state["sia_downstream_payload"]
        if "external_imported_slides" in st.session_state:
            del st.session_state["external_imported_slides"]

    # --- WORKFLOW STEP NAVIGATION ---
    if "sia_workflow_step" not in st.session_state:
        st.session_state["sia_workflow_step"] = "step1_content"

    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("📝 Step 1: Content Engine", use_container_width=True, key="sia_nav_step1"):
            st.session_state["sia_workflow_step"] = "step1_content"
            st.rerun()
    with nav_col2:
        if st.button("🎨 Step 2: Visual Foundation & Engine", use_container_width=True, key="sia_nav_step2"):
            st.session_state["sia_workflow_step"] = "step2_visual"
            st.rerun()

    st.divider()

    # ==========================================
    # STEP 1: CONTENT ENGINE ONLY
    # ==========================================
    slide_count = st.session_state.get("sia_global_slide_count", 4)
    if "sia_slide_contents" in st.session_state and st.session_state["sia_slide_contents"]:
        slide_count = len(st.session_state["sia_slide_contents"])

    if st.session_state["sia_workflow_step"] == "step1_content":
        render_universal_canvas(spec={}, slide_count=slide_count, content_only_mode=True)

    # ==========================================
    # STEP 2: CHOOSE VISUAL FOUNDATION & ASSET MODES
    # ==========================================
    elif st.session_state["sia_workflow_step"] == "step2_visual":
        st.markdown("### 🧭 Step 3: Choose Visual Foundation & Asset Modes")
        visual_path = st.radio(
            "Select your visual foundation method:",
            [
                "3A. Reference Slide (Visual DNA & 3 Asset Extraction Modes)",
                "3B. Standalone Visual Modules (No Reference Slide)"
            ],
            key="visual_path_choice_main"
        )

        st.divider()

        # ==========================================
        # WORKFLOW 2: PATH 3A (Reference Slide & 3 Asset Modes)
        # ==========================================
        if "3A" in visual_path:
            st.session_state["is_standalone_mode"] = False
            
            st.markdown("#### 🧬 Visual Asset Extraction & Composition Suite")
            uploaded_file = st.file_uploader("Upload Inspiration Reference Slide", type=["png", "jpg", "jpeg"], key="sia_swipe_upload_3a")
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Reference Inspiration Slide", width=350)
                ref_bytes = uploaded_file.getvalue()
                st.session_state["sia_persisted_image"] = ref_bytes
                
                extractor = SlideVisualAssetExtractor()
                
                # Choose among the 3 Asset Modes
                asset_mode = st.radio(
                    "Choose Asset Extraction / Composition Mode:",
                    [
                        "Mode 1: Background Extraction (Background texture/color only)",
                        "Mode 2: Inspiration Slide Extraction (Textless Original Composition)",
                        "Mode 3: Custom Visual Composition (User-supplied background + subject)"
                    ],
                    key="sia_asset_mode_selector"
                )
                
                st.divider()
                
                if "Mode 1" in asset_mode:
                    st.info("💡 **Mode 1:** Isolates pure background textures and color gradients from your reference slide.")
                    if st.button("✨ Extract Background Asset", key="btn_extract_mode1", type="primary"):
                        extracted_bg = extractor.render_mode_1_background(ref_bytes)
                        st.image(extracted_bg, caption="Extracted Background Asset", width=400)
                        st.download_button("📥 Download Background (.png)", extracted_bg, "extracted_background.png", "image/png", key="dl_mode1")
                        st.session_state["visual_brief"] = {"design_style": "Mode 1 Background", "extracted_bytes": extracted_bg}
                        st.session_state["visual_approved"] = True

                elif "Mode 2" in asset_mode:
                    st.info("💡 **Mode 2:** Preserves the original slide composition, subjects, and decorations as-is while removing typography.")
                    if st.button("✨ Extract Textless Original Slide", key="btn_extract_mode2", type="primary"):
                        clean_slide = extractor.render_mode_2_textless(ref_bytes)
                        st.image(clean_slide, caption="Textless Inspiration Slide", width=400)
                        st.download_button("📥 Download Textless Slide (.png)", clean_slide, "textless_inspiration_slide.png", "image/png", key="dl_mode2")
                        st.session_state["visual_brief"] = {"design_style": "Mode 2 Textless", "extracted_bytes": clean_slide}
                        st.session_state["visual_approved"] = True

                elif "Mode 3" in asset_mode:
                    st.info("💡 **Mode 3:** Combines your custom background and subject assets using the reference composition rules.")
                    custom_bg = st.file_uploader("Upload Custom Background Image", type=["png", "jpg", "jpeg"], key="mode3_custom_bg")
                    custom_sub = st.file_uploader("Upload Subject / Object Image (transparent PNG recommended)", type=["png", "jpg", "jpeg"], key="mode3_custom_sub")
                    
                    if custom_bg and custom_sub:
                        if st.button("🚀 Generate Custom Composition", key="btn_gen_mode3", type="primary"):
                            composed_bytes = extractor.render_mode_3_composition(custom_bg.getvalue(), custom_sub.getvalue(), ref_bytes)
                            st.image(composed_bytes, caption="Custom Composed Asset", width=400)
                            st.download_button("📥 Download Composed Slide (.png)", composed_bytes, "custom_composed_slide.png", "image/png", key="dl_mode3")
                            st.session_state["visual_brief"] = {"design_style": "Mode 3 Composition", "extracted_bytes": composed_bytes}
                            st.session_state["visual_approved"] = True

            if st.session_state.get("visual_approved", False) and "visual_brief" in st.session_state:
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)

                # --- EXPORT OPTIONS & KINETIC HANDOFF ---
                st.divider()
                st.markdown("### 📥 Export Options & Kinetic Handoff")
                exp_col1, exp_col2, exp_col3 = st.columns(3)
                
                with exp_col1:
                    if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="sia_3a_kinetic_btn"):
                        st.session_state["slides_data"] = st.session_state.get("sia_slide_contents", [])
                        st.session_state["deck_json"] = st.session_state.get("sia_slide_contents", [])
                        st.session_state["active_view"] = "kinetic_ui"
                        st.rerun()

                with exp_col2:
                    slides_data = st.session_state.get("sia_slide_contents", [])
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for idx, s in enumerate(slides_data):
                            zip_file.writestr(f"carousel_slide_{idx+1}.json", json.dumps(s, indent=2))
                    zip_buffer.seek(0)
                    st.download_button(
                        label="📦 Download Deck (.zip)",
                        data=zip_buffer,
                        file_name="carousel_deck_package.zip",
                        mime="application/zip",
                        use_container_width=True,
                        key="sia_3a_download_zip"
                    )

                with exp_col3:
                    if st.button("🔄 Edit Content Again", key="sia_3a_restart", use_container_width=True):
                        st.session_state["sia_workflow_step"] = "step1_content"
                        st.rerun()

        # ==========================================
        # WORKFLOW 1: PATH 3B (Standalone Models)
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
                key="standalone_model_radio_3b"
            )

            standalone_payload = {"type": standalone_choice}

            if "Smart AI Background" in standalone_choice:
                st.info("💡 **Smart AI Background Module:** Dynamically queries live Unsplash context streams for professional background photography across your deck.")
            elif "Unified Motif" in standalone_choice:
                motif_val = st.text_input("Enter Motif Description (e.g. floral, luxury, minimal):", value="floral", key="sia_3b_motif_input")
                standalone_payload["motif"] = motif_val
            elif "Custom Image" in standalone_choice:
                custom_file = st.file_uploader("Upload Custom Background Image (Applied across the deck)", type=["png", "jpg", "jpeg"], key="custom_standalone_img_3b")
                if custom_file is not None:
                    st.image(custom_file, caption="Custom Background Asset", width=250)
                    standalone_payload["custom_image_bytes"] = custom_file.getvalue()

            if st.button("🚀 Generate Full Dummy Deck", type="primary", key="btn_gen_standalone_deck_3b"):
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
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=True)

                # --- EXPORT OPTIONS & KINETIC HANDOFF ---
                st.divider()
                st.markdown("### 📥 Export Options & Kinetic Handoff")
                exp_col1, exp_col2, exp_col3 = st.columns(3)
                
                with exp_col1:
                    if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="sia_3b_kinetic_btn"):
                        st.session_state["slides_data"] = st.session_state.get("sia_slide_contents", [])
                        st.session_state["deck_json"] = st.session_state.get("sia_slide_contents", [])
                        st.session_state["active_view"] = "kinetic_ui"
                        st.rerun()

                with exp_col2:
                    slides_data = st.session_state.get("sia_slide_contents", [])
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for idx, s in enumerate(slides_data):
                            zip_file.writestr(f"carousel_slide_{idx+1}.json", json.dumps(s, indent=2))
                    zip_buffer.seek(0)
                    st.download_button(
                        label="📦 Download Deck (.zip)",
                        data=zip_buffer,
                        file_name="carousel_deck_package.zip",
                        mime="application/zip",
                        use_container_width=True,
                        key="sia_3b_download_zip"
                    )

                with exp_col3:
                    if st.button("🔄 Edit Content Again", key="sia_3b_restart", use_container_width=True):
                        st.session_state["sia_workflow_step"] = "step1_content"
                        st.rerun()