# assembly_module.py • Multi-Platform Staging & Relay Hub
import streamlit as st
import io
import zipfile
from telegram_relay import send_to_telegram
from calendar_bridge import render_calendar_scheduler

def render_unified_assembler():
    st.markdown("<h1 style='text-align: center;'>🎬 Unified Multi-Platform Export & Staging Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Customer Zero (Apex) Distribution Engine • Zero-Risk Multi-Channel Handoff</p>", unsafe_allow_html=True)
    st.divider()

    # --- 1. PLATFORM TARGET SELECTION ---
    st.markdown("### 🌐 Select Target Distribution Channels")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        target_ig = st.checkbox("Instagram (Reel/Carousel)", value=True)
    with col_p2:
        target_li = st.checkbox("LinkedIn (Text/Image)", value=True)
    with col_p3:
        target_tk = st.checkbox("TikTok (Vertical Video)", value=False)
    with col_p4:
        target_x = st.checkbox("X / Twitter (Thread)", value=False)

    st.divider()

    # --- 2. CAPTION & METADATA TAILORING ---
    st.markdown("### ✍️ Master Caption & Payload Vault")
    
    default_title = "Scale Your Coaching Business with Automated Systems"
    default_caption = (
        "🚀 Stop trading time for manual client delivery. "
        "When you package your expertise into automated micro-assets and repeatable systems, "
        "your revenue scales while your hours drop.\n\n"
        "Here is the exact framework to transition from a manual operator to an automated digital business model.\n\n"
        "#CreatorSuite #BusinessAutomation #DigitalProducts #Scaling"
    )

    deck_title = st.text_input("Asset Campaign Title:", value=default_title)
    deck_caption = st.text_area("Optimized Caption & Hashtags:", value=default_caption, height=140)

    st.divider()

    # --- 3. PHYSICAL CALENDAR SCHEDULING (CUSTOMER ZERO) ---
    render_calendar_scheduler(deck_title, deck_caption)

    st.divider()

    # --- 4. DISPATCH TO STAGING RELAY ---
    st.markdown("### 🚀 Execute Staging & Mobile Handoff")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        if st.button("📤 Push to Private Telegram Relay", type="primary", use_container_width=True):
            # Compile selected platforms string
            selected_channels = []
            if target_ig: selected_channels.append("Instagram")
            if target_li: selected_channels.append("LinkedIn")
            if target_tk: selected_channels.append("TikTok")
            if target_x: selected_channels.append("X")
            
            full_payload = f"🎯 **Targets:** {', '.join(selected_channels)}\n\n{deck_caption}"
            
            success, msg = send_to_telegram(caption=full_payload)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")
                
    with col_d2:
        # Generate Master Asset Bundle Download
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("campaign_metadata.txt", f"TITLE: {deck_title}\n\nCAPTION:\n{deck_caption}\n\nCHANNELS: IG, LI, TK, X")
        zip_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Master Multi-Platform ZIP",
            data=zip_buffer,
            file_name="apex_master_campaign_bundle.zip",
            mime="application/zip",
            use_container_width=True
        )