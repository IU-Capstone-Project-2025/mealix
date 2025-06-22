from typing import Dict, Any

from fastapi import FastAPI, HTTPException  # type: ignore
from pydantic import BaseModel  # type: ignore
import traceback

from app.services import (
    dish_selector,
    rag_search,
    menu_builder,
    product_matcher,
)

print("Инициализируем RAGSearch...")
rag_engine = rag_search.RAGSearch()
print("✅ RAGSearch готов")

app = FastAPI(
    title="Mealix diet API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)

class MenuRequest(BaseModel):
    allergies: str = ""
    general_prefs: str = ""
    today_prefs: str = ""

@app.post("/menu")
def generate_menu(payload: MenuRequest) -> Dict[str, Any]:
    try:
        print("📥 Получен запрос:")
        print(f"   allergies:      {payload.allergies}")
        print(f"   general_prefs:  {payload.general_prefs}")
        print(f"   today_prefs:    {payload.today_prefs}")

        dishes = dish_selector.select_dishes(
            allergies=payload.allergies,
            general_prefs=payload.general_prefs,
            today_prefs=payload.today_prefs,
        )
        print("🍽 Выбраны блюда:", dishes)

        print("🔧 Строим меню через build_menu...")
        menu = menu_builder.build_menu(dishes, rag_engine)
        print("✅ Меню построено:", menu)

        print("🧩 Обогащаем продукты через enrich_products...")
        enriched_menu = product_matcher.enrich_products(menu)
        print("✅ Меню обогащено:", enriched_menu)

        return enriched_menu

    except Exception as exc:
        print("❌ Произошла ошибка:")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))
