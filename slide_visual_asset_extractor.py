# slide_visual_asset_extractor.py • High-Performance Corner Flood-Fill Background Remover
from PIL import Image, ImageFilter, ImageEnhance
import io
from collections import deque

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
        Mode 2: Two-Output Separation Pipeline:
        1. Column 1: Clean solid background canvas.
        2. Column 2: Core asset with background removed via deterministic corner flood-fill transparency.
        """
        img = self._open_rgb(image_bytes)
        w, h = img.size
        
        # 1. Column 1: Sample dominant background color from corner & generate clean canvas
        try:
            bg_color = img.getpixel((10, h - 10))
        except Exception:
            bg_color = (200, 40, 30)

        bg_canvas = Image.new("RGB", (w, h), bg_color[:3])
        bg_out = io.BytesIO()
        bg_canvas.save(bg_out, format="PNG", optimize=True)
        bg_out.seek(0)
        bg_bytes_data = bg_out.getvalue()

        # 2. Column 2: Corner Flood-Fill Background Stripper (True Alpha Transparency)
        rgba_img = img.convert("RGBA")
        pixels = rgba_img.load()

        # Gather seed background colors from all 4 corners
        seeds = [
            pixels[0, 0][:3],
            pixels[w - 1, 0][:3],
            pixels[0, h - 1][:3],
            pixels[w - 1, h - 1][:3]
        ]

        visited = [[False for _ in range(h)] for _ in range(w)]
        queue = deque()

        def matches(rgb):
            for seed in seeds:
                if (abs(rgb[0] - seed[0]) < 55 and 
                    abs(rgb[1] - seed[1]) < 55 and 
                    abs(rgb[2] - seed[2]) < 55):
                    return True
            return False

        # Seed edges
        for x in range(w):
            if matches(pixels[x, 0][:3]):
                queue.append((x, 0))
                visited[x][0] = True
            if matches(pixels[x, h - 1][:3]):
                queue.append((x, h - 1))
                visited[x][h - 1] = True
                
        for y in range(h):
            if matches(pixels[0, y][:3]):
                queue.append((0, y))
                visited[0][y] = True
            if matches(pixels[w - 1, y][:3]):
                queue.append((w - 1, y))
                visited[w - 1][y] = True

        # BFS Flood Fill
        while queue:
            cx, cy = queue.popleft()
            r, g, b, _ = pixels[cx, cy]
            pixels[cx, cy] = (r, g, b, 0) # Set alpha to 0 (fully transparent)
            
            for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                    if matches(pixels[nx, ny][:3]):
                        visited[nx][ny] = True
                        queue.append((nx, ny))

        trans_out = io.BytesIO()
        rgba_img.save(trans_out, format="PNG", optimize=True)
        trans_out.seek(0)
        trans_bytes_data = trans_out.getvalue()

        # 3. Coordinate Map Report
        coords_report = {
            "top": int(h * 0.05),
            "bottom": int(h * 0.05),
            "left": int(w * 0.05),
            "right": int(w * 0.05),
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