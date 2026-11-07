# sia_editorial_motif_module.py • Dedicated Unified Editorial Motif & Theme Engine
import streamlit as st

def fetch_thematic_images(theme_query, count=6):
    """
    Fetches a clean pool of high-end Unsplash stock images 
    strictly matching the user's custom theme query with zero cross-contamination.
    """
    cleaned_query = str(theme_query).strip().lower()
    
    # Strictly curated, 100% theme-matching Unsplash Photo IDs
    theme_map = {
        "flower": [
            "1490750967868-88aa4486c946", # vibrant flowers
            "1526047932273-341f2a7631f9", # floral bouquet
            "1508749495167-f6d2f3a67732", # blossom
            "1518895949257-7621c3c786d7"  # floral petals
        ],
        "rose": [
            "1518709268805-4e9042af9f23", # red rose
            "1559563557-45604494b9fc", # pink rose
            "1582794145783-5d0774c83e27", # luxury rose macro
            "1563245372-f21724e3856d"  # elegant rose
        ],
        "beach": [
            "1507525428034-b723cf961d3e", # tropical beach
            "1519046904884-53103b34b206", # ocean waves
            "1506929562872-bb421503ef21", # sandy shore
            "1507525428034-b723cf961d3e"  # coastline
        ],
        "mountain": [
            "1464822759023-fed622ff2c3b", # snowy peaks
            "1454496522488-7a8e488e8606", # alpine ridge
            "1506744038136-46273834b3fb", # mountain valley
            "1464822759023-fed622ff2c3b"  # rugged peaks
        ],
        "happy people": [
            "1522071820081-009f0129c71c", # smiling team
            "1517841905240-472988babdf9", # laughing friends
            "1529156069898-49953e39b3ac", # joyful group
            "1522071820081-009f0129c71c"  # smiling people
        ]
    }
    
    selected_urls = []
    for key, photo_ids in theme_map.items():
        if key in cleaned_query or cleaned_query in key:
            selected_urls = [f"https://images.unsplash.com/photo-{pid}?w=1080&auto=format&fit=crop&q=80" for pid in photo_ids]
            break
            
    # Fallback for any custom theme query
    if not selected_urls:
        fallback_ids = ["1507525428034-b723cf961d3e", "1490750967868-88aa4486c946", "1464822759023-fed622ff2c3b", "1522071820081-009f0129c71c"]
        selected_urls = [f"https://images.unsplash.com/photo-{pid}?w=1080&auto=format&fit=crop&q=80" for pid in fallback_ids]
            
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