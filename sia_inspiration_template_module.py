# sia_inspiration_template_module.py • Full-Bleed Background Replicator for Exact Inspiration Match
import streamlit as st
import base64
import io
import textwrap

def get_uploaded_swipe_base64():
    swipe_bytes = st.session_state.get("sia_uploaded_swipe_bytes", None)
    if not swipe_bytes:
        uploaded_files = st.session_state.get("sia_uploaded_files", None)
        if uploaded_files:
            try:
                swipe_bytes = uploaded_files[0].getvalue()
                st.session_state["sia_uploaded_swipe_bytes"] = swipe_bytes
            except Exception:
                pass
    if swipe_bytes:
        try:
            encoded_b64 = base64.b64encode(swipe_bytes).decode("utf-8")
            return "data:image/png;base64," + encoded_b64
        except Exception:
            pass
    return None

def build_inspiration_editorial_deck(deck, main_title="", flower_query="white rose", object_query="ceramic vase", date_str="OCT 8 • 2026"):
    uploaded_swipe_b64 = get_uploaded_swipe_base64()
    
    styled = []
    total = len(deck)
    
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        slide_title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        active_headline = main_title.strip() if main_title and main_title.strip() else slide_title
        formatted_title = active_headline.replace("&", "<br>&")
        
        if uploaded_swipe_b64:
            # Full-bleed absolute image wrapper + dark gradient overlay for crystal-clear text legibility
            html = textwrap.dedent(f"""
            <div style="position: relative; width: 100%; max-width: 580px; height: 560px; margin: 0 auto; border-radius: 24px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7); font-family: Georgia, serif;">
                <img src="{uploaded_swipe_b64}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1;" />
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.75)); z-index: 2;"></div>
                <div style="position: relative; z-index: 3; height: 100%; padding: 50px 36px; display: flex; flex-direction: column; justify-content: space-between; text-align: center; color: #ffffff; box-sizing: border-box;">
                    <div>
                        <div style="color: #fde047; font-size: 11px; font-weight: 800; letter-spacing: 2px; margin-bottom: 16px; text-transform: uppercase; font-family: sans-serif;">
                            SLIDE {idx+1} OF {total} • {cat}
                        </div>
                        <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 18px; text-shadow: 0 2px 6px rgba(0,0,0,0.8);">
                            {formatted_title}
                        </h2>
                        <p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; margin-bottom: 20px; font-family: sans-serif; text-shadow: 0 1px 4px rgba(0,0,0,0.8);">
                            {content}
                        </p>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; color: #e2e8f0; font-size: 11px; font-weight: 600; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 16px; text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif;">
                        <div>{date_str}</div>
                        <div>NIKKI'S SALON</div>
                    </div>
                </div>
            </div>
            """).strip()
        else:
            html = textwrap.dedent(f"""
            <div style="background-color: #b0543c; padding: 48px 36px; border-radius: 16px; max-width: 580px; margin: 0 auto; font-family: Georgia, serif; color: #ffffff; box-shadow: 0 30px 60px -15px rgba(0,0,0,0.6);">
                <div style="text-align: center; margin-bottom: 24px;">
                    <div style="color: #fde047; font-size: 10px; font-weight: 700; letter-spacing: 4px; margin-bottom: 8px; text-transform: uppercase; font-family: sans-serif;">
                        {cat} • {idx+1}/{total}
                    </div>
                    <h1 style="color: #ffffff; font-size: 26px; font-weight: 400; letter-spacing: 2.5px; line-height: 1.25; margin: 0; text-transform: uppercase;">
                        {formatted_title}
                    </h1>
                </div>
                <div style="text-align: center; margin-bottom: 30px; padding: 0 16px;">
                    <p style="color: #f3f4f6; font-size: 15px; line-height: 1.6; font-family: sans-serif; margin: 0; font-weight: 300;">
                        {content}
                    </p>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; color: #ffffff; font-size: 10px; letter-spacing: 2px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 16px; text-transform: uppercase; font-family: sans-serif;">
                    <div>{date_str}</div>
                    <div>NIKKI'S SALON</div>
                </div>
            </div>
            """).strip()
        
        styled.append({
            "category": cat,
            "title": slide_title,
            "content": content,
            "rendered_html": html
        })
    return styled
