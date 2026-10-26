import io
import os
import zipfile
import textwrap
from PIL import Image, ImageDraw, ImageFont

def generate_png_zip_from_slides(slides_list, bg_hex="#1a1a1a", text_hex="#ffffff", body_hex="#d1d1d1", tag_hex="#ffcc00", handle_text="@nikki.coachpages"):
    zip_buffer = io.BytesIO()
    
    def hex_to_rgb(hex_str):
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
        
    bg_rgb = hex_to_rgb(bg_hex)
    text_rgb = hex_to_rgb(text_hex)
    body_rgb = hex_to_rgb(body_hex)
    tag_rgb = hex_to_rgb(tag_hex)
    
    # Cross-platform font loader
    if os.name == "nt":
        title_font_path = "arialbd.ttf"
        body_font_path = "arial.ttf"
    else:
        title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        body_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    try:
        font_tag = ImageFont.truetype(body_font_path, 36)
        font_title = ImageFont.truetype(title_font_path, 68)
        font_body = ImageFont.truetype(body_font_path, 44)
        font_handle = ImageFont.truetype(body_font_path, 36)
    except IOError:
        font_tag = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_handle = ImageFont.load_default()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for idx, s in enumerate(slides_list):
            img = Image.new("RGB", (1080, 1350), color=bg_rgb)
            draw = ImageDraw.Draw(img)
            
            if isinstance(s, dict):
                s_tag = str(s.get("tag", f"SLIDE {idx+1}")).upper()
                s_title = s.get("title", "")
                s_body = s.get("body", "")
            else:
                s_tag = f"SLIDE {idx+1}"
                s_title = str(s)
                s_body = ""
                
            wrapped_title_lines = textwrap.wrap(s_title, width=22)
            wrapped_body_lines = textwrap.wrap(s_body, width=32)
            
            current_y = 180
            draw.text((120, current_y), f"SLIDE {idx+1} • {s_tag}", fill=tag_rgb, font=font_tag)
            current_y += 110
            
            for line in wrapped_title_lines:
                draw.text((120, current_y), line, fill=text_rgb, font=font_title)
                current_y += 90
                
            current_y += 50
            
            for line in wrapped_body_lines:
                draw.text((120, current_y), line, fill=body_rgb, font=font_body)
                current_y += 65
                
            if handle_text:
                draw.text((1080 - 120 - len(handle_text)*20, 1220), handle_text, fill=body_rgb, font=font_handle)
                
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)
            zip_file.writestr(f"slide_{idx+1}_ig_1080x1350.png", img_byte_arr.read())
            
    zip_buffer.seek(0)
    return zip_buffer.getvalue()