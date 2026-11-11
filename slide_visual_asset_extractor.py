# slide_visual_asset_extractor.py • Exact Coordinate Asset Splitter & Clean Renderer
from PIL import Image, ImageFilter, ImageEnhance
import io

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
        Mode 2: Two-Output Extractor with Exact Coordinate Mapping.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Sample dominant background color from bottom-left corner
        try:
            bg_color = img.getpixel((15, h - 15))
        except Exception:
            bg_color = (200, 40, 30)

        # Generate solid background canvas and ensure PNG bytes output
        bg_canvas = Image.new("RGB", (w, h), bg_color)
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG")
        bg_bytes_data = bg_out.getvalue()

        # 2. Define precise cropping coordinates to exclude outer text banners (like 'NEW DROP')
        # We crop slightly inward on the right and top/bottom to isolate the clean central artwork
        left_pos = int(w * 0.05)
        top_pos = int(h * 0.05)
        right_pos = int(w * 0.20)  # Cuts off the right-side text banner cleanly
        bottom_pos = int(h * 0.05)

        crop_box = (left_pos, top_pos, w - right_pos, h - bottom_pos)
        core_card = img.crop(crop_box)

        cw, ch = core_card.size

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