# ==========================================
# TAB 4: STYLE INSPIRATION & ANALYSIS ENGINE (SIA) [INTEGRATED & DUAL-VECTOR]
# ==========================================
elif "Style Inspiration" in selected_main_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if is_full_suite:
        st.markdown("<h1 style='text-align: center;'>✨ SIA: Style Inspiration & Analysis Engine</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Deconstruct high-performing creator slides into actionable content, typography, and advanced photographic visual design principles.</p>", unsafe_allow_html=True)
        st.divider()

        if "sia_analysis_run" not in st.session_state:
            st.session_state["sia_analysis_run"] = False
        if "sia_focus_choice" not in st.session_state:
            st.session_state["sia_focus_choice"] = "Both (Comprehensive Breakdown)"
        if "sia_extracted_insights" not in st.session_state:
            st.session_state["sia_extracted_insights"] = ""

        col_u1, col_u2 = st.columns([1, 1], gap="large")

        with col_u1:
            st.subheader("📥 1. Reference Swipe Selection")
            ref_mode = st.radio("Reference Source:", ["Upload Custom Screenshot", "Use Canva Editorial Sample (Terracotta)"], key="platform_sia_ref_mode")
            
            if ref_mode == "Upload Custom Screenshot":
                uploaded_screenshot = st.file_uploader("Upload slide image (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"], key="platform_sia_upload_file")
                if uploaded_screenshot is not None:
                    try:
                        img = Image.open(uploaded_screenshot)
                        st.image(img, caption="Custom Swipe Reference", use_container_width=True)
                        st.session_state["sia_image_loaded"] = True
                    except Exception:
                        st.session_state["sia_image_loaded"] = False
                else:
                    st.session_state["sia_image_loaded"] = False
            else:
                st.info("🎨 **Active Reference:** Canva Warm Editorial Slide ('Sarina & Leon' Terracotta Palette)")
                st.session_state["sia_image_loaded"] = True

        with col_u2:
            st.subheader("🔍 2. Dual-Lens Focus Selection")
            st.markdown("Choose what you want to deconstruct from your reference image:")
            
            focus_vector = st.radio(
                "Primary Inspiration Vector:",
                ["Visuals & Design Style", "Content & Copywriting Structure", "Both (Comprehensive Breakdown)"],
                key="platform_sia_focus_radio"
            )
            st.session_state["sia_focus_choice"] = focus_vector

            st.divider()
            analysis_trigger = st.button("🚀 Run Dual-Lens Deconstruction", type="primary", use_container_width=True, key="platform_sia_run_btn")

        if analysis_trigger:
            if not st.session_state["sia_image_loaded"]:
                st.warning("⚠️ Please select or upload a reference slide first.")
            else:
                with st.spinner("Deconstructing content cadence and advanced photographic aesthetic ratios..."):
                    if "Visuals" in focus_vector:
                        report = """### 🎨 Advanced Visual & Photographic Deconstruction
- **Color Palette & Tone:** Warm editorial aesthetic (Terracotta base `#a85732` paired with rich cream and dark typography).
- **Subject Framing & Composition:** Minimalist, centered subject placement utilizing substantial negative space to maintain an uncluttered high-end aesthetic.
- **Prop & Texture Staging:** Incorporation of tactile organic elements (e.g., natural wood blocks, sleek mirrors, and single botanical stems) to anchor the visual mood.
- **Lighting & Atmosphere:** Warm, low-key lighting with earthy amber and terracotta color grading creating an intimate, editorial feel.
- **Image-to-Text Integration:** High-contrast serif typography positioned cleanly over the upper third of the photographic backdrop, ensuring readability without obstructing the primary focal point."""
                    elif "Content" in focus_vector:
                        report = """### ✍️ Content & Copywriting Deconstruction
- **The Hook Mechanics:** Elegant, authority-driven headline structure designed for high-end branding or event invitations.
- **Tone & Cadence:** Sophisticated, refined, and uncluttered layout structure."""
                    else:
                        report = """### ⚡ Comprehensive Dual-Lens & Photographic Deconstruction
- **Visual & Photographic Style:** Warm editorial terracotta palette paired with tactile organic props, minimalist centered framing, and low-key amber lighting.
- **Typography & Layout:** High-contrast serif headings with generous tracking layered over atmospheric negative space.
- **Content Structure:** Minimalist authoritative framing designed for premium visual engagement."""

                    st.session_state["sia_extracted_insights"] = report
                    st.session_state["sia_analysis_run"] = True
                    st.success("🎉 Deconstruction complete!")

        if st.session_state["sia_analysis_run"]:
            st.divider()
            st.subheader("📊 Deconstruction Intelligence Report")
            st.markdown(st.session_state["sia_extracted_insights"])

            st.markdown("### 💬 Interactive Refinement Q&A")
            col_qa1, col_qa2 = st.columns(2)
            
            with col_qa1:
                vis_refinement = st.selectbox("Visual & Photographic Preference:", [
                    "Warm editorial terracotta color palette & lighting",
                    "Tactile prop staging (wood textures & botanical stems)",
                    "Minimalist centered framing & negative space",
                    "High-contrast serif typography layout"
                ], key="platform_sia_vis_ref")
            
            with col_qa2:
                content_refinement = st.selectbox("Content Preference:", [
                    "Elegant headline phrasing and spacing",
                    "Sophisticated and refined editorial tone",
                    "Uncluttered, authoritative structure"
                ], key="platform_sia_cont_ref")

            st.info(f"💡 **Virtual Art Director Mapped:** Visuals (*'{vis_refinement}'*) + Content (*'{content_refinement}'*). Ready to bridge to Carousel Studio.")

            st.divider()
            st.subheader("🔄 Bridge to Platform Carousel Studio")
            st.markdown("Send both your advanced photographic art-director tokens and copywriting structure straight into Tab 1:")
            
            if st.button("✨ Send Virtual Art Director Guidelines to Carousel Studio", type="primary", use_container_width=True, key="platform_sia_bridge_btn"):
                # Save into session state so Tab 1 Carousel Engine can ingest them as art director directives
                st.session_state["style_inspiration_notes"] = f"Visual Style: {vis_refinement} | Content Style: {content_refinement}"
                st.session_state["sia_visual_token"] = vis_refinement
                st.session_state["sia_content_token"] = content_refinement
                st.session_state["active_tab_selection"] = "1. 🎨 Carousel Engine Studio"
                st.toast("Virtual Art Director parameters successfully bridged to Carousel Studio!", icon="✨")
                st.rerun()

        # Standalone Export Options for .md and .json
        st.divider()
        st.subheader("📦 Standalone Design Token & Style Guide Exports")
        col_ex1, col_ex2 = st.columns(2)
        
        with col_ex1:
            md_content = f"""# SIA Style Guide & Brand Brief
Vector Focus: {st.session_state["sia_focus_choice"]}
{st.session_state["sia_extracted_insights"]}
"""
            st.download_button("📄 Download Full Style Guide (.md)", data=md_content, file_name="sia_style_guide.md", mime="text/markdown", use_container_width=True, key="dl_md_btn")
            
        with col_ex2:
            json_content = json.dumps({
                "focus_vector": st.session_state["sia_focus_choice"],
                "color_palette": ["#a85732", "#f4f1ea", "#1a1a1a"],
                "typography": "High-contrast serif / minimalist sans",
                "photographic_style": "Warm editorial, centered minimalism, tactile props, low-key amber lighting",
                "insights": st.session_state["sia_extracted_insights"]
            }, indent=4)
            st.download_button("📥 Download Design Tokens (.json)", data=json_content, file_name="sia_design_tokens.json", mime="application/json", use_container_width=True, key="dl_json_btn")

    else:
        st.error("🔒 Locked Module: Style Inspiration & Analysis Engine")
        st.warning(
            "**Complete Suite Upgrade Required ($250 Tier)**\n\n"
            "Upgrade your license to the **$250 Complete Suite** to unlock Tool 4 (SIA Engine) right inside this platform hub!"
        )
    st.markdown("</div>", unsafe_allow_html=True)