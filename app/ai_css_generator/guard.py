from pydantic import BaseModel, field_validator
import re
from langdetect import detect

LANG_PATTERNS = {
    "en": [
        r"(?i)\b(ignore|disregard|override|forget)\b.*?(instructions|previous|above)",
        r"(?i)\b(you are now|you will pretend to|you will no longer)\b",
        r"(?i)\b(role:|system:|user:|assistant:)\b",
        r"(?i)\b(show|reveal|output|print)\b.*?(prompt|template|html|source)",
    ],
    "ru": [
        r"(?i)\b(игнорируй|забудь|отмени)\b.*?(инструкции|предыдущие|выше)",
        r"(?i)\b(действуй как|притворись|измени роль)\b",
        r"(?i)\b(выдай|раскрой|покажи)\b.*?(шаблон|html|инструкции|исходник)",
    ],
    "code": [
        r"(?i)<script>.*?</script>",
        r"(?i)\b(eval|exec|os\.|subprocess\.|rm\s+-rf|wget|curl)\b",
        r"(?i)<?php.*?>",
        r"(?i)```.*?```",
    ]
}

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return "ru" if lang == "ru" else "en"
    except:
        return "en"

class PromptRequest(BaseModel):    
    prompt: str
    @field_validator('prompt')
    def check_prompt(cls, v):
        lang = detect_language(v)
        patterns = LANG_PATTERNS.get(lang, []) + LANG_PATTERNS["code"]
        for pattern in patterns:
            if re.search(pattern, v):
                raise ValueError(f"Prompt injection detected in {lang} text.")
        return v
