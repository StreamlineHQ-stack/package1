import streamlit as st

def verify_license_sidebar():
    with st.sidebar:
        st.divider()
        st.subheader("🔐 License Activation")
        
        # Check session state right away at the top
        if st.session_state.get('licensed', False):
            st.caption("🟢 Status: Unlocked & Active")
            return True
            
        license_key = st.text_input("Enter License Key:", type="password")
        
        if st.button("Activate Tool"):
            if not license_key:
                st.error("Please enter a valid license key.")
                return False
                
            # Basic validation check placeholder for launch
            if len(license_key) > 8:
                st.success("✅ License Verified Successfully!")
                st.session_state['licensed'] = True
                st.rerun() # Immediate rerun to lock in the persistent state
            else:
                st.error("❌ Invalid license key. Please check and try again.")
                return False
        
        st.warning("⚠️ Restricted Mode: Enter key to unlock full features.")
        return False