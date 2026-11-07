# sia_inspiration_template_module.py • Robust Full-Bleed Background Replicator for Exact Inspiration Match
import streamlit as st
import base64
import io
import textwrap
from sia_vision_parser import deconstruct_uploaded_swipe, fetch_unsplash_by_query

def get_uploaded_swipe_base64():
    uploaded_files = st.session_state.get("sia_uploaded_files", None)
    if uploaded_files:
        try:
            file_obj = uploaded_files[0]
            file_bytes = file_obj.getvalue()
            encoded_b64 = base64.b64encode(file_bytes).decode("utf-8")
            return "data:image/png;base64," + encoded_b64
        except Exception:
            pass
    return None

def build_inspiration_editorial_deck(deck, main_title="", flower_query="white rose", object_query="ceramic vase", date_str="OCT 8 • 2026"):
    uploaded_swipe_b64 = get_uploaded_swipe_base64()
    uploaded_files = st.session_state.get("sia_uploaded_files", None)
    report = deconstruct_uploaded_swipe(uploaded_files[0]) if uploaded_files else {
        "bg_color": "#f8fafc",
        "text_color": "#111827",
        "sub_color": "#374151",
        "font_family": "Georgia, serif"
    }
    
    font_family = report["font_family"]
    
    object_img = fetch_unsplash_by_query(object_query)
    flower_img = fetch_unsplash_by_query(flower_query)
    
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        slide_title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        active_headline = main_title.strip() if main_title and main_title.strip() else slide_title
        formatted_title = active_headline.replace("&", "<br>&")
        
        if uploaded_swipe_b64:
            html = textwrap.dedent(f"""
            <div style="background: linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.35)), url('{uploaded_swipe_b64}'); background-size: cover; background-position: center; padding: 40px 30px; border-radius: 20px; max-width: 600px; margin: 0 auto; font-family: {font_family}; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.6);">
                <div style="background: rgba(255, 255, 255, 0.94); backdrop-filter: blur(12px); padding: 36px 32px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.6); box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
                    <div style="color: #b0543c; font-size: 12px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 8px; text-transform: uppercase;">
                        SLIDE {idx+1} OF {total} • {cat}
                    </div>
                    <h2 style="color: #111827; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 14px; font-family: {font_family};">
                        {formatted_title}
                    </h2>
                    <p style="color: #374151; font-size: 15px; line-height: 1.6; margin-bottom: 24px; font-family: sans-serif;">
                        {content}
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center; color: #4b5563; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 14px; text-transform: uppercase;">
                        <div>{date_str}</div>
                        <div>NIKKI'S SALON</div>
                    </div>
                </div>
            </div>
            """).strip()
        else:
            html = textwrap.dedent(f"""
            <div style="background-color: #b0543c; padding: 48px 36px; border-radius: 16px; max-width: 580px; margin: 0 auto; font-family: Georgia, serif; color: #ffffff; box-shadow: 0 30px 60px -15px rgba(0,0,0,0.6);">
                <div style="text-align: center; margin-bottom: 24px;">
                    <div style="color: #fde047; font-size: 10px; font-weight: 700; letter-spacing: 4px; margin-bottom: 8px; text-transform: uppercase; font-family: sans-serif;">
                        {cat} • {idx+1}/{total}
                    </div>
                    <h1 style="color: #ffffff; font-size: 26px; font-weight: 400; letter-spacing: 2.5px; line-height: 1.25; margin: 0; text-transform: uppercase;">
                        {formatted_title}
                    </h1>
                </div>
                <div style="text-align: center; margin-bottom: 30px; padding: 0 16px;">
                    <p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; font-family: sans-serif; margin: 0; font-weight: 300;">
                        {content}
                    </p>
                </div>
                <div style="display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 26px;">
                    <div style="width: 54px; height: 54px; border-radius: 50%; overflow: hidden; border: 2px solid rgba(255,255,255,0.8); box-shadow: 0 8px 20px rgba(0,0,0,0.4);">
                        <img src="{object_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
                    </div>
                    <div style="width: 54px; height: 54px; border-radius: 50%; overflow: hidden; border: 2px solid rgba(255,255,255,0.8); box-shadow: 0 8px 20px rgba(0,0,0,0.4);">
                        <img src="{flower_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 10px; letter-spacing: 2px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 16px; text-transform: uppercase; font-family: sans-serif;">
                    <div>{date_str}</div>
                    <div>NIKKI'S SALON</div>
                </div>
            </div>
            """).strip()
        
        styled.append({
            "category": cat,
            "title": slide_title,
            "content": content,
            "rendered_html": html
        })
    return styled
