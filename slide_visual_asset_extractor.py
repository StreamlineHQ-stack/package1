# slide_visual_asset_extractor.py • Bulletproof Two-Output Extractor with True Alpha Transparency
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
        Mode 2: Separates slide into:
        1. Solid reconstructed background canvas.
        2. Transparent core asset with absolute alpha background removal.
        3. Exact pixel coordinates report.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Sample background color from the corner
        try:
            bg_color = img.getpixel((10, h - 10))
        except Exception:
            bg_color = (200, 40, 30)

        # Generate solid background canvas explicitly saved as PNG
        bg_canvas = Image.new("RGB", (w, h), bg_color)
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Isolate core card (cropping out text borders)
        left_pos = int(w * 0.05)
        top_pos = int(h * 0.05)
        right_pos = int(w * 0.20)
        bottom_pos = int(h * 0.05)

        crop_box = (left_pos, top_pos, w - right_pos, h - bottom_pos)
        core_card = img.crop(crop_box).convert("RGBA")
        cw, ch = core_card.size

        # 3. Force absolute alpha transparency on any pixel matching the background tone or red borders
        r_bg, g_bg, b_bg = bg_color[:3]
        pixels = core_card.load()
        
        for y in range(ch):
            for x in range(cw):
                r, g, b, a = pixels[x, y]
                # If pixel matches background or outer red band, make it 100% transparent (alpha = 0)
                if (abs(r - r_bg) < 55 and abs(g - g_bg) < 55 and abs(b - b_bg) < 55) or (r > 180 and g < 50 and b < 50):
                    pixels[x, y] = (r, g, b, 0)

        trans_out = io.BytesIO()
        core_card.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        # Coordinate Map Report
        coords_report = {
            "top": top_pos,
            "bottom": bottom_pos,
            "left": left_pos,
            "right": right_pos,
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