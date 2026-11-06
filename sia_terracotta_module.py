# sia_terracotta_module.py • Isolated Module 1: Terracotta Background & White Font
def build_terracotta_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        styled_slides.append({
            "card_num": idx + 1,
            "style": "Terracotta Background & White Font",
            "bg_color": "#a85732",
            "font_color": "#FFFFFF",
            "accent_bg": "rgba(0,0,0,0.2)",
            "imagery": "Solid Terracotta Editorial Backdrop",
            "category": s.get("category", "SLIDE"),
            "title": s.get("title", ""),
            "content": s.get("content", "")
        })
    return styled_slides