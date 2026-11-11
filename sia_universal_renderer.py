import streamlit as st
import json
import os
import io
import zipfile
import base64
import html
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from sia_ai_context_module import build_ai_context_deck
from sia_editorial_motif_module import build_unified_editorial_deck

def render_universal_canvas(spec={}, slide_count=4, content_only_mode=False, standalone_mode=False):
    palette = spec.get("palette", ["Red", "Black", "Yellow", "White"])
    visual_mood = spec.get("visual_mood", "Bold and Energetic")
    
    # --- CROSS-MODULE BRIDGE ---
    external_payload = (
        st.session_state.get("sia_slide_contents") or 
        st.session_state.get("feature_benefits_slides") or 
        st.session_state.get("imported_carousel_content")
    )
    
    incoming_flag = False
    if external_payload and isinstance(external_payload, list) and len(external_payload) > 0:
        is_default = len(external_payload) == 4 and "Hook & Core Angle" in str(external_payload[0])
        if not is_default or "sia_content_received_banner" not in st.session_state:
            st.session_state["sia_slide_contents"] = external_payload
            st.session_state["sia_content_received_banner"] = True
            incoming_flag = True

    if "sia_slide_contents" not in st.session_state or len(st.session_state["sia_slide_contents"]) != slide_count:
        if not incoming_flag and not st.session_state.get("sia_slide_contents"):
            st.session_state["sia_slide_contents"] = [
                {"category": f"STEP {i+1}", "title": f"Slide {i+1}: Hook & Core Angle", "content": f"Core angle addressing your topic for slide {i+1}."} for i in range(slide_count)
            ]

    # ==========================================
    # STEP 1: CONTENT ENGINE ONLY
    # ==========================================
    if content_only_mode:
        st.markdown("### 📝 Content Engine & Copywriting Suite")
        
        if st.session_state.get("sia_content_received_banner", False):
            st.success("✨ Content successfully received! Loaded into Live Content Editor below for review and approval.")
        
        st.markdown(f"Building custom carousel with **{slide_count} slides**. Refine and structure your copy below.")
        
        tab1, tab2, tab3 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Expert Notes", "🪄 Guided Framework Wizard"])
        
        with tab1:
            topic_prompt = st.text_input("Enter core topic or pain point:", value="Why time management matters", key="sia_autopilot_input")
            if st.button("Generate Auto-Pilot Carousel", type="primary", key="sia_btn_gen_auto"):
                with st.spinner(f"Crafting direct-response {slide_count}-slide carousel deck..."):
                    default_titles = [
                        f"Why {topic_prompt} Is Costing You Clients",
                        "The Hidden Cost of Inefficiency",
                        "The 3-Step Execution Model",
                        "Step 1: Audit Your Time Blocks",
                        "Step 2: Eliminate Friction Points",
                        "Step 3: Automate Workflows"
                    ]
                    new_slides = []
                    for i in range(slide_count):
                        cat = "HOOK" if i == 0 else ("CTA" if i == slide_count - 1 else f"STEP {i+1}")
                        t = default_titles[i % len(default_titles)]
                        c = f"Detailed breakdown and actionable execution strategy for slide {i+1} addressing {topic_prompt}."
                        new_slides.append({"category": cat, "title": t, "content": c})
                        
                    st.session_state["sia_slide_contents"] = new_slides
                    st.session_state["sia_content_received_banner"] = False
                    for idx, s in enumerate(new_slides):
                        st.session_state[f"sia_content_t_{idx}"] = s["title"]
                        st.session_state[f"sia_content_b_{idx}"] = s["content"]
                        st.session_state[f"sia_content_c_{idx}"] = s["category"]
                    st.success("Auto-pilot generated successfully!")
                    st.rerun()
        
        with tab2:
            custom_notes = st.text_area("Paste notes:", value="Hook: Time management is leverage.", key="sia_custom_notes_input")
            if st.button("Format Custom Notes", type="primary", key="sia_btn_gen_notes"):
                new_slides = [
                    {"category": f"INSIGHT {i+1}", "title": f"Expert Breakdown {i+1}", "content": f"Structured insights based on notes: {custom_notes[:30]}..."}
                    for i in range(slide_count)
                ]
                st.session_state["sia_slide_contents"] = new_slides
                st.session_state["sia_content_received_banner"] = False
                for idx, s in enumerate(new_slides):
                    st.session_state[f"sia_content_t_{idx}"] = s["title"]
                    st.session_state[f"sia_content_b_{idx}"] = s["content"]
                    st.session_state[f"sia_content_c_{idx}"] = s["category"]
                st.success("Custom notes compiled!")
                st.rerun()
                
        with tab3:
            selected_pillar = st.selectbox("Choose Content Pillar:", list(FRAMEWORK_LIBRARY.keys()), key="sia_pillar_select")
            templates_in_pillar = FRAMEWORK_LIBRARY[selected_pillar]
            selected_template_name = st.selectbox("Choose Blueprint:", list(templates_in_pillar.keys()), key="sia_template_select")
            if st.button("Format Framework Carousel", type="primary", key="sia_btn_gen_frame"):
                new_slides = [
                    {"category": selected_template_name.upper(), "title": f"Step {i+1}: Framework execution", "content": f"Executing blueprint step {i+1} for maximum engagement."}
                    for i in range(slide_count)
                ]
                st.session_state["sia_slide_contents"] = new_slides
                st.session_state["sia_content_received_banner"] = False
                for idx, s in enumerate(new_slides):
                    st.session_state[f"sia_content_t_{idx}"] = s["title"]
                    st.session_state[f"sia_content_b_{idx}"] = s["content"]
                    st.session_state[f"sia_content_c_{idx}"] = s["category"]
                st.success("Framework applied!")
                st.rerun()

        st.divider()
        st.markdown(f"#### ✍️ Live Content Editor ({slide_count} Slides Active)")
        slides = st.session_state["sia_slide_contents"]
        total_slides = len(slides)
        updated_slides = []
        for i in range(total_slides):
            s = slides[i] if isinstance(slides[i], dict) else {"title": str(slides[i]), "content": ""}
            with st.container(border=True):
                st.markdown(f"**Slide {i+1} of {total_slides}**")
                t_input = st.text_input(f"Headline {i+1}", value=s.get("title", ""), key=f"sia_content_t_{i}")
                b_input = st.text_area(f"Body {i+1}", value=s.get("content", s.get("body", "")), key=f"sia_content_b_{i}")
                cat_input = st.text_input(f"Category {i+1}", value=s.get("category", f"STEP {i+1}"), key=f"sia_content_c_{i}")
                updated_slides.append({"category": cat_input, "title": t_input, "content": b_input})
        st.session_state["sia_slide_contents"] = updated_slides
        
        st.divider()
        if st.button("🚀 Lock Content & Proceed to Step 2: Visual Engine", type="primary", use_container_width=True):
            st.session_state["sia_content_locked"] = True
            st.success("✨ Content locked! Switch to Step 2 above to configure your visual engine.")
            st.session_state["sia_workflow_step"] = "step2_visual"
            st.rerun()
        return

    # ==========================================
    # CHECK FOR EXTRACTED INSPIRATION VISUAL ASSET (MODE 2 / MODE 1 / MODE 3)
    # ==========================================
    visual_asset_url = spec.get("visual_asset_data_url")
    visual_asset_bytes = spec.get("visual_asset_bytes") or spec.get("extracted_bytes")
    
    if (spec.get("asset_mode") == "inspiration_visual" or visual_asset_bytes or visual_asset_url) and not standalone_mode:
        if not visual_asset_url and visual_asset_bytes:
            visual_asset_url = "data:image/png;base64," + base64.b64encode(visual_asset_bytes).decode("ascii")

        st.markdown("### 🎨 Visual Asset Foundation Deck Preview")
        st.caption("Your extracted visual asset is rendered as the live background canvas across all carousel slides.")

        slides = st.session_state.get("sia_slide_contents", [])
        if not slides:
            slides = [{"category": "HOOK", "title": "Sample Title", "content": "Sample slide content"}]
        total_slides = len(slides)

        safe_url = html.escape(visual_asset_url, quote=True)
        for i, slide in enumerate(slides):
            s_title = html.escape(str(slide.get("title", "")))
            s_body = html.escape(str(slide.get("content", slide.get("body", ""))))
            s_cat = html.escape(str(slide.get("category", f"SLIDE {i+1}")).upper())

            slide_html = f"""
            <div style="
                width:100%;
                max-width:680px;
                aspect-ratio:1/1;
                margin:0 auto 28px auto;
                position:relative;
                overflow:hidden;
                border-radius:16px;
                background-image:url('{safe_url}');
                background-size:cover;
                background-position:center;
                background-repeat:no-repeat;
                box-shadow:0 15px 30px rgba(0,0,0,0.3);
                border: 2px solid #3b82f6;
            ">
                <div style="
                    position:absolute;
                    left:4%;
                    right:4%;
                    bottom:4%;
                    padding:20px 24px;
                    border-radius:12px;
                    background:rgba(11, 15, 25, 0.85);
                    backdrop-filter: blur(8px);
                    color:#ffffff;
                    font-family:sans-serif;
                    border: 1px solid rgba(59, 130, 246, 0.4);
                ">
                    <div style="color:#60a5fa; font-size:12px; font-weight:800; letter-spacing:1.5px; margin-bottom:8px; text-transform:uppercase;">
                        SLIDE {i+1} OF {total_slides} · {s_cat}
                    </div>
                    <div style="color:#ffffff; font-size:22px; font-weight:800; line-height:1.3; margin-bottom:10px;">
                        {s_title}
                    </div>
                    <div style="color:#d1d5db; font-size:15px; line-height:1.5; white-space:pre-wrap;">
                        {s_body}
                    </div>
                </div>
            </div>
            """
            st.markdown(slide_html, unsafe_allow_html=True)
        return

    # ==========================================
    # STANDALONE MODE
    # ==========================================
    if standalone_mode:
        payload = spec.get("standalone_payload", {})
        mod_type = payload.get("type", "Smart AI Background")
        slides = st.session_state.get("sia_slide_contents", [])
        
        st.markdown(f"### 📊 Standalone Visual Modules — Full Deck Preview (`{mod_type}`)")
        
        rendered_deck = []
        if "Smart AI Background" in mod_type:
            rendered_deck = build_ai_context_deck(slides)
        elif "Unified Motif" in mod_type:
            motif_theme = payload.get("motif", "floral")
            rendered_deck = build_unified_editorial_deck(slides, motif_theme=motif_theme)
        else:
            custom_bytes = payload.get("custom_image_bytes")
            img_data_uri = ""
            if custom_bytes:
                encoded = base64.b64encode(custom_bytes).decode("utf-8")
                img_data_uri = f"data:image/png;base64,{encoded}"
                
            for idx, slide in enumerate(slides):
                cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
                title = str(slide.get("title", f"Slide {idx+1}"))
                content = str(slide.get("content", ""))
                
                html_str = f"""
                <div style="background: #0b0f19; padding: 40px; border-radius: 24px; border: 3px solid #3b82f6; max-width: 680px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
                    <div style="width: 100%; height: 240px; border-radius: 16px; overflow: hidden; margin-bottom: 24px; border: 2px solid #60a5fa;">
                        {f'<img src="{img_data_uri}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />' if img_data_uri else '<div style="background:#1e293b; width:100%; height:100%; display:flex; align-items:center; justify-content:center; color:#94a3b8;">No Custom Image</div>'}
                    </div>
                    <div style="color: #60a5fa; font-size: 14px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 12px; text-transform: uppercase;">
                        CUSTOM IMAGE • SLIDE {idx+1} OF {len(slides)} • {cat}
                    </div>
                    <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 16px;">
                        {title}
                    </h2>
                    <p style="color: #d1d5db; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                        {content}
                    </p>
                </div>
                """
                rendered_deck.append({"rendered_html": html_str})

        for item in rendered_deck:
            st.markdown(item["rendered_html"], unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        return

    # ==========================================
    # DEFAULT ART DIRECTOR ROUTING (3A)
    # ==========================================
    st.markdown("### 🎨 Visual Engine & Art Director Asset Routing")
    slides = st.session_state.get("sia_slide_contents", [])
    for i, slide in enumerate(slides):
        s_title = slide.get("title", "")
        s_body = slide.get("content", "")
        s_cat = slide.get("category", f"SLIDE {i+1}").upper()
        st.markdown(f"**Slide {i+1}: {s_cat}** — {s_title}")
        st.text(s_body)
        st.divider()
