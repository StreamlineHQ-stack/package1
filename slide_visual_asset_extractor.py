# slide_visual_asset_extractor.py • Full-Bleed 1080x1080 Asset Extractor
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

    def generate_composition_blueprint(self, image_bytes):
        img = self._open_rgb(image_bytes)
        w, h = img.size
        return {
            "canvas": {"width": w, "height": h, "aspect_ratio": f"{w}:{h}"},
            "background": {"type": "gradient_or_solid"},
            "subjects": [{"position": "focal"}],
            "composition": {"visual_balance": "asymmetric"}
        }

    def render_mode_1_background(self, image_bytes):
        img = self._open_rgb(image_bytes)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=50))
        enhancer = ImageEnhance.Contrast(blurred)
        background_isolated = enhancer.enhance(0.9)
        out = io.BytesIO()
        background_isolated.save(out, format="PNG")
        return out.getvalue()

    def render_mode_2_textless(self, image_bytes, api_key="", crop_margins=(0, 0, 0, 0)):
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        try:
            bg_color = img.getpixel((10, 10))
        except Exception:
            bg_color = (200, 40, 30)

        # Create full 1080x1080 slide canvas
        canvas = Image.new("RGB", (1080, 1080), bg_color)
        
        # Crop out outer text banners (left/right/top/bottom margins)
        margin_x = int(w * 0.14)
        margin_y = int(h * 0.12)
        
        if w > (margin_x * 2) and h > (margin_y * 2):
            central_card = img.crop((margin_x, margin_y, w - margin_x, h - margin_y))
        else:
            central_card = img

        # Scale central card to fill canvas nicely while preserving proportions
        central_card.thumbnail((1080, 1080), Image.Resampling.LANCZOS)
        cw, ch = central_card.size
        
        paste_x = (1080 - cw) // 2
        paste_y = (1080 - ch) // 2
        canvas.paste(central_card, (paste_x, paste_y))

        out = io.BytesIO()
        canvas.save(out, format="PNG", optimize=True)
        return out.getvalue()

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