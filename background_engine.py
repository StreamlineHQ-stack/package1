# background_engine.py • Complete Visual Style Engine
import base64

def handle_smart_ai_match(slide_tag, slide_index, slide_text=""):
    """
    Smart AI Contextual Match Engine.
    Dynamically maps slide tags (Hook, Problem, Agitation, Solution, Proof, Action) 
    and slide text to high-end, context-aware visual backgrounds.
    """
    text_blob = f"{slide_tag} {slide_text}".lower()
    
    pools = {
        "hook": [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1080&auto=format&fit=crop&q=80"
        ],
        "problem": [
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80"
        ],
        "solution": [
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&auto=format&fit=crop&q=80"
        ],
        "proof": [
            "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1080&auto=format&fit=crop&q=80"
        ],
        "action": [
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80"
        ]
    }
    
    # Check tag match
    tag_key = str(slide_tag).lower()
    for key in pools:
        if key in tag_key:
            p = pools[key]
            return p[slide_index % len(p)]
            
    # Default smart editorial fallback pool
    default_pool = [
        "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80"
    ]
    return default_pool[slide_index % len(default_pool)]


def handle_unified_motif(motif_choice, slide_index):
    """
    Unified Editorial Motif Engine.
    Maps user keywords to verified photo pools with intelligent fallbacks.
    """
    theme_str = str(motif_choice).strip().lower()
    if not theme_str:
        theme_str = "editorial-luxury"
        
    categories = {
        "ballet": [
            "https://images.unsplash.com/photo-1518834195013-6d09b4697328?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=1080&auto=format&fit=crop&q=80"
        ],
        "train": [
            "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1515165562839-978bbcfc9cc4?w=1080&auto=format&fit=crop&q=80"
        ],
        "cyber": [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1080&auto=format&fit=crop&q=80"
        ],
        "cafe": [
            "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1080&auto=format&fit=crop&q=80"
        ],
        "car": [
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1080&auto=format&fit=crop&q=80"
        ],
        "balloon": [
            "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=1080&auto=format&fit=crop&q=80"
        ],
        "bird": [
            "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=1080&auto=format&fit=crop&q=80"
        ],
        "baseball": [
            "https://images.unsplash.com/photo-1593341646782-e0b495cff86d?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1508344928928-7be3c656230f?w=1080&auto=format&fit=crop&q=80"
        ],
        "city": [
            "https://images.unsplash.com/photo-1477959858617-67f30bc47b82?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1080&auto=format&fit=crop&q=80"
        ]
    }
    
    for keyword, pool in categories.items():
        if keyword in theme_str:
            return pool[slide_index % len(pool)]
            
    fallback_pool = [
        "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80"
    ]
    return fallback_pool[slide_index % len(fallback_pool)]


def get_modular_background(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64="", exact_insp_b64="", sia_notes=""):
    if style_mode == "☕ Terracotta Background & White Font":
        return ""

    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"

    if style_mode == "🎯 Smart AI Contextual Match":
        return handle_smart_ai_match(slide_tag, slide_index)

    if style_mode == "🏛️ Unified Editorial Motif":
        return handle_unified_motif(motif_choice, slide_index)

    return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"