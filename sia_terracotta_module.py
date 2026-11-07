# sia_terracotta_module.py • Vision-Powered Dynamic Swipe Theme Module
import streamlit as st
import textwrap
from sia_vision_parser import deconstruct_uploaded_swipe

def build_terracotta_deck(deck):
    uploaded_files = st.session_state.get("sia_uploaded_files", None)
    report = deconstruct_uploaded_swipe(uploaded_files[0]) if uploaded_files else {
        "bg_color": "#b0543c",
        "text_color": "#ffffff",
        "sub_color": "#f3f4f6",
        "font_family": "sans-serif"
    }
    
    bg_color = report["bg_color"]
    text_color = report["text_color"]
    sub_color = report["sub_color"]
    font_family = report["font_family"]
    
    styled = []
    total = len(deck)
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", "SLIDE " + str(idx+1))).upper()
        title = str(slide.get("title", "Slide " + str(idx+1)))
        content = str(slide.get("content", ""))
        
        html = textwrap.dedent(f"""
        <div style="background-color: {bg_color}; padding: 48px 36px; border-radius: 16px; max-width: 580px; margin: 0 auto; font-family: {font_family}; color: {text_color}; box-shadow: 0 30px 60px -15px rgba(0,0,0,0.3); border: 1px solid rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="color: #b0543c; font-size: 11px; font-weight: 800; letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase;">
                    {cat} • {idx+1}/{total}
                </div>
                <h1 style="color: {text_color}; font-size: 26px; font-weight: 700; line-height: 1.3; margin: 0; font-family: {font_family};">
                    {title}
                </h1>
            </div>
            <div style="text-align: center; margin-bottom: 30px; padding: 0 16px;">
                <p style="color: {sub_color}; font-size: 15px; line-height: 1.6; margin: 0; font-weight: 400; font-family: sans-serif;">
                    {content}
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; color: {sub_color}; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(0,0,0,0.15); padding-top: 16px; text-transform: uppercase;">
                <div>OCT 8 • 2026</div>
                <div>NIKKI'S SALON</div>
            </div>
        </div>
        """).strip()
        
        styled.append({
            "category": cat,
            "title": title,
            "content": content,
            "rendered_html": html
        })
    return styled
