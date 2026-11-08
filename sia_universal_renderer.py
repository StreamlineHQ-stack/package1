import streamlit as st

def render_universal_canvas(spec, slide_count=6):
    st.markdown("### 🎨 Rendered Universal Carousel Canvas")
    style = spec.get("design_style", "Clean & Professional")
    mood = spec.get("visual_mood", "Modern")
    
    st.info(f"Rendering {slide_count} slides using Style: {style} | Mood: {mood}")
    
    # Render interactive mock slides
    for i in range(1, slide_count + 1):
        with st.container(border=True):
            st.markdown(f"**Slide {i} of {slide_count} • {style.upper()}**")
            st.markdown(f"### Hook & Core Message for Slide {i}")
            st.markdown(f"*Design Intent / Visual Brief:* {spec.get('design_intent', 'High-converting layout')} style framework.")