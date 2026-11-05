# background_engine.py • Dedicated Background & Motif Module
import base64

def get_modular_background(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64="", sia_notes=""):
    if style_mode == "☕ Terracotta Background & White Font":
        return ""

    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"

    if style_mode == "🎯 Exact Inspiration Match (Objects & Layout)" or sia_notes:
        editorial_pool = [
            "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"
        ]
        return editorial_pool[slide_index % len(editorial_pool)]

    if style_mode == "🏛️ Unified Editorial Motif":
        theme_str = str(motif_choice).strip().lower()
        
        # Comprehensive curated pools guaranteed to load instantly
        motif_pools = {
            "sunset": [
                "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=1080&auto=format&fit=crop&q=80"
            ],
            "wood": [
                "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=1080&auto=format&fit=crop&q=80"
            ],
            "arch": [
                "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=1080&auto=format&fit=crop&q=80"
            ],
            "minimalist": [
                "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80"
            ],
            "ocean": [
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&auto=format&fit=crop&q=80"
            ]
        }
        
        for key in motif_pools:
            if key in theme_str:
                pool = motif_pools[key]
                return pool[slide_index % len(pool)]
        
        # Default fallback editorial pool if custom keyword doesn't match
        fallback_pool = [
            "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80"
        ]
        return fallback_pool[slide_index % len(fallback_pool)]

    # Smart AI Match Fallback
    default_smart_pool = [
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
    ]
    return default_smart_pool[slide_index % len(default_smart_pool)]