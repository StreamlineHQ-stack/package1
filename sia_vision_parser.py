# sia_vision_parser.py • Dynamic Image Color & Mood Analyzer for Reference Swipes
from PIL import Image
import io

def deconstruct_uploaded_swipe(uploaded_file):
    try:
        if hasattr(uploaded_file, "getvalue"):
            img_bytes = uploaded_file.getvalue()
        else:
            img_bytes = uploaded_file.read()
            
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        small = img.resize((50, 50), Image.Resampling.BOX)
        pixels = list(small.getdata())
        
        r_sum = sum(p[0] for p in pixels)
        g_sum = sum(p[1] for p in pixels)
        b_sum = sum(p[2] for p in pixels)
        count = len(pixels)
        
        avg_r = r_sum // count
        avg_g = g_sum // count
        avg_b = b_sum // count
        
        hex_color = f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"
        
        if avg_r > avg_g + 30 and avg_r > avg_b + 30:
            mood = "Bold Streetwear / Crimson"
            text_color = "#ffffff"
            sub_color = "#fde047"
        elif avg_g > avg_r and avg_g > avg_b:
            mood = "Serene Botanical / Forest"
            text_color = "#ffffff"
            sub_color = "#86efac"
        elif avg_b > avg_r and avg_b > avg_g:
            mood = "Deep Ocean / Minimalist"
            text_color = "#ffffff"
            sub_color = "#93c5fd"
        elif avg_r > 200 and avg_g > 200 and avg_b > 200:
            mood = "Clean Minimalist / Light"
            text_color = "#111827"
            sub_color = "#2563eb"
        else:
            mood = "Dark Editorial / Noir"
            text_color = "#ffffff"
            sub_color = "#fde047"
            
        return {
            "mood": mood,
            "bg_color": hex_color,
            "sub_color": sub_color,
            "text_color": text_color,
            "font_family": "Impact, sans-serif" if "Streetwear" in mood else "Georgia, serif"
        }
    except Exception:
        return {
            "mood": "Bold Editorial",
            "bg_color": "#b91c1c",
            "sub_color": "#fde047",
            "text_color": "#ffffff",
            "font_family": "Impact, sans-serif"
        }
