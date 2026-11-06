# sia_ai_context_module.py • Isolated Module 2: Smart AI Contextual Match with Rich Visual Assets
def build_ai_context_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        text_blob = (s.get("title", "") + " " + s.get("content", "")).lower()
        
        # Deep contextual keyword & semantic mapping
        matched_img = "🖼️ AI Visual Asset: Minimalist Abstract Editorial Graphic"
        if "focus" in text_blob or "target" in text_blob or "sell" in text_blob or "words" in text_blob:
            matched_img = "🎯 Visual Asset: Bulls-eye Precision Target & Conversion Icon"
        elif "long" in text_blob or "road" in text_blob or "journey" in text_blob or "market" in text_blob:
            matched_img = "🌉 Visual Asset: Winding Bridge & Horizon Growth Vector"
        elif "growth" in text_blob or "scale" in text_blob or "roi" in text_blob or "pay" in text_blob:
            matched_img = "📈 Visual Asset: Upward Escalation & Revenue Milestone Chart"
        elif "protect" in text_blob or "joint" in text_blob or "pain" in text_blob or "killer" in text_blob:
            matched_img = "🛡️ Visual Asset: Ergonomic Shield & Core Protection Emblem"
        elif "art" in text_blob or "craft" in text_blob or "persuasion" in text_blob:
            matched_img = "🎨 Visual Asset: Creative Design Studio Motif & Palette"
            
        styled_slides.append({
            "card_num": idx + 1,
            "style": "Smart AI Contextual Match",
            "bg_color": "#111827", # Deep sleek obsidian matching AI aesthetic
            "font_color": "#F9FAFB",
            "accent_bg": "rgba(37, 99, 235, 0.25)", # Rich blue accent badge
            "imagery": matched_img,
            "category": s.get("category", "SLIDE"),
            "title": s.get("title", ""),
            "content": s.get("content", "")
        })
    return styled_slides