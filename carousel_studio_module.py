# carousel_studio_module.py • Visual Asset Merger, Slide Editor & Export Hub
import streamlit as st
import zipfile
import io

def render_carousel_studio():
    st.markdown("<h1 style='text-align: center;'>🎨 Carousel Studio & Visual Assembler</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Merge Content Engine output with visual assets, preview, edit, export PNGs, or send to Kinetic Animator.</p>", unsafe_allow_html=True)
    st.divider()

    # --- 1. CHECK FOR CONTENT ENGINE PAYLOAD ---
    if "sia_slide_contents" not in st.session_state or not st.session_state["sia_slide_contents"]:
        st.warning("⚠️ No deck found! Please generate structured content in the **Content Engine** first.")
        if st.button("⬅️ Return to Content Engine"):
            st.session_state["active_tool_idx"] = 0
            st.rerun()
        return

    slides = st.session_state["sia_slide_contents"]

    # --- 2. VISUAL THEME & LAYOUT STYLING ---
    st.sidebar.markdown("### 🎨 Visual Theme Selector")
    theme_choice = st.sidebar.radio("Select Style Preset:", ["November Dark Vault", "Clean Minimalist Light", "High-Contrast Direct Response"])
    
    if theme_choice == "November Dark Vault":
        bg_col, accent_col, text_col = "#121218", "#ff4b4b", "#ffffff"
    elif theme_choice == "Clean Minimalist Light":
        bg_col, accent_col, text_col = "#ffffff", "#0066cc", "#111111"
    else:
        bg_col, accent_col, text_col = "#000000", "#ffcc00", "#ffffff"

    # --- 3. SLIDE-BY-SLIDE INSPECTION & EDITING SCOPE ---
    st.markdown("### 👁️ Slide Visual Preview & Individual Editing Scope")
    
    selected_idx = st.selectbox(
        "Select Slide to Inspect/Edit:",
        range(len(slides)),
        format_func=lambda i: f"Slide {i+1}: {slides[i]['title'][:35]}..."
    )
    
    current_slide = slides[selected_idx]
    
    col_prev, col_edit = st.columns([1.3, 1])
    
    with col_prev:
        st.markdown(f"""
        <div style="background-color: {bg_col}; border: 3px solid {accent_col}; border-radius: 16px; padding: 35px; min-height: 340px; color: {text_col}; box-shadow: 0px 8px 24px rgba(0,0,0,0.4);">
            <p style="color: {accent_col}; font-weight: bold; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px;">Slide {selected_idx + 1} of {len(slides)} • {theme_choice}</p>
            <h2 style="color: {text_col}; margin-top: 12px; font-size: 24px; line-height: 1.3;">{current_slide['title']}</h2>
            <hr style="border-color: rgba(255,255,255,0.15); margin: 20px 0;">
            <p style="font-size: 16px; line-height: 1.6; white-space: pre-wrap; opacity: 0.9;">{current_slide['body']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_edit:
        st.markdown("#### ✏️ Scope Edit: Current Slide")
        edited_title = st.text_input("Edit Slide Title", value=current_slide['title'], key=f"edit_t_{selected_idx}")
        edited_body = st.text_area("Edit Slide Body", value=current_slide['body'], height=150, key=f"edit_b_{selected_idx}")
        
        if st.button("💾 Save Slide Updates", use_container_width=True):
            slides[selected_idx]['title'] = edited_title
            slides[selected_idx]['body'] = edited_body
            st.session_state["sia_slide_contents"] = slides
            st.success("✅ Slide updated in deck successfully!")
            st.rerun()

    st.divider()

    # --- 4. FINISHED DECK EXPORT & PIPELINE HANDOFF ---
    st.markdown("### 🚀 Finished Deck Export & Pipeline Handoff")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        # Generate simulated PNG ZIP export bundle
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for idx, s in enumerate(slides):
                slide_txt = f"SLIDE {idx+1}\nTITLE: {s['title']}\nBODY:\n{s['body']}"
                zip_file.writestr(f"slide_{idx+1}.txt", slide_txt) # Placeholder text-to-image bundle
        zip_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Finished Deck (.zip)",
            data=zip_buffer,
            file_name="carousel_deck_assets.zip",
            mime="application/zip",
            use_container_width=True
        )
        
    with col_e2:
        if st.button("⚡ Send to Kinetic Animator", type="primary", use_container_width=True):
            st.session_state["active_tool_idx"] = 3  # Jump to Kinetic Animator
            st.success("✅ Deck passed to Kinetic Animator!")
            st.rerun()
            
    with col_e3:
        if st.button("🎵 Send to Audio & Assembler", type="secondary", use_container_width=True):
            st.session_state["active_tool_idx"] = 4  # Jump to Audio Engine
            st.success("✅ Deck passed to Audio Engine!")
            st.rerun()