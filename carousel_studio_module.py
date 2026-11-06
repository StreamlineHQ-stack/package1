# Render GIF buffer
                    gif_buffer = io.BytesIO()
                    if frames:
                        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=int(seconds_per_slide * 1000), loop=0)
                    gif_bytes = gif_buffer.getvalue()

                    # Render MP4 video buffer (temporarily without try/except to expose any error)
                    import imageio
                    import numpy as np

                    fps = int(frame_rate)
                    frames_per_slide = int(fps * seconds_per_slide)

                    paced_frames = []
                    for f in frames:
                        np_f = np.array(f)
                        for _ in range(frames_per_slide):
                            paced_frames.append(np_f)

                    mp4_path = "temp_kinetic_deck_local.mp4"
                    imageio.mimwrite(
                        mp4_path,
                        paced_frames,
                        fps=fps,
                        codec="libx264",
                        quality=8,
                        pixelformat="yuv420p",
                    )
                    with open(mp4_path, "rb") as mf:
                        mp4_bytes = mf.read()
                    os.remove(mp4_path)
                    
                st.success("🎉 Kinetic Loop rendered successfully!")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="⬇️ Download Animated GIF", 
                        data=gif_bytes, 
                        file_name="kinetic_carousel_loop.gif", 
                        mime="image/gif", 
                        use_container_width=True, 
                        key="local_dl_gif"
                    )
                with col_d2:
                    st.download_button(
                        label="🎬 Download Instagram MP4",
                        data=mp4_bytes,
                        file_name="kinetic_carousel_loop.mp4",
                        mime="video/mp4",
                        use_container_width=True,
                        key="local_dl_mp4"
                    )