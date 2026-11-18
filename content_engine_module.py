# content_engine_module.py • Direct-Response Ideation & Full Framework Library Hub
import streamlit as st
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

try:
    from templates.november import NOVEMBER_FRAMEWORK_LIBRARY
except Exception:
    NOVEMBER_FRAMEWORK_LIBRARY = {}

def render_content_engine():
    st.markdown("<h1 style='text-align: center;'>🧠 Content Engine (Step 1)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Direct-Response Ideation • 100-Framework Proprietary USP Library & Downstream Hub</p>", unsafe_allow_html=True)
    st.divider()

    # Merge core framework library with any seasonal/vault additions
    active_library = FRAMEWORK_LIBRARY.copy()
    if NOVEMBER_FRAMEWORK_LIBRARY:
        active_library.update(NOVEMBER_FRAMEWORK_LIBRARY)

    with st.container(border=True):
        st.markdown("### ⚙️ Configure Proprietary Frameworks & Custom Angles")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            selected_pillar = st.selectbox(
                "Select Content Pillar (USP Library):",
                list(active_library.keys())
            )
        with col_f2:
            templates_in_pillar = active_library[selected_pillar]
            selected_template_name = st.selectbox(
                "Select Direct-Response Blueprint (1-100):",
                list(templates_in_pillar.keys())
            )

        # Pull default blueprint data
        blueprint_data = templates_in_pillar[selected_template_name]

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            core_hook = st.text_input("Core Hook / Headline Idea:", value=blueprint_data["hook"])
            target_audience = st.text_input("Target Audience:", value="Fitness and marketing coaches scaling to $10k/mo.")
        with col_h2:
            custom_notes = st.text_area(
                "Custom Notes & Specific Angles:", 
                value=f"Problem: {blueprint_data['problem']} | Solution: {blueprint_data['solution']} | CTA: {blueprint_data['cta']}", 
                height=106
            )

        slide_count = st.slider("Target Slide Count:", min_value=3, max_value=8, value=6)

        if st.button("🚀 Generate Structured Deck Content via Framework", type="primary", use_container_width=True):
            with st.spinner("Synthesizing direct-response deck from proprietary framework library..."):
                raw_prompt = f"Pillar: {selected_pillar}\nTemplate: {selected_template_name}\nHook: {core_hook}\nProblem: {blueprint_data['problem']}\nSolution: {blueprint_data['solution']}\nCTA: {blueprint_data['cta']}\nNotes: {custom_notes}"
                res, status_msg = generate_carousel_deck(raw_prompt, slide_count=slide_count, mode="framework")
                
                # Save into session state for downstream handoffs
                st.session_state["deck_json"] = res
                st.session_state["engine_status"] = status_msg
                st.success("✅ Structured deck generated successfully from proprietary framework! Ready for downstream handoff.")

    # --- DOWNSTREAM HANDOFF ACTIONS ---
    if "deck_json" in st.session_state and st.session_state["deck_json"]:
        st.divider()
        st.markdown("### 🔄 Downstream Handoff & Distribution")
        
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            if st.button("🎨 Send to Carousel Studio ➔", type="primary", use_container_width=True):
                st.session_state["active_tool_idx"] = 1  # Index for Carousel Studio
                st.rerun()
        with col_d2:
            if st.button("✨ Send to Style Inspiration ➔", use_container_width=True):
                st.session_state["sia_downstage_payload"] = st.session_state["deck_json"]
                st.session_state["active_tool_idx"] = 3  # Index for SIA
                st.rerun()
        with col_d3:
            if st.button("🎬 Send to Unified Export ➔", use_container_width=True):
                st.session_state["active_tool_idx"] = 6  # Index for Unified Export
                st.rerun()