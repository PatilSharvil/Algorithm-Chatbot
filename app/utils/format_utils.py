import re

def clean_response_format(response_text):
    """
    Clean up the response text by removing HTML tags and formatting appropriately
    """
    if not response_text:
        return response_text
    
    # More robust and comprehensive HTML tag removal - remove all HTML tags
    # This pattern matches <tag> and </tag> with optional attributes
    # First pass: more specific removal of common HTML tags including <strong>, <em>, etc.
    cleaned = re.sub(r'<(strong|em|b|i|u|s|strike|del|ins|mark|small|sub|sup|code|pre|span|div|p|br|hr|ol|ul|li|a|img|blockquote|h1|h2|h3|h4|h5|h6)[^>]*?>', '', response_text, flags=re.IGNORECASE)
    # Second pass: remove any remaining HTML tags that might have been missed
    cleaned = re.sub(r'</(strong|em|b|i|u|s|strike|del|ins|mark|small|sub|sup|code|pre|span|div|p|br|hr|ol|ul|li|a|img|blockquote|h1|h2|h3|h4|h5|h6)>', '', cleaned, flags=re.IGNORECASE)
    # Final pass: remove any other HTML tags that might still exist
    cleaned = re.sub(r'<[^>]*?>', '', cleaned)
    
    # Replace multiple consecutive newlines with double newline
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    
    # Clean up any extra spaces around newlines
    cleaned = re.sub(r'[ \t]+\n', '\n', cleaned)
    
    # Remove extra spaces at beginning of lines that are not needed
    cleaned = re.sub(r'\n\s+', '\n', cleaned)
    
    # Remove any remaining HTML entities that might be left
    # Common HTML entities
    cleaned = re.sub(r'&nbsp;', ' ', cleaned)
    cleaned = re.sub(r'&lt;', '<', cleaned)
    cleaned = re.sub(r'&gt;', '>', cleaned)
    cleaned = re.sub(r'&amp;', '&', cleaned)
    cleaned = re.sub(r'&quot;', '"', cleaned)
    cleaned = re.sub(r'&#39;', "'", cleaned)
    cleaned = re.sub(r'&[a-zA-Z]+;', '', cleaned)  # Remove other HTML entities
    
    return cleaned.strip()

def format_response_for_display(response_text):
    """
    Format the response for better display in the UI
    """
    cleaned = clean_response_format(response_text)
    return cleaned