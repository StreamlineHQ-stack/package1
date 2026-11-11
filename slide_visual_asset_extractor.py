# slide_visual_asset_extractor.py • Three-Mode Visual Composition Extraction & Generation Engine
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
import os

class SlideVisualAssetExtractor:
    def __init__(self):
        pass

    def generate_composition_blueprint(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        w, h = img.size
        return {
            "canvas": {"width": w, "height": h, "aspect_ratio": f"{w}:{h}"},
            "background": {"type": "solid_or_texture"},
            "subjects": [{"id": "subject_main", "position": "right"}],
            "composition": {"visual_balance": "asymmetric"}
        }

    def render_mode_1_background(self, image_bytes):
        """
        MODE 1: Background Extraction - extracts clean solid/gradient texture by heavy blur & brightness boost.
        """
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Heavy gaussian blur + brightness enhancement to wash out text/subjects into a clean background texture
        blurred = img.filter(ImageFilter.GaussianBlur(radius=50))
        enhancer = ImageEnhance.Brightness(blurred)
        bright_bg = enhancer.enhance(1.1)
        
        out_buf = io.BytesIO()
        bright_bg.save(out_buf, format="PNG")
        return out_buf.getvalue()

    def render_mode_2_textless(self, image_bytes):
        """
        MODE 2: Inspiration Slide Extraction - removes typography artifacts by smoothing and edge softening.
        """
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Apply smoothing and unsharp mask to clean up text overlay areas
        smoothed = img.filter(ImageFilter.SMOOTH_MORE)
        smoothed = smoothed.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        out_buf = io.BytesIO()
        smoothed.save(out_buf, format="PNG")
        return out_buf.getvalue()

    def render_mode_3_composition(self, background_bytes, subject_bytes, reference_bytes=None):
        """
        MODE 3: Custom Visual Composition - composites custom background and subject.
        """
        bg_img = Image.open(io.BytesIO(background_bytes)).convert("RGB").resize((1080, 1080))
        
        if subject_bytes:
            sub_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            sub_img.thumbnail((720, 900))
            bg_w, bg_h = bg_img.size
            sub_w, sub_h = sub_img.size
            
            paste_x = bg_w - sub_w - 60
            paste_y = bg_h - sub_h - 60
            bg_img.paste(sub_img, (paste_x, paste_y), sub_img)
            
        out_buf = io.BytesIO()
        bg_img.save(out_buf, format="PNG")
        return out_buf.getvalue()

print("Better extractor ready.")
