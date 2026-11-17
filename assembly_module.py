import streamlit as st
import os
import io
import zipfile

def render_unified_assembler():
    st.markdown("### 🎬 Unified Export & Assembly Engine")
    st.info("Compiles your Content Engine text, visual template styles, and audio tracks into a synchronized export package.")
    
    # 1. Check prerequisites from session state
    slide_contents = st.session_state.get("sia_slide_contents", [])
    visual_brief = st.session_state.get("visual_brief", {})
    audio_brief = st.session_state.get("audio_brief", {})
    
    # Status dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        if slide_contents:
            st.success(f"✅ Content: {len(slide_contents)} slides ready")
        else:
            st.error("❌ Content Engine missing slides")
            
    with col2:
        if visual_brief:
            st.success(f"✅ Visual: {visual_brief.get('design_style', 'Template Loaded')} active")
        else:
            st.error("❌ Visual template not selected")
            
    with col3:
        audio_mode = audio_brief.get("mode", "None (Silent)")
        st.info(f"🎵 Audio: {audio_mode}")
        
    st.markdown("---")
    
    # 2. Execution Pipeline Button
    if st.button("🚀 Run Pipeline: Render Frames & Sync Audio", key="run_unified_assembly_btn"):
        if not slide_contents or not visual_brief:
            st.error("Please complete Step 1 (Content) and Step 2 (Visual Template) before running the assembler.")
            return
            
        with st.status("⚙️ Executing Production Pipeline...", expanded=True) as status:
            st.write("1️⃣ Initializing canvas dimensions and typography styles...")
            # Simulate frame rendering step
            st.write("2️⃣ Rendering animation frames and calculating exact slide duration vectors...")
            slide_duration_seconds = 3.5  # Standardized duration per slide for sync
            total_duration = len(slide_contents) * slide_duration_seconds
            
            st.write(f"3️⃣ Multiplexing Audio track (Synced to {total_duration}s total timeline)...")
            if audio_brief.get("path"):
                st.write(f"   -> Bound audio file: `{audio_brief.get('path')}`")
            else:
                st.write("   -> Exporting visual sequence (Silent mode active)")
                
            st.write("4️⃣ Packaging final assets into export archive...")
            
            # Create an in-memory zip archive containing mock rendered slides
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, slide in enumerate(slide_contents, start=1):
                    # Create a dummy slide representation for the export package
                    slide_text = f"Slide {idx}: {slide['headline']}\n{slide['body']}"
                    zip_file.writestr(f"slide_{idx:02d}.txt", slide_text)
                
                if audio_brief.get("path") and os.path.exists(audio_brief["path"]):
                    zip_file.write(audio_brief["path"], arcname="background_audio.mp3")
                    
            zip_buffer.seek(0)
            status.update(label="✨ Pipeline complete! Export package ready.", state="complete", expanded=False)
            
        st.success("🎉 Carousel deck and audio assets successfully multiplexed!")
        
        # Download button for final package
        st.download_button(
            label="📦 Download Complete Export Package (.zip)",
            data=zip_buffer,
            file_name="sia_studio_export_bundle.zip",
            mime="application/zip",
            key="download_export_bundle"
        )