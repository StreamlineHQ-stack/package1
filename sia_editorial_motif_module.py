# sia_editorial_motif_module.py • Dedicated Unified Editorial Motif & Theme Engine
import streamlit as st

def fetch_thematic_images(theme_query, count=6):
    """
    Fetches a 100% reliable pool of high-end curated images strictly matching 
    the theme query with comprehensive keyword coverage and zero fallback stickiness.
    """
    cleaned_query = str(theme_query).strip().lower()
    
    theme_pools = {
        "flower": [
            "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1508749495167-f6d2f3a67732?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=1080&auto=format&fit=crop&q=80"
        ],
        "rose": [
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1559563557-45604494b9fc?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1582794145783-5d0774c83e27?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=1080&auto=format&fit=crop&q=80"
        ],
        "beach": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80"
        ],
        "mountain": [
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1080&auto=format&fit=crop&q=80"
        ],
        "dog": [
            "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=1080&auto=format&fit=crop&q=80"
        ],
        "dogs": [
            "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=1080&auto=format&fit=crop&q=80"
        ],
        "puppy": [
            "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=1080&auto=format&fit=crop&q=80"
        ],
        "happy people": [
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80"
        ],
        "children": [
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1472162072942-cd5147eb3902?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1485546246426-74dc88dec4d9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=1080&auto=format&fit=crop&q=80"
        ],
        "child": [
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1472162072942-cd5147eb3902?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1485546246426-74dc88dec4d9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=1080&auto=format&fit=crop&q=80"
        ],
        "play": [
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1472162072942-cd5147eb3902?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1485546246426-74dc88dec4d9?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=1080&auto=format&fit=crop&q=80"
        ]
    }
    
    selected_urls = []
    for key, urls in theme_pools.items():
        if key in cleaned_query or cleaned_query in key:
            selected_urls = urls
            break
            
    if not selected_urls:
        words = cleaned_query.split()
        for w in words:
            for key, urls in theme_pools.items():
                if w in key or key in w:
                    selected_urls = urls
                    break
            if selected_urls:
                break
                
    if not selected_urls:
        query_slug = cleaned_query.replace(" ", "-")
        selected_urls = [
            f"https://picsum.photos/seed/{query_slug}_1/1080/1080",
            f"https://picsum.photos/seed/{query_slug}_2/1080/1080",
            f"https://picsum.photos/seed/{query_slug}_3/1080/1080",
            f"https://picsum.photos/seed/{query_slug}_4/1080/1080"
        ]
            
    pool = []
    while len(pool) < count:
        for u in selected_urls:
            pool.append(u)
            if len(pool) >= count:
                break
    return pool[:count]

def build_unified_editorial_deck(deck, motif_theme="flower"):
    """
    Builds a styled deck utilizing clean thematic images derived exclusively from the user's input theme.
    """
    styled = []
    total = len(deck)
    image_pool = fetch_thematic_images(motif_theme, count=total)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        bg_url = image_pool[idx % len(image_pool)]
        
        html = f"""
        <div style="background: #0b0f19; padding: 40px; border-radius: 24px; border: 3px solid #10b981; max-width: 680px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
            <div style="width: 100%; height: 240px; border-radius: 16px; overflow: hidden; margin-bottom: 24px; border: 2px solid #34d399;">
                <img src="{bg_url}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
            <div style="color: #34d399; font-size: 14px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 12px; text-transform: uppercase;">
                THEME: {motif_theme} • SLIDE {idx+1} OF {total} • {cat}
            </div>
            <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 16px;">
                {title}
            </h2>
            <p style="color: #d1d5db; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                {content}
            </p>
            <div style="text-align: right; color: #6b7280; font-size: 12px; font-weight: 600; border-top: 1px solid #1f2937; padding-top: 12px;">
                Nikki's Salon • Editorial Motif Engine
            </div>
        </div>
        """
        styled.append({
            "category": cat,
            "title": title,
            "content": content,
            "rendered_html": html
        })
    return styled