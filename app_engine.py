# app_engine.py • Robust AI Carousel Deck Generator with Smart Topic Context & OpenRouter API Integration
import os
import json
import requests
import streamlit as st

def generate_carousel_deck(prompt_or_notes, slide_count=6, mode="autopilot"):
    # Multi-variant lookup across Streamlit Secrets, Session State, and Environment Variables
    api_key = None
    
    # 1. Check Streamlit Cloud Secrets (checking common casing variants)
    try:
        for key_candidate in ["OPENROUTER_API_KEY", "openrouter_api_key", "OPENROUTER_KEY", "openrouter_key"]:
            if key_candidate in st.secrets:
                api_key = st.secrets[key_candidate]
                break
    except Exception:
        pass
        
    # 2. Check Session State Override and Environment Variables if not found in secrets
    if not api_key:
        api_key = (
            st.session_state.get("admin_openrouter_api_key_override") 
            or os.environ.get("OPENROUTER_API_KEY") 
            or os.environ.get("openrouter_api_key")
            or os.environ.get("GROQ_API_KEY")
        )
    
    if api_key:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://apexmorph.app",
                "X-Title": "ApexMorph Carousel Engine"
            }
            
            system_prompt = (
                f"You are an expert direct-response copywriter and social media growth strategist. "
                f"Generate exactly {slide_count} high-converting carousel slides for the given topic/notes. "
                f"Return ONLY valid JSON as a list of objects, where each object has keys: "
                f"'category' (e.g. HOOK, PROBLEM, SOLUTION 1, CTA), 'title' (punchy headline), and 'content' (detailed body text)."
            )
            
            payload = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Topic/Notes: {prompt_or_notes}\nSlide Count: {slide_count}"}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                content_str = res_json["choices"][0]["message"]["content"]
                if "```json" in content_str:
                    content_str = content_str.split("```json")[1].split("```")[0].strip()
                elif "```" in content_str:
                    content_str = content_str.split("```")[1].split("```")[0].strip()
                    
                slides = json.loads(content_str)
                if isinstance(slides, list) and len(slides) > 0:
                    return slides, "⚡ AI Live Generation Successful via OpenRouter!"
            else:
                return [], f"⚠️ OpenRouter Error ({response.status_code}): {response.text[:150]}"
        except Exception as e:
            return [], f"⚠️ API Exception: {str(e)}"

    # Intelligent Contextual Generator tailored specifically to the user's prompt (Fallback)
    slides = []
    topic = prompt_or_notes.strip() if prompt_or_notes else "Mastering Your Craft"
    
    if "time" in topic.lower() or "management" in topic.lower():
        deck_templates = [
            ("HOOK", "Why is time management important?", "Time is your only non-renewable resource. Once spent, it is gone forever."),
            ("PROBLEM", "The trap of busywork vs. real leverage.", "Most people fill their days with low-value tasks and wonder why they feel exhausted."),
            ("THE SHIFT", "Adopt the 80/20 rule for daily execution.", "Identify the 20% of actions that drive 80% of your business and personal growth."),
            ("SYSTEM", "Time blocking is your ultimate superpower.", "Schedule your deep work blocks ruthlessly and protect them like meetings with VIP clients."),
            ("LEVERAGE", "Audit where your hours actually go.", "Track your time for 3 days and eliminate energy drains and digital distractions."),
            ("CTA", "Ready to reclaim your schedule?", "Comment 'TIME' below or click the link in bio to get our complete productivity planner.")
        ]
    else:
        deck_templates = [
            ("HOOK", f"The hidden truth about {topic.lower()}.", f"Mastering {topic.lower()} separates top performers from everyone else."),
            ("PROBLEM", "Why traditional approaches always fail.", "Relying on old habits and willpower leads straight to burnout and stagnation."),
            ("SOLUTION", "Build a repeatable system that scales.", "Create a streamlined framework designed for speed, efficiency, and consistent results."),
            ("EXECUTION", "Step 1: Focus on high-leverage inputs.", "Prioritize quality over quantity and eliminate unnecessary friction in your workflow."),
            ("OPTIMIZATION", "Step 2: Refine and measure your progress.", "Track key metrics weekly so you can double down on what's actually working."),
            ("CTA", f"Ready to master {topic.lower()}?", f"Comment 'GROWTH' below or click the link in bio to access our complete framework.")
        ]
        
    for i in range(slide_count):
        if i < len(deck_templates):
            cat, title, body = deck_templates[i]
        else:
            cat = f"STEP {i+1}"
            title = f"Advanced execution strategy for {topic.lower()}."
            body = f"Consistent execution of fundamentals compounds into extraordinary results over time."
            
        slides.append({
            "category": cat,
            "title": title,
            "content": body
        })
        
    return slides, "⚡ Smart Contextual Generator Active (No API Key Detected)"