st.divider()
        st.markdown("### 📝 Content Source & Generation Engine")
        
        # Context-aware content source options based on whether a downstream payload actually exists
        if downstream_payload:
            st.markdown("Choose whether to use the incoming feature content payload or generate fresh carousel content inside SIA.")
            content_choice = st.radio(
                "Select Content Source Strategy:",
                [
                    "📦 Keep & Use Passed Down Feature Content",
                    "✨ Generate New Carousel Content inside SIA (AI Auto-Pilot & Notes)"
                ],
                key="sia_content_choice_radio"
            )
        else:
            st.info("💡 No downstream feature script detected. Set up your content generation strategy below:")
            content_choice = "✨ Generate New Carousel Content inside SIA (AI Auto-Pilot & Notes)"

        if "Keep & Use Passed Down Feature Content" in content_choice and downstream_payload:
            st.info("✅ Feature content retained. Generating white background preview deck from passed-down script.")
            if isinstance(downstream_payload, list):
                st.session_state["sia_preview_deck"] = downstream_payload
            else:
                st.session_state["sia_preview_deck"] = [
                    {"category": "HOOK", "title": "Tired of aching joints?", "content": "Meet the Ergonomic Garden Kneeler."},
                    {"category": "PROBLEM", "title": "Traditional gardening causes pain.", "content": "Hard earth causes severe strain."},
                    {"category": "SOLUTION", "title": "Protect your knees with EVA padding.", "content": "Thick foam cushions joints."},
                    {"category": "CTA", "title": "Ready to garden in comfort?", "content": "Comment GARDEN today!"}
                ]
        else:
            st.success("✨ New content generation active. Use AI Auto-Pilot or Custom Notes below:")
            sub_tab1, sub_tab2 = st.tabs(["⚡ AI Auto-Pilot", "📝 Custom Notes"])
            
            with sub_tab1:
                auto_topic = st.text_input("Core Topic / Hook for SIA Deck:", "High-converting digital product strategies for creators", key="sia_auto_topic")
                slide_count = st.slider("Target Slide Count:", 4, 8, 6, key="sia_slide_count")
                if st.button("Generate AI Content Deck", type="primary", key="sia_gen_ai_deck"):
                    st.session_state["sia_preview_deck"] = [
                        {"category": f"SLIDE {i+1}", "title": f"Key Principle #{i+1} for {auto_topic}", "content": f"Detailed strategic breakdown and actionable implementation step {i+1}."}
                        for i in range(slide_count)
                    ]
                    st.success("🎉 AI Content Deck generated successfully!")

            with sub_tab2:
                custom_notes = st.text_area("Paste Custom Outline or Script Notes:", "Slide 1: Hook\nSlide 2: Mechanism\nSlide 3: Offer", key="sia_custom_notes")
                if st.button("Load Custom Notes into Deck", key="sia_load_notes"):
                    st.session_state["sia_preview_deck"] = [
                        {"category": "CUSTOM SLIDE", "title": "Custom Outline Point", "content": custom_notes}
                    ]
                    st.success("🎉 Custom notes loaded into preview deck!")