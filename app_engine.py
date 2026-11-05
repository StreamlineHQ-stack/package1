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
    openrouter_key = get_clean_secret("OPENROUTER_API_KEY")

    system_prompt = f"""You are an expert direct-response social media strategist. 
Transform the following input text/report/features into EXACTLY {slide_count} high-converting carousel slides. 
Return ONLY a valid JSON array of objects with no extra text, markdown formatting, or backticks. 
Each object in the array must have these exact keys: "category", "title", "content".
- Slide 1 must be a powerful hook as the "title", with empty "content".
- Slide 2 must state the core problem as the "title", with empty "content".
- Slides 3 through {slide_count-1} must state a specific feature/solution benefit as the "title", with a supporting explanatory sentence as the "content".
- The final slide must be a strong Call to Action as the "title", with action steps as "content"."""

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
                pass
        except Exception:
            pass

    # --- BULLETPROOF LOCAL FALLBACK PARSER ---
    raw_lines = input_text.split("\n")
    cleaned_lines = []
    for l in raw_lines:
        l_str = l.strip()
        if not l_str or l_str.startswith("#") or l_str.startswith("---") or l_str.startswith("==="):
            continue
        # Strip workflow prefixes like "- SLIDE 3 (SOLUTION): "
        if ":" in l_str and ("SLIDE" in l_str.upper() or "HOOK" in l_str.upper() or "PROBLEM" in l_str.upper() or "SOLUTION" in l_str.upper() or "FEATURE" in l_str.upper() or "CTA" in l_str.upper()):
            parts = l_str.split(":", 1)
            l_str = parts[1].strip()
        
        for prefix in ["*", "-", "•", ">", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."]:
            if l_str.startswith(prefix):
                l_str = l_str[len(prefix):].strip()
        if l_str:
            cleaned_lines.append(l_str)

    blueprint = []
    for idx in range(slide_count):
        if idx < len(cleaned_lines):
            text = cleaned_lines[idx]
        else:
            text = f"Strategic execution guideline {idx+1} for maximum creator growth."

        # Assign structured title and body based on slide position
        if idx == 0:
            title = text
            content = ""
        elif idx == 1:
            title = text
            content = ""
        elif idx == slide_count - 1:
            title = "Ready to take action?"
            content = text
        else:
            if "," in text:
                parts = text.split(",", 1)
                title = parts[0].strip()
                content = parts[1].strip().capitalize()
            elif "with" in text.lower():
                parts = text.lower().split("with", 1)
                title = text[:len(parts[0])].strip()
                content = "Featuring " + parts[1].strip().capitalize()
            else:
                title = text
                content = "Designed to deliver absolute reliability and top-tier performance."

        blueprint.append({
            "category": f"SLIDE {idx+1}",
            "title": title,
            "content": content
        })

    return json.dumps(blueprint[:slide_count]), "⚡ Bulletproof Content Extractor Active"

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
                        "title": f"Strategic execution point {idx+1}",
                        "content": ""
                    })
            elif len(formatted) > slide_count:
                formatted = formatted[:slide_count]
            return formatted
    except Exception:
        pass
    return None