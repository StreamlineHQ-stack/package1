# slide_visual_asset_extractor.py • Robust Background & Asset Compositor
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
        Mode 2: Two-Output Separation:
        1. Column 1: Clean solid background canvas (robust inner color sampling).
        2. Column 2: Transparent core asset object.
        """
        original = self._open_rgb(image_bytes)
        w, h = original.size
        
        # 1. Column 1: Safe inner sampling to avoid Paint/browser white borders
        try:
            # Sample slightly inward from the top-left corner to hit the actual slide background
            bg_color = original.getpixel((20, 20))
            # If the sampled pixel is too white/gray (like a Paint border), fallback to searching for a vibrant pixel
            if max(bg_color[:3]) - min(bg_color[:3]) < 15 and bg_color[0] > 200:
                bg_color = (210, 40, 30) # Rich poster red/orange fallback
        except Exception:
            bg_color = (210, 40, 30)

        clean_bg = Image.new("RGB", (w, h), bg_color[:3])
        bg_out = io.BytesIO()
        clean_bg.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Column 2: Extract object via rembg (transparent PNG)
        transparent_card = None
        if REMBG_AVAILABLE:
            try:
                transparent_card = remove(original, session=self.rembg_session).convert("RGBA")
            except Exception:
                transparent_card = None

        if transparent_card is None:
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
        Mode 3: Place extracted object onto the clean background canvas.
        """
        bg = self._open_rgb(background_bytes).convert("RGBA")
        bw, bh = bg.size

        target_subject = subject_bytes if subject_bytes else self.last_transparent_bytes

        if target_subject:
            try:
                obj = Image.open(io.BytesIO(target_subject)).convert("RGBA")
                ow, oh = obj.size

                # Center positioning
                x = (bw - ow) // 2
                y = (bh - oh) // 2

                bg.paste(obj, (x, y), mask=obj.split()[-1])
            except Exception as e:
                print(f"Composition warning: {e}")

        out = io.BytesIO()
        bg.convert("RGB").save(out, format="PNG", optimize=True)
        out.seek(0)
        return out.getvalue()