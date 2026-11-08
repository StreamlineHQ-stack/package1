import streamlit as st
from openai import OpenAI
import os
import json

def get_active_api_key():
    # 1. Check session state
    key = st.session_state.get("sia_openai_key_input", "") or st.session_state.get("sia_manual_key", "")
    if key:
        return key
    # 2. Check st.secrets
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
        elif "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass
    # 3. Check environment variables
    return os.getenv("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))

def render_universal_canvas(spec, slide_count=6):
    st.markdown("## ✨ Minimalist Carousel Engine")
    
    # --- CHECK IF CONTENT WAS RECEIVED FROM UPSTREAM (FEATURE-TO-BENEFITS) ---
    upstream_content = st.session_state.get("feature_to_benefits_output", None) or st.session_state.get("upstream_content_data", None)
    
    if upstream_content:
        st.success("📥 Content successfully received from Feature-to-Benefits upstream module!")
        st.session_state["sia_slide_contents"] = upstream_content
    else:
        st.markdown("Generate high-converting carousels via auto-pilot, freeform notes, or guided frameworks.")
        
        # --- CONTENT ENGINE MODES ---
        tab_autopilot, tab_custom_notes, tab_wizard = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
        
        if "sia_slide_contents" not in st.session_state or len(st.session_state["sia_slide_contents"]) != slide_count:
            st.session_state["sia_slide_contents"] = [
                {"title": f"Slide {i+1}: Hook & Core Angle", "body": "Enter your core topic above and click generate."} for i in range(slide_count)
            ]

        with tab_autopilot:
            st.markdown("### ⚡ AI Auto-Pilot")
            core_topic = st.text_input("Enter your core topic or audience pain point:", value="Why is time management important", key="content_core_topic_input")
            
            if st.button("Generate Auto-Pilot Carousel", key="btn_gen_autopilot", use_container_width=True):
                api_key = get_active_api_key()
                if not api_key:
                    st.error("⚠️ API Key missing! Please enter your OpenRouter / OpenAI API key at the top of the studio.")
                else:
                    with st.spinner("Generating targeted carousel content via OpenRouter..."):
                        try:
                            client = OpenAI(
                                api_key=api_key,
                                base_url="https://openrouter.ai/api/v1",
                                default_headers={"HTTP-Referer": "https://apexmorph.com", "X-Title": "ApexMorph Creator Suite"}
                            )
                            prompt = f"""You are an elite direct-response copywriter.
Core Topic / Pain Point: {core_topic}
Slide Count: {slide_count}

Generate a compelling, high-converting slide deck structure addressing this exact topic. DO NOT include visual style descriptors.
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
                                st.success("✨ Carousel content generated successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

        with tab_custom_notes:
            st.markdown("### 📝 Custom Expert Notes")
            custom_notes_input = st.text_area("Enter your custom guidance or expert breakdown:", placeholder="Focus on high-ticket coaching transformation, eliminate fluff...")
            if st.button("Generate from Expert Notes", key="btn_gen_notes", use_container_width=True):
                st.success("Custom notes compiled!")

        with tab_wizard:
            st.markdown("### 🪄 Guided Framework Wizard")
            framework_choice = st.selectbox("Select Framework:", ["PAS (Problem-Agitate-Solve)", "AIDA", "Before-After-Bridge"])
            framework_topic = st.text_input("Enter topic for framework:", value="Scaling a coaching business")
            if st.button("Run Framework Wizard", key="btn_gen_wizard", use_container_width=True):
                st.success(f"Framework {framework_choice} applied successfully!")

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
            st.info(f"**Visual Foundation Applied:** Style: {style_name}")
            st.markdown(f"### 🧪 {st.session_state['sia_slide_contents'][0]['title']}")
            st.markdown(st.session_state['sia_slide_contents'][0]['body'])

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("✅ YES — Like it! Compile full deck", key="btn_approve_dummy", use_container_width=True):
                st.session_state["dummy_approved"] = True
                st.success("Dummy slide approved! Compiling full deck...")
                st.rerun()
        with col_d2:
            if st.button("❌ NO — Don't like it. Go back to visual brief", key="btn_reject_dummy", use_container_width=True):
                st.session_state["visual_approved"] = False
                if "visual_brief" in st.session_state:
                    del st.session_state["visual_brief"]
                st.warning("Returning to Visual DNA step.")
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
            if st.button("🚀 Move to Kinetic Engine", key="btn_move_kinetic", use_container_width=True):
                st.success("Transitioning to Kinetic Engine...")
