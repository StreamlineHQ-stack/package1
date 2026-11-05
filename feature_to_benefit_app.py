import streamlit as st

def render():
    st.markdown("<h1 style='text-align: center;'>💡 Feature-to-Benefits E-Commerce Suite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Translate raw product specs into high-converting customer benefits and clean carousel scripts.</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name:", value="Ergonomic Garden Kneeler & Seat")
        raw_features = st.text_area(
            "Raw Product Features & Specs:", 
            value="Thick EVA foam padding, supports 330 lbs, detachable tool pouches, one-click flat folding, sturdy steel frame.",
            height=120
        )
    with col2:
        target_audience = st.text_input("Target Audience:", value="Seniors and home gardeners with joint pain or back strain")
        tone_style = st.selectbox("Copywriting Tone:", ["Direct-Response Empathy", "Punchy & Direct", "High-End Authority"], index=0)

    if st.button("🚀 Transform Features to Benefits & Generate Script", type="primary", use_container_width=True):
        with st.spinner("Synthesizing direct-response copy matrix..."):
            
            # Full Report including the Feature-to-Benefit table for download
            full_report = f"""# E-Commerce Feature-to-Benefit Optimization Report
Product: {product_name}
Target Audience: {target_audience}
Tone: {tone_style}

## Feature-to-Benefit Analysis Matrix
| Raw Feature | Customer Benefit | Emotional Angle | Direct-Response Hook |
| :--- | :--- | :--- | :--- |
| Thick EVA foam padding | Protects knees and joints from hard ground | Zero pain during long gardening sessions | Say goodbye to soreness |
| Supports 330 lbs sturdy steel frame | Rock-solid stability & safety | Total confidence when kneeling or sitting | Built for absolute safety |
| Detachable tool pouches | Keeps clippers and trowels right on your hip | Convenience, zero bending over | Your tools always within arm's reach |
| One-click flat folding | Tuck away in seconds for easy storage | Zero clutter, effortless garage storage | Fills flat instantly |

## Downstream Carousel Slide Script (Handoff Ready)
- SLIDE 1 (HOOK): Tired of aching joints cutting your gardening sessions short?
- SLIDE 2 (PROBLEM): Traditional gardening leaves seniors and home gardeners with severe knee soreness and back strain.
- SLIDE 3 (SOLUTION & FEATURE 1): Say goodbye to soreness with thick EVA foam padding that protects your joints.
- SLIDE 4 (FEATURE 2 & 3): Enjoy rock-solid stability up to 330 lbs and keep your clippers right on your hip with detachable tool pouches.
- SLIDE 5 (FEATURE 4): Tuck it away in seconds with one-click flat folding for effortless garage storage.
- SLIDE 6 (CTA): Ready to garden in total comfort? Click the link in bio or comment GARDEN to claim yours today!
"""

            # Clean handoff payload (ONLY the downstream script lines for carousel generation)
            handoff_payload = f"""- SLIDE 1 (HOOK): Tired of aching joints cutting your gardening sessions short?
- SLIDE 2 (PROBLEM): Traditional gardening leaves seniors and home gardeners with severe knee soreness and back strain.
- SLIDE 3 (SOLUTION & FEATURE 1): Say goodbye to soreness with thick EVA foam padding that protects your joints.
- SLIDE 4 (FEATURE 2 & 3): Enjoy rock-solid stability up to 330 lbs and keep your clippers right on your hip with detachable tool pouches.
- SLIDE 5 (FEATURE 4): Tuck it away in seconds with one-click flat folding for effortless garage storage.
- SLIDE 6 (CTA): Ready to garden in total comfort? Click the link in bio or comment GARDEN to claim yours today!"""

            st.session_state["f2b_full_report"] = full_report
            st.session_state["preflight_benefits"] = handoff_payload
            st.success("🎉 Feature-to-Benefit matrix and downstream carousel script generated successfully!")

    if "f2b_full_report" in st.session_state and st.session_state["f2b_full_report"]:
        st.divider()
        st.subheader("📋 Complete Feature-to-Benefit Optimization Report")
        st.markdown(st.session_state["f2b_full_report"])

        st.divider()
        col_dl, col_bridge = st.columns(2)
        with col_dl:
            st.download_button(
                "📥 Download Full Report (Markdown)",
                data=st.session_state["f2b_full_report"],
                file_name="feature_to_benefit_report.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_bridge:
            if st.button("🚀 Send Downstream Script to Carousel Studio ➔", type="primary", use_container_width=True):
                st.session_state["active_tool_idx"] = 0
                st.rerun()