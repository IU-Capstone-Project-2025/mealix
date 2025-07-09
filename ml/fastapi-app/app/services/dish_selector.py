"""app/services/dish_selector.py
Шаг 1: выбираем 3 блюда (breakfast, lunch, dinner).
"""

from __future__ import annotations
import json, re
from typing import List

from app.clients.yandex_gpt import call_gpt


_SYSTEM_PROMPT = """Ты — диетолог. Составь список из 3 блюд (завтрак, обед и ужин)
на 1 день. Учитывай аллергии, предпочтения, бюджет и цели по КБЖУ.
Верни **строго один** JSON-объект, без markdown, без пояснений.
Формат:
{
  "dishes": ["...", "...", "..."]
}
"""

_JSON_RE = re.compile(r"\{.*?\}", re.S)


def _extract_dishes(text: str) -> List[str]:
    m = _JSON_RE.search(text)
    if not m:
        raise ValueError("JSON not найден в ответе LLM")
    data = json.loads(m.group(0))
    if "dishes" not in data or not isinstance(data["dishes"], list):
        raise ValueError("Поле 'dishes' отсутствует или не массив")
    return data["dishes"]


def build_user_prompt(*,
                      allergies: str = "",
                      general_prefs: str = "",
                      today_prefs: str = "",
                      budget: str = "",
                      nutrition_goals: str = "") -> str:
    return (
        f"Общие предпочтения: {general_prefs}\n"
        f"Предпочтения на день: {today_prefs}\n"
        f"Аллергии / нельзя: {allergies}\n"
        f"Бюджет: {budget}\n"
        f"КБЖУ цели: {nutrition_goals}"
    )



def select_dishes(allergies: str,
                  general_prefs: str,
                  today_prefs: str,
                  budget: str = "",
                  nutrition_goals: str = "") -> List[str]:
    user_prompt = build_user_prompt(
        allergies=allergies,
        general_prefs=general_prefs,
        today_prefs=today_prefs,
        budget=budget,
        nutrition_goals=nutrition_goals,
    )
    raw = call_gpt(_SYSTEM_PROMPT, user_prompt, max_tokens=150)
    dishes = _extract_dishes(raw)
    return dishes
