# sia_inspiration_template_module.py • Exact Inspiration Match Replicator Engine
import streamlit as st
import requests

def fetch_inspiration_image(query):
    """Fetches a high-end Unsplash image for a specific custom prop or flower."""
    access_key = "LpVeDWfvBMlwXyFMRsZ8UKe7ri4vZwOc8oHeX6Wv1wE"
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&orientation=squarish"
        headers = {"Authorization": f"Client-ID {access_key}"}
        resp = requests.get(url, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                return results[0]["urls"]["regular"]
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&auto=format&fit=crop&q=80"

def render_terracotta_editorial_inspiration(main_title="SARINA & LEON", flower_query="white rose", object_query="ceramic vase", date_str="OCT 8 • 2026", location_str="THE LENTON ESTATE", time_str="10:00 AM"):
    flower_img = fetch_inspiration_image(flower_query)
    object_img = fetch_inspiration_image(object_query)
    
    formatted_title = main_title.replace("&", "<br>&")
    
    html_code = f"""
    <div style="background-color: #b0543c; padding: 40px 24px; border-radius: 20px; max-width: 580px; margin: 0 auto; font-family: Georgia, serif; text-align: center; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);">
        <h1 style="color: #ffffff; font-size: 36px; font-weight: 400; letter-spacing: 3px; line-height: 1.2; margin-bottom: 30px; text-transform: uppercase;">
            {formatted_title}
        </h1>
        <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 30px; background: rgba(0,0,0,0.1); padding: 16px; border-radius: 12px;">
            <div style="width: 48%; height: 260px; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 15px rgba(0,0,0,0.2);">
                <img src="{object_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
            <div style="width: 48%; height: 260px; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 15px rgba(0,0,0,0.2);">
                <img src="{flower_img}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 11px; letter-spacing: 1.5px; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 16px; text-transform: uppercase;">
            <div style="text-align: left;">
                <span style="opacity: 0.7; display: block; font-size: 9px;">DATE</span>
                <strong>{date_str}</strong>
            </div>
            <div style="text-align: center;">
                <span style="opacity: 0.7; display: block; font-size: 9px;">LOCATION</span>
                <strong>{location_str}</strong>
            </div>
            <div style="text-align: right;">
                <span style="opacity: 0.7; display: block; font-size: 9px;">TIME</span>
                <strong>{time_str}</strong>
            </div>
        </div>
    </div>
    """
    return html_code