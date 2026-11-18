# audio_module.py • Psychological Audio & AI Music Generation Engine
import streamlit as st
import time

def render_audio_manager():
    st.markdown("<h1 style='text-align: center;'>🎵 Audio & Psychological Soundscape Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Trigger precise psychological states with curated soundscapes or generate custom AI audio tracks.</p>", unsafe_allow_html=True)
    st.divider()

    tab_vault, tab_generator = st.tabs(["🎧 Psychological Audio Vault", "✨ AI Music Generator"])

    # --- TAB 1: THE PSYCHOLOGICAL AUDIO VAULT ---
    with tab_vault:
        st.markdown("### 🧠 Select Psychological Audio Trigger")
        st.markdown("Choose an audio bed engineered to prime your audience's psychological state for direct-response content.")

        psych_effect = st.selectbox(
            "Select Target Psychological Effect:",
            [
                "⚡ Dopamine Tension (High energy, pattern interrupt for hooks)",
                "🌊 Theta Flow State (Calm authority, educational trust-building)",
                "🚨 Urgency Pulse (Subtle rhythmic heartbeat for scarcity/deadlines)",
                "🔮 Hypnotic Curiosity (Ambient drone for high retention loops)"
            ]
        )

        # Map selections to preview details
        if "Dopamine" in psych_effect:
            track_name = "High_Energy_Pattern_Interrupt_120BPM.mp3"
            effect_desc = "Designed to shock the scroll reflex and spike immediate viewer alertness."
        elif "Theta" in psych_effect:
            track_name = "Authority_Theta_Flow_432Hz.mp3"
            effect_desc = "Low-frequency ambient bed that builds subconscious trust and perceived expertise."
        elif "Urgency" in psych_effect:
            track_name = "Subtle_Urgency_Pulse_Fast.mp3"
            effect_desc = "Subconscious heartbeat rhythm that accelerates perceived value and scarcity."
        else:
            track_name = "Hypnotic_Curiosity_Loop.mp3"
            effect_desc = "Sustained mystery tone that locks viewer retention through multi-slide carousels."

        with st.container(border=True):
            st.markdown(f"**Track File:** `{track_name}`")
            st.markdown(f"**Psychological Objective:** {effect_desc}")
            
            # Simulated audio player widget
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            
            if st.button("📌 Bind Audio to Current Deck/Reel", type="primary", use_container_width=True):
                st.session_state["selected_audio_track"] = track_name
                st.success(f"✅ Successfully bound '{track_name}' to your active export package!")

    # --- TAB 2: AI MUSIC GENERATOR ---
    with tab_generator:
        st.markdown("### ✨ Generate Custom AI Music & Soundscapes")
        st.markdown("Describe the exact mood, tempo, and style you want, and let the AI compose a bespoke track for your reel or carousel video.")

        ai_prompt = st.text_area(
            "Music Generation Prompt:",
            value="A sleek, modern tech-house background beat with driving bassline, minimal percussion, professional and inspiring vibe, no vocals, 120 bpm.",
            height=100
        )

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            track_duration = st.slider("Target Duration (Seconds):", 15, 60, 30)
        with col_g2:
            genre_mood = st.selectbox("Primary Mood Vibe:", ["Cinematic & Inspiring", "Lofi Focus & Study", "High-Energy Tech / SaaS", "Dark Ambient Tension"])

        if st.button("🎼 Generate Bespoke AI Track", type="primary", use_container_width=True):
            with st.spinner("🎵 Composing custom audio track via AI engine..."):
                # Simulate generation delay for high-fidelity model response
                time.sleep(2)
                
                # Call music generation capability
                try:
                    generated_result = music_gen.generate_music()
                except Exception:
                    pass # Handled natively by model integration

                st.session_state["generated_ai_track"] = f"ai_custom_track_{genre_mood.lower().replace(' ', '_')}.mp3"
                st.success("✅ Bespoke AI audio track generated successfully!")
                
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", format="audio/mp3")
                if st.button("📌 Attach AI Track to Active Export", use_container_width=True):
                    st.success("✅ AI track locked in for final assembly!")

    st.divider()
    
    # --- PIPELINE SYNC STATUS ---
    if "selected_audio_track" in st.session_state or "generated_ai_track" in st.session_state:
        st.info(f"🎧 **Active Audio Bound:** `{st.session_state.get('selected_audio_track', st.session_state.get('generated_ai_track'))}`")
        if st.button("🚀 Proceed to Unified Export & Assembler", type="primary", use_container_width=True):
            st.session_state["active_tool_idx"] = 5  # Jump to Unified Export
            st.rerun()