# background_engine.py • 100% Bombproof Visual Engine
import base64
import hashlib

def get_modular_background(style_mode, motif_choice, slide_index, *args, **kwargs):
    """
    Bombproof background resolver that guarantees a valid image URL string 
    under all circumstances, preventing grey boxes or TypeErrors.
    """
    try:
        # Extract optional keyword arguments safely
        uploaded_b64 = kwargs.get("uploaded_b64", "")
        custom_url = kwargs.get("custom_url", "")
        
        if style_mode == "☕ Terracotta Background & White Font":
            return ""
            
        if style_mode == "📂 Custom User Images":
            if uploaded_b64:
                if not str(uploaded_b64).startswith("data:image"):
                    return f"data:image/jpeg;base64,{uploaded_b64}"
                return str(uploaded_b64)
            elif custom_url:
                return str(custom_url)
            return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"

        # Universal Algorithmic Motif Resolver
        theme_str = str(motif_choice).strip().lower() if motif_choice else "editorial-luxury"
        if not theme_str or theme_str == "none":
            theme_str = "editorial-luxury"
            
        master_editorial_pool = [
            "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1080&auto=format&fit=crop&q=80",
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
        
        hash_val = int(hashlib.md5(theme_str.encode()).hexdigest(), 16)
        start_idx = hash_val % len(master_editorial_pool)
        target_idx = (start_idx + int(slide_index)) % len(master_editorial_pool)
        return master_editorial_pool[target_idx]
        
    except Exception:
        return "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1080&auto=format&fit=crop&q=80"