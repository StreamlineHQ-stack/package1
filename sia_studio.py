# ==========================================
        # OPTION 2: 3-MODE VISUAL ASSET EXTRACTOR & COMPOSER (ROUTER INTEGRATION)
        # ==========================================
        elif "2. 3-Mode Visual Asset Extractor" in visual_path:
            st.session_state["is_standalone_mode"] = False
            st.markdown("#### 🔍 3-Mode Intelligent Extraction Pipeline")
            
            uploaded_slide = st.file_uploader("Upload Inspiration Slide for Router Processing", type=["png", "jpg", "jpeg"], key="sia_router_upload")
            
            if uploaded_slide is not None:
                st.image(uploaded_slide, caption="Uploaded Inspiration Slide", width=320)
                
                if st.button("🚀 Run Extraction Router Pipeline", key="run_extraction_router_btn"):
                    with st.spinner("Analyzing structure & executing multi-stage extraction router..."):
                        try:
                            from PIL import Image
                            import io
                            import base64
                            from stage1_image_intelligence import analyze_image_structure
                            from stage3_extraction_router import process_with_router

                            img = Image.open(uploaded_slide).convert("RGB")
                            stage1_report = analyze_image_structure(img)
                            cleaned_img, mask_img, combined_report = process_with_router(img, stage1_report)

                            buffered = io.BytesIO()
                            cleaned_img.save(buffered, format="PNG")
                            img_bytes = buffered.getvalue()
                            b64_str = base64.b64encode(img_bytes).decode()
                            data_url = f"data:image/png;base64,{b64_str}"

                            # Fully populated spec so the universal canvas renders properly downstream
                            visual_spec = {
                                "asset_mode": "inspiration_visual",
                                "visual_asset_bytes": img_bytes,
                                "visual_asset_data_url": data_url,
                                "router_report": combined_report,
                                "design_style": "Intelligent Extracted Asset",
                                "palette": ["#000000", "#FFFFFF", "#3B82F6"],
                                "typography": "Modern Clean",
                                "visual_mood": "Professional High-Converting"
                            }

                            st.session_state["visual_brief"] = visual_spec
                            st.session_state["visual_approved"] = True
                            st.success("Extraction pipeline executed & canvas spec loaded!")
                        except Exception as e:
                            st.error(f"Error during routing execution: {e}")

            if st.session_state.get("visual_approved", False) and "visual_brief" in st.session_state:
                st.markdown("#### 📋 Processed Extraction & Canvas Preview:")
                active_brief = st.session_state["visual_brief"]
                if isinstance(active_brief, dict):
                    if "visual_asset_bytes" in active_brief:
                        st.image(active_brief["visual_asset_bytes"], caption="Extracted Clean Background / Asset", width=320)
                
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)