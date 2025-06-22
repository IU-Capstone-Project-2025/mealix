import requests # type: ignore
from typing import Dict
from app.core.settings import settings

_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

def call_gpt(system_prompt: str, user_prompt: str,
             temperature: float = 0.7,
             max_tokens: int = 1000) -> str:
    payload: Dict = {
        "modelUri": f"gpt://{settings.yandex_folder_id}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens
        },
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user",   "text": user_prompt}
        ]
    }
    headers = {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json"
    }
    resp = requests.post(_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["result"]["alternatives"][0]["message"]["text"]
