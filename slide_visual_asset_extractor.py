# slide_visual_asset_extractor.py • Pure Python Transparency & Clean Background Generator
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
        Mode 2: Two-Output Extractor:
        1. Solid reconstructed background canvas.
        2. Transparent core asset with background color made fully transparent (alpha channel).
        3. Exact pixel coordinates report.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Sample dominant background color from the corner
        try:
            bg_color = img.getpixel((10, h - 10))
        except Exception:
            bg_color = (200, 40, 30)

        # Generate clean solid background canvas
        bg_canvas = Image.new("RGB", (w, h), bg_color)
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG")
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

        # 3. Make background transparent using pure Python color-keying
        r_bg, g_bg, b_bg = bg_color[:3]
        datas = core_card.getdata()
        new_data = []
        for item in datas:
            # If pixel matches the background color tone, make it transparent
            if abs(item[0] - r_bg) < 45 and abs(item[1] - g_bg) < 45 and abs(item[2] - b_bg) < 45:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        core_card.putdata(new_data)

        trans_out = io.BytesIO()
        core_card.save(trans_out, format="PNG")
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