from inpainting_handler import apply_inpainting_box
import os

# ... inside render_sia_studio, right after uploaded_slide is checked ...

if uploaded_slide is not None:
    original_image = Image.open(uploaded_slide).convert("RGB")
    w, h = original_image.size
    
    # Save uploaded file temporarily to disk so OpenCV/inpainting handler can process it
    temp_input_path = "temp_uploaded_slide.jpg"
    original_image.save(temp_input_path)
    
    # Extract dominant aesthetic color from upper reference zone for template theming
    sample_color = original_image.getpixel((int(w * 0.5), int(h * 0.1)))
    hex_color = '#%02x%02x%02x' % sample_color
    
    # Automatically generate clean structural blueprint by inpainting the central text bounding box
    # (Approximating the central text zone coordinates from the image dimensions)
    text_box_guess = {
        'x1': int(w * 0.1),
        'y1': int(h * 0.3),
        'x2': int(w * 0.9),
        'y2': int(h * 0.8)
    }
    
    clean_blueprint_path = "clean_blueprint.jpg"
    apply_inpainting_box(temp_input_path, text_box_guess, output_path=clean_blueprint_path)
    
    # Load the cleaned blueprint image for preview
    blueprint_image = Image.open(clean_blueprint_path).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Inspiration Reference Slide**")
        st.image(original_image, use_container_width=True)
        
    with col2:
        st.markdown("**Extracted Structural Blueprint (Text Removed)**")
        st.image(blueprint_image, use_container_width=True)
        
    st.success(f"Layout blueprint extracted & cleaned! Dominant theme color detected: `{hex_color}`")