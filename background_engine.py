# background_engine.py • Dedicated Background & Motif Module
import base64

def get_modular_background(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64="", exact_insp_b64="", sia_notes=""):
    # 1. Terracotta Background Mode
    if style_mode == "☕ Terracotta Background & White Font":
        return ""

    # 2. Custom User Images Mode
    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://picsum.photos/seed/custom/1080/1080"

    # 3. Exact Inspiration Match Mode
    if style_mode == "🎯 Exact Inspiration Match (Objects & Layout)":
        if exact_insp_b64:
            return f"data:image/jpeg;base64,{exact_insp_b64}"
        # Guaranteed stable editorial default background if no file uploaded yet
        return "https://picsum.photos/seed/editorial/1080/1080"

    # 4. Unified Editorial Motif Mode (Guaranteed 100% stable picsum/unsplash seeds)
    if style_mode == "🏛️ Unified Editorial Motif":
        theme_str = str(motif_choice).strip().lower()
        clean_theme = theme_str.replace(" ", "-") if theme_str else "editorial"
        
        # Generates a stable, beautiful thematic background for every slide
        return f"https://picsum.photos/seed/{clean_theme}-{slide_index}/1080/1080"

    # 5. Smart AI Match Fallback
    return f"https://picsum.photos/seed/smartai-{slide_index}/1080/1080"