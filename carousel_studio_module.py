col_bridge_btn, col_zip_btn, col_download_btn = st.columns(3)
            
            with col_bridge_btn:
                if st.button("🚀 Send to Audio & Export Engine", type="primary", use_container_width=True, key="cs_open_export_engine"):
                    st.session_state["sia_slide_contents"] = slides
                    st.session_state["visual_brief"] = {
                        "asset_mode": "carousel_studio",
                        "design_style": style_theme,
                        "palette": [bg_color, tag_color, text_color],
                        "typography": "Modern Professional"
                    }
                    st.success("Deck sent to Export Engine! Switch to Tool #5 in the dropdown above to add your audio track.")

            with col_zip_btn:
                if st.button("📦 Download Images (.zip)", type="primary", use_container_width=True, key="cs_gen_zip_imgs"):
                    # (Keep existing zip generation logic as-is)