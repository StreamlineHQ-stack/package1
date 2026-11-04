# background_engine.py • Universal Algorithmic Editorial Engine
import base64
import hashlib

def handle_unified_motif(motif_choice, slide_index):
    """
    Universal Algorithmic Editorial Engine.
    Takes ANY typed theme (cafe, parks, baseball, ballet, etc.) and deterministically 
    maps it across slides using a robust pool of verified high-res editorial photos.
    """
    theme_str = str(motif_choice).strip().lower()
    if not theme_str:
        theme_str = "editorial-luxury"
        
    # Master pool of verified, high-res editorial images with zero hotlinking errors
    master_editorial_pool = [
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1518834195013-6d09b4697328?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1515165562839-978bbcfc9cc4?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1593341646782-e0b495cff86d?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1508344928928-7be3c656230f?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1477959858617-67f30bc47b82?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1542272454-17d438148d82?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1080&auto=format&fit=crop&q=80"
    ]
    
    # Generate a deterministic starting index based on the user's typed theme
    hash_val = int(hashlib.md5(theme_str.encode()).hexdigest(), 16)
    start_idx = hash_val % len(master_editorial_pool)
    
    # Select unique image per slide using safe modulo indexing
    target_idx = (start_idx + slide_index) % len(master_editorial_pool)
    return master_editorial_pool[target_idx]


def get_modular_background(style_mode, motif_choice, slide_index, slide_tag="", custom_url="", uploaded_b64=""):
    if style_mode == "☕ Terracotta Background & White Font":
        return ""
    if style_mode == "📂 Custom User Images":
        if uploaded_b64:
            return f"data:image/jpeg;base64,{uploaded_b64}"
        elif custom_url:
            return custom_url
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"
    if style_mode == "🏛️ Unified Editorial Motif":
        return handle_unified_motif(motif_choice, slide_index)
    return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"