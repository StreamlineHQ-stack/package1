# sia_studio.py • Style Inspiration & Analysis Studio (SIA) with Carousel Content Engine & Deck Carousel Player
import streamlit as st
import json
import base64
import io
import os
import requests
import zipfile
from PIL import Image, ImageDraw, ImageFont
from app_engine import generate_carousel_deck
from framework_data import FRAMEWORK_LIBRARY
from sia_terracotta_module import build_terracotta_deck
from sia_ai_context_module import build_ai_context_deck
from sia_editorial_motif_module import build_unified_editorial_deck
from sia_inspiration_template_module import build_inspiration_editorial_deck
from background_engine import get_modular_background
from smart_ai_engine import get_smart_ai_background

try:
    from templates.november import NOVEMBER_FRAMEWORK_LIBRARY
except Exception:
    NOVEMBER_FRAMEWORK_LIBRARY = {}

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

def build_custom_user_deck(deck, custom_img_base64=""):
    styled = []
    total = len(deck)
    for idx, slide in enumerate(deck):
        cat = str(slide.get("category", f"SLIDE {idx+1}")).upper()
        title = str(slide.get("title", f"Slide {idx+1}"))
        content = str(slide.get("content", ""))
        
        img_src = custom_img_base64 if custom_img_base64 else "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1080&auto=format&fit=crop&q=80"
        
        html = f"""
        <div style="background: #0b0f19; padding: 40px; border-radius: 24px; border: 3px solid #1f2937; max-width: 680px; margin: 0 auto; font-family: sans-serif; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
            <div style="width: 100%; height: 240px; border-radius: 16px; overflow: hidden; margin-bottom: 24px; border: 2px solid #374151;">
                <img src="{img_src}" style="width: 100%; height: 100%; object-fit: cover; display: block;" />
            </div>
            <div style="color: #ffcc00; font-size: 14px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px;">
                SLIDE {idx+1} OF {total} • {cat}
            </div>
            <h2 style="color: #ffffff; font-size: 26px; font-weight: 700; line-height: 1.3; margin-bottom: 16px;">
                {title}
            </h2>
            <p style="color: #9ca3af; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                {content}
            </p>
            <div style="text-align: right; color: #6b7280; font-size: 12px; font-weight: 600; border-top: 1px solid #1f2937; padding-top: 12px;">
                Nikki's Salon • ApexMorph
            </div>
        </div>
        """
        styled.append({
            "category": cat,
            "title": title,
            "content": content,