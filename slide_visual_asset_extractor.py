# slide_visual_asset_extractor.py • Clean Poster Card Isolation & Canvas Transparency
from PIL import Image, ImageFilter, ImageEnhance
import io

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
        out.seek(0)
        return out.getvalue()

    def render_mode_2_textless(self, image_bytes, api_key="", crop_margins=(0, 0, 0, 0)):
        """
        Mode 2: Two-Output Separation:
        1. Column 1: Clean solid background canvas matching the slide's tone.
        2. Column 2: The central poster card isolated onto a true alpha-transparent canvas.
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

        # 2. Column 2: Isolate the poster card cleanly onto a transparent RGBA canvas
        # We create a transparent full-size canvas and paste the original poster card in the center,
        # ensuring the internal red design stays 100% intact while the outer background is transparent.
        margin_x = int(w * 0.08)
        margin_top = int(h * 0.05)
        margin_bottom = int(h * 0.05)

        crop_box = (margin_x, margin_top, w - margin_x, h - margin_bottom)
        core_card = img.crop(crop_box).convert("RGBA")
        cw, ch = core_card.size

        transparent_canvas = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        transparent_canvas.paste(core_card, (margin_x, margin_top))

        trans_out = io.BytesIO()
        transparent_canvas.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        # 3. Coordinate Map Report
        coords_report = {
            "top": margin_top,
            "bottom": margin_bottom,
            "left": margin_x,
            "right": margin_x,
            "width": cw,
            "height": ch,
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
            sub_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            sub_img.thumbnail((750, 850))
            bg_w, bg_h = bg_img.size
            sub_w, sub_h = sub_img.size
            bg_img.paste(sub_img, ((bg_w - sub_w) // 2, bg_h - sub_h - 60), sub_img)
        out = io.BytesIO()
        bg_img.save(out, format="PNG")
        out.seek(0)
        return out.getvalue()