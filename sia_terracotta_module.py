# sia_terracotta_module.py • Dynamic Terracotta / Swipe Deconstruction Deck Builder
import textwrap

def build_terracotta_deck(deck, report=None):
    if report is None:
        report = {
            "mood": "Bold Editorial",
            "bg_color": "#a85732",
            "sub_color": "#fde047",
            "text_color": "#ffffff",
            "font_family": "Georgia, serif"
        }
    
    bg_color = report.get("bg_color", "#a85732")
    sub_color = report.get("sub_color", "#fde047")
    text_color = report.get("text_color", "#ffffff")
    font_family = report.get("font_family", "Georgia, serif")
    
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        html = textwrap.dedent(f"""
        <div style="width: 100%; max-width: 580px; height: 580px; margin: 0 auto; border-radius: 24px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7); background: {bg_color}; font-family: {font_family}; display: flex; flex-direction: column; justify-content: space-between; padding: 50px 36px; box-sizing: border-box; text-align: center; color: {text_color};">
            <div>
                <div style="color: {sub_color}; font-size: 11px; font-weight: 800; letter-spacing: 2px; margin-bottom: 16px; text-transform: uppercase; font-family: sans-serif;">
                    SLIDE {idx+1} OF {total} • {cat}
                </div>
                <h2 style="color: {text_color}; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 18px;">
                    {title}
                </h2>
                <p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; margin-bottom: 20px; font-family: sans-serif;">
                    {content}
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; color: #e2e8f0; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 16px; text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif;">
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
