import re


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)      # trailing spaces
    text = re.sub(r"\n{3,}", "\n\n", text)       # collapse extra blank lines
    return text.strip()