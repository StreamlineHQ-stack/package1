st.markdown("### 🔄 Pipeline Data Bridge & Export")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        if st.button("🚀 1. Send to Kinetic Animator", type="primary", use_container_width=True):
            st.session_state["bridge_active_tool"] = "Kinetic Animator"
            st.success("✅ Handed off to Kinetic Animation Engine!")
            st.rerun()
            
    with col_b2:
        # Only enable once kinetic render or base state is ready, or keep as next sequential step
        if st.button("🎵 2. Send to Audio & Unified Assembler", type="secondary", use_container_width=True):
            st.session_state["bridge_active_tool"] = "Audio & Assembler"
            st.success("✅ Handed off to Audio & Unified Export Engine!")
            st.rerun()
            
    with col_b3:
        if st.button("📥 Download Static Assets (.zip)", type="secondary", use_container_width=True):
            # Static backup download
            pass