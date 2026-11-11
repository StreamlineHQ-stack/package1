# sia_studio.py • Cleanly Isolated Studio with Robust State Synchronization
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
        st.markdown("### 📝 Content Engine & Copywriting Suite")
        
        if st.session_state.get("sia_content_received_banner", False):
            st.success("✨ Content successfully received! Loaded into Live Content Editor below for review and approval.")
        
        st.markdown(f"Building custom carousel with **{slide_count} slides**. Refine and structure your copy below.")
        
        tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
        
        with tab1:
            topic_prompt = st.text_input("Enter core topic or pain point:", value="Why time management matters", key="sia_autopilot_input")
            if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
                with st.spinner(f"Crafting direct-response {slide_count}-slide carousel deck..."):
                    default_titles = [
                        f"Why {topic_prompt} Is Costing You Clients",
                        "The Hidden Cost of Inefficiency",
                        "The 3-Step Execution Model",
                        "Step 1: Audit Your Time Blocks",
                        "Step 2: Eliminate Friction Points",
                        "Step 3: Automate Workflows",
                        "Overcoming Common Bottlenecks",
                        "Scaling Your Daily Output"
                    ]
                    new_slides = []
                    for i in range(slide_count):
                        cat = "HOOK" if i == 0 else ("CTA" if i == slide_count - 1 else f"STEP {i+1}")
                        t = default_titles[i % len(default_titles)]
                        c = f"Detailed breakdown and actionable execution strategy for slide {i+1} addressing {topic_prompt}."
                        new_slides.append({"category": cat, "title": t, "content": c})
                        
                    st.session_state["sia_slide_contents"] = new_slides
                    st.session_state["sia_content_received_banner"] = False
                    
                    # Clear stale widget keys so Streamlit rebinds them correctly
                    for idx in range(10):
                        for prefix in ["sia_content_t_", "sia_content_b_", "sia_content_c_"]:
                            if prefix + str(idx) in st.session_state:
                                del st.session_state[prefix + str(idx)]
                                
                    st.success("Auto-pilot generated successfully!")
                    st.rerun()
        
        with tab2:
            custom_notes = st.text_area("Paste notes:", value="Hook: Time management is leverage.", key="sia_custom_notes_input")
            if st.button("Format Custom Notes", type="primary", key="sia_btn_gen_notes"):
                new_slides = [
                    {"category": f"INSIGHT {i+1}", "title": f"Expert Breakdown {i+1}", "content": f"Structured insights based on notes: {custom_notes[:30]}..."}
                    for i in range(slide_count)
                ]
                st.session_state["sia_slide_contents"] = new_slides
                st.session_state["sia_content_received_banner"] = False
                for idx in range(10):
                    for prefix in ["sia_content_t_", "sia_content_b_", "sia_content_c_"]:
                        if prefix + str(idx) in st.session_state:
                            del st.session_state[prefix + str(idx)]
                st.success("Custom notes compiled!")
                st.rerun()
                
        with tab3:
            from framework_data import FRAMEWORK_LIBRARY
            selected_pillar = st.selectbox("Choose Content Pillar:", list(FRAMEWORK_LIBRARY.keys()), key="sia_pillar_select")
            templates_in_pillar = FRAMEWORK_LIBRARY[selected_pillar]
            selected_template_name = st.selectbox("Choose Blueprint:", list(templates_in_pillar.keys()), key="sia_template_select")
            if st.button("Format Framework Carousel", type="primary", key="sia_btn_gen_frame"):
                new_slides = [
                    {"category": selected_template_name.upper(), "title": f"Step {i+1}: Framework execution", "content": f"Executing blueprint step {i+1} for maximum engagement."}
                    for i in range(slide_count)
                ]
                st.session_state["sia_slide_contents"] = new_slides
                st.session_state["sia_content_received_banner"] = False
                for idx in range(10):
                    for prefix in ["sia_content_t_", "sia_content_b_", "sia_content_c_"]:
                        if prefix + str(idx) in st.session_state:
                            del st.session_state[prefix + str(idx)]
                st.success("Framework applied!")
                st.rerun()

        st.divider()
        st.markdown(f"#### ✍️ Live Content Editor ({slide_count} Slides Active)")
        slides = st.session_state["sia_slide_contents"]
        total_slides = len(slides)
        updated_slides = []
        for i in range(total_slides):
            s = slides[i] if isinstance(slides[i], dict) else {"title": str(slides[i]), "content": ""}
            with st.container(border=True):
                st.markdown(f"**Slide {i+1} of {total_slides}**")
                t_input = st.text_input(f"Headline {i+1}", value=s.get("title", ""), key=f"sia_content_t_{i}")
                b_input = st.text_area(f"Body {i+1}", value=s.get("content", s.get("body", "")), key=f"sia_content_b_{i}")
                cat_input = st.text_input(f"Category {i+1}", value=s.get("category", f"STEP {i+1}"), key=f"sia_content_c_{i}")
                updated_slides.append({"category": cat_input, "title": t_input, "content": b_input})
        st.session_state["sia_slide_contents"] = updated_slides
        
        st.divider()
        if st.button("🚀 Lock Content & Proceed to Step 2: Visual Engine", type="primary", use_container_width=True):
            st.session_state["sia_content_locked"] = True
            st.success("✨ Content locked! Switch to Step 2 above to configure your visual engine.")
            st.session_state["sia_workflow_step"] = "step2_visual"
            st.rerun()
        return

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
                    "Mode 2: Inspiration Slide Extraction (Textless Original Composition)",
                    "Mode 3: Custom Visual Composition (User Background + Subject)"
                ],
                key="asset_pipeline_mode_radio"
            )
            
            st.divider()
            
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

            elif "Mode 2" in extract_mode:
                st.info("💡 **Mode 2:** Removes text overlays while preserving background art and subjects.")
                m2_file = st.file_uploader("Upload Reference Inspiration Slide", type=["png", "jpg", "jpeg"], key="m2_upload")
                if m2_file is not None:
                    st.image(m2_file, caption="Original Inspiration Slide", width=320)
                    if st.button("✨ Extract Textless Original Slide", key="btn_m2_run", type="primary"):
                        res_bytes = extractor.render_mode_2_textless(m2_file.getvalue())
                        st.session_state["extracted_asset_bytes"] = res_bytes
                        st.session_state["visual_brief"] = {
                            "design_style": "Mode 2 Textless Original Composition",
                            "asset_mode": "inspiration_visual",
                            "visual_asset_bytes": res_bytes,
                            "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(res_bytes).decode("ascii"),
                            "visual_approved": True
                        }
                        st.success("Textless slide composition extracted successfully!")

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

            if "extracted_asset_bytes" in st.session_state:
                st.divider()
                st.markdown("#### 🖼️ Processed Asset Output")
                st.image(st.session_state["extracted_asset_bytes"], caption="Extracted Visual Asset", width=400)
                st.download_button(
                    "📥 Download Processed Asset (.png)",
                    st.session_state["extracted_asset_bytes"],
                    "processed_visual_asset.png",
                    "image/png",
                    key="dl_extracted_asset_final"
                )
                
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

        # --- EXPORT OPTIONS & KINETIC HANDOFF ---
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
                    if active_visual.get("asset_email") == "inspiration_visual" or active_visual.get("visual_asset_bytes"):
                        visual_bytes = active_visual.get("visual_asset_bytes")
                        if visual_bytes:
                            zip_file.writestr("visual_assets/extracted_inspiration.png", visual_bytes)
                zip_buffer.seek(0)
                st.download_button(
                    label="📦 Download Deck (.zip)",
                    data=zip_file if 'zip_file' in locals() else zip_buffer,
                    file_name="carousel_deck_package.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="common_download_zip"
                )

            with exp_col3:
                if st.button("🔄 Edit Content Engine Again", key="common_restart_btn", use_container_width=True):
                    st.session_state["sia_workflow_step"] = "step1_content"
                    st.rerun()
