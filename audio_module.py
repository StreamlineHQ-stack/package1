import streamlit as st
import os
import wave
import struct
import math

def render_audio_manager():
    st.markdown("### 🎵 Slide Audio & Voiceover Engine")
    st.info("Manage background tracks, voiceovers, and text-to-speech synchronization for your export bundle.")
    
    # --- AUTOMATED TEST AUDIO GENERATOR ---
    with st.expander("🛠️ Quick Test Audio Generator", expanded=False):
        st.write("Click below to instantly create a test audio file right in your workspace without using the command line.")
        if st.button("⚡ Generate Test Audio (.wav)", key="btn_gen_test_audio"):
            filename = "test_voiceover.wav"
            sample_rate = 44100
            duration = 3.0  # seconds
            frequency = 440.0  # A4 note tone
            
            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(1) # Mono
                wav_file.setsampwidth(2) # 2 bytes per sample
                wav_file.setframerate(sample_rate)
                
                for i in range(int(sample_rate * duration)):
                    value = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
                    data = struct.pack('<h', value)
                    wav_file.writeframes(data)
                    
            st.success(f"✅ Successfully generated `{filename}`! You can now select it below.")
    
    st.markdown("---")
    
    # Audio Selection Mode
    audio_source = st.radio(
        "Select Audio Source:",
        ["Upload Custom MP3/WAV", "Use Local Workspace Audio (e.g. test_voiceover.wav)", "None (Silent Export)"],
        key="audio_source_mode"
    )
    
    audio_path = None
    audio_mode_label = "None (Silent)"
    
    if "Upload Custom" in audio_source:
        uploaded_audio = st.file_uploader("Upload audio track (MP3/WAV)", type=["mp3", "wav"], key="custom_audio_uploader")
        if uploaded_audio is not None:
            audio_path = f"temp_{uploaded_audio.name}"
            with open(audio_path, "wb") as f:
                f.write(uploaded_audio.getvalue())
            audio_mode_label = f"Custom Upload: {uploaded_audio.name}"
            st.success(f"Audio file loaded: {uploaded_audio.name}")
            
    elif "Use Local Workspace" in audio_source:
        # Check for local audio files in the directory
        local_audio_files = [f for f in os.listdir(".") if f.endswith((".mp3", ".wav"))]
        if local_audio_files:
            selected_local = st.selectbox("Select local audio file:", local_audio_files, key="local_audio_select")
            audio_path = selected_local
            audio_mode_label = f"Local File: {selected_local}"
            st.info(f"Using local file: {selected_local}")
        else:
            st.warning("No local audio files found. Expand the 'Quick Test Audio Generator' above and click generate!")
    else:
        audio_mode_label = "None (Silent)"
        st.info("Export will be generated without background audio.")

    # Save choice to session state for the Unified Assembler
    st.session_state["audio_brief"] = {
        "mode": audio_mode_label,
        "path": audio_path
    }
    
    if audio_path and os.path.exists(audio_path):
        st.markdown("#### 🎧 Audio Preview")
        st.audio(audio_path)