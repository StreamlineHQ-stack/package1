with col_bridge_btn:
    if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="cs_open_local_kinetic"):
        st.session_state["slides_data"] = slides
        st.session_state["active_view"] = "kinetic_ui"
        st.rerun()