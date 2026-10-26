import os
import json
import time
import random
import requests
import streamlit as st

# --- LOCAL DESKTOP API CONFIGURATION ---
API_KEY = "AQ.Ab8RN6JUe7otxlzSqjkjyeGWI6pMgryfzo3oGBa2mk9CUsYYXQ"

if not API_KEY:
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if not API_KEY:
    API_KEY = os.environ.get("GEMINI_API_KEY", "")

def get_fallback_deck(input_text, slide_count, mode):
    """Zero-failure local fallback engine with strict narrative sequencing."""
    deck = []
    
    if mode == "framework":
        hook, problem, solution, cta = "", "", "", ""
        for line in input_text.split('\n'):
            line_str = line.strip()
            if "Hook Element:" in line_str:
                hook = line_str.split("Hook Element:")[-1].strip()
            elif "Problem/Agitation:" in line_str:
                problem = line_str.split("Problem/Agitation:")[-1].strip()
            elif "Solution/Steps:" in line_str:
                solution = line_str.split("Solution/Steps:")[-1].strip()
            elif "Call to Action:" in line_str:
                cta = line_str.split("Call to Action:")[-1].strip()
        
        deck.append({"category": "HOOK", "title": "Core Headline", "content": hook or "Why you face this bottleneck."})
        deck.append({"category": "PROBLEM", "title": "The Pain Point", "content": problem or "The underlying issue holding you back."})
        deck.append({"category": "SOLUTION", "title": "The System", "content": solution or "The exact tactical steps to resolve it."})
        
        total_steps_needed = max(1, slide_count - 4)
        for step_num in range(1, total_steps_needed + 1):
            deck.append({
                "category": f"STEP {step_num}", 
                "title": f"Implementation Phase {step_num}", 
                "content": f"Execute protocol step {step_num} consistently for maximum compounding leverage."
            })
            
        deck.append({"category": "CTA", "title": "Next Steps", "content": cta or "Take action today."})
        return json.dumps(deck[:slide_count])

    elif mode == "custom":
        raw_lines = [line.strip() for line in input_text.split('\n') if line.strip() and not line.strip().startswith("Framework Style:")]
        for i in range(1, slide_count + 1):
            category = "CUSTOM NOTE"
            title = f"Key Insight #{i}"
            if raw_lines and i <= len(raw_lines):
                content = raw_lines[i-1]
            else:
                content = f"Detailed breakdown and execution step {i} based on your input."
            deck.append({
                "category": category,
                "title": title,
                "content": content
            })
        return json.dumps(deck)

    else:
        categories = ["HOOK", "PROBLEM", "AGITATION", "SYSTEM", "PROOF", "CTA"]
        clean_headline = input_text.strip()
        for i in range(1, slide_count + 1):
            cat = categories[(i - 1) % len(categories)]
            if i == 1:
                title = "The Core Dilemma"
                content = f"Why everyone struggles with: {clean_headline}"
            elif i == slide_count:
                title = "Final Takeaway"
                content = f"Mastering {clean_headline} starts with taking consistent daily action."
            else:
                title = f"Strategic Pillar #{i}"
                content = f"Detailed execution phase {i} addressing the nuances of {clean_headline}."
                
            deck.append({
                "category": cat,
                "title": title,
                "content": content
            })
        return json.dumps(deck)

def generate_carousel_deck(input_text, slide_count=6, mode="autopilot"):
    if not API_KEY:
        st.warning("⚠️ Warning: No API Key found. Using local instant generator.")
        return get_fallback_deck(input_text, slide_count, mode)

    # Priority-ordered list of model endpoints to try for zero downtime
    model_candidates = [
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash"
    ]

    if mode == "autopilot":
        system_instruction = f"""
        You are an expert social media strategist. Turn the following headline/topic into a high-converting carousel deck.
        Generate EXACTLY {slide_count} slides.
        
        Return ONLY a valid JSON array of objects with no extra text or markdown code blocks:
        [
          {{"category": "HOOK", "title": "Slide Title", "content": "Punchy body content..."}},
          ...
        ]
        """
    elif mode == "framework":
        system_instruction = f"""
        You are a precision content editor. Transform the structured framework notes into a high-impact direct-response carousel deck.
        Generate EXACTLY {slide_count} slides following this mandatory logical flow: 
        Slide 1: Hook, Slide 2: Problem, Slide 3: Solution, Intermediate Slides: Sequenced Execution Steps (Step 1, Step 2, etc.), Final Slide: Call to Action (CTA).
        
        Return ONLY a valid JSON array of objects with no extra text or markdown code blocks:
        [
          {{"category": "HOOK", "title": "Slide Title", "content": "Punchy body content..."}},
          ...
        ]
        """
    else:
        system_instruction = f"""
        You are a content editor. Take the raw coaching notes and format them directly into a cohesive slide sequence.
        Generate EXACTLY {slide_count} slides.
        
        Return ONLY a valid JSON array of objects with no extra text or markdown code blocks:
        [
          {{"category": "INSIGHT", "title": "Slide Title", "content": "Formatted body content..."}},
          ...
        ]
        """
    
    prompt = f"{system_instruction}\n\nUser Input:\n{input_text}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    # Iterate through models with automatic retry and failover
    for model_name in model_candidates:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=20)
                
                # Handle 401 Unauthorized gracefully
                if response.status_code == 401:
                    st.error("🔑 Authentication Error (401): Please verify your Gemini API key.")
                    return get_fallback_deck(input_text, slide_count, mode)
                
                if response.status_code != 200:
                    raise Exception(f"API status code {response.status_code}")
                    
                res_json = response.json()
                raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                
                cleaned_response = raw_text.strip().replace("```json", "").replace("```", "")
                slides_data = json.loads(cleaned_response)
                
                if mode == "framework" and isinstance(slides_data, list) and len(slides_data) > 0:
                    extracted_cta = ""
                    for line in input_text.split('\n'):
                        if "Call to Action:" in line:
                            extracted_cta = line.split("Call to Action:")[-1].strip()
                    
                    while len(slides_data) < slide_count:
                        slides_data.insert(-1, {
                            "category": f"STEP {len(slides_data)}",
                            "title": f"Implementation Phase",
                            "content": "Execute protocol steps consistently for maximum momentum."
                        })
                    if len(slides_data) > slide_count:
                        slides_data = slides_data[:slide_count]
                    
                    if extracted_cta:
                        slides_data[-1] = {
                            "category": "CTA",
                            "title": "Next Steps",
                            "content": extracted_cta
                        }
                
                return json.dumps(slides_data)
                
            except Exception as e:
                print(f"Model {model_name} attempt {attempt+1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1 + random.uniform(0.2, 0.8))
                    continue
                break  # Failover to the next candidate model

    # Absolute safety net: zero disruption for users if all endpoints experience congestion
    st.info("ℹ️ AI servers are experiencing high traffic. Generated via instant local fallback engine.")
    return get_fallback_deck(input_text, slide_count, mode)