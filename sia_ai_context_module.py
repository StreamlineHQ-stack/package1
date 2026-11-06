# sia_ai_context_module.py • Isolated Module 2: Smart AI Contextual Match
def build_ai_context_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        text_blob = (s.get("title", "") + " " + s.get("content", "")).lower()
        
        # Contextual mapping rules (ready for API integration)
        matched_img = "🧠 AI Contextual Graphic Match"
        if "focus" in text_blob or "target" in text_blob:
            matched_img = "🎯 Bulls-eye Precision Target Graphic"
        elif "long" in text_blob or "road" in text_blob or "journey" in text_blob:
            matched_img = "🌉 Winding Bridge & Horizon Road"
        elif "growth" in text_blob or "scale" in text_blob:
            matched_img = "📈 Upward Escalation Vector"
        elif "protect" in text_blob or "joint" in text_blob:
            matched_img = "🛡️ Ergonomic Protection Shield"
            
        styled_slides.append({
            "card_num": idx + 1,
            "style": "Smart AI Contextual Match",
            "bg_color": "#1E293B",
            "font_color": "#F8FAFC",
            "accent_bg": "rgba(59, 130, 246, 0.2)",
            "imagery": matched_img,
            "category": s.get("category", "SLIDE"),
            "title": s.get("title", ""),
            "content": s.get("content", "")
        })
    return styled_slides