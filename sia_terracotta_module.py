# sia_terracotta_module.py • Isolated Module 1: Terracotta Background & White Font (Fully Baked Deck)
def build_terracotta_deck(preview_deck):
    styled_slides = []
    for idx, s in enumerate(preview_deck):
        # Fully baked HTML card payload for Terracotta editorial theme
        baked_card_html = f"""
        <div style="background-color: #a85732; color: #FFFFFF; padding: 35px; border-radius: 16px; margin-top: 15px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.22); font-family: Arial, sans-serif;">
            <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1.8px; opacity: 0.85; margin-bottom: 12px;">
                Slide {idx + 1} • {s.get('category', 'SLIDE')}
            </div>
            <div style="font-size: 13px; font-weight: bold; opacity: 0.95; margin-bottom: 16px; background: rgba(0,0,0,0.2); padding: 6px 14px; border-radius: 6px; display: inline-block;">
                Solid Terracotta Editorial Backdrop
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
            "style": "Terracotta Background & White Font",
            "rendered_html": baked_card_html
        })
        
    return styled_slides