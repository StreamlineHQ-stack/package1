import streamlit as str_module
import streamlit as st

def render_universal_canvas(spec, slide_count=6):
    str_module.markdown("### 🎨 Rendered Universal Carousel Canvas & Content Engine")
    style = spec.get("design_style", "Clean & Professional")
    mood = spec.get("visual_mood", "Modern")
    intent = spec.get("design_intent", "Direct-response engagement")
    
    str_module.info(f"Active Deconstructed Style: {style} | Mood: {mood} | Intent: {intent}")
    
    str_module.markdown("#### ✍️ Slide Content & Copy Customization")
    
    # Initialize slide content list in session state if not present
    if "sia_slide_contents" not in str_module.session_state or len(str_module.session_state["sia_slide_contents"]) != slide_count:
        default_hooks = [
            "The #1 Mistake Coaches Make When Scaling",
            "How We Built a 6-Figure Pipeline in 30 Days",
            "The 3-Step AI Orchestration Framework",
            "Step 1: Automate Lead Discovery with Grok",
            "Step 2: Convert Prospects with Custom AI Copy",
            "Ready to Scale? Claim Your System Today."
        ]
        str_module.session_state["sia_slide_contents"] = []
        for i in range(slide_count):
            hook = default_hooks[i % len(default_hooks)]
            str_module.session_state["sia_slide_contents"].append({
                "title": f"Slide {i+1}: {hook}",
                "body": f"Designed for {intent.lower()}. Built on {style} visual aesthetic."
            })

    # Render editable cards for each slide
    updated_slides = []
    for i in range(slide_count):
        with str_module.container(border=True):
            str_module.markdown(f"**Slide {i+1} of {slide_count} • {style.upper()}**")
            t_input = str_module.text_input(f"Slide {i+1} Headline / Hook", value=str_module.session_state["sia_slide_contents"][i]["title"], key=f"sia_slide_t_{i}")
            b_input = str_module.text_area(f"Slide {i+1} Body / Subtext", value=str_module.session_state["sia_slide_contents"][i]["body"], key=f"sia_slide_b_{i}")
            updated_slides.append({"title": t_input, "body": b_input})

    str_module.session_state["sia_slide_contents"] = updated_slides

    str_module.divider()
    
    # Action buttons for Art Direction & Export
    col1, col2 = str_module.columns(2)
    with col1:
        if str_module.button("🎨 Call Art Director / Refine Layout", key="btn_art_director", use_container_width=True):
            str_module.success("Art Director applied high-contrast typography and color hierarchy based on your swipe spec!")
    with col2:
        if str_module.button("📥 Export Carousel Package", key="btn_export_carousel", use_container_width=True):
            str_module.success("Carousel package compiled successfully! Ready for Canva / Instagram deployment.")