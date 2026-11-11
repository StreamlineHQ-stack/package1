# ------------------------------------------
            # MODE 2 PIPELINE
            # ------------------------------------------
            elif "Mode 2" in extract_mode:
                st.info("💡 **Mode 2:** Removes text overlays using AI Vision and precise margin trimming.")
                m2_file = st.file_uploader("Upload Reference Inspiration Slide", type=["png", "jpg", "jpeg"], key="m2_upload")
                
                # Add instant manual margin adjustment sliders for absolute control
                st.markdown("#### ✂️ Optional Margin Trims (Percentage to crop from edges)")
                m_top = st.slider("Trim Top %", 0, 30, 0, key="m_trim_top")
                m_bottom = st.slider("Trim Bottom %", 0, 30, 0, key="m_trim_bottom")
                m_left = st.slider("Trim Left %", 0, 30, 0, key="m_trim_left")
                m_right = st.slider("Trim Right %", 0, 30, 0, key="m_trim_right")

                if m2_file is not None:
                    st.image(m2_file, caption="Original Inspiration Slide", width=320)
                    if st.button("✨ Extract Textless Original Slide", key="btn_m2_run", type="primary"):
                        with st.spinner("Extracting textless asset..."):
                            res_bytes = extractor.render_mode_2_textless(
                                m2_file.getvalue(), 
                                api_key=api_key, 
                                crop_margins=(m_top, m_bottom, m_left, m_right)
                            )
                        st.session_state["extracted_asset_bytes"] = res_bytes
                        st.session_state["visual_brief"] = {
                            "design_style": "Mode 2 Textless Original Composition",
                            "asset_mode": "inspiration_visual",
                            "visual_asset_bytes": res_bytes,
                            "visual_asset_data_url": "data:image/png;base64," + base64.b64encode(res_bytes).decode("ascii"),
                            "visual_approved": True
                        }
                        st.success("Textless slide composition extracted successfully!")