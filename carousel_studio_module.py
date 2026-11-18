import streamlit as st

def render_carousel_studio():
    st.markdown("<h1 style='text-align: center;'>🎨 Carousel Engine Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Direct-Response Content Engine & Slide Workspace</p>", unsafe_allow_html=True)
    st.divider()

    # --- 1. CONTENT ENGINE INITIALIZATION & INPUTS ---
    st.markdown("### ✍️ Step 1: Content Engine Core")
    
    with st.expander("⚙️ Configure Raw Content & Hook Parameters", expanded=not bool(st.session_state.get("sia_slide_contents"))):
        core_hook = st.text_input("Core Hook / Headline Idea:", value="Stop trading time for pennies. Build systems that scale.")
        core_target = st.text_input("Target Audience:", value="Fitness and marketing coaches making $5k-$10k/mo.")
        slide_count = st.slider("Number of Slides:", 3, 10, 4)
        
        if st.button("🚀 Generate Structured Deck Content", type="primary", use_container_width=True):
            # Generate programmatic structure based on inputs
            generated_slides = [
                {"title": core_hook, "body": f"Designed specifically for {core_target}. Read closely."},
                {"title": "The Core Bottleneck", "body": "Most creators rely 100% on manual execution. When you stop working, revenue stops."},
                {"title": "The High-Leverage Solution", "body": "1. Package your expertise into micro-assets\n2. Automate distribution\n3. Build predictable funnels."},
                {"title": "Your Next Action", "body": "Deploy this framework today and scale your output."}
            ]
            st.session_state["sia_slide_contents"] = generated_slides[:slide_count]
            st.success("✅ Content Engine generated deck successfully!")
            st.rerun()

    st.divider()

    # --- 2. SLIDE REVIEW & VISUAL WORKSPACE ---
    st.markdown("### 👁️ Step 2: Slide Review & Editing Window")
    
    if "sia_slide_contents" not in st.session_state or not st.session_state["sia_slide_contents"]:
        st.info("ℹ️ Generate content above or send a payload from Feature-to-Benefits to populate your slides.")
        return

    slides = st.session_state["sia_slide_contents"]
    
    selected_slide_idx = st.selectbox("Select Slide to Inspect:", range(len(slides)), format_func=lambda i: f"Slide {i+1}: {slides[i]['title'][:30]}...")
    current_slide = slides[selected_slide_idx]
    
    col_prev, col_edit = st.columns([1.2, 1])
    
    with col_prev:
        st.markdown(f"""
        <div style="background-color: #121218; border: 2px solid #ff4b4b; border-radius: 12px; padding: 30px; min-height: 320px; color: #ffffff;">
            <p style="color: #ff4b4b; font-weight: bold; font-size: 14px;">SLIDE {selected_slide_idx + 1} OF {len(slides)}</p>
            <h2 style="color: #ffffff; margin-top: 10px; font-size: 22px;">{current_slide['title']}</h2>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
            <p style="color: #d0d0d0; font-size: 15px; line-height: 1.5; white-space: pre-wrap;">{current_slide['body']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_edit:
        st.markdown("#### ✏️ Quick Edit Slide")
        new_title = st.text_input("Slide Title", value=current_slide['title'], key=f"ce_title_{selected_slide_idx}")
        new_body = st.text_area("Slide Body", value=current_slide['body'], height=130, key=f"ce_body_{selected_slide_idx}")
        
        if st.button("💾 Save Slide Changes", use_container_width=True):
            slides[selected_slide_idx]['title'] = new_title
            slides[selected_slide_idx]['body'] = new_body
            st.session_state["sia_slide_contents"] = slides
            st.success("✅ Saved!")
            st.rerun()

    st.divider()
    
    # --- 3. PIPELINE DATA BRIDGE ---
    st.markdown("### 🔄 Downstream Handoff")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🚀 Send to Kinetic Animator", type="primary", use_container_width=True):
            st.session_state["bridge_active_tool"] = "Kinetic Animator"
            st.success("✅ Handed off to Kinetic Animator!")
            st.rerun()
    with col_b2:
        if st.button("🎵 Send to Audio & Assembler", type="secondary", use_container_width=True):
            st.session_state["bridge_active_tool"] = "Audio & Assembler"
            st.success("✅ Handed off to Assembler!")
            st.rerun()