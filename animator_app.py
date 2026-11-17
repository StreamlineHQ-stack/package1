st.markdown("#### 📥 Download Package")
        if "last_rendered_gif" in st.session_state:
            st.download_button(
                label="⬇️ Download Animated GIF",
                data=st.session_state["last_rendered_gif"],
                file_name="kinetic_carousel_loop.gif",
                mime="application/gif",
                use_container_width=True,
            )
        st.download_button(
            label="🎬 Download Instagram MP4",
            data=mp4_bytes,
            file_name="kinetic_carousel_loop.mp4",
            mime="video/mp4",
            use_container_width=True,
        )
        
        # --- HANDOFF BRIDGE TO UNIFIED EXPORT ENGINE ---
        st.markdown("---")
        if st.button("🚀 Send Active Deck to Audio & Export Engine", use_container_width=True, key="animator_send_to_export"):
            st.session_state["sia_slide_contents"] = st.session_state.get("slides_data", [])
            st.session_state["visual_brief"] = {
                "asset_mode": "kinetic_studio",
                "design_style": "Kinetic Dark Pro Loop",
                "palette": ["#0e1117", "#ffcc00", "#ffffff"],
                "typography": "Modern Kinetic"
            >
            st.success("Deck synced successfully! Head over to your Platform Hub and select Tool #5 to mix your audio track.")