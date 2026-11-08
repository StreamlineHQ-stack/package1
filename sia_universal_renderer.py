# sia_universal_renderer.py • Universal Procedural Renderer based on OpenAI Vision AI Design Intent JSON Spec
import textwrap

def build_universal_deck(deck, intent_spec=None):
    if intent_spec is None:
        intent_spec = {
            "design_style": "minimal editorial",
            "visual_mood": ["clean", "professional"],
            "palette": [
                {"name": "background", "hex": "#111827", "role": "background"},
                {"name": "accent", "hex": "#fde047", "role": "accent"},
                {"name": "text", "hex": "#ffffff", "role": "text"}
            ],
            "composition": {"layout": "balanced"}
        }
    
    # Extract palette dynamically from Max's Vision JSON spec
    palette = intent_spec.get("palette", [])
    bg_color = "#111827"
    accent_color = "#fde047"
    text_color = "#ffffff"
    
    for color in palette:
        role = str(color.get("role", "")).lower()
        hex_val = color.get("hex", "")
        if "background" in role or "bg" in role:
            bg_color = hex_val
        elif "accent" in role or "primary" in role:
            accent_color = hex_val
        elif "text" in role:
            text_color = hex_val
            
    # Fallback if roles aren't explicitly named
    if not bg_color and len(palette) > 0:
        bg_color = palette[0].get("hex", "#111827")
    if not accent_color and len(palette) > 1:
        accent_color = palette[1].get("hex", "#fde047")
    if not text_color and len(palette) > 2:
        text_color = palette[2].get("hex", "#ffffff")

    style = str(intent_spec.get("design_style", "editorial")).lower()
    is_bold = "streetwear" in style or "bold" in style or "high-impact" in style
    active_font = "'Impact', 'Arial Black', sans-serif" if is_bold else "'Georgia', serif"
    
    moods = intent_spec.get("visual_mood", ["Editorial"])
    mood_str = " • ".join(moods).upper() if isinstance(moods, list) else str(moods).upper()

    styled = []
    total = len(deck)

    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))

        html = textwrap.dedent(f"""
        <div style="position: relative; width: 100%; max-width: 580px; height: 580px; margin: 0 auto; border-radius: 24px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7); background: {bg_color}; font-family: {active_font}; display: flex; flex-direction: column; justify-content: space-between; padding: 45px 36px; box-sizing: border-box; text-align: center; color: {text_color};">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 11px; letter-spacing: 2px; font-weight: 800; color: {accent_color}; text-transform: uppercase; font-family: sans-serif;">
                    <div>{mood_str}</div>
                    <div>SLIDE {idx+1} OF {total} • {cat}</div>
                </div>
                <h2 style="color: {accent_color if is_bold else text_color}; font-size: {34 if is_bold else 26}px; font-weight: 900; line-height: 1.2; margin-bottom: 16px; text-transform: uppercase; letter-spacing: {1.5 if is_bold else 0}px;">
                    {title}
                </h2>
                <p style="color: #f3f4f6; font-size: 14px; line-height: 1.5; margin-bottom: 16px; font-family: sans-serif; background: rgba(0,0,0,0.25); padding: 12px 16px; border-radius: 12px; border-left: 4px solid {accent_color};">
                    {content}
                </p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; color: {accent_color}; font-size: 11px; font-weight: 800; border-top: 2px solid rgba(255,255,255,0.25); padding-top: 14px; text-transform: uppercase; letter-spacing: 1.5px; font-family: sans-serif;">
                <div>NOV 2026</div>
                <div>NIKKI'S SALON • APEXMORPH</div>
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
