# sia_inspiration_template_module.py • Exact Inspiration Match Deck Replicator
import streamlit as st
import requests

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

def build_inspiration_editorial_deck(deck, main_title="", flower_query="white rose", object_query="ceramic vase", date_str="OCT 8 • 2026"):
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
        
        # Locked-in high-end magazine editorial layout
        html = '<div style="background-color: #b0543c; padding: 48px 36px; border-radius: 16px; max-width: 580px; margin: 0 auto; font-family: Georgia, serif; color: #ffffff; box-shadow: 0 30px 60px -15px rgba(0,0,0,0.6);">'
        html += '<div style="text-align: center; margin-bottom: 24px;">'
        html += f'<div style="color: #fde047; font-size: 10px; font-weight: 700; letter-spacing: 4px; margin-bottom: 8px; text-transform: uppercase; font-family: sans-serif;">{cat} • {idx+1}/{total}</div>'
        html += f'<h1 style="color: #ffffff; font-size: 26px; font-weight: 400; letter-spacing: 2.5px; line-height: 1.25; margin: 0; text-transform: uppercase;">{formatted_title}</h1>'
        html += '</div>'
        html += '<div style="text-align: center; margin-bottom: 28px; padding: 0 16px;">'
        html += f'<p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; font-family: sans-serif; margin: 0; font-weight: 300;">{content}</p>'
        html += '</div>'
        html += '<div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 26px; background: rgba(0,0,0,0.15); padding: 10px; border-radius: 12px; width: fit-content; margin-left: auto; margin-right: auto; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 15px 30px rgba(0,0,0,0.3);">'
        html += f'<div style="width: 110px; height: 110px; border-radius: 8px; overflow: hidden;"><img src="{object_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" /></div>'
        html += f'<div style="width: 110px; height: 110px; border-radius: 8px; overflow: hidden;"><img src="{flower_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" /></div>'
        html += '</div>'
        html += '<div style="display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 10px; letter-spacing: 2px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 16px; text-transform: uppercase; font-family: sans-serif;">'
        html += f'<div>{date_str}</div><div>EXACT INSPIRATION</div><div>NIKKI\'S SALON</div>'
        html += '</div>'
        html += '</div>'
        
        styled.append({
            "category": cat,
            "title": slide_title,
            "content": content,
            "rendered_html": html
        })
    return styled