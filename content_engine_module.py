# content_engine_module.py • Direct-Response Ideation & Full Framework Library Hub
import inspect
import streamlit as st
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY

try:
    from templates.december import DECEMBER_FRAMEWORK_LIBRARY
except Exception:
    DECEMBER_FRAMEWORK_LIBRARY = {}


def _run_generator(prompt_payload, slide_count, mode, topic="", audience="", tone="", desired_outcome=""):
    """Calls generate_carousel_deck while supporting optional context parameters if present."""
    sig = inspect.signature(generate_carousel_deck)
    kwargs = {}
    if "topic" in sig.parameters:
        kwargs["topic"] = topic
    if "audience" in sig.parameters:
        kwargs["audience"] = audience
    if "tone" in sig.parameters:
        kwargs["tone"] = tone
    if "desired_outcome" in sig.parameters:
        kwargs["desired_outcome"] = desired_outcome

    context_header = (
        f"Topic: {topic}\n"
        f"Audience: {audience}\n"
        f"Tone: {tone}\n"
        f"Desired Outcome: {desired_outcome}\n\n"
    )
    return generate_carousel_deck(
        f"{context_header}{prompt_payload}".strip(),
        slide_count=int(slide_count),
        mode=mode,
        **kwargs,
    )


def render_content_engine():
    st.markdown("<h1 style='text-align: center;'>🧠 Content Engine (Step 1)</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: gray;'>Direct-Response Ideation • 100+ Framework Library & Downstream Hub (December Edition Coming Up)</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    if "ce_mode" not in st.session_state:
        st.session_state["ce_mode"] = "AI"

    # --- TOP 3 MODE SELECTOR BUTTONS ---
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        if st.button(
            "⚡ AI Mode",
            type="primary" if st.session_state["ce_mode"] == "AI" else "secondary",
            use_container_width=True,
            key="ce_tab_ai",
        ):
            st.session_state["ce_mode"] = "AI"
            st.rerun()
    with col_m2:
        if st.button(
            "📝 Custom Mode",
            type="primary" if st.session_state["ce_mode"] == "Custom" else "secondary",
            use_container_width=True,
            key="ce_tab_custom",
        ):
            st.session_state["ce_mode"] = "Custom"
            st.rerun()
    with col_m3:
        if st.button(
            "🪄 Framework Mode",
            type="primary" if st.session_state["ce_mode"] == "Framework" else "secondary",
            use_container_width=True,
            key="ce_tab_framework",
        ):
            st.session_state["ce_mode"] = "Framework"
            st.rerun()

    st.divider()
    active_mode = st.session_state["ce_mode"]

    tone_choices = [
        "Direct-Response & Punchy",
        "Authority & Strategic",
        "Empathetic & Conversational",
        "Bold & Contrarian",
    ]
    outcome_choices = [
        "Drive Saves & Shares",
        "Start DM Conversations",
        "Build Authority & Trust",
        "Promote an Offer / Product",
        "Educate on a Core Skill / Habit",
    ]

    # =========================================================
    # MODE 1: AI MODE (4 Clean Input Fields)
    # =========================================================
    if active_mode == "AI":
        with st.container(border=True):
            st.markdown("### ⚡ AI Auto-Pilot")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                core_topic = st.text_input(
                    "Core Topic / Problem:",
                    value="Why time management is a crucial life and professional skill",
                    key="ce_ai_topic",
                )
                target_audience = st.text_input(
                    "Target Audience:",
                    value="Coaches, sellers, and businesses on Instagram",
                    key="ce_ai_audience",
                )
            with col_a2:
                slide_count = st.number_input(
                    "Number of Slides:",
                    min_value=3,
                    max_value=10,
                    value=6,
                    step=1,
                    key="ce_ai_slides",
                )
                tone = st.selectbox(
                    "Tone:",
                    tone_choices,
                    index=0,
                    key="ce_ai_tone",
                )

            if st.button("🚀 Generate AI Deck", type="primary", use_container_width=True, key="ce_run_ai"):
                with st.spinner("Generating deck via AI Auto-Pilot..."):
                    prompt_body = (
                        f"Core Topic / Problem: {core_topic}\n"
                        f"Target Audience: {target_audience}\n"
                        f"Tone: {tone}"
                    )
                    res, status_msg = _run_generator(
                        prompt_body,
                        slide_count=slide_count,
                        mode="autopilot",
                        topic=core_topic,
                        audience=target_audience,
                        tone=tone,
                        desired_outcome="Drive Saves & Shares",
                    )
                    st.session_state["deck_json"] = res
                    st.session_state["engine_status"] = status_msg
                    st.success("✅ Structured deck generated via AI Mode! Ready for downstream handoff.")

    # =========================================================
    # MODE 2: CUSTOM MODE (Unstructured Notes)
    # =========================================================
    elif active_mode == "Custom":
        with st.container(border=True):
            st.markdown("### 📝 Custom Expert Notes")
            custom_notes = st.text_area(
                "Paste your unstructured notes:",
                height=160,
                value="Hook: Time management is leverage.\nProblem: People waste hours on low-value tasks.\nCTA: Comment TIME to get the planner.",
                key="ce_custom_notes",
            )
            custom_slides = st.number_input(
                "Number of Slides:",
                min_value=3,
                max_value=10,
                value=6,
                step=1,
                key="ce_custom_slides",
            )

            if st.button("Format Custom Notes", type="primary", use_container_width=True, key="ce_run_custom"):
                with st.spinner("Formatting unstructured notes into a structured deck..."):
                    res, status_msg = _run_generator(
                        custom_notes,
                        slide_count=custom_slides,
                        mode="custom",
                        topic=custom_notes[:120],
                        audience="Coaches, sellers, and businesses on Instagram",
                        tone="Direct-Response & Punchy",
                        desired_outcome="Start DM Conversations",
                    )
                    st.session_state["deck_json"] = res
                    st.session_state["engine_status"] = status_msg
                    st.success("✅ Custom notes formatted into a deck! Ready for downstream handoff.")

    # =========================================================
    # MODE 3: FRAMEWORK MODE (Monthly-Expandable Library)
    # =========================================================
    elif active_mode == "Framework":
        # Merge core framework library with December / monthly vault additions
        active_library = {pillar: dict(blueprints) for pillar, blueprints in FRAMEWORK_LIBRARY.items()}
        if DECEMBER_FRAMEWORK_LIBRARY:
            for pillar, blueprints in DECEMBER_FRAMEWORK_LIBRARY.items():
                if pillar in active_library:
                    active_library[pillar].update(blueprints)
                else:
                    active_library[pillar] = dict(blueprints)

        with st.container(border=True):
            st.markdown("### ⚙️ Configure Frameworks & Custom Angles")

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                selected_pillar = st.selectbox(
                    "Select Content Pillar (Framework Library):",
                    list(active_library.keys()),
                    key="ce_fw_pillar",
                )
            with col_f2:
                templates_in_pillar = active_library[selected_pillar]
                selected_template_name = st.selectbox(
                    "Select Blueprint:",
                    list(templates_in_pillar.keys()),
                    key="ce_fw_template",
                )

            blueprint_data = templates_in_pillar[selected_template_name]

            # Show optional 2-sentence summary only when the chosen template defines one
            if blueprint_data.get("summary"):
                st.caption(f"ℹ️ {blueprint_data['summary']}")

            col_c1, col_c2 = st.columns(2)
            with col_c1:
                fw_topic = st.text_input(
                    "Core Topic / Question:",
                    value="Why time management is a crucial life and professional skill",
                    key="ce_fw_topic",
                )
                fw_outcome = st.selectbox(
                    "Desired Outcome:",
                    outcome_choices,
                    index=0,
                    key="ce_fw_outcome",
                )
            with col_c2:
                fw_tone = st.selectbox(
                    "Desired Tone:",
                    tone_choices,
                    index=0,
                    key="ce_fw_tone",
                )
                core_hook = st.text_input(
                    "Core Hook / Headline Idea:",
                    value=blueprint_data.get("hook", ""),
                    key="ce_fw_hook",
                )

            default_notes = (
                f"Problem: {blueprint_data.get('problem', '')} | "
                f"Solution: {blueprint_data.get('solution', '')} | "
                f"CTA: {blueprint_data.get('cta', '')}"
            )
            custom_notes = st.text_area(
                "Custom Notes & Specific Angles:",
                value=default_notes,
                height=106,
                key="ce_fw_notes",
            )

            slide_count = st.slider(
                "Target Slide Count:",
                min_value=3,
                max_value=10,
                value=6,
                key="ce_fw_slides",
            )

            if st.button(
                "🚀 Generate Structured Deck Content via Framework",
                type="primary",
                use_container_width=True,
                key="ce_run_fw",
            ):
                with st.spinner("Synthesizing direct-response deck from framework library..."):
                    raw_prompt = (
                        f"Pillar: {selected_pillar}\n"
                        f"Template: {selected_template_name}\n"
                        f"Hook: {core_hook}\n"
                        f"Problem: {blueprint_data.get('problem', '')}\n"
                        f"Solution: {blueprint_data.get('solution', '')}\n"
                        f"CTA: {blueprint_data.get('cta', '')}\n"
                        f"Notes: {custom_notes}"
                    )
                    res, status_msg = _run_generator(
                        raw_prompt,
                        slide_count=slide_count,
                        mode="framework",
                        topic=fw_topic,
                        audience="Coaches, sellers, and businesses on Instagram",
                        tone=fw_tone,
                        desired_outcome=fw_outcome,
                    )

                    st.session_state["deck_json"] = res
                    st.session_state["engine_status"] = status_msg
                    st.success("✅ Structured deck generated successfully from framework library! Ready for downstream handoff.")

    # --- DOWNSTREAM HANDOFF ACTIONS ---
    if "deck_json" in st.session_state and st.session_state["deck_json"]:
        st.divider()
        st.markdown("### 🔄 Downstream Handoff & Distribution")

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            if st.button("🎨 Send to Carousel Studio ➔", type="primary", use_container_width=True, key="ce_go_studio"):
                st.session_state["active_tool_idx"] = 1
                st.rerun()
        with col_d2:
            if st.button("✨ Send to Style Inspiration ➔", use_container_width=True, key="ce_go_sia"):
                st.session_state["sia_downstage_payload"] = st.session_state["deck_json"]
                st.session_state["active_tool_idx"] = 3
                st.rerun()
        with col_d3:
            if st.button("🎬 Send to Unified Export ➔", use_container_width=True, key="ce_go_export"):
                st.session_state["active_tool_idx"] = 6
                st.rerun()