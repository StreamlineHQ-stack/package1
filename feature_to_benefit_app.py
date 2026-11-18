# When Feature-to-Benefits generates results...
    st.markdown("### 📥 Downstream Platform Handoff")
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        if st.button("🚀 Push to Carousel Studio", type="primary", use_container_width=True):
            # Convert generated features/benefits into standard slide structure
            st.session_state["sia_slide_contents"] = [
                {"title": "Feature Breakthrough", "body": result_summary_text}
            ]
            st.session_state["active_tool_idx"] = 0  # Jump to Carousel Studio
            st.success("✅ Synced with Carousel Studio!")
            st.rerun()
            
    with col_h2:
        if st.button("✨ Push to Style Inspiration (SIA)", type="secondary", use_container_width=True):
            st.session_state["sia_slide_contents"] = [
                {"title": "SIA Brief", "body": result_summary_text}
            ]
            st.session_state["active_tool_idx"] = 2  # Jump to SIA
            st.success("✅ Synced with SIA!")
            st.rerun()