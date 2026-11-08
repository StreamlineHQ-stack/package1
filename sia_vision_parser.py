import base64
import json
from io import BytesIO
from PIL import Image
from openai import OpenAI

def image_to_data_url(uploaded_file, max_dimension=1600):
    if hasattr(uploaded_file, "getvalue"):
        image = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGB")
    else:
        image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((max_dimension, max_dimension))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=88)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}", image

def analyze_image(api_key, model, image_data_url, user_focus="Analyze visual elements."):
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://apexmorph.com",
            "X-Title": "ApexMorph Creator Suite",
        }
    )
    system_prompt = """You are an expert visual layout analyst. Return ONLY valid JSON with these exact keys:
- design_style (string)
- visual_mood (string)
- design_intent (string)
- palette (array of strings)
- foreground_figure (string: describe any human figure, object, or person present, or 'None')
- background_scene (string: describe the total background scene/environment e.g. solid color, gradient, forest, beach, studio, mountains, etc.)
- composition (string)
- background_generation_brief (string)"""
    
    prompt = system_prompt + "\n\nFocus: " + user_focus
    
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ],
        max_tokens=1000
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[:-3].strip()
    return json.loads(raw)