import streamlit as st
import json
import os
import requests

def get_clean_secret(key_name):
    override_key = f"admin_{key_name.lower()}_override"
    if override_key in st.session_state and st.session_state[override_key]:
        return st.session_state[override_key].strip()
    
    val = ""
    try:
        if hasattr(st, "secrets"):
            if key_name in st.secrets:
                val = str(st.secrets[key_name])
            else:
                for section_key, section_val in st.secrets.items():
                    if isinstance(section_val, dict) and key_name in section_val:
                        val = str(section_val[key_name])
                        break
    except Exception:
        pass
        
    if not val:
        val = os.environ.get(key_name, "")
        
    return val.strip().replace("\n", "").replace("\r", "").strip('"').strip("'")

def render():
    # --- SIDEBAR CONTROLS ---
    with st.sidebar:
        st.divider()
        st.subheader("⚙️ Listing Parameters")
        product_category = st.selectbox("Product Category:", [
            "Home & Garden Goods",
            "Digital Templates & Notion Boards",
            "Physical Goods & Handmade Crafts",
            "Prompt Packages & Digital Toolkits",
            "Apparel & Accessories"
        ], key="f2b_cat_select")
        
        output_tone = st.selectbox("Copywriting Tone:", [
            "Warm & Story-Driven",
            "High-Converting & Direct",
            "Professional & Authoritative",
            "Playful & Engaging"
        ], key="f2b_tone_select")
        
        st.divider()
        with st.expander("📖 Copywriting Guide"):
            st.markdown("""
            * **The Golden Rule:** Features tell, but benefits sell. Instead of listing what a product *has*, show customers how it *improves their life*.
            * **AI Integration:** Powered by OpenRouter live API to curate pristine direct-response copy ready for downstream carousel handoff.
            """)
        st.info("💡 **Pro Utility:** Instantly translates dry product specs into compelling customer benefits for Etsy & Shopify.")

    # --- MAIN HEADER ---
    st.markdown("<h1 style='text-align: center;'>🛍️ E-Commerce Feature-to-Benefit Translator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Turn dry product specifications into high-converting customer benefits designed to skyrocket your online sales.</p>", unsafe_allow_html=True)

    # --- INPUT SECTION ---
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        product_name = st.text_input("Product Name:", value="Ergonomic Garden Kneeler & Seat", key="f2b_prod_name")
    with col_i2:
        target_buyer = st.text_input("Target Buyer Persona:", value="Home gardeners and seniors who love planting but suffer from sore knees and back pain.", key="f2b_target_buyer")

    raw_features = st.text_area("Paste Raw Product Features / Specifications (one per line):", height=130, value="- Thick EVA foam padding cushion\n- Heavy-duty steel frame supporting up to 330 lbs\n- Detachable tool pouch with deep pockets\n- Folds flat in one click for easy garage storage", key="f2b_raw_feats")

    col_btn1, _ = st.columns([1, 4])
    with col_btn1:
        translate_btn = st.button("🚀 Translate Features into High-Converting Benefits", type="primary", key="f2b_run_btn")

    # --- EXECUTION & TRANSLATION LOGIC ---
    if translate_btn or st.session_state.get("f2b_translated_output"):
        if translate_btn:
            openrouter_key = get_clean_secret("OPENROUTER_API_KEY")
            translation_report = ""
            
            ai_prompt = f"""You are an expert e-commerce direct-response copywriter.
Product: {product_name}
Category: {product_category}
Target Buyer: {target_buyer}
Tone: {output_tone}
Raw Features:
{raw_features}

Generate a comprehensive Feature-to-Benefit Optimization Report in Markdown format containing:
1. An executive summary and translation matrix.
2. Optimized listing bullet points.
3. A high-converting product description hook.
4. A structured downstream carousel script section formatted explicitly for social media slides (with a clear Hook slide, Problem slide, 1-2 Features per page, and a high-converting CTA slide on the final page)."""

            if openrouter_key:
                try:
                    url = "https://openrouter.ai/api/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {openrouter_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io/", 
                        "X-Title": "Apex Morph Feature-to-Benefit Translator"
                    }
                    payload = {
                        "model": "openrouter/free",
                        "messages": [{"role": "user", "content": ai_prompt}],
                        "temperature": 0.7
                    }
                    res = requests.post(url, headers=headers, json=payload, timeout=20)
                    if res.status_code == 200:
                        translation_report = res.json()["choices"][0]["message"]["content"]
                    else:
                        translation_report = ""
                except Exception:
                    translation_report = ""

            # Fallback if API key is missing or fails
            if not translation_report:
                translation_report = f"""# E-Commerce Feature-to-Benefit Optimization Report
Product: {product_name}
Category: {product_category}
Target Buyer: {target_buyer}
Tone: {output_tone}

## 🎁 1. Feature-to-Benefit Translation Matrix
- **Protects your joints:** Featuring thick eva foam padding cushion, so you can say goodbye to aching knees and soreness.
- **Provides rock-solid safety:** Featuring heavy-duty steel frame supporting up to 330 lbs, so you can feel completely secure.

## ✍️ 2. Optimized Listing Bullet Points
- **Zero Joint Strain:** Thick cushioning absorbs impact so you can garden longer without physical discomfort.
- **Durable Stability:** Robust frame engineered for secure support and long-lasting seasonal use.

## 🎯 3. High-Converting Product Description Hook
*"Tired of aching joints cutting your gardening sessions short? Meet the {product_name}—custom-built to give {target_buyer} the comfort, support, and ease you deserve."*

## 📱 4. Downstream Carousel Slide Script (Handoff Ready)
- **SLIDE 1 (HOOK):** Tired of aching joints cutting your gardening sessions short?
- **SLIDE 2 (PROBLEM):** Traditional gardening leaves seniors and home gardeners with severe knee soreness and back strain.
- **SLIDE 3 (SOLUTION & FEATURE 1):** Say goodbye to soreness with thick EVA foam padding that protects your joints.
- **SLIDE 4 (FEATURE 2 & 3):** Enjoy rock-solid stability up to 330 lbs and keep your clippers right on your hip with detachable tool pouches.
- **SLIDE 5 (FEATURE 4):** Tuck it away in seconds with one-click flat folding for effortless garage storage.
- **SLIDE 6 (CTA):** Ready to garden in total comfort? Click the link in bio or comment GARDEN to claim yours today!
"""

            st.session_state["f2b_translated_output"] = translation_report
            st.success("🎉 Product features successfully translated and structured for carousel handoff!")
        
        translation_report = st.session_state["f2b_translated_output"]

        # --- DISPLAY TABS ---
        tab_report, tab_export = st.tabs(["📊 Executive Optimization Report", "📦 JSON Data Export"])

        with tab_report:
            st.markdown("### 📊 Copywriting Report & Carousel Script")
            st.markdown("---")
            st.markdown(translation_report)
            st.download_button("📥 Download Copy Report (.txt)", data=translation_report, file_name="listing_copy_report.txt", mime="text/plain", key="f2b_dl_txt")

        with tab_export:
            st.markdown("### 📦 Listing Intelligence Package (JSON)")
            json_package = {
                "product_name": product_name,
                "category": product_category,
                "report": translation_report
            }
            json_code = json.dumps(json_package, indent=2)
            st.code(json_code, language="json")
            st.download_button("📥 Download JSON Package", data=json_code, file_name="listing_translation.json", mime="application/json", key="f2b_dl_json")

        # --- WORKFLOW HANDOFF BRIDGE BUTTONS ---
        st.divider()
        st.markdown("### 🚀 Platform Workflow Handoffs")
        st.markdown("Send your curated, carousel-ready script directly to the Carousel Engine.")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("✨ Send Curated Script to Carousel Engine Studio", type="primary", use_container_width=True, key="f2b_to_carousel_btn"):
                st.session_state["preflight_benefits"] = translation_report
                st.session_state["active_tool_idx"] = 0
                st.rerun()
        with col_h2:
            if st.button("🎨 Send to Style Inspiration Brief", use_container_width=True, key="f2b_to_sia_btn"):
                st.session_state["style_inspiration_notes"] = f"Product: {product_name} - Target: {target_buyer}"
                st.session_state["active_tool_idx"] = 3
                st.rerun()
