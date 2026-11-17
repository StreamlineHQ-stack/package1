def chunk_text_for_spillover(user_text, template_bounding_box):
    """
    Splits heavy user copy into contextually relevant chunks 
    distributed across sequential slides.
    """
    max_chars = template_bounding_box.get('max_chars', 280)
    paragraphs = user_text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chars:
            current_chunk = f"{current_chunk}\n\n{para}".strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            if len(para) > max_chars:
                sentences = para.split('. ')
                sub_chunk = ""
                for sent in sentences:
                    sent_cleaned = sent.strip() + (". " if not sent.endswith('.') else "")
                    if len(sub_chunk) + len(sent_cleaned) <= max_chars:
                        sub_chunk += sent_cleaned
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk.strip())
                        sub_chunk = sent_cleaned
                if sub_chunk:
                    current_chunk = sub_chunk.strip()
                else:
                    current_chunk = ""
            else:
                current_chunk = para
                
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks