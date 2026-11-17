# Sample background colors intelligently from multiple clean corner zones
            # to avoid hitting central text or borders
            corner_samples = [
                original_image.getpixel((int(w * 0.05), int(h * 0.05))),
                original_image.getpixel((int(w * 0.95), int(h * 0.05))),
                original_image.getpixel((int(w * 0.05), int(h * 0.95))),
                original_image.getpixel((int(w * 0.95), int(h * 0.95)))
            ]
            
            # Use the most representative background tone
            sample_color_top = corner_samples[0]
            sample_color_center = corner_samples[2]
            
            hex_top = '#%02x%02x%02x' % sample_color_top
            hex_center = '#%02x%02x%02x' % sample_color_center