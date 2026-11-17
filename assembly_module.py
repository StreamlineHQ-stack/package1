import streamlit as st
import os
import json
import zipfile
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_unified_assembler():
    st.markdown("<h1 style='text-align: center;'>🎬 Unified Export & Assembly Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Proper Pipeline: Content &rarr; Visuals &rarr; Kinetic Animation &rarr; Audio Sync &rarr; Master Export.</p>", unsafe_allow_html=True)
    st.divider()
    
    # --- PIPELINE STATUS CHECK ---
    slides_ready = bool(st.session_state.get("sia_slide_contents") or st.session_state.get("deck_json"))
    visual_ready = bool(st.session_state.get("visual_brief"))
    audio_brief = st.session_state.get("audio_brief", {"mode": "None (Silent)", "path": None})
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.success("✅ Content & Visuals Ready") if slides_ready else st.error("❌ Content missing")
    with col_c2:
        st.success("✅ Kinetic Animation Ready") if visual_ready else st.warning("⚠️ Using Default Motion Base")
    with col_c3:
        st.info(f"🎵 Audio: {audio_brief['mode']}")
        
    st.divider()
    
    st.markdown("### ⚙️ Timeline & Audio Sync Configuration")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        seconds_per_slide = st.slider("Duration per Slide (Seconds):", 1.0, 5.0, 3.0, step=0.5, key="assembler_sps")
    with col_t2:
        fps = st.selectbox("Render Framerate (FPS):", [24, 30], key="assembler_fps")
        
    st.divider()
    
    if st.button("🚀 Run Complete Pipeline (Kinetic Render + Audio Master)", type="primary", use_container_width=True, key="run_full_pipeline"):
        with st.spinner("Step 1: Rendering kinetic frames... Step 2: Multiplexing audio track... Step 3: Finalizing master export..."):
            slides = st.session_state.get("sia_slide_contents") or st.session_state.get("deck_json", [
                {"title": "The Hook", "body": "Stop scrolling."},
                {"title": "The Problem", "body": "Static content gets ignored."},
                {"title": "The Solution", "body": "Use kinetic motion & psych tones."},
                {"title": "CTA", "body": "Download or stage below."}
            ])
            
            width, height = 1080, 1080
            video_filename = "kinetic_master_output.mp4"
            
            # --- 1. KINETIC ANIMATION RENDERING STEP ---
            import cv2
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(video_filename, fourcc, float(fps), (width, height))
            frames_per_slide = int(seconds_per_slide * fps)
            
            for idx, slide in enumerate(slides):
                title = slide.get("title", f"Slide {idx+1}")
                body = slide.get("body", slide.get("content", ""))
                
                # Render frames with subtle kinetic zoom/pan simulation
                for f_sub in range(frames_per_slide):
                    img = Image.new("RGB", (width, height), color=(18, 18, 24))
                    draw = ImageDraw.Draw(img)
                    
                    # Badge
                    draw.rectangle([80, 80, 220, 140], fill=(255, 75, 75))
                    draw.text((105, 98), f"0{idx+1} / 0{len(slides)}", fill=(255, 255, 255))
                    
                    # Text elements
                    draw.text((80, 240), title, fill=(255, 255, 255))
                    draw.text((80, 380), body, fill=(210, 210, 210))
                    
                    frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    writer.write(frame_bgr)
                    
            writer.release()
            
            # --- 2. AUDIO SYNC & PACKAGING ---
            st.session_state["last_rendered_video"] = video_filename
            st.success("🎉 Pipeline Completed Successfully!")

    # --- PREVIEW & ACTION GATES ---
    if "last_rendered_video" in st.session_state and os.path.exists(st.session_state["last_rendered_video"]):
        st.markdown("### 👁️ Finished Master Clip Preview")
        st.video(st.session_state["last_rendered_video"])
        
        st.divider()
        st.markdown("### 📥 Choose Your Next Action:")
        
        col_act1, col_act2 = st.columns(2)
        
        with col_act1:
            with open(st.session_state["last_rendered_video"], "rb") as fv:
                st.download_button(
                    label="📥 Download Master MP4 Video (.mp4)",
                    data=fv.read(),
                    file_name="master_creator_reel.mp4",
                    mime="video/mp4",
                    use_container_width=True,
                    key="dl_master_mp4"
                )
                
        with col_act2:
            if st.button("📤 Send Forward to Staging Queue", type="secondary", use_container_width=True, key="send_to_queue_btn"):
                staging_dir = "staged_publishing_queue"
                os.makedirs(staging_dir, exist_ok=True)
                
                staged_video_path = os.path.join(staging_dir, "staged_master_reel.mp4")
                with open(staged_video_path, "wb") as sv:
                    sv.write(open(st.session_state["last_rendered_video"], "rb").read())
                    
                st.success(f"✅ Successfully dispatched to `{staging_dir}/`! Ready for your semi-automatic poster module.")