# Theme color mapping (Fixed to properly respect selected style_theme)
            if style_theme == "Custom" and custom_colors:
                bg_color, text_color, body_color, tag_color, border_style = custom_colors["bg"], custom_colors["text"], custom_colors["body"], custom_colors["tag"], custom_colors["border"]
            elif style_theme == "High-Contrast Canary":
                bg_color, text_color, body_color, tag_color, border_style = "#1a1a1a", "#ffffff", "#d1d1d1", "#ffcc00", "none"
            elif style_theme == "Warning Red Alert":
                bg_color, text_color, body_color, tag_color, border_style = "#181212", "#ffffff", "#e5cdc5", "#ef4444", "1px solid #3d2222"
            elif style_theme == "Minimalist Clean":
                bg_color, text_color, body_color, tag_color, border_style = "#ffffff", "#111111", "#444444", "#0066cc", "1px solid #e0e0e0"
            elif style_theme == "Warm Editorial":
                bg_color, text_color, body_color, tag_color, border_style = "#fbf9f5", "#2c221e", "#5c4e47", "#a85732", "1px solid #e6dfd3"
            elif style_theme == "Neon Cyber/Tech":
                bg_color, text_color, body_color, tag_color, border_style = "#0b0f19", "#f8fafc", "#94a3b8", "#06b6d4", "1px solid #1e293b"
            elif style_theme == "Midnight Luxury":
                bg_color, text_color, body_color, tag_color, border_style = "#121212", "#f5e6c8", "#d4c5a9", "#d4af37", "1px solid #2a2415"
            elif style_theme == "Emerald Growth":
                bg_color, text_color, body_color, tag_color, border_style = "#0a1f1c", "#e6f4f1", "#a3cbd0", "#10b981", "1px solid #133e38"
            elif style_theme == "Nordic Slate":
                bg_color, text_color, body_color, tag_color, border_style = "#1e242b", "#f1f5f9", "#cbd5e1", "#38bdf8", "1px solid #334155"
            elif style_theme == "Bold Coral Pop":
                bg_color, text_color, body_color, tag_color, border_style = "#231818", "#fff0ed", "#e2c4be", "#ff6b6b", "1px solid #422929"
            elif style_theme == "Monochrome Obsidian":
                bg_color, text_color, body_color, tag_color, border_style = "#000000", "#ffffff", "#a3a3a3", "#ffffff", "1px solid #262626"
            else:
                bg_color, text_color, body_color, tag_color, border_style = "#1a1a1a", "#ffffff", "#d1d1d1", "#ffcc00", "none"