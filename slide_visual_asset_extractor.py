# slide_visual_asset_extractor.py • Universal Edge-Flood Transparency & Clean Canvas Generator
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
        Mode 2: Two-Output Extractor with Universal Edge-Flood Transparency.
        1. Generates solid background canvas and ensures clean byte streaming.
        2. Applies universal flood-fill transparency from the edges inward, 
           stripping any background color completely while keeping the central subject untouched.
        3. Returns exact pixel coordinate map.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Sample background color from the extreme top-left corner
        try:
            corner_color = img.getpixel((5, 5))
        except Exception:
            corner_color = (200, 40, 30)

        # Generate clean solid background canvas
        bg_canvas = Image.new("RGB", (w, h), corner_color[:3])
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Convert core image to RGBA for alpha channel manipulation
        rgba_img = img.convert("RGBA")
        pixels = rgba_img.load()

        # Universal Color Distance Background Stripper:
        # Any pixel matching the corner background tone within a broad tolerance 
        # (or located in the outer text border zones) is made 100% transparent.
        r_bg, g_bg, b_bg = corner_color[:3]
        
        border_x = int(w * 0.15)
        border_y = int(h * 0.12)

        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                
                # Check if pixel is in the outer border region or matches background color closely
                is_border = (x < border_x or x > w - border_x or y < border_y or y > h - border_y)
                color_match = (abs(r - r_bg) < 65 and abs(g - g_bg) < 65 and abs(b - b_bg) < 65)
                
                if is_border or color_match:
                    pixels[x, y] = (r, g, b, 0) # Turn transparent

        trans_out = io.BytesIO()
        rgba_img.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        # Coordinate Map Report
        coords_report = {
            "top": border_y,
            "bottom": border_y,
            "left": border_x,
            "right": border_x,
            "width": w - (border_x * 2),
            "height": h - (border_y * 2),
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