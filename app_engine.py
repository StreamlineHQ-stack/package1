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

def generate_carousel_deck(input_text, slide_count=6, mode="autopilot", preferred_provider="Auto-Cascade"):
    raw_input = input_text.strip() if input_text else "Core Strategy"
    clean_topic = raw_input.split("\n")[0].replace("#", "").replace("Product:", "").strip()
    if len(clean_topic) > 50:
        clean_topic = "High-Converting Product Benefits"

    debug_errors = []
    openrouter_key = get_clean_secret("OPENROUTER_API_KEY")

    system_prompt = f"""You are an expert direct-response social media strategist. 
Transform the following input text/report into EXACTLY {slide_count} high-converting carousel slides. 
Return ONLY a valid JSON array of objects with no extra text, markdown formatting, or backticks. 
Each object in the array must have these exact keys: "category", "title", "content"."""

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
    else:
        debug_errors.append("No OpenRouter API key found in secrets.")

    # --- INTELLIGENT NOTES / F2B FALLBACK PARSER ---
    lines = [line.strip() for line in input_text.split("\n") if line.strip() and not line.startswith("#")]
    blueprint = []
    categories = ["HOOK", "PROBLEM", "FEATURE 1", "FEATURE 2", "FEATURE 3", "ACTION"]
    for i in range(slide_count):
        cat = categories[i % len(categories)]
        if i < len(lines):
            line_clean = lines[i].lstrip("-*•").strip()
            title = line_clean[:40] + "..." if len(line_clean) > 40 else line_clean
            content = line_clean
        else:
            title = f"Key Advantage {i+1}"
            content = f"Leveraging direct-response benefits for {clean_topic} to maximize customer acquisition and sales conversion."
        
        blueprint.append({"category": cat, "title": title, "content": content})

    return json.dumps(blueprint[:slide_count]), "⚡ Intelligent Notes Parser Active (Fallback)"

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
            if len(parsed) < slide_count:
                while len(parsed) < slide_count:
                    parsed.insert(-1, {"category": f"STEP {len(parsed)}", "title": "Execution Phase", "content": "Apply tactical focus to accelerate momentum."})
            elif len(parsed) > slide_count:
                parsed = parsed[:slide_count]
            return parsed
    except Exception:
        pass
    return None