# slide_visual_asset_extractor.py • Bulletproof Extractor & Compositor
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
        self.rembg_session = None
        if REMBG_AVAILABLE:
            try:
                self.rembg_session = new_session("isnet-general-use")
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
        1. Column 1: Clean solid background canvas.
        2. Column 2: Transparent core asset with backdrop separation and color restoration.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Column 1: Sample dominant background color & generate solid canvas
        try:
            bg_color = img.getpixel((5, 5))
        except Exception:
            bg_color = (200, 40, 30)

        bg_canvas = Image.new("RGB", (w, h), bg_color[:3])
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Column 2: Transparent asset extraction with color restoration
        transparent_card = None
        if REMBG_AVAILABLE:
            try:
                rgb_arr = np.array(img)
                raw_rgba = remove(img, session=self.rembg_session)
                rgba_arr = np.array(raw_rgba)
                rgba_arr[..., :3] = rgb_arr
                transparent_card = Image.fromarray(rgba_arr)
            except Exception:
                transparent_card = None

        if transparent_card is None:
            margin_x = int(w * 0.08)
            margin_top = int(h * 0.05)
            margin_bottom = int(h * 0.05)
            crop_box = (margin_x, margin_top, w - margin_x, h - margin_bottom)
            core_card = img.crop(crop_box).convert("RGBA")
            
            transparent_card = Image.new("RGBA", (w, h), (255, 255, 255, 0))
            transparent_card.paste(core_card, (margin_x, margin_top))

        trans_out = io.BytesIO()
        transparent_card.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        # 3. Coordinate Map Report
        coords_report = {
            "top": int(h * 0.05),
            "bottom": int(h * 0.05),
            "left": int(w * 0.08),
            "right": int(w * 0.08),
            "width": w - int(w * 0.16),
            "height": h - int(h * 0.10),
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
        """
        Composites the transparent subject/card onto the generated solid background canvas.
        """
        bg_img = self._open_rgb(background_bytes).convert("RGBA")
        bg_w, bg_h = bg_img.size

        if subject_bytes:
            sub_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            sub_img.thumbnail((int(bg_w * 0.85), int(bg_h * 0.85)))
            sub_w, sub_h = sub_img.size

            paste_x = (bg_w - sub_w) // 2
            paste_y = (bg_h - sub_h) // 2
            
            bg_img.paste(sub_img, (paste_x, paste_y), sub_img)

        out = io.BytesIO()
        bg_img.save(out, format="PNG", optimize=True)
        out.seek(0)
        return out.getvalue()