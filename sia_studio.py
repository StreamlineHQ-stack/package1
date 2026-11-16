# ==========================================
        # OPTION 2: ASSET & LAYOUT CLONER (CLEAN BACKGROUND SWATCH & HEADER BLOCK)
        # ==========================================
        elif "2. 3-Mode Visual Asset Extractor" in visual_path:
            st.session_state["is_standalone_mode"] = False
            st.markdown("#### 🎨 SIA Studio: Asset & Layout Cloner")
            st.info("Clean background swatch mode enabled. Replaces the header zone with a seamless color block from your image.")
            
            uploaded_slide = st.file_uploader("Upload Inspiration Slide for Asset Cloning", type=["png", "jpg", "jpeg"], key="sia_router_upload")
            
            if uploaded_slide is not None:
                original_image = Image.open(uploaded_slide).convert("RGB")
                w, h = original_image.size
                
                cleaned_bg = original_image.copy()
                draw_patch = ImageDraw.Draw(cleaned_bg)
                
                # Sample the dominant background color from the top edge
                bg_color = original_image.getpixel((int(w * 0.5), int(h * 0.05)))
                
                # Draw a clean, solid background swatch over the entire upper header zone to completely erase old text
                draw_patch.rectangle([0, 0, w, int(h * 0.45)], fill=bg_color)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original Inspiration Slide**")
                    st.image(original_image, use_container_width=True)
                    
                with col2:
                    st.markdown("**Cleaned Asset Canvas**")
                    st.image(cleaned_bg, use_container_width=True)
                    
                st.success("Header zone replaced cleanly with background color swatch!")
                
                st.markdown("---")
                st.subheader("✍️ Headline Placement & Layout Controls")
                
                with st.expander("Configure Headline Text Box", expanded=True):
                    headline_text = st.text_area("Headline Text", value="YOUR COMPELLING HOOK HERE\nSubheadline details go here.")
                    text_pos_y = st.slider("Vertical Position (Y Offset %)", min_value=5, max_value=35, value=10)
                    
                if st.button("Apply Headline to Canvas Asset", key="apply_headline_cloner_btn"):
                    rendered_canvas = cleaned_bg.copy()
                    draw = ImageDraw.Draw(rendered_canvas)
                    y_coord = int(h * (text_pos_y / 100.0))
                    x_coord = int(w * 0.1)
                    draw.text((x_coord, y_coord), headline_text, fill=(255, 255, 255))
                    
                    st.markdown("**Final Rendered Slide Preview:**")
                    st.image(rendered_canvas, use_container_width=True)
                    st.success("Layout generated successfully!")

                buffered = io.BytesIO()
                cleaned_bg.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()
                b64_str = base64.b64encode(img_bytes).decode()
                data_url = f"data:image/png;base64,{b64_str}"

                visual_spec = {
                    "asset_mode": "inspiration_visual",
                    "visual_asset_bytes": img_bytes,
                    "visual_asset_data_url": data_url,
                    "design_style": "Pristine Asset Cloner",
                    "palette": ["#000000", "#FFFFFF", "#3B82F6"],
                    "typography": "Modern Clean",
                    "visual_mood": "Professional High-Converting"
                }

                st.session_state["visual_brief"] = visual_spec
                st.session_state["visual_approved"] = True
                
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)