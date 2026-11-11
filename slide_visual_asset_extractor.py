def render_mode_3_composition(self, background_bytes, subject_bytes, reference_bytes=None):
        """
        Composites the transparent subject/card onto the generated solid background canvas.
        """
        # Open the solid background canvas
        bg_img = self._open_rgb(background_bytes).convert("RGBA")
        bg_w, bg_h = bg_img.size

        if subject_bytes:
            # Open the transparent subject asset
            sub_img = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            
            # Resize subject proportionally if needed
            sub_img.thumbnail((int(bg_w * 0.85), int(bg_h * 0.85)))
            sub_w, sub_h = sub_img.size

            # Center the asset perfectly onto the background canvas using alpha transparency
            paste_x = (bg_w - sub_w) // 2
            paste_y = (bg_h - sub_h) // 2
            
            bg_img.paste(sub_img, (paste_x, paste_y), sub_img)

        out = io.BytesIO()
        bg_img.save(out, format="PNG", optimize=True)
        out.seek(0)
        return out.getvalue()