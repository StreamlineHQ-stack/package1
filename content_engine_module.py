# content_engine_module.py • Dedicated Content Ideation & Framework Generator
import streamlit as st

def render_content_engine():
    st.markdown("<h1 style='text-align: center;'>✍️ Content Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Direct-Response Ideation, Frameworks & Upstream/Downstream Hub</p>", unsafe_allow_html=True)
    st.divider()

    # --- 1. CATCH UPSTREAM PAYLOAD FROM FEATURE-TO-BENEFITS (IF ANY) ---
    if "f2b_payload" in st.session_state and st.session_state["f2b_payload"]:
        st.info(f"📥 **Upstream Payload Received from Feature-to-Benefits:**\n\n_{st.session_state['f2b_payload']}_")
        if st.button("✨ Load Upstream Payload into Hook & Notes"):
            st.session_state["default_hook"] = f"How to leverage: {st.session_state['f2b_payload'][:50]}..."
            st.session_state["default_notes"] = f"Derived from Feature-to-Benefits analysis: {st.session_state['f2b_payload']}"
            del st.session_state["f2b_payload"]
            st.rerun()

    # --- 2. CONFIGURATION & FRAMEWORKS ---
    st.markdown("### ⚙️ Configure Frameworks & Custom Angles")
    
    default_hook_val = st.session_state.get("default_hook", "Stop trading time for pennies. Build systems that scale.")
    default_notes_val = st.session_state.get("default_notes", "Emphasize leverage, micro-SaaS automation, and escaping manual client delivery.")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        copy_framework = st.selectbox(
            "Select Copywriting Framework:",
            ["Problem-Agitate-Solve (PAS)", "AIDA (Attention, Interest, Desire, Action)", "Before-After-Bridge (BAB)", "Direct Value Breakdown"]
        )
        core_hook = st.text_input("Core Hook / Headline Idea:", value=default_hook_val)
        target_audience = st.text_input("Target Audience:", value="Fitness and marketing coaches making $5k-$10k/mo.")

    with col_c2:
        slide_count = st.slider("Target Slide Count:", 3, 10, 4)
        custom_notes = st.text_area(
            "📝 Custom Notes & Specific Angles:",
            value=default_notes_val,
            height=110
        )
    
    if st.button("🚀 Generate Structured Deck Content", type="primary", use_container_width=True):
        generated_slides = [
            {"title": core_hook, "body": f"Framework: {copy_framework}\nTarget: {target_audience}\n\nLet's break down why your current workflow is leaking time."},
            {"title": "The Core Bottleneck & Notes", "body": f"Notes applied: {custom_notes[:140]}...\n\nWhen you rely purely on manual delivery, your revenue is capped by your personal hours."},
            {"title": "The High-Leverage Solution", "body": "1. Package your expertise into automated micro-assets\n2. Deploy repeatable systems\n3. Scale your digital footprint effortlessly."},
            {"title": "Your Next Step", "body": "Deploy this exact structure into your creator suite and start scaling today."}
        ]
        st.session_state["sia_slide_contents"] = generated_slides[:slide_count]
        st.success("✅ Content Engine generated deck successfully!")

    # --- 3. PREVIEW & DOWNSTREAM ROUTING ---
    if "sia_slide_contents" in st.session_state and st.session_state["sia_slide_contents"]:
        st.divider()
        st.markdown("### 👁️ Generated Content Preview & Downstream Handoff")
        
        for i, slide in enumerate(st.session_state["sia_slide_contents"]):
            with st.expander(f"Slide {i+1}: {slide['title'][:40]}..."):
                st.markdown(f"**Title:** {slide['title']}")
                st.markdown(f"**Body:** {slide['body']}")

        st.markdown("---")
        st.markdown("### 🔄 Downstream Pipeline Routing")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🚀 Send to Carousel Studio", type="primary", use_container_width=True):
                st.session_state["active_tool_idx"] = 1  # Jump to Carousel Studio
                st.success("✅ Synced with Carousel Studio!")
                st.rerun()
        with col_r2:
            if st.button("✨ Send to Style Inspiration (SIA)", type="secondary", use_container_width=True):
                st.session_state["active_tool_idx"] = 2  # Jump to SIA
                st.success("✅ Synced with SIA!")
                st.rerun()