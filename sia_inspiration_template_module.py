# sia_inspiration_template_module.py • Exact Inspiration Match Deck Replicator
import streamlit as st
import requests

def fetch_inspiration_image(query):
    """Fetches a high-end Unsplash image for a specific custom prop or flower."""
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

def build_inspiration_editorial_deck(deck, main_title="", flower_query="white rose", object_query="ceramic vase", date_str="OCT 8 • 2026"):
    flower_img = fetch_inspiration_image(flower_query)
    object_img = fetch_inspiration_image(object_query)
    
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", "SLIDE " + str(idx+1))).upper()
        slide_title = str(slide.get("title", "Slide " + str(idx+1)))
        content = str(slide.get("content", ""))
        
        # If user left main_title blank in sidebar, use the generated slide title dynamically
        active_headline = main_title.strip() if main_title and main_title.strip() else slide_title
        formatted_title = active_headline.replace("&", "<br>&")
        
        # Flattened HTML string to prevent Streamlit markdown escaping / code block rendering
        html = '<div style="background-color: #b0543c; padding: 40px 32px; border-radius: 20px; max-width: 580px; margin: 0 auto; font-family: Georgia, serif; color: #ffffff; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">'
        html += '<div style="text-align: center; margin-bottom: 20px;">'
        html += f'<div style="color: #ffd700; font-size: 11px; font-weight: 700; letter-spacing: 3px; margin-bottom: 8px; text-transform: uppercase; font-family: sans-serif;">SLIDE {idx+1} OF {total} • {cat}</div>'
        html += f'<h1 style="color: #ffffff; font-size: 26px; font-weight: 400; letter-spacing: 2px; line-height: 1.2; margin: 0; text-transform: uppercase;">{formatted_title}</h1>'
        html += '</div>'
        html += '<div style="text-align: center; margin-bottom: 22px; padding: 0 16px;">'
        html += f'<p style="color: #f9fafb; font-size: 15px; line-height: 1.6; font-family: sans-serif; margin: 0;">{content}</p>'
        html += '</div>'
        html += '<div style="display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 22px;">'
        html += f'<div style="width: 48%; height: 210px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15);"><img src="{object_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" /></div>'
        html += f'<div style="width: 48%; height: 210px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15);"><img src="{flower_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" /></div>'
        html += '</div>'
        html += '<div style="display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 10px; letter-spacing: 1.5px; border-top: 1px solid rgba(255,255,255,0.25); padding-top: 16px; text-transform: uppercase; font-family: sans-serif;">'
        html += f'<div style="text-align: left;"><span style="opacity: 0.7; display: block; font-size: 8px;">DATE</span><strong>{date_str}</strong></div>'
        html += '<div style="text-align: center;"><span style="opacity: 0.7; display: block; font-size: 8px;">CURATION</span><strong>EDITORIAL MOTO</strong></div>'
        html += '<div style="text-align: right;"><span style="opacity: 0.7; display: block; font-size: 8px;">APEXMORPH</span><strong>NIKKI\'S SALON</strong></div>'
        html += '</div>'
        html += '</div>'
        
        styled.append({
            "category": cat,
            "title": slide_title,
            "content": content,
            "rendered_html": html
        })
    return styled