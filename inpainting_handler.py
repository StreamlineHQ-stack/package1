import cv2
import numpy as np

def apply_inpainting_box(image_path, box_coords, output_path="healed_slide.jpg"):
    """
    Takes a slide image and user-defined bounding box coordinates (MS Paint-style selection)
    and uses OpenCV inpainting to heal and remove the text underneath, 
    returning a clean background asset ready for custom text placement.
    
    box_coords format: {'x1': int, 'y1': int, 'x2': int, 'y2': int}
    """
    # Load the slide image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")
        
    h, w, _ = img.shape
    
    # Create a blank mask of the same dimensions
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Extract coordinates from the user's selection box
    x1 = max(0, box_coords.get('x1', 0))
    y1 = max(0, box_coords.get('y1', 0))
    x2 = min(w, box_coords.get('x2', w))
    y2 = min(h, box_coords.get('y2', h))
    
    # Fill the selected area with white (255) on the mask to designate it for inpainting
    mask[y1:y2, x1:x2] = 255
    
    # Apply Telea inpainting algorithm to reconstruct the background texture/gradient
    inpaint_radius = 3
    healed_img = cv2.inpaint(img, mask, inpaint_radius, cv2.INPAINT_TELEA)
    
    # Save and return the clean background asset path
    cv2.imwrite(output_path, healed_img)
    return output_path