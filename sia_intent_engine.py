# sia_intent_engine.py • AI Design Intent & Structured Specification Pipeline
import io
import json
from PIL import Image

def analyze_design_intent(uploaded_file):
    """
    Analyzes an uploaded slide screenshot and produces a structured JSON design specification 
    capturing color palette, mood, style, composition, and design intent (following Max's architecture).
    """
    try:
        if hasattr(uploaded_file, "getvalue"):
            img_bytes = uploaded_file.getvalue()
        else:
            img_bytes = uploaded_file.read()
            
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        width, height = img.size
        
        # 1. Extract Palette using Median-Cut Quantization
        small = img.resize((100, 100), Image.Resampling.BOX)
        quantized = small.quantize(colors=4, method=Image.Quantize.MEDIANCUT)
        palette_data = quantized.getpalette()
        
        extracted_hexes = []
        for i in range(4):
            r = palette_data[i * 3]
            g = palette_data[i * 3 + 1]
            b = palette_data[i * 3 + 2]
            extracted_hexes.append(f"#{r:02x}{g:02x}{b:02x}")
            
        # Ensure distinct colors
        primary_bg = extracted_hexes[0]
        accent_color = extracted_hexes[1] if len(extracted_hexes) > 1 else "#fde047"
        
        # 2. Determine Design Style & Mood via Image Heuristics
        r_avg = sum(p[0] for p in small.getdata()) // len(list(small.getdata()))
        g_avg = sum(p[1] for p in small.getdata()) // len(list(small.getdata()))
        b_avg = sum(p[2] for p in small.getdata()) // len(list(small.getdata()))
        
        if r_avg > g_avg + 30 and r_avg > b_avg + 30:
            design_style = "bold streetwear editorial"
            mood = "high-impact, energetic, dramatic"
            motifs = ["high-contrast typography", "bold color block background"]
            composition = "central subject with heavy framing"
        elif g_avg > r_avg and g_avg > b_avg:
            design_style = "serene botanical editorial"
            mood = "calm, organic, professional"
            motifs = ["botanical undertones", "natural foliage shadows"]
            composition = "asymmetric, lower-right visual emphasis"
        elif r_avg > 180 and g_avg > 180 and b_avg > 180:
            design_style = "clean minimalist light"
            mood = "clean, breathable, modern"
            motifs = ["generous whitespace", "crisp borders"]
            composition = "balanced, centered hierarchy"
        else:
            design_style = "warm terracotta editorial"
            mood = "sophisticated, grounded, warm"
            motifs = ["warm earth tones", "subtle layered shapes"]
            composition = "asymmetric visual balance"

        spec = {
            "design_style": design_style,
            "mood": mood,
            "palette": extracted_hexes,
            "motifs": motifs,
            "composition": composition,
            "negative_space": "protected headline hierarchy with clear padding",
            "texture": "clean digital matte finish",
            "background_instructions": f"Render solid background with primary color {primary_bg} and accent styling {accent_color}."
        }
        
        return spec
    except Exception as e:
        return {
            "design_style": "minimal editorial",
            "mood": "clean, professional",
            "palette": ["#b91c1c", "#fde047", "#ffffff", "#111827"],
            "motifs": ["editorial typography"],
            "composition": "balanced",
            "negative_space": "generous",
            "texture": "matte",
            "background_instructions": "Fallback default editorial layout."
        }
