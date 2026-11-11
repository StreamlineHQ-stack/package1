# slide_visual_asset_extractor.py
# Three-Mode Visual Composition Extraction & Generation Engine
#
# Mode 2 is implemented as true OCR-guided text removal:
# original non-text pixels are retained; only detected text regions are
# reconstructed. Requires opencv-python-headless, pytesseract and Tesseract OCR.

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import io
import os


class SlideVisualAssetExtractor:
    def __init__(self):
        self.last_mode2_report = {}

    def _open_rgb(self, image_bytes):
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")

    def generate_composition_blueprint(self, image_bytes):
        """Basic image metadata. This is not an AI scene-understanding model."""
        img = self._open_rgb(image_bytes)
        w, h = img.size
        return {
            "canvas": {
                "width": w,
                "height": h,
                "aspect_ratio": f"{w}:{h}"
            },
            "background": {"type": "not_yet_classified"},
            "subjects": [],
            "decorations": [],
            "text_regions": [],
            "composition": {"analysis_status": "metadata_only"}
        }

    def render_mode_1_background(self, image_bytes):
        """
        LEGACY MODE 1 PLACEHOLDER.
        This blur-based operation is not true foreground/background separation.
        Kept unchanged to avoid altering the other workflow in this patch.
        """
        img = self._open_rgb(image_bytes)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=40))
        out_buf = io.BytesIO()
        blurred.save(out_buf, format="PNG")
        return out_buf.getvalue()

    @staticmethod
    def _load_vision_dependencies():
        try:
            import cv2
            import numpy as np
            import pytesseract
            from pytesseract import Output
            return cv2, np, pytesseract, Output
        except Exception as exc:
            raise RuntimeError(
                "Mode 2 needs OpenCV and pytesseract. Install "
                "'opencv-python-headless' and 'pytesseract', and install "
                "the Tesseract OCR system package (tesseract-ocr). "
                f"Dependency error: {exc}"
            )

    def _detect_text_boxes(self, rgb_image):
        """
        Detect word-level text boxes on several image variants.
        Multi-pass OCR improves detection on small, low-contrast and
        slightly stylized text. Coordinates are mapped to original size.
        """
        cv2, np, pytesseract, Output = self._load_vision_dependencies()

        original = np.array(rgb_image)
        h, w = original.shape[:2]
        gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)

        # Upscale small slides for OCR, without changing final output size.
        scale = 2 if max(w, h) < 1800 else 1
        if scale != 1:
            gray = cv2.resize(
                gray, None, fx=scale, fy=scale,
                interpolation=cv2.INTER_CUBIC
            )

        variants = [
            gray,
            cv2.createCLAHE(
                clipLimit=2.0, tileGridSize=(8, 8)
            ).apply(gray),
            cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 31, 11
            )
        ]

        found = []
        configs = [
            "--oem 3 --psm 11",
            "--oem 3 --psm 6"
        ]

        for variant in variants:
            for config in configs:
                try:
                    data = pytesseract.image_to_data(
                        variant,
                        config=config,
                        output_type=Output.DICT
                    )
                except Exception:
                    continue

                count = len(data.get("text", []))
                for i in range(count):
                    word = (data["text"][i] or "").strip()
                    try:
                        confidence = float(data["conf"][i])
                    except (TypeError, ValueError):
                        confidence = -1

                    # Discard OCR noise but retain moderately confident text.
                    if not word or confidence < 25:
                        continue

                    x = int(data["left"][i] / scale)
                    y = int(data["top"][i] / scale)
                    bw = int(data["width"][i] / scale)
                    bh = int(data["height"][i] / scale)

                    if bw <= 0 or bh <= 0:
                        continue

                    x1 = max(0, x)
                    y1 = max(0, y)
                    x2 = min(w, x + bw)
                    y2 = min(h, y + bh)

                    if x2 > x1 and y2 > y1:
                        found.append((x1, y1, x2, y2, confidence, word))

        # Deduplicate overlapping boxes from OCR passes.
        found.sort(key=lambda item: item[4], reverse=True)
        deduped = []
        for box in found:
            x1, y1, x2, y2 = box[:4]
            duplicate = False
            for old in deduped:
                ox1, oy1, ox2, oy2 = old[:4]
                ix1, iy1 = max(x1, ox1), max(y1, oy1)
                ix2, iy2 = min(x2, ox2), min(y2, oy2)
                inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
                area = max(1, (x2-x1)*(y2-y1))
                old_area = max(1, (ox2-ox1)*(oy2-oy1))
                if inter / min(area, old_area) > 0.55:
                    duplicate = True
                    break
            if not duplicate:
                deduped.append(box)

        return deduped

    def render_mode_2_textless(self, image_bytes):
        """
        MODE 2: Textless original visual composition.

        The source image is not globally blurred or regenerated. OCR finds
        text regions; OpenCV inpaints only those masked regions. All pixels
        outside the expanded text mask remain unchanged.
        """
        cv2, np, _, _ = self._load_vision_dependencies()
        original_pil = self._open_rgb(image_bytes)
        original = np.array(original_pil)
        h, w = original.shape[:2]

        boxes = self._detect_text_boxes(original_pil)

        mask = np.zeros((h, w), dtype=np.uint8)

        for x1, y1, x2, y2, confidence, word in boxes:
            box_h = max(1, y2 - y1)

            # Expand to include anti-aliasing, outline and nearby shadow.
            pad_x = max(2, int(box_h * 0.12))
            pad_y = max(2, int(box_h * 0.20))

            left = max(0, x1 - pad_x)
            top = max(0, y1 - pad_y)
            right = min(w, x2 + pad_x)
            bottom = min(h, y2 + pad_y)

            cv2.rectangle(
                mask, (left, top), (right, bottom), 255, thickness=-1
            )

        # Merge nearby characters/words into coherent text-line masks.
        kernel_size = max(3, int(min(w, h) * 0.003))
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
        )
        mask = cv2.dilate(mask, kernel, iterations=1)

        if np.count_nonzero(mask) == 0:
            cleaned = original.copy()
            status = (
                "No text regions were detected. The original image was "
                "returned unchanged; check OCR language/contrast if text exists."
            )
        else:
            # Small radius limits collateral changes to nearby artwork.
            # Telea is generally suitable for narrow text strokes/regions.
            radius = max(3, min(7, int(min(w, h) * 0.006)))
            bgr = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)
            mask_for_cv = mask.astype(np.uint8)
            restored = cv2.inpaint(
                bgr, mask_for_cv, radius, cv2.INPAINT_TELEA
            )
            cleaned = cv2.cvtColor(restored, cv2.COLOR_BGR2RGB)
            status = (
                "Text-region reconstruction completed. Review areas where "
                "text overlapped faces, detailed objects, or complex artwork."
            )

        out = io.BytesIO()
        Image.fromarray(cleaned).save(out, format="PNG", optimize=True)

        mask_out = io.BytesIO()
        Image.fromarray(mask).save(mask_out, format="PNG")

        self.last_mode2_report = {
            "status": status,
            "detected_text_regions": len(boxes),
            "masked_pixel_percentage": round(
                100 * float(np.count_nonzero(mask)) / (w * h), 2
            ),
            "width": w,
            "height": h,
            "mask_png": mask_out.getvalue()
        }

        return out.getvalue()

    def render_mode_3_composition(
        self, background_bytes, subject_bytes, reference_bytes=None
    ):
        """
        LEGACY MODE 3 PLACEHOLDER.
        Existing fixed-position compositing retained in this patch.
        Reference-aware placement requires the separate renderer integration.
        """
        bg_img = self._open_rgb(background_bytes).resize((1080, 1080))

        if subject_bytes:
            sub_img = Image.open(
                io.BytesIO(subject_bytes)
            ).convert("RGBA")
            sub_img.thumbnail((720, 900))
            bg_w, bg_h = bg_img.size
            sub_w, sub_h = sub_img.size
            paste_x = bg_w - sub_w - 60
            paste_y = bg_h - sub_h - 60
            bg_img.paste(sub_img, (paste_x, paste_y), sub_img)

        out_buf = io.BytesIO()
        bg_img.save(out_buf, format="PNG")
        return out_buf.getvalue()
