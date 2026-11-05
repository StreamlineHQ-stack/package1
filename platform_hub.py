import streamlit as st
import base64
from background_engine import get_modular_background

st.set_page_config(page_title="ApexMorph Platform Hub", layout="wide")

st.sidebar.title("Enhanced Background & Visual Style Engine")
style_mode = st.sidebar.radio(
    "Style Mode Control:",
    [
        "🎯 Smart AI Contextual Match",
        "🏛️ Unified Editorial Motif",
        "📂 Custom User Images",
        "☕ Terracotta Background & White Font"
    ]
)

motif_choice = ""
uploaded_b64 = ""

if style_mode == "🏛️ Unified Editorial Motif":
    motif_choice = st.sidebar.text_input("Enter Motif Theme (e.g., shoes, train, cityscape, urban):", value="cityscape")

if style_mode == "📂 Custom User Images":
    uploaded_file = st.sidebar.file_uploader("Upload Reference Asset", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            if bytes_data:
                uploaded_b64 = base64.b64encode(bytes_data).decode("utf-8")
        except Exception as e:
            st.sidebar.error(f"Upload error: {e}")

# Example slide rendering loop demonstration
slide_count = 6
for i in range(slide_count):
    slide_tag = f"SLIDE {i+1} • HOOK" if i == 0 else f"SLIDE {i+1} • SECTION"
    
    # Resolve background safely using the bulletproof background engine
    bg_url = get_modular_background(
        style_mode=style_mode,
        motif_choice=motif_choice,
        slide_index=i,
        slide_tag=slide_tag,
        uploaded_b64=uploaded_b64
    )
    
    # Render preview card
    if bg_url:
        st.markdown(
            f"""
            <div style="background-image: url('{bg_url}'); background-size: cover; background-position: center; padding: 40px; border-radius: 12px; color: white; margin-bottom: 20px;">
                <h4>{slide_tag}</h4>
                <h3>Optimized Modular Architecture</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #c45c3d; padding: 40px; border-radius: 12px; color: white; margin-bottom: 20px;">
                <h4>{slide_tag}</h4>
                <h3>Terracotta Editorial Mode</h3>
            </div>
            """,
            unsafe_allow_html=True
        )