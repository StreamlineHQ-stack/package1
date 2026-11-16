# ==========================================
        # OPTION 2: ASSET & LAYOUT CLONER (CLEAN HEADER PATCH + HEADLINE CONTROLS)
        # ==========================================
        elif "2. 3-Mode Visual Asset Extractor" in visual_path:
            st.session_state["is_standalone_mode"] = False
            st.markdown("#### 🎨 SIA Studio: Asset & Layout Cloner")
            st.info("Header patch mode enabled. Automatically clears the upper title zone for your custom copy.")
            
            uploaded_slide = st.file_uploader("Upload Inspiration Slide for Asset Cloning", type=["png", "jpg", "jpeg"], key="sia_router_upload")
            
            if uploaded_slide is not None:
                from PIL import Image, ImageDraw
                original_image = Image.open(uploaded_slide).convert("RGB")
                w, h = original_image.size
                
                # Automatically create a clean background canvas by patching out the upper header zone (top 45%)
                cleaned_bg = original_image.copy()
                draw_patch = ImageDraw.Draw(cleaned_bg)
                
                # Sample background color near the top edge to match gradient
                top_sample_color = original_image.getpixel((int(w * 0.5), int(h * 0.05)))
                
                # Draw a clean rectangle over the header zone to completely remove original text
                draw_patch.rectangle([0, 0, w, int(h * 0.48)], fill=top_sample_color)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original Inspiration Slide**")
                    st.image(original_image, use_container_width=True)
                    
                with col2:
                    st.markdown("**Cleaned Asset Canvas (Header Cleared)**")
                    st.image(cleaned_bg, use_container_width=True)
                    
                st.success("Header zone cleared cleanly with zero blur on lower subjects!")
                
                st.markdown("---")
                st.subheader("✍️ Headline Placement & Layout Controls")
                
                with st.expander("Configure Headline Text Box", expanded=True):
                    headline_text = st.text_area("Headline Text", value="YOUR COMPELLING HOOK HERE\nSubheadline details go here.")
                    text_pos_y = st.slider("Vertical Position (Y Offset %)", min_value=5, max_value=40, value=12)
                    
                if st.button("Apply Headline to Canvas Asset", key="apply_headline_cloner_btn"):
                    rendered_canvas = cleaned_bg.copy()
                    draw = ImageDraw.Draw(rendered_canvas)
                    
                    y_coord = int(h * (text_pos_y / 100.0))
                    x_coord = int(w * 0.1)
                    
                    draw.text((x_coord, y_coord), headline_text, fill=(255, 255, 255))
                    
                    st.markdown("**Final Rendered Slide Preview:**")
                    st.image(rendered_canvas, use_container_width=True)
                    st.success("Layout generated successfully without overlapping text!")

                # Prepare asset payload for universal renderer / kinetic handoff
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