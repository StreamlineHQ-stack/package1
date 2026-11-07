# sia_editorial_motif_module.py • Dedicated Unified Editorial Motif & Live Unsplash API Engine
import streamlit as st
import requests

def fetch_thematic_images(theme_query, count=6):
    """
    Queries the live Unsplash Search API in real-time using Nikki's Access Key 
    to fetch stunning, professional photography matching any custom theme query.
    """
    cleaned_query = str(theme_query).strip()
    access_key = "LpVeDWfvBMlwXyFMRsZ8UKe7ri4vZwOc8oHeX6Wv1wE"
    
    selected_urls = []
    
    try:
        url = f"https://api.unsplash.com/search/photos?query={cleaned_query}&per_page={max(count, 4)}&orientation=landscape"
        headers = {"Authorization": f"Client-ID {access_key}"}
        resp = requests.get(url, headers=headers, timeout=4)
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            for item in results:
                urls = item.get("urls", {})
                regular_url = urls.get("regular") or urls.get("small")
                if regular_url:
                    selected_urls.append(regular_url)
    except Exception:
        pass
        
    if not selected_urls:
        fallback_pool = [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80"
        ]
        selected_urls = fallback_pool
        
    pool = []
    while len(pool) < count:
        for u in selected_urls:
            pool.append(u)
            if len(pool) >= count:
                break
    return pool[:count]

def build_unified_editorial_deck(deck, motif_theme="flower"):
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
                Nikki's Salon • Live Unsplash API Engine
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