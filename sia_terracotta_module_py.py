# sia_terracotta_module.py • Dynamic Swipe Background & Deconstruction Module
import streamlit as st
import textwrap
from PIL import Image
import io

def analyze_swipe_image():
    uploaded_files = st.session_state.get("sia_uploaded_files", None)
    bg_color = "#f8fafc"
    text_color = "#111827"
    sub_color = "#374151"
    accent_color = "#b0543c"
    mood = "Light & Airy Editorial"
    
    if uploaded_files:
        try:
            img = Image.open(io.BytesIO(uploaded_files[0].getvalue())).convert("RGB")
            img_small = img.resize((40, 40))
            pixels = list(img_small.getdata())
            avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
            
            if avg_brightness > 130:
                bg_color = "#f8fafc"
                text_color = "#111827"
                sub_color = "#374151"
                accent_color = "#b0543c"
                mood = "Light Minimalist Editorial (Matched to Swipe)"
            else:
                bg_color = "#1e293b"
                text_color = "#ffffff"
                sub_color = "#94a3b8"
                accent_color = "#fde047"
                mood = "Moody Cinematic Dark"
        except Exception:
            pass
            
    return bg_color, text_color, sub_color, accent_color, mood

def build_terracotta_deck(deck):
    bg_color, text_color, sub_color, accent_color, mood = analyze_swipe_image()
    styled = []
    total = len(deck)
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", "SLIDE " + str(idx+1))).upper()
        title = str(slide.get("title", "Slide " + str(idx+1)))
        content = str(slide.get("content", ""))
        
        uploaded_files = st.session_state.get("sia_uploaded_files", None)
        banner_html = ""
        if uploaded_files:
            try:
                import base64
                file_bytes = uploaded_files[0].getvalue()
                b64_str = base64.b64encode(file_bytes).decode("utf-8")
                banner_html = f"""
                <div style="width: 100%; height: 260px; border-radius: 14px; overflow: hidden; margin-bottom: 20px; border: 1px solid rgba(0,0,0,0.1);">
                    <img src="data:image/png;base64,{b64_str}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
                </div>
                """
            except Exception:
                pass

        html = textwrap.dedent(f"""
        <div style="background-color: {bg_color}; padding: 48px 36px; border-radius: 16px; max-width: 580px; margin: 0 auto; font-family: sans-serif; color: {text_color}; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15); border: 1px solid rgba(0,0,0,0.08);">
            {banner_html}
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="color: {accent_color}; font-size: 11px; font-weight: 800; letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase;">
                    {cat} • {idx+1}/{total}
                </div>
                <h1 style="color: {text_color}; font-size: 26px; font-weight: 700; line-height: 1.3; margin: 0;">
                    {title}
                </h1>
            </div>
            <div style="text-align: center; margin-bottom: 30px; padding: 0 16px;">
                <p style="color: {sub_color}; font-size: 15px; line-height: 1.6; margin: 0; font-weight: 400;">
                    {content}
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; color: {sub_color}; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 16px; text-transform: uppercase;">
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