# sia_terracotta_module.py • Dynamic Swipe Background Module
import streamlit as st
import textwrap
from PIL import Image
import io

def get_upload_dominant_color():
    uploaded_files = st.session_state.get("sia_uploaded_files", None)
    if uploaded_files:
        try:
            img = Image.open(io.BytesIO(uploaded_files[0].getvalue())).convert("RGB")
            img_small = img.resize((30, 30))
            colors = img_small.getcolors(30 * 30)
            if colors:
                colors.sort(key=lambda x: x[0], reverse=True)
                for _, col in colors:
                    r, g, b = col
                    if not (r < 20 and g < 20 and b < 20) and not (r > 235 and g > 235 and b > 235):
                        return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            pass
    return "#334151"  # Default moody slate if no upload

def build_terracotta_deck(deck):
    bg_color = get_upload_dominant_color()
    styled = []
    total = len(deck)
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", "SLIDE " + str(idx+1))).upper()
        title = str(slide.get("title", "Slide " + str(idx+1)))
        content = str(slide.get("content", ""))
        
        html = textwrap.dedent(f"""
        <div style="background-color: {bg_color}; padding: 48px 36px; border-radius: 16px; max-width: 580px; margin: 0 auto; font-family: sans-serif; color: #ffffff; box-shadow: 0 30px 60px -15px rgba(0,0,0,0.6);">
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="color: #ffcc00; font-size: 11px; font-weight: 800; letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase;">
                    {cat} • {idx+1}/{total}
                </div>
                <h1 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin: 0;">
                    {title}
                </h1>
            </div>
            <div style="text-align: center; margin-bottom: 30px; padding: 0 16px;">
                <p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; margin: 0; font-weight: 400;">
                    {content}
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; color: #cbd5e1; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 16px; text-transform: uppercase;">
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
