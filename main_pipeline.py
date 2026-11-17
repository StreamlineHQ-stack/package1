from content_gate import evaluate_content_fit
from spillover_engine import chunk_text_for_spillover

def process_slide_generation(user_text, template_spec, user_mode_preference):
    """
    Main controller linking Mode 2 resolution, content evaluation, and spillover.
    """
    fit_result = evaluate_content_fit(user_text, template_spec)
    slides_to_generate = []
    
    if fit_result["status"] == "OVERFLOW":
        text_chunks = chunk_text_for_spillover(user_text, template_spec)
        for idx, chunk in enumerate(text_chunks):
            slides_to_generate.append({
                "sequence_index": idx + 1,
                "text": chunk,
                "routing": "spillover_equivalent"
            })
    else:
        if user_mode_preference == "as_is" and template_spec.get("is_mappable", True):
            routing_mode = "as_is"
        elif user_mode_preference == "u_do_manual":
            routing_mode = "u_do_inpainting"
        else:
            routing_mode = "equivalent"
            
        slides_to_generate.append({
            "sequence_index": 1,
            "text": user_text,
            "routing": routing_mode
        })
        
    return slides_to_generate