# sia_ai_context_module.py • Isolated Module 2: Smart AI Contextual Match with Real Images
def build_ai_context_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        text_blob = (s.get("category", "") + " " + s.get("title", "") + " " + s.get("content", "")).lower()
        
        # Contextual Unsplash Photography URLs matching slide themes
        img_url = "https://images.unsplash.com/photo-1432821596592-e2c18b78144f?auto=format&fit=crop&w=1080&q=80" # Default editorial
        img_label = "Focal Point Editorial"
        
        if "hook" in text_blob or "why" in text_blob or "flat" in text_blob or "ads" in text_blob or "sell" in text_blob:
            img_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1080&q=80" # Analytics / Target
            img_label = "Target & Conversion Analytics"
        elif "problem" in text_blob or "cost" in text_blob or "poor" in text_blob or "hidden" in text_blob:
            img_url = "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1080&q=80" # Friction / Business challenge
            img_label = "Friction & Diagnostic Analysis"
        elif "solution" in text_blob or "craft" in text_blob or "art" in text_blob or "system" in text_blob:
            img_url = "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1080&q=80" # Blueprint / Strategy
            img_label = "Blueprint & Strategic Framework"
        elif "growth" in text_blob or "scale" in text_blob or "roi" in text_blob or "pay" in text_blob:
            img_url = "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1080&q=80" # Growth / Revenue
            img_label = "Milestone & Revenue Growth"
        elif "cta" in text_blob or "comment" in text_blob or "ready" in text_blob:
            img_url = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1080&q=80" # Action / Growth
            img_label = "Direct-Response Action Trigger"
            
        styled_slides.append({
            "card_num": idx + 1,
            "style": "Smart AI Contextual Match",
            "bg_color": "#111827",
            "font_color": "#F9FAFB",
            "accent_bg": "rgba(37, 99, 235, 0.25)",
            "imagery": img_label,
            "img_url": img_url,
            "category": s.get("category", "SLIDE"),
            "title": s.get("title", ""),
            "content": s.get("content", "")
        })
    return styled_slides