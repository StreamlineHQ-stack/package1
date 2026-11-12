# slide_visual_asset_extractor.py • Master Slide Composition Pipeline
from PIL import Image, ImageFilter, ImageEnhance
import io
import numpy as np

try:
    from rembg import remove, new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class SlideVisualAssetExtractor:
    def __init__(self):
        self.last_mode2_report = {}
        self.last_transparent_bytes = None
        self.rembg_session = None
        if REMBG_AVAILABLE:
            try:
                self.rembg_session = new_session("silueta")
            except Exception:
                self.rembg_session = None

    def _open_rgb(self, image_bytes):
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")

    def render_mode_1_background(self, image_bytes):
        img = self._open_rgb(image_bytes)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=50))
        enhancer = ImageEnhance.Contrast(blurred)
        background_isolated = enhancer.enhance(0.9)
        out = io.BytesIO()
        background_isolated.save(out, format="PNG")
        out.seek(0)
        return out.getvalue()

    def render_mode_2_textless(self, image_bytes, api_key="", crop_margins=(0, 0, 0, 0)):
        """
        Mode 2: Two-Output Separation Workflow:
        1. Column 1: Clean solid background canvas matching original dimensions.
        2. Column 2: Transparent core asset mapped to exact full-canvas size.
        """
        original = self._open_rgb(image_bytes)
        w, h = original.size
        
        # 1. Sample dominant background color from inner border safely
        try:
            bg_color = original.getpixel((20, 20))
            if max(bg_color[:3]) - min(bg_color[:3]) < 15 and bg_color[0] > 200:
                bg_color = (210, 40, 30) # Rich poster red/orange fallback
        except Exception:
            bg_color = (210, 40, 30)

        # Generate solid color background canvas
        clean_bg = Image.new("RGB", (w, h), bg_color[:3])
        bg_out = io.BytesIO()
        clean_bg.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Extract object into a transparent layer matching full canvas dimensions
        transparent_card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        if REMBG_AVAILABLE:
            try:
                extracted_obj = remove(original, session=self.rembg_session).convert("RGBA")
                transparent_card.paste(extracted_obj, (0, 0), extracted_obj)
            except Exception:
                transparent_card = original.convert("RGBA")
        else:
            transparent_card = original.convert("RGBA")

        trans_out = io.BytesIO()
        transparent_card.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        self.last_transparent_bytes = trans_bytes_data

        coords_report = {
            "top": 0,
            "bottom": 0,
            "left": 0,
            "right": 0,
            "width": w,
            "height": h,
            "canvas_width": w,
            "canvas_height": h
        }
        self.last_mode2_report = coords_report

        return {
            "background_bytes": bg_bytes_data,
            "transparent_asset_bytes": trans_bytes_data,
            "coordinates": coords_report
        }

    def render_mode_3_composition(self, background_bytes, subject_bytes=None, reference_bytes=None):
        """
        Mode 3: Pastes the transparent subject layer back onto the solid background canvas
        at exact dimensions without altering internal proportions.
        """
        bg = self._open_rgb(background_bytes).convert("RGBA")
        bw, bh = bg.size

        target_subject = subject_bytes if subject_bytes else self.last_transparent_bytes

        if target_subject:
            try:
                obj = Image.open(io.BytesIO(target_subject)).convert("RGBA")
                if obj.size != (bw, bh):
                    obj = obj.resize((bw, bh), Image.Resampling.LANCZOS)

                bg.paste(obj, (0, 0), mask=obj.split()[-1])
            except Exception as e:
                print(f"Composition warning: {e}")

        out = io.BytesIO()
        bg.convert("RGB").save(out, format="PNG", optimize=True)
        out.seek(0)
        return out.getvalue()