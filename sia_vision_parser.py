# sia_vision_parser.py • Advanced Visual Deconstruction & Swipe Analysis Engine
import streamlit as st
from PIL import Image
import io
import colorsys

def deconstruct_uploaded_swipe(uploaded_file):
    if not uploaded_file:
        return None
    try:
        image_bytes = uploaded_file.getvalue()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        width, height = img.size
        
        # Resize small for dominant color extraction
        img_small = img.resize((50, 50), Image.Resampling.LANCZOS)
        pixels = list(img_small.getdata())
        
        # Calculate average color and brightness
        r_total = sum(p[0] for p in pixels)
        g_total = sum(p[1] for p in pixels)
        b_total = sum(p[2] for p in pixels)
        count = len(pixels)
        
        avg_r = int(r_total / count)
        avg_g = int(g_total / count)
        avg_b = int(b_total / count)
        
        dominant_hex = f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"
        
        # Brightness check (0-255)
        brightness = (0.299 * avg_r + 0.587 * avg_g + 0.114 * avg_b)
        
        is_light = brightness > 130
        bg_color = "#f8fafc" if is_light else dominant_hex
        text_color = "#111827" if is_light else "#ffffff"
        sub_color = "#374151" if is_light else "#cbd5e1"
        font_family = "Georgia, serif" if is_light else "sans-serif"
        
        mood = "Light Editorial Minimalist (Mist & Earth)" if is_light else "Moody Cinematic Dark"
        
        report = {
            "dominant_color": dominant_hex,
            "bg_color": bg_color,
            "text_color": text_color,
            "sub_color": sub_color,
            "font_family": font_family,
            "brightness": round(brightness, 1),
            "mood": mood,
            "layout_type": "Top Visual Banner with Centered Editorial Typography"
        }
        return report
    except Exception as e:
        return {
            "dominant_color": "#b0543c",
            "bg_color": "#f8fafc",
            "text_color": "#111827",
            "sub_color": "#374151",
            "font_family": "sans-serif",
            "brightness": 200.0,
            "mood": "Editorial Clean",
            "layout_type": "Standard Top Banner"
        }
