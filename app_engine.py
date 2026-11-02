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
    clean_topic = raw_input
    if clean_topic.lower().startswith(("why is ", "how to ", "what is ", "why do ")):
        clean_topic = clean_topic.split(" ", 2)[-1]

    debug_errors = []
    
    # Retrieve OpenRouter Key (checks secrets or environment)
    openrouter_key = get_clean_secret("OPENROUTER_API_KEY")

    system_prompt = f"""You are an expert direct-response social media strategist. 
Generate EXACTLY {slide_count} carousel slides for the topic: "{input_text}". 
Return ONLY a valid JSON array of objects with no extra text, markdown formatting, or backticks. 
Each object in the array must have these exact keys: "category", "title", "content"."""

    # --- OPENROUTER FREE-TIER ROUTER ENGINE ---
    if openrouter_key:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io/", 
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

    # --- ULTIMATE SAFETY NET: PERMUTATION ENGINE ---
    error_summary = " | ".join(debug_errors)
    status_msg = f"⚡ High-Performance Permutation Engine Active (Diagnostics: {error_summary})"
    
    blueprint = [
        {"category": "HOOK", "title": f"The Brutal Truth About {raw_input}", "content": f"Most creators struggle with {raw_input.lower()} because they lack a systematic, friction-free execution framework."},
        {"category": "PROBLEM", "title": "Why Standard Approaches Fail", "content": f"Trying to navigate {raw_input.lower()} through sheer guesswork leads to high friction, constant burnout, and stalled momentum."},
        {"category": "AGITATION", "title": "The True Cost of Inaction", "content": "Every single day you delay fixing this wastes valuable hours, drains your energy, and leaves high-value opportunities on the table."},
        {"category": "SOLUTION", "title": "The Streamlined Solution", "content": f"Enter the streamlined blueprint: a zero-friction system built specifically to master {clean_topic} without the fluff."},
        {"category": "PROOF", "title": "Engineered for Efficiency", "content": "Built for speed, high visual contrast, and direct-response impact that commands attention in a crowded feed."},
        {"category": "ACTION", "title": "Take Control Today", "content": "Stop guessing, stop spinning your wheels, and start executing with precision infrastructure."}
    ]
    return json.dumps(blueprint[:slide_count]), status_msg

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