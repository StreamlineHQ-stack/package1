st.divider()
        st.markdown("### 📥 Export Options & Kinetic Handoff")
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="sia_kinetic_bridge_btn"):
                st.session_state["slides_data"] = slides
                st.session_state["deck_json"] = slides
                st.session_state["active_view"] = "kinetic_ui"
                st.rerun()

        with exp_col2:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, s in enumerate(slides):
                    # Generate real PNG image bytes for each slide card
                    png_bytes = render_carousel_slide_to_image(
                        slide_data=s,
                        slide_num=idx + 1,
                        total_slides=len(slides),
                        bg_color="#0b0f19",
                        text_color="#ffffff",
                        body_color="#d1d5db",
                        tag_color="#34d399"
                    )
                    zip_file.writestr(f"carousel_slide_{idx+1}.png", png_bytes)
            zip_buffer.seek(0)
            
            st.download_button(
                label="📦 Download Carousel (.zip)",
                data=zip_buffer,
                file_name="carousel_deck_images.zip",
                mime="application/zip",
                use_container_width=True,
                key="sia_download_zip_archive"
            )

        with exp_col3:
            if st.button("🔄 Edit Content Again", key="sia_restart_btn", use_container_width=True):
                st.session_state["sia_workflow_step"] = "step1_content"
                st.rerun()