# sia_inspiration_template_module.py • Exact Inspiration Match Deck Replicator
import streamlit as st
import requests
import base64
import io
import textwrap

def fetch_inspiration_image(query):
    access_key = "LpVeDWfvBMlwXyFMRsZ8UKe7ri4vZwOc8oHeX6Wv1wE"
    try:
        url = "https://api.unsplash.com/search/photos?query=" + query + "&per_page=1&orientation=squarish"
        headers = {"Authorization": "Client-ID " + access_key}
        resp = requests.get(url, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                return results[0]["urls"]["regular"]
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&auto=format&fit=crop&q=80"

def get_uploaded_swipe_base64():
    uploaded_files = st.session_state.get("sia_uploaded_files", None)
    if uploaded_files:
        try:
            # Get the first uploaded file bytes
            file_obj = uploaded_files[0]
            file_bytes = file_obj.getvalue()
            encoded = base64.b64decode(file_bytes) if isinstance(file_bytes, bytes) else file_bytes
            encoded_b64 = base64.b64encode(file_bytes).decode("utf-8")
            return "data:image/png;base64," + encoded_b64
        except Exception:
            pass
    return None

def build_inspiration_editorial_deck(deck, main_title="", flower_query="white rose", object_query="ceramic vase", date_str="OCT 8 • 2026"):
    uploaded_swipe_b64 = get_uploaded_swipe_base64()
    
    flower_img = fetch_inspiration_image(flower_query)
    object_img = fetch_inspiration_image(object_query)
    
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        slide_title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        active_headline = main_title.strip() if main_title and main_title.strip() else slide_title
        formatted_title = active_headline.replace("&", "<br>&")
        
        # If user uploaded a reference swipe image, use it as the background or top banner card!
        if uploaded_swipe_b64:
            html = textwrap.dedent(f"""
            <div style="background-color: #0b0f19; padding: 36px 32px; border-radius: 20px; border: 3px solid #1f2937; max-width: 600px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);">
                <div style="width: 100%; height: 280px; border-radius: 14px; overflow: hidden; margin-bottom: 20px; border: 2px solid #374151;">
                    <img src="{uploaded_swipe_b64}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
                </div>
                <div style="color: #ffcc00; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 10px; text-transform: uppercase;">
                    SLIDE {idx+1} OF {total} • {cat}
                </div>
                <h2 style="color: #ffffff; font-size: 24px; font-weight: 700; line-height: 1.3; margin-bottom: 14px;">
                    {formatted_title}
                </h2>
                <p style="color: #9ca3af; font-size: 15px; line-height: 1.6; margin-bottom: 24px;">
                    {content}
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #94a3b8; font-size: 11px; font-weight: 600; border-top: 1px solid #1f2937; padding-top: 14px; text-transform: uppercase;">
                    <div>{date_str}</div>
                    <div>NIKKI'S SALON</div>
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