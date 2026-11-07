# sia_inspiration_template_module.py • Full-Bleed Background Replicator for Exact Inspiration Match
import streamlit as st
import base64
import io
import textwrap
import requests

@st.cache_data(show_spinner=False)
def get_cached_scenic_bg_base64(query="misty forest mountains"):
    try:
        q_lower = query.lower()
        if "mountain" in q_lower or "forest" in q_lower or "mist" in q_lower or "tree" in q_lower:
            url = "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&auto=format&fit=crop&q=80"
        elif "ocean" in q_lower or "beach" in q_lower or "sea" in q_lower:
            url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80"
        else:
            url = "https://images.unsplash.com/photo-1511497584788-8767611925b6?w=1080&auto=format&fit=crop&q=80"
            
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            encoded = base64.b64encode(resp.content).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&auto=format&fit=crop&q=80"

def build_inspiration_editorial_deck(deck, main_title="", flower_query="white rose", object_query="misty forest mountains", date_str="OCT 8 • 2026"):
    bg_data_uri = get_cached_scenic_bg_base64(object_query)
    
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        slide_title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        active_headline = main_title.strip() if main_title and main_title.strip() else slide_title
        formatted_title = active_headline.replace("&", "<br>&")
        
        # Bulletproof CSS background-image with base64 data-URI + dark gradient scrim overlay
        html = textwrap.dedent(f"""
        <div style="width: 100%; max-width: 580px; height: 580px; margin: 0 auto; border-radius: 24px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7); background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.8)), url('{bg_data_uri}'); background-size: cover; background-position: center; font-family: Georgia, serif; display: flex; flex-direction: column; justify-content: space-between; padding: 50px 36px; box-sizing: border-box; text-align: center; color: #ffffff;">
            <div>
                <div style="color: #fde047; font-size: 11px; font-weight: 800; letter-spacing: 2px; margin-bottom: 16px; text-transform: uppercase; font-family: sans-serif;">
                    SLIDE {idx+1} OF {total} • {cat}
                </div>
                <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 18px; text-shadow: 0 2px 6px rgba(0,0,0,0.8);">
                    {formatted_title}
                </h2>
                <p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; margin-bottom: 20px; font-family: sans-serif; text-shadow: 0 1px 4px rgba(0,0,0,0.8);">
                    {content}
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; color: #e2e8f0; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 16px; text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif;">
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
