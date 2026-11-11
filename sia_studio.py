# sia_studio.py • Cleanly Isolated 3-Mode Studio Pipeline
import os
import streamlit as st
import json
import io
import base64
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

    # --- CROSS-MODULE BRIDGE & CONTENT STATE SAFEGUARD ---
    downstream_payload = st.session_state.get("sia_downstream_payload") or st.session_state.get("external_imported_slides")
    if downstream_payload and isinstance(downstream_payload, list) and len(downstream_payload) > 0:
        st.session_state["sia_slide_contents"] = downstream_payload
        if "sia_downstream_payload" in st.session_state:
            del st.session_state["sia_downstream_payload"]
        if "external_imported_slides" in st.session_state:
            del st.session_state["external_imported_slides"]

    if "sia_slide_contents" not in st.session_state:
        st.session_state["sia_slide_contents"] = []

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
    # STEP 2: CHOOSE VISUAL FOUNDATION
    # ==========================================
    elif st.session_state["sia_workflow_step"] == "step2_visual":
        st.markdown("### 🧭 Step 2: Visual Foundation & Asset Engine")
        
        visual_path = st.radio(
            "Select Method:",
            [
                "1. Visual DNA Analysis (AI Art Director Style Brief)",
                "2. 3-Mode Visual Asset Extractor & Composer",
                "3. Standalone Visual Modules (No Reference Slide)"
            ],
            key="visual_path_choice_main_v2"
        )

        st.divider()

        # ==========================================
        # OPTION 1: VISUAL DNA ANALYSIS
        # ==========================================
        if "1. Visual DNA Analysis" in visual_path:
            st.session_state["is_standalone_mode"] = False
            st.markdown("#### 🧬 Visual DNA Analysis Suite")
            uploaded_file = st.file_uploader("Upload Inspiration Slide for DNA Analysis", type=["png", "jpg", "jpeg"], key="sia_dna_upload")
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Reference Swipe Preview", width=320)
                st.session_state["sia_persisted_image"] = uploaded_file.getvalue()
                
                user_focus = st.text_input("Design Focus / Custom Prompt:", value="Analyze overall design intent, color palette, and typography.", key="sia_dna_focus")
                
                if st.button("🔍 Run Visual DNA Analysis", key="run_dna_analysis_btn"):
                    if not api_key:
                        st.error("Please provide an API key.")
                    else:
                        with st.spinner("Deconstructing visual DNA into Art Director specification..."):
                            try:
                                data_url, _ = image_to_data_url(uploaded_file)
                                spec = analyze_image(api_key=api_key, model="openai/gpt-4o-mini", image_data_url=data_url, user_focus=user_focus)
                                st.session_state["visual_brief"] = spec
                                st.session_state["visual_approved"] = True
                            except Exception as e:
                                st.error(f"Error during analysis: {e}")

            if st.session_state.get("visual_approved", False) and "visual_brief" in st.session_state:
                st.success("✨ Visual DNA Analysis Complete!")
                st.markdown("#### 📋 Extracted Art Director Specification:")
                st.json(st.session_state["visual_brief"])
                
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)

        # ==========================================
        # OPTION 2: 3-MODE ASSET EXTRACTOR & COMPOSER
        # ==========================================
        elif "2. 3-Mode Visual Asset Extractor" in visual_path:
            st.session_state["is_standalone_mode"] = False
            st.markdown("#### 🛠️ Three-Mode Visual Asset Extractor & Composer")
            
            extractor = SlideVisualAssetExtractor()
            
            extract_mode = st.radio(
                "Select Asset Extraction / Composition Pipeline:",
                [
                    "Mode 1: Background Extraction (Pure texture & gradient isolation)",
                    "Mode 2: Inspiration Slide Extraction (Two-Output Separation & Coordinates)",
                    "Mode 3: Custom Visual Composition (User Background + Subject)"
                ],
                key="asset_pipeline_mode_radio"
            )
            
            st.divider()
            
            # ------------------------------------------
            # MODE 1 PIPELINE
            # ------------------------------------------
            if "Mode 1" in extract_mode:
                st.info("💡 **Mode 1:** Isolates background texture and color gradient, stripping away text and foreground subjects.")
                m1_file = st.file_uploader("Upload Reference Slide for Mode 1", type=["png", "jpg", "jpeg"], key="m1_upload")
                if m1_file is not None:
                    st.image(m1_file, caption="Reference Slide", width=320)
                    if st.button("✨ Extract Background Asset", key="btn_m1_run", type="primary"):
                        res_bytes = extractor.render_mode_1_background(m1_file.getvalue())
                        st.session_state["extracted_asset_bytes"] = res_bytes
                        st.session_state["visual_brief"] = {
                            "design_style": "Mode 1 Background",
                            "asset_mode": "inspiration_visual",
                            "visual_asset_bytes": res_bytes,
                            "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(res_bytes).decode("ascii"),
                            "visual_approved": True
                        }
                        st.success("Background extracted successfully!")
                        st.rerun()

            # ------------------------------------------
            # MODE 2 PIPELINE (Two Outputs + Transparency + Coordinates)
            # ------------------------------------------
            elif "Mode 2" in extract_mode:
                st.info("💡 **Mode 2:** Generates clean background canvas, creates transparent asset, and maps exact pixel coordinates.")
                m2_file = st.file_uploader("Upload Reference Inspiration Slide", type=["png", "jpg", "jpeg"], key="m2_upload")
                
                if m2_file is not None:
                    st.image(m2_file, caption="Original Inspiration Slide", width=320)
                    if st.button("✨ Extract Background & Transparent Asset", key="btn_m2_run", type="primary"):
                        with st.spinner("Separating background and isolating transparent asset..."):
                            outputs = extractor.render_mode_2_textless(m2_file.getvalue())
                        
                        st.session_state["m2_bg_bytes"] = outputs["background_bytes"]
                        st.session_state["m2_trans_bytes"] = outputs["transparent_asset_bytes"]
                        st.session_state["m2_coords"] = outputs["coordinates"]
                        
                        st.session_state["extracted_asset_bytes"] = outputs["background_bytes"]
                        st.session_state["visual_brief"] = {
                            "design_style": "Mode 2 Textless Original Composition",
                            "asset_mode": "inspiration_visual",
                            "visual_asset_bytes": outputs["background_bytes"],
                            "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(outputs["background_bytes"]).decode("ascii"),
                            "visual_approved": True
                        }
                        st.success("Two-output separation complete!")
                        st.rerun()

            # ------------------------------------------
            # MODE 3 PIPELINE
            # ------------------------------------------
            elif "Mode 3" in extract_mode:
                st.info("💡 **Mode 3:** Combines your custom background and subject assets into a professional composition.")
                u_bg = st.file_uploader("Upload Custom Background Image", type=["png", "jpg", "jpeg"], key="m3_bg_file")
                u_sub = st.file_uploader("Upload Subject / Object Image (transparent PNG)", type=["png", "jpg", "jpeg"], key="m3_sub_file")
                
                if u_bg and u_sub:
                    st.image(u_bg, caption="Background Preview", width=250)
                    st.image(u_sub, caption="Subject Preview", width=250)
                    if st.button("🚀 Generate Custom Composition", key="btn_m3_run", type="primary"):
                        res_bytes = extractor.render_mode_3_composition(u_bg.getvalue(), u_sub.getvalue())
                        st.session_state["extracted_asset_bytes"] = res_bytes
                        st.session_state["visual_brief"] = {
                            "design_style": "Mode 3 Composition",
                            "asset_mode": "inspiration_visual",
                            "visual_asset_bytes": res_bytes,
                            "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(res_bytes).decode("ascii"),
                            "visual_approved": True
                        }
                        st.success("Custom composition generated successfully!")
                        st.rerun()

            # Display Mode 2 Two Outputs & Coordinates if available
            if "m2_trans_bytes" in st.session_state:
                st.divider()
                st.markdown("### 🎯 Mode 2: Two Clean Outputs & Coordinate Map")
                
                out_col1, out_col2 = st.columns(2)
                with out_col1:
                    st.markdown("#### 1. Generated Solid Background")
                    st.image(st.session_state["m2_bg_bytes"], caption="Clean Background Canvas", width=300)
                    st.download_button("📥 Download Background (.png)", st.session_state["m2_bg_bytes"], "clean_background.png", "image/png", key="dl_m2_bg")

                with out_col2:
                    st.markdown("#### 2. Transparent Core Asset")
                    st.image(st.session_state["m2_trans_bytes"], caption="Transparent Subject/Card", width=300)
                    st.download_button("📥 Download Transparent Asset (.png)", st.session_state["m2_trans_bytes"], "transparent_asset.png", "image/png", key="dl_m2_trans")

                st.markdown("#### 📍 Exact Pixel Position & Dimensions:")
                coords = st.session_state["m2_coords"]
                st.json(coords)

                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)

        # ==========================================
        # OPTION 3: STANDALONE VISUAL MODULES
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
                key="standalone_model_radio_v2"
            )

            standalone_payload = {"type": standalone_choice}

            if "Smart AI Background" in standalone_choice:
                st.info("💡 **Smart AI Background Module:** Dynamically queries live Unsplash context streams for professional background photography across your deck.")
            elif "Unified Motif" in standalone_choice:
                motif_val = st.text_input("Enter Motif Description (e.g. floral, luxury, minimal):", value="floral", key="sia_motif_input_v2")
                standalone_payload["motif"] = motif_val
            elif "Custom Image" in standalone_choice:
                custom_file = st.file_uploader("Upload Custom Background Image", type=["png", "jpg", "jpeg"], key="custom_standalone_img_v2")
                if custom_file is not None:
                    st.image(custom_file, caption="Custom Background Asset", width=250)
                    standalone_payload["custom_image_bytes"] = custom_file.getvalue()

            if st.button("🚀 Generate Full Dummy Deck", type="primary", key="btn_gen_standalone_v2"):
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

        # --- EXPORT OPTIONS & KINETIC HANDOFF (Common for all paths) ---
        if st.session_state.get("visual_brief") or st.session_state.get("is_standalone_mode", False):
            st.divider()
            st.markdown("### 📥 Export Options & Kinetic Handoff")
            exp_col1, exp_col2, exp_col3 = st.columns(3)
            
            with exp_col1:
                if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="common_kinetic_btn"):
                    st.session_state["slides_data"] = st.session_state.get("sia_slide_contents", [])
                    st.session_state["deck_json"] = st.session_state.get("sia_slide_contents", [])
                    active_visual = st.session_state.get("visual_brief", {})
                    if active_visual.get("asset_mode") == "inspiration_visual":
                        st.session_state["kinetic_visual_asset_bytes"] = active_visual.get("visual_asset_bytes")
                        st.session_state["kinetic_visual_asset_data_url"] = active_visual.get("visual_asset_data_url")
                    st.session_state["active_view"] = "kinetic_ui"
                    st.rerun()

            with exp_col2:
                slides_data = st.session_state.get("sia_slide_contents", [])
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, s in enumerate(slides_data):
                        zip_file.writestr(f"carousel_slide_{idx+1}.json", json.dumps(s, indent=2))
                    active_visual = st.session_state.get("visual_brief", {})
                    if active_visual.get("asset_mode") == "inspiration_visual":
                        visual_bytes = active_visual.get("visual_asset_bytes")
                        if visual_bytes:
                            zip_file.writestr("visual_assets/extracted_inspiration.png", visual_bytes)
                zip_buffer.seek(0)
                st.download_button(
                    label="📦 Download Deck (.zip)",
                    data=zip_buffer,
                    file_name="carousel_deck_package.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="common_download_zip"
                )

            with exp_col3:
                if st.button("🔄 Edit Content Again", key="common_restart_btn", use_container_width=True):
                    st.session_state["sia_workflow_step"] = "step1_content"
                    st.rerun()