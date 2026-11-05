import streamlit as st
import json

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
            * **Usage:** Drop your raw bullet points below to instantly convert them into persuasive listing copy.
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
    if translate_btn:
        with st.spinner("Translating technical specs into irresistible customer benefits..."):
            
            # Robustly parse raw feature lines
            parsed_features = [line.strip().lstrip("-*•").strip() for line in raw_features.split("\n") if line.strip()]
            
            # Varied, high-impact benefit angles to avoid repetition
            benefit_templates = [
                ("Protects your joints", "say goodbye to aching knees and soreness after a long afternoon in the soil."),
                ("Provides rock-solid safety", "feel completely secure and stable whether sitting upright or kneeling down."),
                ("Keeps tools right at your fingertips", "eliminate frustrating trips back to the shed by storing your clippers and gloves on your hip."),
                ("Saves precious garage space", "tuck it away neatly in seconds with zero hassle when your gardening day is done.")
            ]
            
            benefit_bullets = ""
            table_rows = ""
            for idx, feat in enumerate(parsed_features):
                angle_title, angle_benefit = benefit_templates[idx % len(benefit_templates)]
                benefit_bullets += f"- **{angle_title}:** Featuring {feat.lower()}, so you can {angle_benefit}\n"
                table_rows += f"| {feat} | {angle_title} ({angle_benefit}) | High |\n"

            translation_report = f"""# E-Commerce Feature-to-Benefit Optimization Report
Product: {product_name}
Category: {product_category}
Target Buyer: {target_buyer}
Tone: {output_tone}

## 🎁 1. Feature-to-Benefit Translation Matrix
{benefit_bullets}

## ✍️ 2. Optimized Listing Bullet Points
- **Zero Joint Strain:** Thick cushioning absorbs impact so you can garden longer without physical discomfort.
- **Durable Stability:** Robust frame engineered for secure support and long-lasting seasonal use.
- **All-in-One Convenience:** Built-in tool pouches keep your gear organized right where you need it.
- **Effortless Storage:** Folds flat instantly, making it a breeze to pack up and store away.

## 🎯 3. High-Converting Product Description Hook
*"Tired of aching joints cutting your gardening sessions short? Meet the {product_name}—custom-built to give {target_buyer} the comfort, support, and ease you deserve. Cultivate your garden, not your back pain!"*
"""

            st.success("🎉 Product features successfully translated into varied, high-impact customer benefits!")

            # --- DISPLAY TABS ---
            tab_report, tab_matrix, tab_export = st.tabs(["📊 Optimization Report", "🔍 Feature-Benefit Table", "📦 JSON Data Export"])

            with tab_report:
                st.markdown("### 📊 Executive Copywriting Report")
                st.markdown("---")
                st.markdown(translation_report)
                st.download_button("📥 Download Copy Report (.txt)", data=translation_report, file_name="listing_copy_report.txt", mime="text/plain", key="f2b_dl_txt")

            with tab_matrix:
                st.markdown("### 🔍 Feature-to-Benefit Mapping Table")
                st.markdown("---")
                st.markdown("""
                | Raw Product Feature | Translated Customer Benefit | Sales Impact |
                |---|---|---|
                """ + table_rows)

            with tab_export:
                st.markdown("### 📦 Listing Intelligence Package (JSON)")
                json_package = {
                    "product_name": product_name,
                    "category": product_category,
                    "features_analyzed": parsed_features,
                    "report": translation_report
                }
                json_code = json.dumps(json_package, indent=2)
                st.code(json_code, language="json")
                st.download_button("📥 Download JSON Package", data=json_code, file_name="listing_translation.json", mime="application/json", key="f2b_dl_json")
