import os
import httpx
from dotenv import load_dotenv
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_random_exponential,
    stop_after_attempt,
)
from httpx import HTTPError, TimeoutException, ConnectError

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4"

headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

# Retry только при сетевых ошибках
@retry(
    retry=retry_if_exception_type((TimeoutException, ConnectError, HTTPError)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True,
)
async def call_openai(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ты помощник, генерирующий стили HTML-страниц по описанию."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_URL, json=payload, headers=headers)
        response.raise_for_status()  # вызовет исключение при ошибке 4xx/5xx
        data = response.json()
        return data["choices"][0]["message"]["content"]