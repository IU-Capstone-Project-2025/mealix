import os, re, json, argparse, pathlib, sys
from typing import Dict
import requests

URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
HEADERS = {
    "Authorization": f"Api-Key {API_KEY}",
    "Content-Type":  "application/json",
}

SYSTEM_PROMPT = """Ты — диетолог. Составь описание блюда на 1 день (завтрак, обед и ужин) с ингредиентами и шагами.
Ответь текстом для каждого блюда без JSON.
Завтрак: описание блюда, ингредиенты и шаги.
Обед: описание блюда, ингредиенты и шаги.
Ужин: описание блюда, ингредиенты и шаги."""

def read_txt(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8").strip()

def build_user_prompt(allergies: str, general: str, today: str) -> str:
    return (
        f"Общие предпочтения: {general}\n"
        f"Предпочтения на день: {today}\n"
        f"Аллергии / нельзя: {allergies}"
    )

def call_yandex_gpt(system_prompt: str, user_prompt: str) -> str:
    if "PASTE_API_KEY_HERE" in API_KEY or "PASTE_FOLDER_ID_HERE" in FOLDER_ID:
        raise RuntimeError("Заполни API_KEY и FOLDER_ID или передай их в env.")

    payload: Dict = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 800
        },
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user",   "text": user_prompt}
        ]
    }

    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["result"]["alternatives"][0]["message"]["text"]

def extract_meal_data(text: str) -> Dict:
    meals = {}
    meals["breakfast"], meals["lunch"], meals["dinner"] = text.split('\n')[:3]
    return meals

def generate_json(meals: Dict) -> dict:
    return {
        "meals": [
            {
                "type": "breakfast",
                "dish": meals["breakfast"],
                "ingredients": [],
                "steps": []
            },
            {
                "type": "lunch",
                "dish": meals["lunch"],
                "ingredients": [],
                "steps": []
            },
            {
                "type": "dinner",
                "dish": meals["dinner"],
                "ingredients": [],
                "steps": []
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="Сгенерировать меню на 1 день.")
    parser.add_argument("--allergies", default="allergies.txt",
                        help="Файл со списком аллергий")
    parser.add_argument("--general",   default="general_prefs.txt",
                        help="Файл с общими предпочтениями")
    parser.add_argument("--today",     default="today_prefs.txt",
                        help="Файл с пожеланиями на сегодня")
    parser.add_argument("--out",       default="menu.json",
                        help="Имя выходного JSON-файла")
    args, _ = parser.parse_known_args()

    try:
        allergies = read_txt(pathlib.Path(args.allergies))
        general   = read_txt(pathlib.Path(args.general))
        today     = read_txt(pathlib.Path(args.today))
    except FileNotFoundError as e:
        print("Нет входного файла:", e.filename, file=sys.stderr)
        sys.exit(1)

    user_prompt = build_user_prompt(allergies, general, today)

    try:
        raw_answer = call_yandex_gpt(SYSTEM_PROMPT, user_prompt)
    except Exception as err:
        print("LLM request failed:", err, file=sys.stderr)
        sys.exit(1)

    try:
        meal_data = extract_meal_data(raw_answer)
        menu = generate_json(meal_data)
    except Exception as err:
        print("Не удалось обработать ответ:", err, file=sys.stderr)
        sys.exit(1)

    pathlib.Path(args.out).write_text(
        json.dumps(menu, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
