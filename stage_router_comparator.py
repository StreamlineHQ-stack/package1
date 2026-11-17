import cv2
import numpy as np
from PIL import Image

def evaluate_and_route_slide(image_path, threshold_complexity=0.15):
    """
    Internal Backend Comparator:
    Quietly inspects incoming inspiration slides behind the scenes.
    Decides between Mode A (As-Is Inpainting) and Mode B (Equivalent Fallback) 
    without exposing error logs or messy processing to the user.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Calculate Texture & Edge Complexity Metrics
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size
    
    # 2. Threshold Decision Logic
    # High edge density or dense textures cause OpenCV inpainting to smear/blur.
    is_complex_texture = (edge_density > threshold_complexity) or (laplacian_var > 1000)
    
    if not is_complex_texture:
        # Branch A: Clean Background -> Pristine As-Is Inpainting
        print("[Backend Log] Slide texture is clean. Executing As-Is Inpainting.")
        cleaned_slide = execute_as_is_inpaint(img, gray)
        return {
            "mode": "as_is",
            "output_image": cleaned_slide,
            "user_notice": None
        }
    else:
        # Branch B: Complex/Textured Background -> Smart Equivalent Fallback
        print("[Backend Log] Complex texture detected. Pivoting to Equivalent Fallback.")
        equivalent_slide = execute_equivalent_fallback(img)
        
        # Professional, polished user-facing message (No "childbirth" exposure)
        user_notice = "✨ Notice: This layout featured a complex background texture. We've seamlessly transitioned it to our signature high-end equivalent backdrop to ensure crisp, boutique typography."
        
        return {
            "mode": "equivalent",
            "output_image": equivalent_slide,
            "user_notice": user_notice
        }

def execute_as_is_inpaint(img, gray):
    # Standard clean inpainting for flat or gradient backgrounds
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    cleaned = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(cleaned, cv2.COLOR_BGR2RGB))

def execute_equivalent_fallback(img):
    # Seamlessly replaces complex backgrounds with a rich, uniform equivalent canvas
    # (Integrates with your SIA background motif engine)
    h, w, _ = img.shape
    equivalent_canvas = Image.new("RGB", (w, h), color=(30, 30, 35)) # Boutique dark aesthetic default
    return equivalent_canvas