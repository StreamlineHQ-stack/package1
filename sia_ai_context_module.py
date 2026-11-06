# sia_ai_context_module.py • Isolated Module 2: Smart AI Contextual Match
def build_ai_context_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        text_blob = (s.get("category", "") + " " + s.get("title", "") + " " + s.get("content", "")).lower()
        
        # Comprehensive semantic & keyword asset matching
        matched_img = "🖼️ Visual Asset: Editorial Minimalist Focal Point"
        if "hook" in text_blob or "why" in text_blob or "flat" in text_blob or "ads" in text_blob:
            matched_img = "🎯 Visual Asset: High-Impact Attention Magnet & Core Hook Target"
        elif "problem" in text_blob or "cost" in text_blob or "poor" in text_blob or "hidden" in text_blob:
            matched_img = "⚠️ Visual Asset: Friction Point & Diagnostic Leak Analysis"
        elif "solution" in text_blob or "craft" in text_blob or "art" in text_blob or "system" in text_blob:
            matched_img = "⚙️ Visual Asset: Step-by-Step Blueprint & Mechanism Framework"
        elif "growth" in text_blob or "scale" in text_blob or "roi" in text_blob or "pay" in text_blob:
            matched_img = "📈 Visual Asset: Upward Escalation & Revenue Milestone Chart"
        elif "cta" in text_blob or "comment" in text_blob or "ready" in text_blob:
            matched_img = "🚀 Visual Asset: Direct-Response Action Banner & Conversion Trigger"
            
        styled_slides.append({
            "card_num": idx + 1,
            "style": "Smart AI Contextual Match",
            "bg_color": "#111827",
            "font_color": "#F9FAFB",
            "accent_bg": "rgba(37, 99, 235, 0.25)",
            "imagery": matched_img,
            "category": s.get("category", "SLIDE"),
            "title": s.get("title", ""),
            "content": s.get("content", "")
        })
    return styled_slides