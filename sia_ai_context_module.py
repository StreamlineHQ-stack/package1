# sia_ai_context_module.py • Isolated Module 2: Smart AI Contextual Match (Fully Baked Deck)
def build_ai_context_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        text_blob = (s.get("category", "") + " " + s.get("title", "") + " " + s.get("content", "")).lower()
        
        # Contextual Unsplash Photography URLs matching slide themes
        img_url = "https://images.unsplash.com/photo-1432821596592-e2c18b78144f?auto=format&fit=crop&w=1080&q=80" # Default editorial
        
        if "hook" in text_blob or "why" in text_blob or "flat" in text_blob or "ads" in text_blob or "sell" in text_blob:
            img_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1080&q=80" # Target/Analytics
        elif "problem" in text_blob or "cost" in text_blob or "poor" in text_blob or "hidden" in text_blob:
            img_url = "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1080&q=80" # Friction/Challenge
        elif "solution" in text_blob or "craft" in text_blob or "art" in text_blob or "system" in text_blob:
            img_url = "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1080&q=80" # Blueprint
        elif "growth" in text_blob or "scale" in text_blob or "roi" in text_blob or "pay" in text_blob:
            img_url = "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1080&q=80" # Growth
        elif "cta" in text_blob or "comment" in text_blob or "ready" in text_blob:
            img_url = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1080&q=80" # Action

        # Fully bake the HTML card payload inside the module
        baked_card_html = f"""
        <div style="background-color: #111827; color: #F9FAFB; padding: 35px; border-radius: 16px; margin-top: 15px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.22); font-family: Arial, sans-serif;">
            <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1.8px; opacity: 0.85; margin-bottom: 12px;">
                Slide {idx + 1} • {s.get('category', 'SLIDE')} • [Smart AI Contextual Match]
            </div>
            <div style="margin-bottom: 16px; border-radius: 8px; overflow: hidden; max-height: 150px;">
                <img src="{img_url}" style="width: 100%; height: 140px; object-fit: cover; opacity: 0.9;" />
            </div>
            <div style="font-size: 24px; font-weight: bold; margin-bottom: 14px; line-height: 1.35;">
                {s.get('title', '')}
            </div>
            <div style="font-size: 15px; opacity: 0.95; line-height: 1.5;">
                {s.get('content', '')}
            </div>
        </div>
        """

        styled_slides.append({
            "card_num": idx + 1,
            "style": "Smart AI Contextual Match",
            "rendered_html": baked_card_html
        })
        
    return styled_slides