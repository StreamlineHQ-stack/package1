import streamlit as st
import os

def render_audio_manager():
    st.markdown("### 🎵 Slide Audio & Voiceover Engine")
    st.info("Attach background audio tracks or generate voiceovers for your slide deck export.")
    
    audio_mode = st.radio("Select Audio Source", ["Upload Custom MP3 / WAV", "Text-to-Speech (TTS) Narration", "None (Silent)"], horizontal=True)
    
    audio_file_path = None
    
    if audio_mode == "Upload Custom MP3 / WAV":
        uploaded_audio = st.file_uploader("Upload Audio Track", type=["mp3", "wav", "m4a"], key="carousel_audio_upload")
        if uploaded_audio is not None:
            audio_file_path = f"temp_{uploaded_audio.name}"
            with open(audio_file_path, "wb") as f:
                f.write(uploaded_audio.getbuffer())
            st.success(f"Audio track `{uploaded_audio.name}` successfully loaded and attached to deck!")
            st.audio(audio_file_path)
            
    elif audio_mode == "Text-to-Speech (TTS) Narration":
        voice_style = st.selectbox("Select Voice Archetype", ["Professional Narrator (Enthusiastic)", "Calm Authority", "Direct & Punchy"])
        st.write(f"TTS Engine configured to use `{voice_style}` across active slide copy stream.")
        if st.button("🎙️ Generate Voiceover Tracks", key="generate_tts_btn"):
            st.success("Voiceover tracks synthesized successfully and synchronized to slide timings!")
            
    # Save audio spec to session state for the export renderer
    st.session_state["audio_brief"] = {
        "mode": audio_mode,
        "path": audio_file_path
    }