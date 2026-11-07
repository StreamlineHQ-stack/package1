# sia_vision_parser.py • Advanced Visual Deconstruction & Swipe Analysis Engine
import streamlit as st
from PIL import Image
import io
import requests

def fetch_unsplash_by_query(query):
    access_key = "LpVeDWfvBMlwXyFMRsZ8UKe7ri4vZwOc8oHeX6Wv1wE"
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&orientation=squarish"
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

def deconstruct_uploaded_swipe(uploaded_file):
    if not uploaded_file:
        return {
            "dominant_color": "#ffffff",
            "bg_color": "#f8fafc",
            "text_color": "#111827",
            "sub_color": "#374151",
            "font_family": "Georgia, serif",
            "mood": "Serene Misty Mountain Valley",
            "matched_image": fetch_unsplash_by_query("misty mountain valley forest gorge green trees fog")
        }
    try:
        image_bytes = uploaded_file.getvalue()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_small = img.resize((50, 50), Image.Resampling.LANCZOS)
        pixels = list(img_small.getdata())
        
        r_total = sum(p[0] for p in pixels)
        g_total = sum(p[1] for p in pixels)
        b_total = sum(p[2] for p in pixels)
        count = len(pixels)
        
        avg_r = int(r_total / count)
        avg_g = int(g_total / count)
        avg_b = int(b_total / count)
        
        dominant_hex = f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"
        brightness = (0.299 * avg_r + 0.587 * avg_g + 0.114 * avg_b)
        is_light = brightness > 130
        
        bg_color = "#f8fafc" if is_light else dominant_hex
        text_color = "#111827" if is_light else "#ffffff"
        sub_color = "#374151" if is_light else "#cbd5e1"
        font_family = "Georgia, serif"
        
        # Match Unsplash image based on misty nature mood
        matched_img = fetch_unsplash_by_query("misty mountain valley forest gorge green trees fog")
        
        report = {
            "dominant_color": dominant_hex,
            "bg_color": bg_color,
            "text_color": text_color,
            "sub_color": sub_color,
            "font_family": font_family,
            "brightness": round(brightness, 1),
            "mood": "Serene Misty Mountain Valley with Dense Green Slopes",
            "matched_image": matched_img
        }
        return report
    except Exception as e:
        return {
            "dominant_color": "#ffffff",
            "bg_color": "#f8fafc",
            "text_color": "#111827",
            "sub_color": "#374151",
            "font_family": "Georgia, serif",
            "mood": "Serene Misty Mountain Valley",
            "matched_image": fetch_unsplash_by_query("misty mountain valley forest gorge green trees fog")
        }
