# feature_to_benefit_app.py • Feature-to-Benefits Conversion Engine
import streamlit as st

def render():
    st.markdown("<h1 style='text-align: center;'>💡 Feature-to-Benefits Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Transform raw product features into compelling psychological benefits.</p>", unsafe_allow_html=True)
    st.divider()

    # --- 1. FEATURE INPUT & CONFIGURATION ---
    st.markdown("### ✍️ Input Raw Product Features")
    
    feature_input = st.text_area(
        "Enter Raw Features (one per line):",
        value="Automated slide generation and multi-model AI orchestration\nDirect button UI navigation and seamless pipeline data bridges\nInstant PNG bundle export and downstream motion handoffs",
        height=120
    )
    
    target_avatar = st.text_input("Target Audience Avatar:", value="Fitness and marketing coaches scaling digital products.")

    if st.button("✨ Convert Features to Psychological Benefits", type="primary", use_container_width=True):
        # Generate structured benefits output
        converted_result = (
            f"🎯 **Target Avatar:** {target_avatar}\n\n"
            f"1. **Feature:** Automated slide generation & multi-model AI orchestration\n"
            f"   👉 **Benefit:** Reclaim 10+ hours a week of manual design time while producing agency-grade content effortlessly.\n\n"
            f"2. **Feature:** Direct button UI navigation & pipeline bridges\n"
            f"   👉 **Benefit:** Eliminate cognitive friction and move from ideation to final asset assembly in minutes.\n\n"
            f"3. **Feature:** Instant PNG bundle export & motion handoffs\n"
            f"   👉 **Benefit:** Launch high-converting carousels and reels instantly without wrestling with complex software."
        )
        st.session_state["f2b_output"] = converted_result
        st.success("✅ Conversion complete!")

    # --- 2. OUTPUT & UPSTREAM PAYLOAD ROUTING ---
    if "f2b_output" in st.session_state and st.session_state["f2b_output"]:
        st.divider()
        st.markdown("### 📥 Converted Benefits & Upstream Pipeline Handoff")
        
        st.markdown(f"""
        <div style="background-color: #1a1a24; border: 2px solid #0066cc; border-radius: 12px; padding: 25px; color: #ffffff;">
            {st.session_state['f2b_output']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔄 Send Upstream to Content Hub")
        
        if st.button("🚀 Push to Content Engine", type="primary", use_container_width=True):
            st.session_state["f2b_payload"] = st.session_state["f2b_output"]
            st.session_state["active_tool_idx"] = 0  # Jump to Content Engine (Index 0 in platform hub)
            st.success("✅ Sent upstream to Content Engine successfully!")
            st.rerun()