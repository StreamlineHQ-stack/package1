with col_dl2:
        if st.button("🚀 Send to Kinetic Engine (Animator)", type="primary", use_container_width=True, key="sia_send_animator_btn"):
            preview_deck_data = st.session_state.get("sia_preview_deck", styled_deck)
            json_str = json.dumps(preview_deck_data)
            encoded_deck = base64.urlsafe_b64encode(json_str.encode("utf-8")).decode("utf-8")
            st.query_params["deck"] = encoded_deck
            st.success("🎉 Deck encoded in-memory! Ready for Kinetic Engine handoff.")
            st.rerun()