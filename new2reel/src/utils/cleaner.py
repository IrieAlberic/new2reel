import re

def clean_script_for_audio(text: str) -> str:
    """
    Cleans script text for TTS engine.
    - Removes Markdown (**, *, #)
    - Removes scene directions [in brackets] or (parentheses) if they look like instructions
    - Removes "Title:", "Scene 1:" prefixes
    """
    if not text:
        return ""

    # Remove bold/italic markdown
    text = re.sub(r'\*\*|__|\*|_', '', text)
    
    # Remove headers (# Title)
    text = re.sub(r'#+\s*', '', text)
    
    # Remove scene directions like [Cut to black] or (Whispering)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    
    # Remove common prefixes from LLM output
    text = re.sub(r'^(Title|Scene|Script|Narrator):\s*', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove quotes around the whole text if present
    text = text.strip().strip('"').strip("'")
    
    # Collapse multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
