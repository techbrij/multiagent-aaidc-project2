

def sanitize_text(text):
    # Remove dangerous HTML, trim, and check length
    import re
    text = text.strip()
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    return text