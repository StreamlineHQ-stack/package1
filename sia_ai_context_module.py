# sia_ai_context_module.py • Isolated Module 2: Smart AI Contextual Match (Unique Images per Slide & Clean Header)
def build_ai_context_deck(preview_deck):
    # Curated array of 6 completely distinct, professional Unsplash background imagery assets
    unique_image_pool = [
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1080&q=80", # Slide 1: Analytics / Data
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1080&q=80", # Slide 2: Executive / Strategy
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1080&q=80", # Slide 3: Workspace / Planning
        "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1080&q=80", # Slide 4: Growth / Metrics
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1080&q=80", # Slide 5: Digital Marketing
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1080&q=80"  # Slide 6: Team Collaboration
    ]

    styled_slides = []
    for idx, s in enumerate(preview_deck):
        # Assign a strictly unique image based on slide index (loops safely if deck exceeds 6 slides)
        img_url = unique_image_pool[idx % len(unique_image_pool)]

        # Fully baked HTML card payload with clean header (No debug metadata text)
        baked_card_html = f"""
        <div style="background-color: #111827; color: #F9FAFB; padding: 35px; border-radius: 16px; margin-top: 15px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.22); font-family: Arial, sans-serif;">
            <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1.8px; opacity: 0.85; margin-bottom: 12px;">
                Slide {idx + 1} • {s.get('category', 'SLIDE')}
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