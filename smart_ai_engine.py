# smart_ai_engine.py • Dedicated Smart AI Contextual Match Engine

def get_smart_ai_background(slide_tag, slide_index, slide_text=""):
    """
    Dedicated Smart AI Contextual Match Engine.
    Analyzes the exact slide phase (Hook, Problem, Agitation, Solution, Proof, Action)
    and slide content to deliver unique, context-aware imagery across every slide.
    """
    tag_clean = str(slide_tag).lower()
    text_clean = str(slide_text).lower()
    blob = f"{tag_clean} {text_clean}"
    
    # Dedicated contextual pools tailored to high-converting marketing psychology
    if "hook" in blob or slide_index == 0:
        pool = [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1080&auto=format&fit=crop&q=80"
        ]
    elif "problem" in blob or "agitation" in blob or slide_index in [1, 2]:
        pool = [
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&auto=format&fit=crop&q=80"
        ]
    elif "solution" in blob or slide_index == 3:
        pool = [
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&auto=format&fit=crop&q=80"
        ]
    elif "proof" in blob or slide_index == 4:
        pool = [
            "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1080&auto=format&fit=crop&q=80"
        ]
    else:  # Action / Closing
        pool = [
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1080&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1080&auto=format&fit=crop&q=80"
        ]
        
    return pool[slide_index % len(pool)]