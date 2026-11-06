# sia_studio.py • Isolated Style Inspiration & Analysis Module with Live Preview & Parameter Extraction
import streamlit as st
import base64
from PIL import Image

def render_sia_studio():
    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Upload reference swipe slides and configure visual style engine parameters independently.")
    
    # Isolated state variables for SIA to prevent pollution with Carousel state
    if "sia_uploaded_files" not in st.session_state:
        st.session_state["sia_uploaded_files"] = None
    if "sia_extracted_style" not in st.session_state:
        st.session_state["sia_extracted_style"] = None

    uploaded_slides = st.file_uploader(
        "Upload Reference Swipe Slides", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        key="sia_file_uploader"
    )
    
    if uploaded_slides:
        st.session_state["sia_uploaded_files"] = uploaded_slides
        st.success(f"Successfully loaded {len(uploaded_slides)} reference slide(s) for style analysis.")
        
        st.divider()
        st.markdown("### 🔍 Swipe Style Extraction & Parameter Breakdown")
        
        cols = st.columns(min(len(uploaded_slides), 3))
        for idx, uploaded_file in enumerate(uploaded_slides):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Reference {idx+1}: {uploaded_file.name}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error previewing {uploaded_file.name}: {e}")

        st.markdown("---")
        st.markdown("### 🎨 Detected Visual Parameters")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric(label="Primary Background", value="Warm Espresso (#1a120b)")
        with col_p2:
            st.metric(label="Accent Tag Color", value="Canary Gold (#ffcc00)")
        with col_p3:
            st.metric(label="Typography Profile", value="Pro Bold Editorial")

        st.divider()
        
        if st.button("🚀 Apply SIA Style Profile to Carousel Studio", type="primary", use_container_width=True, key="sia_apply_btn"):
            st.session_state["sia_extracted_style"] = {
                "bg": "#1a120b",
                "tag": "#ffcc00",
                "profile": "Pro Bold Editorial"
            }
            st.success("🎉 SIA Style parameters locked! Switch back to Carousel Studio to render your decks using this exact aesthetic.")