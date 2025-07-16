from __future__ import annotations
import json
import re
from typing import Any, Dict, List

from app.clients.yandex_gpt import call_gpt
from app.services.rag_search import RAGSearch

_SYSTEM = "Ты — опытный диетолог и нутрициолог."
_JSON_ARR_RE = re.compile(r"\[.*\]", re.S)
_MEAL_RE = re.compile(r"(breakfast|lunch|dinner)", re.I)


def _extract_json_arr(text: str) -> List[Any]:
    m = _JSON_ARR_RE.search(text)
    if not m:
        raise ValueError("JSON array not found in LLM response")
    return json.loads(m.group(0))


def _call(prompt: str, *, max_tokens: int = 400) -> str:
    return call_gpt(system_prompt=_SYSTEM, user_prompt=prompt, max_tokens=max_tokens)


def _safe_extract_json_arr(prompt: str, max_tokens: int = 400, retries: int = 2) -> List[Any]:
    for attempt in range(retries):
        try:
            raw = _call(prompt, max_tokens=max_tokens)
            return _extract_json_arr(raw)
        except Exception as e:
            print(f"[⚠️ LLM Error] попытка {attempt+1}/{retries} — {e}")
            continue
    return []  # fallback


def _determine_meal_type(dish: str, recipe: Dict[str, Any] | None) -> str:
    ctx = f"(рецепт частично: {json.dumps(recipe, ensure_ascii=False)[:200]} …)" if recipe else ""
    raw = _call(
        f"Для блюда «{dish}» {ctx} выбери тип приёма пищи: breakfast, lunch или dinner.\n"
        "Ответи **одним словом** без кавычек.",
        max_tokens=10,
    )
    m = _MEAL_RE.search(raw)
    return (m.group(1).lower() if m else "lunch")


def _determine_ingredients(dish: str, recipe: Dict[str, Any] | None) -> List[Dict[str, Any]]:
    ctx = f"Вот рецепт: {json.dumps(recipe, ensure_ascii=False)}" if recipe else ""
    prompt = (
        f"Составь список ингредиентов для блюда «{dish}». {ctx}\n"
        "Верни строго JSON-массив: "
        '[{"name": "…", "amount": <число>, "unit": "g|ml|pcs"}]'
    )
    return _safe_extract_json_arr(prompt)


def _determine_steps(dish: str, recipe: Dict[str, Any] | None) -> List[str]:
    ctx = f"Используй рецепт: {json.dumps(recipe, ensure_ascii=False)}" if recipe else ""
    prompt = (
        f"Опиши шаги приготовления блюда «{dish}». {ctx}\n"
        'Верни JSON-массив строк, например ["Шаг 1", "Шаг 2"].'
    )
    return _safe_extract_json_arr(prompt)


def build_menu(dishes: List[str], rag: RAGSearch) -> Dict[str, Any]:
    meals: List[Dict[str, Any]] = []

    for dish in dishes:
        print(f"🔍 RAG-поиск для: {dish}")
        recipe = rag.find(dish)

        meal = {
            "type": _determine_meal_type(dish, recipe),
            "dish": dish,
            "ingredients": _determine_ingredients(dish, recipe),
            "steps": _determine_steps(dish, recipe),
        }
        meals.append(meal)

    return {"meals": meals}
