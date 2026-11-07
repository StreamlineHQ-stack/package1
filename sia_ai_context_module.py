# sia_ai_context_module.py • Smart AI Contextual Match with True Randomization
import streamlit as st
import requests
import textwrap
import random
import time

def get_randomized_unsplash_image(slide_idx):
    access_key = "LpVeDWfvBMlwXyFMRsZ8UKe7ri4vZwOc8oHeX6Wv1wE"
    # Pool of diverse professional and creative stock photo keywords
    keywords = [
        "minimalist workspace laptop notebook", 
        "modern executive leadership office", 
        "creative branding design studio", 
        "strategy brainstorming whiteboard analytics", 
        "succulent plant minimal desk aesthetic", 
        "abstract architectural lighting shadow", 
        "entrepreneur working coffee shop modern", 
        "high performance growth chart startup"
    ]
    query = random.choice(keywords)
    page_num = random.randint(1, 25) + slide_num_offset(slide_idx)
    
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&page={page_num}&orientation=squarish"
        headers = {"Authorization": "Client-ID " + access_key}
        resp = requests.get(url, headers=headers, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                return results[0]["urls"]["regular"]
    except Exception:
        pass
    
    # Fallback to unique random unsplash stock photos
    fallbacks = [
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=800&auto=format&fit=crop&q=80",
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&auto=format&fit=crop&q=80"
    ]
    return random.choice(fallbacks)

def slide_num_offset(idx):
    return int(time.time() % 50) + idx

def build_ai_context_deck(deck):
    random.seed(int(time.time()))
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        img_url = get_randomized_unsplash_image(idx)
        
        html = textwrap.dedent(f"""
        <div style="background-color: #0b0f19; padding: 36px 32px; border-radius: 20px; border: 2px solid #374151; max-width: 600px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);">
            <div style="width: 100%; height: 260px; border-radius: 14px; overflow: hidden; margin-bottom: 20px; border: 1px solid #4b5563;">
                <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
            <div style="color: #ffcc00; font-size: 12px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 8px; text-transform: uppercase;">
                SLIDE {idx+1} OF {total} • {cat}
            </div>
            <h2 style="color: #ffffff; font-size: 24px; font-weight: 700; line-height: 1.3; margin-bottom: 14px;">
                {title}
            </h2>
            <p style="color: #9ca3af; font-size: 15px; line-height: 1.6; margin-bottom: 24px;">
                {content}
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 11px; font-weight: 600; border-top: 1px solid #1f2937; padding-top: 14px; text-transform: uppercase;">
                <div>OCT 8 • 2026</div>
                <div>NIKKI'S SALON</div>
            </div>
        </div>
        """).strip()
        
        styled.append({
            "category": cat,
            "title": title,
            "content": content,
            "rendered_html": html
        })
    return styled
