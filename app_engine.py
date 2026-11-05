import os
import json
import requests
import streamlit as st

def get_clean_secret(key_name):
    override_key = f"admin_{key_name.lower()}_override"
    if override_key in st.session_state and st.session_state[override_key]:
        return st.session_state[override_key].strip()
    val = ""
    try:
        if hasattr(st, "secrets") and key_name in st.secrets:
            val = str(st.secrets[key_name])
    except Exception:
        pass
    if not val:
        val = os.environ.get(key_name, "")
    return val.strip().replace("\n", "").replace("\r", "").strip('"').strip("'")

def generate_carousel_deck(input_text, slide_count=6, mode="autopilot", preferred_provider="Auto-Cascade"):
    raw_input = input_text.strip() if input_text else "Core Strategy"
    debug_errors = []
    
    openrouter_key = get_clean_secret("OPENROUTER_API_KEY")

    system_prompt = f"""You are an expert direct-response social media strategist. 
Transform the following input text/report/features into EXACTLY {slide_count} high-converting carousel slides. 
Return ONLY a valid JSON array of objects with no extra text, markdown formatting, or backticks. 
Each object in the array must have these exact keys: "category", "title", "content".
Slide 1 must be a powerful hook. Slides 2 through {slide_count-1} must be problem agitation and solution pillars. The final slide must be a strong Call to Action."""

    if openrouter_key:
        try:
            url = "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)"
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "[https://streamlit.io/](https://streamlit.io/)", 
                "X-Title": "Apex Morph Carousel Engine"
            }
            payload = {
                "model": "openrouter/free",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": input_text}],
                "temperature": 0.7
            }
            res = requests.post(url, headers=headers, json=payload, timeout=15)
            if res.status_code == 200:
                content = res.json()["choices"][0]["message"]["content"]
                parsed = parse_ai_json(content, slide_count)
                if parsed:
                    return json.dumps(parsed), "⚡ OpenRouter Free-Tier Router Active"
            else:
                debug_errors.append(f"OpenRouter HTTP {res.status_code}: {res.text[:100]}")
        except Exception as e:
            debug_errors.append(f"OpenRouter Error: {str(e)}")

    # --- CLEAN PARSER (NO KEY TAKEAWAYS) ---
    blueprint = []
    lines = [l.strip() for l in input_text.split("\n") if l.strip()]
    
    for idx in range(slide_count):
        if idx < len(lines):
            line_text = lines[idx]
            if ":" in line_text:
                line_text = line_text.split(":", 1)[1].strip()
            line_text = line_text.replace("*", "").strip()
        else:
            line_text = f"Strategic pillar and execution guideline {idx+1} for maximum impact."
            
        if idx == 0:
            title_text = line_text
            content_text = ""
        else:
            title_text = f"Core Principle {idx+1}"
            content_text = line_text

        blueprint.append({
            "category": f"SLIDE {idx+1}",
            "title": title_text,
            "content": content_text
        })

    return json.dumps(blueprint[:slide_count]), "⚡ Direct-Response Parser Active"

def parse_ai_json(raw_content, slide_count):
    try:
        cleaned = raw_content.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        parsed = json.loads(cleaned)
        if isinstance(parsed, list) and len(parsed) > 0:
            formatted = []
            for idx, item in enumerate(parsed):
                t = item.get("title", item.get("headline", ""))
                c = item.get("content", item.get("body", ""))
                formatted.append({
                    "category": f"SLIDE {idx+1}",
                    "title": t,
                    "content": c
                })
            if len(formatted) < slide_count:
                while len(formatted) < slide_count:
                    idx = len(formatted)
                    formatted.append({
                        "category": f"SLIDE {idx+1}",
                        "title": f"Strategic Pillar {idx+1}",
                        "content": "Execute with absolute precision and focus."
                    })
            elif len(formatted) > slide_count:
                formatted = formatted[:slide_count]
            return formatted
    except Exception:
        pass
    return None