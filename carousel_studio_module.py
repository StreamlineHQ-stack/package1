import streamlit as st

def render_carousel_studio():
    st.markdown("<h1 style='text-align: center;'>🎨 Carousel Engine Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Generate high-converting direct-response carousels and slide decks.</p>", unsafe_allow_html=True)
    st.divider()

    # --- SESSION STATE INITIALIZATION ---
    if "sia_slide_contents" not in st.session_state:
        st.session_state["sia_slide_contents"] = [
            {"title": "24 Hours in a Day... Are You Using Yours Wisely?", "body": "Did you know the average person spends 3 hours a day scrolling on their phone? Imagine what you could achieve with that time. Time is your most valuable asset—let's learn how to make it work for you!"},
            {"title": "The Time Trap: Why You’re Always Busy But Never Productive", "body": "Feeling overwhelmed? You're not alone. Poor time management leads to missed deadlines, stress, and burnout. It's not about making more time—it's about making the most of the time you have."},
            {"title": "The 3 Pillars of High-Leverage Focus", "body": "1. Eliminate distractions\n2. Batch your administrative tasks\n3. Protect your deep-work hours like your business depends on it (because it does)."},
            {"title": "Ready to Transform Your Workflow?", "body": "Stop trading hours for pennies. Build high-leverage digital assets that work for you 24/7."}
        ]

    # --- VISUAL STYLE SELECTION SIDEBAR / SECTION ---
    st.sidebar.markdown("### 🎨 Visual Layout Styles")
    styling_mode = st.sidebar.radio("Select Styling Mode:", ["November Content Vault (Active)", "Standard Preset Themes", "Custom Brand Hex"])
    
    if styling_mode == "November Content Vault (Active)":
        st.sidebar.success("🍁 November Fall Pack Active!")
        bg_color, accent_color, font_color = "#121218", "#ff4b4b", "#ffffff"
    else:
        bg_color, accent_color, font_color = "#0e1117", "#ffcc00", "#ffffff"

    st.markdown("### 📝 Slide Content & Preview Workspace")
    
    slides = st.session_state["sia_slide_contents"]
    
    # Slide selector for editing
    selected_slide_idx = st.selectbox("Select Slide to Inspect/Edit:", range(len(slides)), format_func=lambda i: f"Slide {i+1}: {slides[i]['title'][:30]}...")
    
    current_slide = slides[selected_slide_idx]
    
    col_prev, col_edit = st.columns([1.2, 1])
    
    with col_prev:
        st.markdown(f"""
        <div style="background-color: {bg_color}; border: 2px solid {accent_color}; border-radius: 12px; padding: 30px; min-height: 320px; color: {font_color}; box-shadow: 0px 4px 20px rgba(0,0,0,0.5);">
            <p style="color: {accent_color}; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Slide {selected_slide_idx + 1} of {len(slides)}</p>
            <h2 style="color: {font_color}; margin-top: 10px; font-size: 24px;">{current_slide['title']}</h2>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
            <p style="color: #d0d0d0; font-size: 16px; line-height: 1.5; white-space: pre-wrap;">{current_slide['body']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_edit:
        st.markdown("#### ✏️ Quick Edit Slide Content")
        new_title = st.text_input("Slide Title", value=current_slide['title'], key=f"edit_title_{selected_slide_idx}")
        new_body = st.text_area("Slide Body Content", value=current_slide['body'], height=140, key=f"edit_body_{selected_slide_idx}")
        
        if st.button("💾 Save Slide Changes", use_container_width=True):
            slides[selected_slide_idx]['title'] = new_title
            slides[selected_slide_idx]['body'] = new_body
            st.session_state["sia_slide_contents"] = slides
            st.success("✅ Slide updated successfully!")
            st.rerun()

    st.divider()
    
    # --- SEQUENTIAL PIPELINE DATA BRIDGE ---
    st.markdown("### 🔄 Pipeline Data Bridge & Export")
    st.markdown("Once your static deck is finalized, send it down the pipeline to render motion or export.")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        if st.button("🚀 1. Send to Kinetic Animator", type="primary", use_container_width=True, key="bridge_to_kinetic_btn"):
            st.session_state["bridge_active_tool"] = "Kinetic Animator"
            st.success("✅ Handed off to Kinetic Animation Engine!")
            st.rerun()
            
    with col_b2:
        if st.button("🎵 2. Send to Audio & Assembler", type="secondary", use_container_width=True, key="bridge_to_audio_btn"):
            st.session_state["bridge_active_tool"] = "Audio & Assembler"
            st.success("✅ Handed off to Audio & Unified Export Engine!")
            st.rerun()
            
    with col_b3:
        if st.button("📥 Download Static Assets (.zip)", type="secondary", use_container_width=True, key="download_static_btn"):
            st.info("📦 Static asset bundle generated for download.")