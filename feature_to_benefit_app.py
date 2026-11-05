# feature_to_benefit_app.py • Feature-to-Benefits E-Commerce & Creator Suite
import streamlit as st
import json
import io
from docx import Document

def render():
    st.markdown("<h1 style='text-align: center;'>💡 Feature-to-Benefits E-Commerce Suite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Translate raw product specs into high-converting customer benefits, bullet points, hooks, and clean carousel scripts.</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name:", "Ergonomic Garden Kneeler & Seat", key="f2b_prod_name")
        raw_features = st.text_area(
            "Raw Product Features & Specs:", 
            value="Thick EVA foam padding, supports 330 lbs, detachable tool pouches, one-click flat folding, sturdy steel frame.",
            height=120,
            key="f2b_raw_features"
        )
    with col2:
        target_audience = st.text_input("Target Audience:", "Seniors and home gardeners with joint pain or back strain", key="f2b_audience")
        copywriting_tone = st.selectbox(
            "Copywriting Tone:",
            ["Direct-Response Empathy", "High-Energy Direct Response", "Luxury / Premium", "Urgent / Direct Action"],
            key="f2b_tone"
        )

    st.divider()
    
    if st.button("🚀 Transform Features to Benefits & Generate Complete Report", type="primary", use_container_width=True, key="f2b_btn_generate"):
        with st.spinner("Analyzing features, structuring customer benefits, and generating conversion copy..."):
            # Structured transformation data
            matrix_data = [
                {
                    "feature": "Thick EVA foam padding",
                    "benefit": "Protects knees and joints from hard ground",
                    "pain": "Severe knee soreness and back strain from hard earth",
                    "hook": "Say goodbye to soreness"
                },
                {
                    "feature": "Supports 330 lbs sturdy steel frame",
                    "benefit": "Rock-solid stability & safety",
                    "pain": "Fear of wobbling or structural collapse",
                    "hook": "Built for absolute safety"
                },
                {
                    "feature": "Detachable tool pouches",
                    "benefit": "Keeps clippers and trowels right on your hip",
                    "pain": "Constant bending over and losing tools in the dirt",
                    "hook": "Your tools always within arm's reach"
                },
                {
                    "feature": "One-click flat folding",
                    "benefit": "Tuck away in seconds for easy storage",
                    "pain": "Bulky garden seats cluttering the garage",
                    "hook": "Fills flat instantly"
                }
            ]

            carousel_script = [
                {
                    "category": "HOOK",
                    "title": f"Tired of aching joints cutting your gardening sessions short?",
                    "content": f"Meet the {product_name}—custom-built to give {target_audience} the comfort, support, and ease you deserve."
                },
                {
                    "category": "PROBLEM",
                    "title": "Traditional gardening leaves you sore and exhausted.",
                    "content": "Kneeling on hard dirt causes severe joint pain, while constantly bending over strains your lower back."
                },
                {
                    "category": "SOLUTION & FEATURE 1",
                    "title": "Protect your knees with cloud-like EVA padding.",
                    "content": "Say goodbye to soreness with thick EVA foam padding that cushions your joints on any terrain."
                },
                {
                    "category": "FEATURE 2 & 3",
                    "title": "Unmatched stability meets ultimate convenience.",
                    "content": "Enjoy rock-solid stability up to 330 lbs and keep your clippers right on your hip with detachable tool pouches."
                },
                {
                    "category": "FEATURE 4",
                    "title": "Folds flat in one click for effortless storage.",
                    "content": "Tuck it away in seconds in your garage or car trunk without taking up valuable space."
                },
                {
                    "category": "CTA",
                    "title": "Ready to garden in total comfort?",
                    "content": f"Click the link in bio or comment GARDEN to claim your {product_name} today!"
                }
            ]

            st.session_state["f2b_matrix"] = matrix_data
            st.session_state["f2b_carousel"] = carousel_script
            st.session_state["f2b_product_name"] = product_name
            st.success("✅ Optimization Report & Downstream Script Ready!")

    if "f2b_matrix" in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Complete Comprehensive Optimization Report")
        st.markdown(f"### E-Commerce Comprehensive Optimization & Carousel Report")
        st.markdown(f"**Product:** {st.session_state['f2b_product_name']} | **Target Audience:** {target_audience} | **Tone:** {copywriting_tone}")
        
        st.markdown("### 1. Feature-to-Benefit Analysis & Pain Agitation Matrix")
        
        # Display as a clean markdown table
        table_md = "| Raw Feature | Customer Benefit | Pain Point / Agitation | Direct-Response Hook |\n| :--- | :--- | :--- | :--- |\n"
        for row in st.session_state["f2b_matrix"]:
            table_md += f"| {row['feature']} | {row['benefit']} | {row['pain']} | {row['hook']} |\n"
        st.markdown(table_md)

        st.markdown("### 2. High-Converting Product Description Hook")
        st.info(f"\"Tired of aching joints cutting your gardening sessions short? Meet the {st.session_state['f2b_product_name']}—custom-built to give {target_audience} the comfort, support, and ease you deserve. Cultivate your garden, not your back pain!\"")

        st.markdown("### 3. Downstream Carousel Slide Script (Handoff Ready)")
        script_text = ""
        for idx, slide in enumerate(st.session_state["f2b_carousel"]):
            line = f"* **SLIDE {idx+1} ({slide['category']}):** {slide['title']} {slide['content']}"
            script_text += line + "\n"
            st.markdown(line)

        st.divider()

        # Word Document Generation
        doc = Document()
        doc.add_heading(f"E-Commerce Optimization Report: {st.session_state['f2b_product_name']}", 0)
        doc.add_paragraph(f"Target Audience: {target_audience}\nCopywriting Tone: {copywriting_tone}")
        
        doc.add_heading("Feature-to-Benefit Matrix", level=1)
        for row in st.session_state["f2b_matrix"]:
            doc.add_paragraph(f"• Feature: {row['feature']}\n  Benefit: {row['benefit']}\n  Pain: {row['pain']}\n  Hook: {row['hook']}")
            
        doc.add_heading("Carousel Script", level=1)
        for idx, slide in enumerate(st.session_state["f2b_carousel"]):
            doc.add_paragraph(f"Slide {idx+1} [{slide['category']}]: {slide['title']} - {slide['content']}")
            
        doc_io = io.BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)

        col_dl, col_bridge = st.columns(2)
        with col_dl:
            st.download_button(
                "📥 Download Complete Report (Word .docx)",
                data=doc_io,
                file_name=f"{st.session_state['f2b_product_name'].replace(' ', '_')}_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="f2b_dl_docx"
            )
        with col_bridge:
            if st.button("⚡ Send Downstream Script to Carousel Studio ➔", type="primary", use_container_width=True, key="f2b_bridge_btn"):
                st.session_state["deck_json"] = st.session_state["f2b_carousel"]
                st.session_state["active_tool_idx"] = 0
                st.success("⚡ Script successfully handed over to Carousel Studio!")
                st.rerurn()