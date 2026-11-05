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
    debug_errors = []
    openrouter_key = get_clean_secret("OPENROUTER_API_KEY")

    system_prompt = f"""You are an expert direct-response social media strategist. 
Transform the following input text/report into EXACTLY {slide_count} high-converting carousel slides. 
Return ONLY a valid JSON array of objects with no extra text, markdown formatting, or backticks. 
Each object in the array must have these exact keys: "category", "title", "content"."""

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

    # --- PRECISE SCRIPT PARSER FOR FEATURE-TO-BENEFIT HANDOFF ---
    blueprint = []
    lines = input_text.split("\n")
    
    for line in lines:
        clean_line = line.strip()
        if "SLIDE" in clean_line.upper() and ":" in clean_line:
            parts = clean_line.split(":", 1)
            header_part = parts[0].upper()
            content_part = parts[1].strip().replace("*", "").strip()
            
            cat = "STEP"
            if "HOOK" in header_part:
                cat = "HOOK"
                title = "The Core Hook"
            elif "PROBLEM" in header_part:
                cat = "PROBLEM"
                title = "The Core Problem"
            elif "SOLUTION" in header_part or "FEATURE 1" in header_part:
                cat = "SOLUTION"
                title = "Key Solution & Feature"
            elif "FEATURE" in header_part:
                cat = "FEATURE"
                title = "Product Advantage"
            elif "CTA" in header_part:
                cat = "ACTION"
                title = "Call To Action"
            else:
                cat = "INSIGHT"
                title = "Key Takeaway"
                
            blueprint.append({"category": cat, "title": title, "content": content_part})

    if not blueprint:
        filtered_lines = [l.strip().lstrip("-*•").strip() for l in lines if l.strip() and not l.startswith("#") and not l.lower().startswith(("product:", "category:", "target buyer:", "tone:"))]
        categories = ["HOOK", "PROBLEM", "BENEFIT 1", "BENEFIT 2", "BENEFIT 3", "CTA"]
        for i in range(slide_count):
            cat = categories[i % len(categories)]
            if i < len(filtered_lines):
                text_chunk = filtered_lines[i]
                if ":" in text_chunk:
                    parts = text_chunk.split(":", 1)
                    title = parts[0].strip().replace("*", "")
                    content = parts[1].strip().replace("*", "")
                else:
                    title = f"Advantage {i+1}"
                    content = text_chunk
            else:
                title = f"Key Advantage {i+1}"
                content = "Designed specifically to give you maximum comfort, support, and ease."
            blueprint.append({"category": cat, "title": title, "content": content})

    return json.dumps(blueprint[:slide_count]), "⚡ Precise Script Parser Active"

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
