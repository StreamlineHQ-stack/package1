import io
import os
import zipfile
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def load_app_font(size):
    possible_paths = [
        "arialbd.ttf",
        "fonts/arialbd.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def wrap_text_to_width(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def fetch_background_image(query_hint="editorial texture minimal"):
    """
    Fetches a theme-based background image from stable free photographic endpoints 
    or falls back to a solid editorial background if offline.
    """
    try:
        # Generate a stable seed from the query hint to load gorgeous photographic textures
        seed_val = abs(hash(query_hint)) % 1000
        url = f"https://picsum.photos/seed/{seed_val}/1080/1080"
        
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            bg_img = Image.open(io.BytesIO(response.content)).convert("RGB")
            return bg_img
    except Exception:
        pass
    return None

def generate_png_zip_from_slides(slides_data, handle_text="@nikki.coachpages", palette=None):
    """
    Generates a ZIP archive containing high-resolution full-bleed PNG slides 
    with photographic background integration and dark gradient scrim overlays.
    """
    if palette is None:
        palette = {
            "bg": "#1a1a1a",
            "border": "none",
            "badge": "#ffcc00",
            "title": "#ffffff",
            "body": "#d1d1d1"
        }

    zip_buffer = io.BytesIO()
    width, height = 1080, 1080
    max_text_width = 800

    badge_font = load_app_font(38)
    title_font = load_app_font(62)
    body_font = load_app_font(42)
    footer_font = load_app_font(30)

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for idx, slide in enumerate(slides_data, start=1):
            if isinstance(slide, dict):
                badge = str(slide.get("category", slide.get("tag", f"SLIDE {idx} | STRATEGY")))
                title = str(slide.get("title", slide.get("headline", f"Slide Title {idx}")))
                body = str(slide.get("content", slide.get("body", "Key actionable breakdown...")))
                visual_hint = slide.get("visual_hint", "coaching,minimal,dark texture")
            else:
                badge = f"SLIDE {idx} | STRATEGY"
                title = str(slide)
                body = ""
                visual_hint = "editorial,minimal,workspace"

            # 1. Try fetching a photographic theme background
            bg_img = fetch_background_image(visual_hint)
            
            if bg_img:
                # Resize/Crop to exact 1080x1080 square
                bg_img = bg_img.resize((width, height), Image.Resampling.LANCZOS)
                # Dim the background image slightly so text pops
                enhancer = ImageEnhance.Brightness(bg_img)
                img = enhancer.enhance(0.4) # Darken background to 40%
            else:
                # Fallback to solid theme background color
                img = Image.new("RGB", (width, height), color=palette["bg"])

            # 2. Apply a subtle gradient scrim overlay for maximum text readability
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            for y in range(height):
                alpha = int(120 + (y / height) * 80) # Gradient shadow fade
                overlay_draw.line([(0, y), (width, y)], fill=(14, 17, 23, alpha))
            
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)

            # 3. Draw category badge
            draw.text((100, 140), badge.upper(), fill=palette["badge"], font=badge_font)

            # 4. Measure and wrap title text
            temp_img = Image.new("RGB", (width, height))
            temp_draw = ImageDraw.Draw(temp_img)
            wrapped_title = wrap_text_to_width(title, title_font, max_text_width, temp_draw)
            
            title_y = 230
            for line in wrapped_title:
                draw.text((100, title_y), line, fill=palette["title"], font=title_font)
                title_y += 74

            # 5. Measure and wrap body text
            if body:
                wrapped_body = wrap_text_to_width(body, body_font, max_text_width, temp_draw)
                body_y = title_y + 40
                for line in wrapped_body:
                    draw.text((100, body_y), line, fill=palette["body"], font=body_font)
                    body_y += 56

            # 6. Draw brand watermark footer
            active_footer = handle_text if handle_text else "Creator Suite Studio"
            draw.text((100, height - 160), active_footer, fill="#8b949e", font=footer_font)

            # Save to zip buffer
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)

            zip_file.writestr(f"slide_{idx}_ig_1080x1080.png", img_byte_arr.getvalue())

    zip_buffer.seek(0)
    return zip_buffer.getvalue()