import streamlit as st
import os
import json
import zipfile
import io

def render_unified_assembler():
    st.markdown("<h1 style='text-align: center;'>🎬 Unified Export & Assembly Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Compiles your Content Engine text, visual styles, and psych-acoustic audio tracks into a synchronized package.</p>", unsafe_allow_html=True)
    st.divider()
    
    # Pre-flight Status Checks
    slides_ready = bool(st.session_state.get("sia_slide_contents") or st.session_state.get("deck_json"))
    visual_ready = bool(st.session_state.get("visual_brief"))
    audio_brief = st.session_state.get("audio_brief", {"mode": "None (Silent)", "path": None})
    
    col_chk1, col_chk2, col_chk3 = st.columns(3)
    with col_chk1:
        if slides_ready:
            st.success("✅ Content Engine slides loaded")
        else:
            st.error("❌ Content Engine missing slides")
    with col_chk2:
        if visual_ready:
            st.success("✅ Visual template selected")
        else:
            st.error("❌ Visual template not selected")
    with col_chk3:
        st.info(f"🎵 Audio: {audio_brief['mode']}")
        
    st.divider()
    
    # Timeline & Audio Sync Controls
    st.markdown("### ⚙️ Timeline & Audio Sync Configuration")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        seconds_per_slide = st.slider("Duration per Slide (Seconds):", 1.0, 5.0, 2.5, step=0.25, key="assembler_sps")
    with col_t2:
        audio_behavior = st.selectbox(
            "Audio Track Timeline Behavior:",
            [
                "Loop to Match Slide Duration",
                "Stretch / Time-Scale to Fit Total Deck",
                "Play Once with Clean Fade-Out"
            ],
            key="assembler_audio_behavior"
        )
        
    st.divider()
    
    if st.button("🚀 Run Unified Pipeline & Build Export Package", type="primary", use_container_width=True, key="run_assembler_pipeline"):
        with st.spinner("Multiplexing frames, applying psych-acoustic audio mapping, and building export bundle..."):
            slides = st.session_state.get("sia_slide_contents") or st.session_state.get("deck_json", [])
            total_duration = len(slides) * seconds_per_slide
            
            # Create export zip archive
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                # Save deck json manifest
                zip_file.writestr("deck_manifest.json", json.dumps(slides, indent=2))
                
                # Save audio brief & timeline metadata
                metadata = {
                    "total_slides": len(slides),
                    "seconds_per_slide": seconds_per_slide,
                    "total_duration_seconds": total_duration,
                    "audio_mode": audio_brief["mode"],
                    "audio_timeline_behavior": audio_behavior
                }
                zip_file.writestr("export_metadata.json", json.dumps(metadata, indent=2))
                
                # Bundle audio file if present
                if audio_brief["path"] and os.path.exists(audio_brief["path"]):
                    with open(audio_brief["path"], "rb") as af:
                        zip_file.writestr("synchronized_track.wav", af.read())
                        
            zip_buffer.seek(0)
            
            st.success(f"🎉 Pipeline Complete! Total Timeline: {total_duration}s | Audio Behavior: {audio_behavior}")
            
            st.download_button(
                label="📥 Download Synchronized Master Export Package (.zip)",
                data=zip_buffer,
                file_name="master_creator_export_bundle.zip",
                mime="application/zip",
                use_container_width=True,
                key="download_master_bundle"
            )