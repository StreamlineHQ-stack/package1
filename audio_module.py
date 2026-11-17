import streamlit as st
import os
import wave
import struct
import math

def render_audio_manager():
    st.markdown("### 🎵 Slide Audio & Voiceover Engine")
    st.info("Manage background tracks, voiceovers, and psych-acoustic frequency beds for your export bundle.")
    
    # --- PSYCH-ACOUSTIC FREQUENCY GENERATOR ---
    with st.expander("🧠 Psych-Acoustic Frequency Generator", expanded=True):
        st.write("Synthesize custom frequency tones designed for specific direct-response psychological triggers.")
        
        psycho_goal = st.selectbox(
            "Select Psychological Effect:",
            [
                "Scroll-Stopping Alert (528Hz High-Clarity Tone)",
                "Problem Tension & Urgency (Dissonant Pulse)",
                "Authoritative Solution Bed (136.1Hz Harmonic Omega)",
                "High-Conversion CTA Pulse (Staccato Tick)"
            ],
            key="psycho_goal_select"
        )
        
        if st.button("⚡ Synthesize Psych-Tone (.wav)", key="btn_gen_psycho_audio"):
            filename = "psych_tone_active.wav"
            sample_rate = 44100
            duration = 3.0  # seconds
            
            if "Scroll-Stopping" in psycho_goal:
                target_freq, mod_factor = 528.0, 1.0
            elif "Tension" in psycho_goal:
                target_freq, mod_factor = 220.0, 8.0
            elif "Authoritative" in psycho_goal:
                target_freq, mod_factor = 136.1, 0.5
            else:
                target_freq, mod_factor = 432.0, 4.0

            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                
                for i in range(int(sample_rate * duration)):
                    t = i / sample_rate
                    envelope = min(t * 5.0, 1.0) * min((duration - t) * 5.0, 1.0)
                    val_raw = math.sin(2.0 * math.pi * target_freq * t)
                    if mod_factor > 1.0:
                        val_raw *= (0.5 + 0.5 * math.sin(2.0 * math.pi * mod_factor * t))
                        
                    value = int(32767.0 * 0.4 * envelope * val_raw)
                    data = struct.pack('<h', value)
                    wav_file.writeframes(data)
                    
            st.success(f"✅ Generated `{filename}` tuned for: {psycho_goal}")

    st.markdown("---")
    
    audio_source = st.radio(
        "Select Audio Source:",
        ["Upload Custom MP3/WAV", "Use Local Workspace Audio", "None (Silent Export)"],
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
    elif "Use Local Workspace" in audio_source:
        local_audio_files = [f for f in os.listdir(".") if f.endswith((".mp3", ".wav"))]
        if local_audio_files:
            selected_local = st.selectbox("Select local audio file:", local_audio_files, key="local_audio_select")
            audio_path = selected_local
            audio_mode_label = f"Local File: {selected_local}"
        else:
            st.warning("No local audio files found. Synthesize one using the generator above!")
    
    st.session_state["audio_brief"] = {
        "mode": audio_mode_label,
        "path": audio_path
    }
    
    if audio_path and os.path.exists(audio_path):
        st.markdown("#### 🎧 Audio Preview")
        st.audio(audio_path)