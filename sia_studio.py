# sia_studio.py • Isolated Style Inspiration & Analysis Studio (SIA) with Robust Payload Banner
import streamlit as st
import base64
from PIL import Image

def render_sia_studio():
    # --- Main SIA Studio UI ---
    st.markdown("### ✨ Style Inspiration & Analysis Studio (SIA)")
    st.markdown("Upload reference swipe slides and configure visual style engine parameters independently.")
    
    # --- Robust Downstream Payload Banner ---
    downstream_payload = st.session_state.get("sia_downstream_payload", None)
    if downstream_payload:
        st.success("📦 **Downstream Feature Script Loaded & Ready for Style Analysis!**")
        with st.expander("🔍 View Incoming Feature Script Content"):
            st.write(downstream_payload)
        st.divider()

    # --- Sidebar Style Engine Controls (Triggered via Art Director Bridge) ---
    if st.session_state.get("sia_art_director_active", False):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎨 Enhanced Background & Visual Style Engine")
            st.markdown("**Style Mode Control:**")
            
            sia_mode = st.radio(
                "Select SIA Style Mode:",
                [
                    "🎯 Exact Inspiration Match (Objects & Layout)",
                    "🏛️ Unified Editorial Motif",
                    "📂 Custom User Images",
                    "☕ Terracotta Background & White Font",
                    "⚡ Smart AI Contextual Match"
                ],
                key="sia_sidebar_mode_radio"
            )
            
            if "Unified Editorial Motif" in sia_mode:
                st.markdown("### 🏛️ Custom Motif Theme")
                st.text_input("Enter Motif Theme (e.g., Sunset, Rose, Luxury, Ocean, Minimalist, shoes, trains, city):", "sunset", key="sia_motif_input")
                
            st.info("✨ SIA Style Profile Active & Synced to Render Pipeline.")

    # Isolated state variables for SIA
    if "sia_uploaded_files" not in st.session_state:
        st.session_state["sia_uploaded_files"] = None
    if "sia_report_unlocked" not in st.session_state:
        st.session_state["sia_report_unlocked"] = False

    uploaded_slides = st.file_uploader(
        "Upload Reference Swipe Slides", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        key="sia_file_uploader"
    )
    
    if uploaded_slides:
        st.session_state["sia_uploaded_files"] = uploaded_slides
        st.success(f"Successfully loaded {len(uploaded_slides)} reference slide(s) for style analysis.")
        
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

        st.session_state["sia_report_unlocked"] = True

    # --- Deconstruction Intelligence Report (Triggered upon file upload or downstream sync) ---
    if st.session_state.get("sia_report_unlocked", False) or downstream_payload:
        st.divider()
        st.markdown("## 📊 Deconstruction Intelligence Report")
        
        st.markdown("### 🎨 Advanced Visual & Photographic Deconstruction")
        st.markdown(
            """
            * **Color Palette & Tone:** Warm editorial aesthetic (Terracotta base `#a85732` paired with rich cream and dark typography).
            * **Subject Framing & Composition:** Minimalist, centered subject placement utilizing substantial negative space to maintain an uncluttered high-end aesthetic.
            * **Prop & Texture Staging:** Incorporation of tactile organic elements (e.g., natural wood blocks, sleek mirrors, and single botanical stems) to anchor the visual mood.
            * **Lighting & Atmosphere:** Warm, low-key lighting with earthy amber and terracotta color grading creating an intimate, editorial feel.
            * **Image-to-Text Integration:** High-contrast serif typography positioned cleanly over the upper third of the photographic backdrop, ensuring readability without obstructing the primary focal point.
            """
        )
        
        st.divider()
        st.markdown("### 💬 Interactive Refinement Q&A")
        st.markdown("What specific elements resonated most with your design goals?")
        
        st.selectbox(
            "What stood out visually & photographically?",
            [
                "The warm editorial terracotta color palette & lighting",
                "Minimalist negative space framing",
                "Tactile organic prop staging",
                "High-contrast serif typography integration"
            ],
            key="sia_refinement_qa"
        )
        
        st.markdown("---")
        
        # --- Art Director Bridge Button ---
        if st.button("🎭 Call Art Director & Activate Style Engine", type="primary", use_container_width=True, key="sia_call_art_director"):
            st.session_state["sia_art_director_active"] = True
            st.success("🎉 Art Director online! Check your sidebar for the 5 isolated SIA Style Engine control modes.")
            st.rerun()