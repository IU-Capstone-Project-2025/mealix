from __future__ import annotations
import json, re
from typing import Any, Dict, List

from app.clients.yandex_gpt import call_gpt
from app.services.rag_search import RAGSearch

_SECOND_SYSTEM = "Ты — опытный диетолог и нутрициолог."

_JSON_RE = re.compile(r"\{.*\}", re.S)


def _extract_json(text: str) -> Dict[str, Any]:
    m = _JSON_RE.search(text)
    if not m:
        raise ValueError("JSON not найден в ответе LLM")
    return json.loads(m.group(0))


# ───────────────────────────────────────────────────────────────────────
def build_menu(dishes: List[str], rag: RAGSearch) -> Dict[str, Any]:

    print("Шаг 1: готовим контекст...")

    ctx = []
    for dish in dishes:
        print(f"🔍 Ищем рецепт для: {dish}")
        recipe = rag.find(dish)
        print(f"✅ Найден рецепт длиной {len(recipe) if recipe else 0}")
        ctx.append({"name": dish, "recipe": recipe})

    print("Контекст готов")

    user_prompt = (
        "Ты — опытный диетолог. Для каждого блюда распиши ингредиенты "
        "с количествами, шаги приготовления и список продуктов к покупке. "
        "Если поле recipe = null — придумай сама, учитывая название блюда. "
        "Если recipe заполнено — можешь адаптировать или уточнять данные.\n\n"
        f"Блюда:\n{json.dumps(ctx, ensure_ascii=False, indent=2)}\n\n"
        "И верни **строго один** JSON-объект, без markdown, без пояснений, на три приёма пищи.\n"
        "Формат:\n"
        "{\n"
        '  "meals": [\n'
        '    {\n'
        '      "type": "lunch" | "dinner" | "breakfast",\n'
        '      "dish": "…",\n'
        '      "ingredients": [\n'
        '        {"name": "…", "amount": <число>, "unit": "g|ml|pcs"}\n'
        "      ],\n"
        '      "steps": ["Шаг 1", "Шаг 2"]\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    print("\n")
    print("\n")
    print(user_prompt)
    print("\n")
    print("\n")
    
    print("Вызываем модель")
    
    raw = call_gpt(
        system_prompt=_SECOND_SYSTEM,
        user_prompt=user_prompt,
        max_tokens=2000,
    )
    
    print("Модель отработала")
    
    return _extract_json(raw)
