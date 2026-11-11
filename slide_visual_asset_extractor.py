# slide_visual_asset_extractor.py • Architectural Multi-Mode Asset Extractor
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import io
import base64
import json
import requests

class SlideVisualAssetExtractor:
    def __init__(self):
        self.last_report = {}

    def _open_rgb(self, image_bytes):
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")

    def render_mode_1_background_isolation(self, image_bytes, api_key=""):
        """
        Mode 1: Background & Texture Isolation.
        Isolates background gradients, textures, and color washes by neutralizing 
        foreground subjects and text overlays.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # Apply high-radius blur and contrast tuning to isolate pure background color/texture
        blurred = img.filter(ImageFilter.GaussianBlur(radius=60))
        enhancer = ImageEnhance.Contrast(blurred)
        bg_isolated = enhancer.enhance(0.85)
        
        out = io.BytesIO()
        bg_isolated.save(out, format="PNG", optimize=True)
        return out.getvalue()

    def render_mode_2_textless_composition(self, image_bytes, api_key=""):
        """
        Mode 2: Preserve Original Visual Composition (Remove Text Only).
        Uses AI Vision to detect text bounding boxes dynamically across any layout 
        (top, side, or center) and inpaits them using adjacent background pixels.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        boxes = []
        if api_key:
            try:
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                base64_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Detect all text blocks, titles, subtitles, headers, or watermarks in this image. Return a JSON object with a key 'boxes' containing a list of bounding boxes normalized from 0 to 1000 in format [ymin, xmin, ymax, xmax]."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{base64_img}"}
                                }
                            ]
                        }
                    ],
                    "response_format": {"type": "json_object"}
                }
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers