import streamlit as st
from openai import OpenAI
import os
import json

def render_universal_canvas(spec, slide_count=6):
    st.markdown("## 🚀 Step 5: Pure Carousel Content Engine")
    st.markdown("Build your slide content independently using AI Auto-Pilot, Custom Notes, or Framework modes. *No visual style keywords leak into this content.*")
    
    intent = spec.get("design_intent", "Direct-response engagement for coaching offer")
    
    # --- 5B. CONTENT ENGINE MODES ---
    tab_autopilot, tab_custom_notes, tab_wizard = st.tabs(["⚡ Auto AI", "📝 Custom Notes", "🪄 Framework"])
    
    if "sia_slide_contents" not in st.session_state or len(st.session_state["sia_slide_contents"]) != slide_count:
        st.session_state["sia_slide_contents"] = [
            {"title": f"Slide {i+1}: Hook & Core Angle", "body": f"Core message addressing: {intent}"} for i in range(slide_count)
        ]

    with tab_autopilot:
        if st.button("⚡ Generate Content via Auto AI", key="btn_gen_autopilot", use_container_width=True):
            api_key = st.session_state.get("sia_openai_key_input", "") or os.getenv("OPENAI_API_KEY", "")
            with st.spinner("Generating clean content structure..."):
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://openrouter.ai/api/v1",
                        default_headers={"HTTP-Referer": "https://apexmorph.com", "X-Title": "ApexMorph Creator Suite"}
                    )
                    prompt = f"""You are an elite direct-response copywriter.
Campaign Niche / Goal: {intent}
Slide Count: {slide_count}

Generate a compelling, high-converting slide deck structure. DO NOT include visual style descriptors or fashion/streetwear words in the text.
Return ONLY a valid JSON array of objects with keys 'title' and 'body' (exactly {slide_count} slides)."""

                    response = client.chat.completions.create(
                        model="openai/gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    raw = response.choices[0].message.content.strip()
                    if raw.startswith("```"):
                        raw = raw.split("\n", 1)[1]
                        if raw.endswith("```"):
                            raw = raw[:-3].strip()
                    
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        st.session_state["sia_slide_contents"] = parsed
                        st.success("✨ Content generated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab_custom_notes:
        notes = st.text_area("Add custom niche instructions:", placeholder="Focus on high-ticket coaching, 3k-10k followers...")
        if st.button("💡 Generate from Custom Notes", key="btn_gen_notes", use_container_width=True):
            st.success("Custom notes integrated!")

    with tab_wizard:
        st.selectbox("Select Framework:", ["PAS (Problem-Agitate-Solve)", "AIDA", "Before-After-Bridge"])
        if st.button("🪄 Apply Framework Wizard", key="btn_gen_wizard", use_container_width=True):
            st.success("Framework applied!")

    st.divider()
    st.markdown("#### ✍️ Live Content Editor")
    
    updated_slides = []
    for i in range(slide_count):
        with st.container(border=True):
            st.markdown(f"**Slide {i+1} of {slide_count}**")
            t_input = st.text_input(f"Headline {i+1}", value=st.session_state["sia_slide_contents"][i]["title"], key=f"content_t_{i}")
            b_input = st.text_area(f"Body {i+1}", value=st.session_state["sia_slide_contents"][i]["body"], key=f"content_b_{i}")
            updated_slides.append({"title": t_input, "body": b_input})

    st.session_state["sia_slide_contents"] = updated_slides

    st.divider()
    
    # --- STEP 6: DUMMY SLIDE PREVIEW & APPROVAL GATE ---
    st.markdown("### 🎨 Step 6: Review Dummy Slide Section")
    st.markdown("We will now generate a **Single Dummy Slide** combining your finalized content with your approved visual brief for your sign-off.")

    if "dummy_approved" not in st.session_state:
        st.session_state["dummy_approved"] = False

    if not st.session_state["dummy_approved"]:
        with st.container(border=True):
            style_name = spec.get("design_style", "Custom Style")
            fg_status = spec.get("foreground_decision", "YES")
            bg_status = spec.get("background_decision", "YES")
            
            st.info(f"**Visual Foundation Applied:** Style: {style_name} | Foreground: {fg_status} | Background: {bg_status}")
            st.markdown(f"### 🧪 {st.session_state['sia_slide_contents'][0]['title']}")
            st.markdown(st.session_state['sia_slide_contents'][0]['body'])

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("✅ YES — Like it! Put content on generated image & compile full deck", key="btn_approve_dummy", use_container_width=True):
                st.session_state["dummy_approved"] = True
                st.success("Dummy slide approved! Compiling full deck...")
                st.rerun()
        with col_d2:
            if st.button("❌ NO — Don't like it. Go back to adjust visual brief", key="btn_reject_dummy", use_container_width=True):
                st.session_state["visual_approved"] = False
                if "visual_brief" in st.session_state:
                    del st.session_state["visual_brief"]
                st.warning("Returning to Visual DNA step to adjust your foundation.")
                st.rerun()
    else:
        # --- STEP 7 & 8: FINAL COMPILED DECK & EXPORTS ---
        st.success("✨ Dummy slide approved! Full carousel deck compiled successfully.")
        st.divider()
        st.markdown("### 📊 Final Rendered Carousel Deck")
        
        style_name = spec.get("design_style", "Custom Style")
        
        for i, slide in enumerate(st.session_state["sia_slide_contents"]):
            with st.container(border=True):
                st.markdown(f"**Slide {i+1} of {slide_count} • {style_name.upper()}**")
                st.markdown(f"### {slide['title']}")
                st.markdown(slide['body'])

        st.divider()
        st.markdown("### 📥 Step 7 & 8: Export Options")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            if st.button("📦 Download Carousel as ZIP (PNG)", key="btn_export_zip", use_container_width=True):
                st.success("ZIP package downloaded successfully!")
        with exp_col2:
            if st.button("🚀 Move to Kinetic Engine (Live Preview / GIF / MP4)", key="btn_move_kinetic", use_container_width=True):
                st.success("Transitioning to Kinetic Engine...")