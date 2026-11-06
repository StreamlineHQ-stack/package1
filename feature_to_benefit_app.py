# feature_to_benefit_app.py • Feature-to-Benefits E-Commerce & Creator Suite
import streamlit as st
import io
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from app_engine import generate_carousel_deck

def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)

def generate_combined_docx(product_name, target_audience, tone_style):
    doc = Document()
    
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    PRIMARY_COLOR = RGBColor(33, 37, 41)
    SECONDARY_COLOR = RGBColor(168, 87, 50)
    TEXT_COLOR = RGBColor(70, 70, 70)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("E-Commerce Comprehensive Optimization & Carousel Report")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_COLOR

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(20)
    run_meta = p_meta.add_run(f"Product: {product_name}  |  Target Audience: {target_audience}  |  Tone: {tone_style}")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(10)
    run_meta.font.color.rgb = SECONDARY_COLOR

    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(12)
    p_h1.paragraph_format.space_after = Pt(8)
    r_h1 = p_h1.add_run("1. Feature-to-Benefit Analysis & Pain Agitation Matrix")
    r_h1.font.name = "Arial"
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    r_h1.font.color.rgb = PRIMARY_COLOR

    table_data = [
        ["Raw Feature", "Customer Benefit", "Pain Point / Agitation", "Direct-Response Hook"],
        ["Thick EVA foam padding", "Protects knees and joints from hard ground", "Severe knee soreness and back strain from hard earth", "Say goodbye to soreness"],
        ["Supports 330 lbs sturdy steel frame", "Rock-solid stability & safety", "Fear of wobbling or structural collapse", "Built for absolute safety"],
        ["Detachable tool pouches", "Keeps clippers and trowels right on your hip", "Constant bending over and losing tools in the dirt", "Your tools always within arm's reach"],
        ["One-click flat folding", "Tuck away in seconds for easy storage", "Bulky garden seats cluttering the garage", "Fills flat instantly"]
    ]

    table = doc.add_table(rows=len(table_data), cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    col_widths = [Inches(1.5), Inches(1.8), Inches(1.7), Inches(1.5)]

    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            cell.text = table_data[row_idx][col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(9.5)
                if row_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                    set_cell_background(cell, "212529")
                else:
                    run.font.color.rgb = TEXT_COLOR
                    if row_idx % 2 == 1:
                        set_cell_background(cell, "F8F9FA")
                    else:
                        set_cell_background(cell, "FFFFFF")

    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(20)
    p_h2.paragraph_format.space_after = Pt(8)
    r_h2 = p_h2.add_run("2. Optimized Listing Bullet Points")
    r_h2.font.name = "Arial"
    r_h2.font.size = Pt(14)
    r_h2.font.bold = True
    r_h2.font.color.rgb = PRIMARY_COLOR

    bullets = [
        ("Zero Joint Strain:", " Thick cushioning absorbs impact so you can garden longer without physical discomfort."),
        ("Durable Stability:", " Robust frame engineered for secure support and long-lasting seasonal use."),
        ("All-in-One Convenience:", " Built-in tool pouches keep your gear organized right where you need it."),
        ("Effortless Storage:", " Folds flat instantly, making it a breeze to pack up and store away.")
    ]
    for b_title, b_desc in bullets:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_after = Pt(3)
        p_b.paragraph_format.left_indent = Inches(0.2)
        r1 = p_b.add_run("• " + b_title)
        r1.font.name = "Arial"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = SECONDARY_COLOR
        r2 = p_b.add_run(b_desc)
        r2.font.name = "Arial"
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_COLOR

    p_h3 = doc.add_paragraph()
    p_h3.paragraph_format.space_before = Pt(20)
    p_h3.paragraph_format.space_after = Pt(8)
    r_h3 = p_h3.add_run("3. High-Converting Product Description Hook")
    r_h3.font.name = "Arial"
    r_h3.font.size = Pt(14)
    r_h3.font.bold = True
    r_h3.font.color.rgb = PRIMARY_COLOR

    p_hook = doc.add_paragraph()
    p_hook.paragraph_format.left_indent = Inches(0.2)
    p_hook.paragraph_format.space_after = Pt(12)
    r_hook = p_hook.add_run('"Tired of aching joints cutting your gardening sessions short? Meet the Ergonomic Garden Kneeler & Seat—custom-built to give home gardeners and seniors the comfort, support, and ease you deserve. Cultivate your garden, not your back pain!"')
    r_hook.font.name = "Arial"
    r_hook.font.size = Pt(10.5)
    r_hook.font.italic = True
    r_hook.font.color.rgb = TEXT_COLOR

    p_h4 = doc.add_paragraph()
    p_h4.paragraph_format.space_before = Pt(16)
    p_h4.paragraph_format.space_after = Pt(8)
    r_h4 = p_h4.add_run("4. Downstream Carousel Slide Script (Handoff Ready)")
    r_h4.font.name = "Arial"
    r_h4.font.size = Pt(14)
    r_h4.font.bold = True
    r_h4.font.color.rgb = PRIMARY_COLOR

    script_lines = [
        ("SLIDE 1 (HOOK):", " Tired of aching joints cutting your gardening sessions short?"),
        ("SLIDE 2 (PROBLEM):", " Traditional gardening leaves seniors and home gardeners with severe knee soreness and back strain."),
        ("SLIDE 3 (SOLUTION & FEATURE 1):", " Say goodbye to soreness with thick EVA foam padding that protects your joints."),
        ("SLIDE 4 (FEATURE 2 & 3):", " Enjoy rock-solid stability up to 330 lbs and keep your clippers right on your hip with detachable tool pouches."),
        ("SLIDE 5 (FEATURE 4):", " Tuck it away in seconds with one-click flat folding for effortless garage storage."),
        ("SLIDE 6 (CTA):", " Ready to garden in total comfort? Click the link in bio or comment GARDEN to claim yours today!")
    ]

    for prefix, body in script_lines:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_after = Pt(4)
        p_item.paragraph_format.left_indent = Inches(0.2)
        r_prefix = p_item.add_run(prefix)
        r_prefix.font.name = "Arial"
        r_prefix.font.size = Pt(10)
        r_prefix.font.bold = True
        r_prefix.font.color.rgb = SECONDARY_COLOR
        r_body = p_item.add_run(body)
        r_body.font.name = "Arial"
        r_body.font.size = Pt(10)
        r_body.font.color.rgb = TEXT_COLOR

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def render():
    st.markdown("<h1 style='text-align: center;'>💡 Feature-to-Benefits E-Commerce Suite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Translate raw product specs into high-converting customer benefits, bullet points, hooks, and clean carousel scripts.</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name:", value="Ergonomic Garden Kneeler & Seat", key="f2b_prod_name")
        raw_features = st.text_area(
            "Raw Product Features & Specs:", 
            value="Thick EVA foam padding, supports 330 lbs, detachable tool pouches, one-click flat folding, sturdy steel frame.",
            height=120,
            key="f2b_raw_features"
        )
    with col2:
        target_audience = st.text_input("Target Audience:", value="Seniors and home gardeners with joint pain or back strain", key="f2b_audience")
        tone_style = st.selectbox("Copywriting Tone:", ["Direct-Response Empathy", "Warm & Story-Driven", "Punchy & Direct"], index=0, key="f2b_tone")

    if st.button("🚀 Transform Features to Benefits & Generate Complete Report", type="primary", use_container_width=True, key="f2b_btn_gen"):
        with st.spinner("Synthesizing comprehensive e-commerce optimization matrix and Word document..."):
            
            full_report_md = f"""# E-Commerce Comprehensive Optimization & Carousel Report
Product: {product_name}
Target Audience: {target_audience}
Tone: {tone_style}

## 1. Feature-to-Benefit Analysis & Pain Agitation Matrix
| Raw Feature | Customer Benefit | Pain Point / Agitation | Direct-Response Hook |
| :--- | :--- | :--- | :--- |
| Thick EVA foam padding | Protects knees and joints from hard ground | Severe knee soreness and back strain from hard earth | Say goodbye to soreness |
| Supports 330 lbs sturdy steel frame | Rock-solid stability & safety | Fear of wobbling or structural collapse | Built for absolute safety |
| Detachable tool pouches | Keeps clippers and trowels right on your hip | Constant bending over and losing tools in the dirt | Your tools always within arm's reach |
| One-click flat folding | Tuck away in seconds for easy storage | Bulky garden seats cluttering the garage | Fills flat instantly |

## 2. Optimized Listing Bullet Points
- **Zero Joint Strain:** Thick cushioning absorbs impact so you can garden longer without physical discomfort.
- **Durable Stability:** Robust frame engineered for secure support and long-lasting seasonal use.
- **All-in-One Convenience:** Built-in tool pouches keep your gear organized right where you need it.
- **Effortless Storage:** Folds flat instantly, making it a breeze to pack up and store away.

## 3. High-Converting Product Description Hook
*"Tired of aching joints cutting your gardening sessions short? Meet the Ergonomic Garden Kneeler & Seat—custom-built to give home gardeners and seniors the comfort, support, and ease you deserve. Cultivate your garden, not your back pain!"*

## 4. Downstream Carousel Slide Script (Handoff Ready)
- SLIDE 1 (HOOK): Tired of aching joints cutting your gardening sessions short?
- SLIDE 2 (PROBLEM): Traditional gardening leaves seniors and home gardeners with severe knee soreness and back strain.
- SLIDE 3 (SOLUTION & FEATURE 1): Say goodbye to soreness with thick EVA foam padding that protects your joints.
- SLIDE 4 (FEATURE 2 & 3): Enjoy rock-solid stability up to 330 lbs and keep your clippers right on your hip with detachable tool pouches.
- SLIDE 5 (FEATURE 4): Tuck it away in seconds with one-click flat folding for effortless garage storage.
- SLIDE 6 (CTA): Ready to garden in total comfort? Click the link in bio or comment GARDEN to claim yours today!
"""

            carousel_script_json = [
                {
                    "category": "HOOK",
                    "title": "Tired of aching joints cutting your gardening sessions short?",
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

            docx_bytes = generate_combined_docx(product_name, target_audience, tone_style)

            st.session_state["f2b_full_report"] = full_report_md
            st.session_state["f2b_docx_bytes"] = docx_bytes
            st.session_state["f2b_carousel"] = carousel_script_json
            st.success("🎉 Comprehensive optimization report and Word document generated successfully!")

    if "f2b_full_report" in st.session_state and st.session_state["f2b_full_report"]:
        st.divider()
        st.subheader("📋 Complete Comprehensive Optimization Report")
        st.markdown(st.session_state["f2b_full_report"])

        st.divider()
        col_dl, col_bridge_car, col_bridge_sia = st.columns(3)
        with col_dl:
            st.download_button(
                "📥 Download Word (.docx)",
                data=st.session_state["f2b_docx_bytes"],
                file_name="ECommerce_Comprehensive_Optimization_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="f2b_dl_btn"
            )
        with col_bridge_car:
            if st.button("🚀 Send to Carousel Studio ➔", type="primary", use_container_width=True, key="f2b_bridge_btn"):
                if "f2b_carousel" in st.session_state:
                    st.session_state["deck_json"] = st.session_state["f2b_carousel"]
                else:
                    st.session_state["deck_json"] = [
                        {"category": "HOOK", "title": "Tired of aching joints?", "content": "Meet the Ergonomic Garden Kneeler."},
                        {"category": "PROBLEM", "title": "Traditional gardening causes pain.", "content": "Hard earth causes severe strain."},
                        {"category": "SOLUTION", "title": "Protect your knees with EVA padding.", "content": "Thick foam cushions joints."},
                        {"category": "STABILITY", "title": "Supports up to 330 lbs.", "content": "Rock-solid stability."},
                        {"category": "CONVENIENCE", "title": "Detachable tool pouches.", "content": "Keep gear on your hip."},
                        {"category": "CTA", "title": "Ready to garden in comfort?", "content": "Comment GARDEN today!"}
                    ]
                st.session_state["engine_status"] = "⚡ Direct Handoff Active"
                st.session_state["current_slide"] = 0
                st.session_state["active_tool_idx"] = 0
                st.success("⚡ Script successfully handed over to Carousel Studio!")
                try:
                    st.rerun()
                except AttributeError:
                    try:
                        st.experimental_rerun()
                    except Exception:
                        pass
        with col_bridge_sia:
            if st.button("✨ Send to Style Inspiration ➔", type="secondary", use_container_width=True, key="f2b_sia_bridge_btn"):
                if "f2b_carousel" in st.session_state:
                    st.session_state["sia_downstream_payload"] = st.session_state["f2b_carousel"]
                else:
                    st.session_state["sia_downstream_payload"] = product_name
                st.session_state["active_tool_idx"] = 2
                st.success("✨ Script handed over to Style Inspiration (SIA)!")
                try:
                    st.rerun()
                except AttributeError:
                    try:
                        st.experimental_rerun()
                    except Exception:
                        pass