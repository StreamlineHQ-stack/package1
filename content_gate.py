def evaluate_content_fit(user_text, template_bounding_box):
    """
    Evaluates text volume against template real estate constraints.
    Returns: 'FIT' or 'OVERFLOW' along with density metrics.
    """
    word_count = len(user_text.split())
    char_count = len(user_text)
    
    max_chars = template_bounding_box.get('max_chars', 280)
    max_lines = template_bounding_box.get('max_lines', 6)
    avg_chars_per_line = template_bounding_box.get('avg_chars_per_line', 45)
    estimated_lines = (char_count // avg_chars_per_line) + 1
    
    if char_count > max_chars or estimated_lines > max_lines:
        return {
            "status": "OVERFLOW",
            "word_count": word_count,
            "char_count": char_count,
            "estimated_lines": estimated_lines,
            "excess_ratio": char_count / max_chars
        }
    
    return {
        "status": "FIT",
        "word_count": word_count,
        "char_count": char_count,
        "estimated_lines": estimated_lines
    }