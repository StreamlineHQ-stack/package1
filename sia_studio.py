# ==========================================
        # OPTION 2: SWIPE-TO-TEMPLATE LAYOUT ARCHITECTURE ENGINE
        # ==========================================
if "2. 3-Mode Visual Asset Extractor" in visual_path:
            st.session_state["is_standalone_mode"] = False
            st.markdown("#### 📐 Swipe-to-Template Layout Architecture Engine")
            st.info("Structural layout cloning active. Deconstructs reference geometry and maps your deck content into a pristine matching template.")
            
            uploaded_slide = st.file_uploader("Upload Inspiration Swipe Slide", type=["png", "jpg", "jpeg"], key="sia_router_upload")
            
            if uploaded_slide is not None:
                original_image = Image.open(uploaded_slide).convert("RGB")
                w, h = original_image.size
                
                # Extract dominant aesthetic color from upper reference zone for template theming
                sample_color = original_image.getpixel((int(w * 0.5), int(h * 0.1)))
                hex_color = '#%02x%02x%02x' % sample_color
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Inspiration Reference Slide**")
                    st.image(original_image, use_container_width=True)
                    
                with col2:
                    st.markdown("**Extracted Structural Blueprint**")
                    # Display a clean structural card preview
                    preview_card = original_image.copy()
                    st.image(preview_card, use_container_width=True)
                    
                st.success(f"Layout blueprint extracted! Dominant theme color detected: `{hex_color}`")
                
                st.markdown("---")
                st.subheader("📝 Map Deck Content into Template Layout")
                
                # Pull active slide contents if available from Step 1
                slide_contents = st.session_state.get("sia_slide_contents", [])
                if slide_contents:
                    st.info(f"Loaded {len(slide_contents)} slides from your Content Engine. Ready to batch-render into the template architecture.")
                else:
                    st.warning("No slides found from Step 1 yet. You can enter a quick headline below or head back to Step 1 to generate your full deck content.")
                
                template_headline = st.text_input("Test Template Headline", value="Scale Your Creator Business Faster")
                template_body = st.text_area("Test Template Body Copy", value="Build modular systems that protect your margins and eliminate external API dependencies.")
                
                if st.button("🚀 Render Template Layout Preview", key="render_template_layout_btn"):
                    # Build clean structural specification for universal renderer
                    template_spec = {
                        "asset_mode": "template_architecture",
                        "layout_archetype": "Top-Header Structural Card",
                        "primary_color": hex_color,
                        "visual_asset_bytes": uploaded_slide.getvalue(),
                        "design_style": "Swipe Structural Clone",
                        "palette": [hex_color, "#111827", "#FFFFFF"],
                        "typography": "Modern Professional"
                    }
                    
                    st.session_state["visual_brief"] = template_spec
                    st.session_state["visual_approved"] = True
                    st.success("Template architecture compiled successfully!")

                # Prepare payload for universal renderer / kinetic handoff
                buffered = io.BytesIO()
                original_image.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()
                b64_str = base64.b64encode(img_bytes).decode()
                data_url = f"data:image/png;base64,{b64_str}"

                visual_spec = {
                    "asset_mode": "template_architecture",
                    "visual_asset_bytes": img_bytes,
                    "visual_asset_data_url": data_url,
                    "design_style": "Swipe Structural Clone",
                    "palette": [hex_color, "#000000", "#FFFFFF"],
                    "typography": "Modern Clean",
                    "visual_mood": "Professional High-Converting"
                }

                st.session_state["visual_brief"] = visual_spec
                st.session_state["visual_approved"] = True
                
                st.divider()
                render_universal_canvas(spec=st.session_state["visual_brief"], slide_count=slide_count, content_only_mode=False, standalone_mode=False)
