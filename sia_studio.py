# sia_studio.py • Style Inspiration & Analysis Studio
import json
import base64
import io
import os
import streamlit as st
from PIL import Image

def render_sia_studio():
    st.markdown("<h1 style='text-align: center;'>🎨 Style Inspiration & Analysis Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Analyze high-converting social media slide aesthetics and feed them directly into the Carousel & Kinetic engines.</p>", unsafe_allow_html=True)
    
    # Sample default slides data if not present
    if "sia_slides_data" not in st.session_state:
        st.session_state["sia_slides_data"] = [
            {"badge": "SLIDE 1 | HOOK", "title": "Unlock the Secret to Skyrocketing Sales", "body": "Most founders struggle with positioning."},
            {"badge": "SLIDE 2 | THE MYTH", "title": "The Silent Killer of Your Business Growth", "body": "Ignoring conversion rate optimization."},
            {"badge": "SLIDE 3 | STRATEGY", "title": "Craft Messages That Resonate", "body": "Speak directly to customer pain points."},
            {"badge": "SLIDE 4 | SOLUTION", "title": "Turn Browsers into Buyers", "body": "Optimize every friction point above the fold."},
            {"badge": "SLIDE 5 | FRAMEWORK", "title": "Build Trust and Credibility", "body": "Use verifiable metrics instead of fluff."},
            {"badge": "SLIDE 6 | CTA", "title": "Ready to Elevate Your Copy?", "body": "Click link in bio to start scaling."}
        ]

    slides = st.session_state["sia_slides_data"]

    st.markdown("---")
    st.markdown("### ⚡ Kinetic Data Bridge & Export")
    
    col_bridge_btn, col_download_btn = st.columns(2)
    
    with col_bridge_btn:
        json_str = json.dumps(slides)
        encoded_deck = base64.urlsafe_b64encode(json_str.encode("utf-8")).decode("utf-8")
        kinetic_url = f"https://kinetic-animator.streamlit.app/?deck={encoded_deck}"
        
        st.markdown(
            f'<a href="{kinetic_url}" target="_blank">'
            f'<button style="width: 100%; background-color: #ff4b4b; color: white; padding: 12px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; text-align: center;">'
            f'🚀 Open Complete Kinetic UI (Motion Suite) ➔'
            f'</button></a>',
            unsafe_allow_html=True
        )

    with col_download_btn:
        st.download_button(
            "📥 Download Deck JSON", 
            data=json.dumps(slides, indent=2), 
            file_name="sia_carousel_deck.json", 
            mime="application/json", 
            use_container_width=True,
            key="sia_download_json"
        )
