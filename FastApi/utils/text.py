import re

def clean_text(text):
    """Replace unsupported characters with ASCII equivalents."""
    replacements = {
        "\u2018": "'", "\u2019": "'",  # Smart single quotes → '
        "\u201C": '"', "\u201D": '"',  # Smart double quotes → "
        "\u2013": "-", "\u2014": "--",  # Dashes → -
        "\u2026": "..."  # Ellipsis → ...
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    # Remove other non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)  
    return text
