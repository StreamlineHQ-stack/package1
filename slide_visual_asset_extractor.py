# slide_visual_asset_extractor.py • Bulletproof rembg & Alpha Canvas Extractor
from PIL import Image, ImageFilter, ImageEnhance
import io

try:
    from rembg import remove, new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class SlideVisualAssetExtractor:
    def __init__(self):
        self.last_mode2_report = {}
        self.rembg_session = None
        if REMBG_AVAILABLE:
            try:
                self.rembg_session = new_session("u2net")
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
        1. Column 1: Solid reconstructed background canvas matching slide tone.
        2. Column 2: Transparent core asset via rembg (with automatic color-key fallback).
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Column 1: Sample background color & generate solid canvas
        try:
            bg_color = img.getpixel((10, h - 10))
        except Exception:
            bg_color = (200, 40, 30)

        bg_canvas = Image.new("RGB", (w, h), bg_color[:3])
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Column 2: Transparent asset extraction
        transparent_card = None
        if REMBG_AVAILABLE:
            try:
                # Run rembg AI background removal
                transparent_card = remove(img, session=self.rembg_session).convert("RGBA")
            except Exception:
                pass

        # Fallback to precise geometric cropping + alpha border if rembg isn't ready
        if transparent_card is None:
            left_margin = int(w * 0.08)
            top_margin = int(h * 0.06)
            right_margin = int(w * 0.18)
            bottom_margin = int(h * 0.06)
            
            crop_box = (left_margin, top_margin, w - right_margin, h - bottom_margin)
            core_card = img.crop(crop_box).convert("RGBA")
            
            transparent_card = Image.new("RGBA", (w, h), (255, 255, 255, 0))
            transparent_card.paste(core_card, (left_margin, top_margin))

        trans_out = io.BytesIO()
        transparent_card.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        # 3. Coordinate Map Report
        coords_report = {
            "top": int(h * 0.06),
            "bottom": int(h * 0.06),
            "left": int(w * 0.08),
            "right": int(w * 0.18),
            "width": w - int(w * 0.26),
            "height": h - int(h * 0.12),
            "canvas_width": w,
            "canvas_height": h
        }
        self.last_mode2_report = coords_report

        return {
            "background_bytes": bg_bytes_data,
            "transparent_asset_bytes": trans_bytes_data,
            "coordinates": coords_report
        }

    def render_mode_3_composition(self, background_bytes, subject_bytes, reference_bytes=None):
        bg_img = self._open_rgb(background_bytes).resize((1080, 1080))
        if subject_bytes:
            if REMBG_AVAILABLE:
                sub_img = remove(Image.open(io.BytesIO(subject_bytes)), session=self.rembg_session).convert("RGBA")
            else:
                sub_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            sub_img.thumbnail((750, 850))
            bg_w, bg_h = bg_img.size
            sub_w, sub_h = sub_img.size
            bg_img.paste(sub_img, ((bg_w - sub_w) // 2, bg_h - sub_h - 60), sub_img)
        out = io.BytesIO()
        bg_img.save(out, format="PNG")
        out.seek(0)
        return out.getvalue()