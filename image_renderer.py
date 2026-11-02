import io
import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

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

def generate_png_zip_from_slides(slides_data, handle_text="@nikki.coachpages", palette=None):
    """
    Generates a ZIP archive containing high-resolution PNG slides matching 
    the exact layout, padding, and typography of the platform preview and Kinetic engine.
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
            else:
                badge = f"SLIDE {idx} | STRATEGY"
                title = str(slide)
                body = ""

            img = Image.new("RGB", (width, height), color="#0e1117")
            draw = ImageDraw.Draw(img)

            # Draw outer card container matching platform hub preview
            draw.rounded_rectangle(
                [80, 100, width - 80, height - 150],
                radius=28,
                fill=palette["bg"],
                outline=palette["badge"] if palette["border"] != "none" else None,
                width=5,
            )

            # Draw category badge
            draw.text((140, 160), badge.upper(), fill=palette["badge"], font=badge_font)

            # Measure and wrap title text
            temp_img = Image.new("RGB", (width, height))
            temp_draw = ImageDraw.Draw(temp_img)
            wrapped_title = wrap_text_to_width(title, title_font, max_text_width, temp_draw)
            
            title_y = 250
            for line in wrapped_title:
                draw.text((140, title_y), line, fill=palette["title"], font=title_font)
                title_y += 74

            # Measure and wrap body text
            if body:
                wrapped_body = wrap_text_to_width(body, body_font, max_text_width, temp_draw)
                body_y = title_y + 30
                for line in wrapped_body:
                    draw.text((140, body_y), line, fill=palette["body"], font=body_font)
                    body_y += 56

            # Draw brand watermark footer
            active_footer = handle_text if handle_text else "Creator Suite Studio"
            draw.text((140, height - 230), active_footer, fill="#8b949e", font=footer_font)

            # Save to zip buffer
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)

            zip_file.writestr(f"slide_{idx}_ig_1080x1080.png", img_byte_arr.getvalue())

    zip_buffer.seek(0)
    return zip_buffer.getvalue()