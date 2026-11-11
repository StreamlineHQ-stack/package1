# slide_visual_asset_extractor.py • Two-Output Asset Separator & Coordinate Mapper
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class SlideVisualAssetExtractor:
    def __init__(self):
        self.last_mode2_report = {}

    def _open_rgb(self, image_bytes):
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")

    def render_mode_1_background(self, image_bytes):
        img = self._open_rgb(image_bytes)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=50))
        enhancer = ImageEnhance.Contrast(blurred)
        background_isolated = enhancer.enhance(0.9)
        out = io.BytesIO()
        background_isolated.save(out, format="PNG")
        return out.getvalue()

    def render_mode_2_textless(self, image_bytes, api_key="", crop_margins=(0, 0, 0, 0)):
        """
        Mode 2: Separates the slide into two clean outputs:
        1. Solid reconstructed background image bytes.
        2. Central transparent cutout image bytes (text-free core).
        3. Returns report with exact pixel coordinates (top, bottom, left, right).
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Sample dominant background color from the corner
        try:
            bg_color = img.getpixel((10, h - 10))
        except Exception:
            bg_color = (200, 40, 30)

        # Generate clean background canvas
        bg_canvas = Image.new("RGB", (w, h), bg_color)
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG")

        # 2. Isolate central card / image (cropping out text borders)
        margin_x = int(w * 0.14)
        margin_y = int(h * 0.12)
        
        if w > (margin_x * 2) and h > (margin_y * 2):
            core_card = img.crop((margin_x, margin_y, w - margin_x, h - margin_y))
            left_pos = margin_x
            top_pos = margin_y
        else:
            core_card = img
            left_pos = 0
            top_pos = 0

        cw, ch = core_card.size
        right_pos = w - (left_pos + cw)
        bottom_pos = h - (top_pos + ch)

        # Make background transparent on the core card
        if REMBG_AVAILABLE:
            try:
                buffered = io.BytesIO()
                core_card.save(buffered, format="PNG")
                transparent_card = remove(buffered.getvalue()).convert("RGBA")
            except Exception:
                transparent_card = core_card.convert("RGBA")
        else:
            transparent_card = core_card.convert("RGBA")

        trans_out = io.BytesIO()
        transparent_card.save(trans_out, format="PNG")

        # Store coordinate report
        self.last_mode2_report = {
            "top": top_pos,
            "bottom": bottom_pos,
            "left": left_pos,
            "right": right_pos,
            "width": cw,
            "height": ch,
            "canvas_width": w,
            "canvas_height": h
        }

        return {
            "background_bytes": bg_out.getvalue(),
            "transparent_asset_bytes": trans_out.getvalue(),
            "coordinates": self.last_mode2_report
        }

    def render_mode_3_composition(self, background_bytes, subject_bytes, reference_bytes=None):
        bg_img = self._open_rgb(background_bytes).resize((1080, 1080))
        if subject_bytes:
            if REMBG_AVAILABLE:
                sub_img = remove(Image.open(io.BytesIO(subject_bytes))).convert("RGBA")
            else:
                sub_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            sub_img.thumbnail((750, 850))
            bg_w, bg_h = bg_img.size
            sub_w, sub_h = sub_img.size
            bg_img.paste(sub_img, ((bg_w - sub_w) // 2, bg_h - sub_h - 60), sub_img)
        out = io.BytesIO()
        bg_img.save(out, format="PNG")
        return out.getvalue()