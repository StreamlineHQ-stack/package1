# background_engine.py • Finetuned Universal Semantic Motif Engine
import base64
import hashlib

def handle_exact_inspiration(exact_insp_b64, slide_index):
    """
    Dedicated, fully isolated Exact Inspiration module.
    Takes the uploaded reference image (base64) and renders it cleanly as the slide background.
    """
    if exact_insp_b64:
        return f"data:image/jpeg;base64,{exact_insp_b64}"
    
    exact_fallback_pool = [
        "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"
    ]
    return exact_fallback_pool[slide_index % len(exact_fallback_pool)]


def handle_unified_motif(motif_choice, slide_index):
    """
    Finetuned Universal Semantic Motif Engine.
    Equipped with expanded master pools for trees, forest, nature, luxury, and business.
    """
    theme_str = str(motif_choice).strip().lower()
    if not theme_str:
        theme_str = "editorial-luxury"
        
    clean_theme = theme_str.replace(" ", "-")
    
    # Finetuned Master Pools
    master_pools = {
        "tree": [
            "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1080&auto=format&fit=crop&q=80"
        ],
        "forest": [
            "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1511497584788-8767611925b1?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80"
        ],
        "nature": [
            "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1426604966848-d7adac902bff?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&auto=format&fit=crop&q=80"
        ],
        "business": [
            "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&auto=format&fit=crop&q=80"
        ],
        "luxury": [
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=1080&auto=format&fit=crop&q=80"
        ],
        "dog": [
            "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=1080&auto=format&fit=crop&q=80"
        ],
        "beach": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=1080&auto=format&fit=crop&q=80"
        ],
        "people": [
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1080&auto=format&fit=crop&q=80"
        ],
        "starry": [
            "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=1080&auto=format&fit=crop&q=80"
        ],
        "paris": [
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1509439572013-33e14f08e08d?w=1080&auto=format&fit=crop&q=80"
        ],
        "new york": [
            "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1080&auto=format&fit=crop&q=80"
        ],
        "cat": [
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=1080&auto=format&fit=crop&q=80"
        ],
        "furniture": [
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1080&auto=format&fit=crop&q=80"
        ],
        "sunset": [
            "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=1080&auto=format&fit=crop&q=80"
        ]
    }
    
    for key in master_pools:
        if key in clean_theme:
            pool = master_pools[key]
            return pool[slide_index % len(pool)]
            
    hash_val = int(hashlib.md5(clean_theme.encode()).hexdigest(), 16)
    dynamic_seed_offset = (hash_val + slide_index * 37) % 500
    return f"https://picsum.photos/seed/{clean_theme}-{slide_index}-{dynamic_seed_offset}/1080/1080"


def get_modular_background(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64="", exact_insp_b64="", sia_notes=""):
    if style_mode == "☕ Terracotta Background & White Font":
        return ""

    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"

    if style_mode == "🎯 Exact Inspiration Match (Objects & Layout)":
        return handle_exact_inspiration(exact_insp_b64, slide_index)

    if style_mode == "🏛️ Unified Editorial Motif":
        return handle_unified_motif(motif_choice, slide_index)

    return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"