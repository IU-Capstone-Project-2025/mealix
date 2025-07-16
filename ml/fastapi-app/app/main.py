from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from app.services import dish_selector, menu_builder, product_matcher_vectors as product_matcher
from app.services.rag_search import RAGSearch

# ──────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Mealix diet API",
    version="0.2.0",
    docs_url="/docs",
    redoc_url=None,
)

# ── Инициализируем RAG один раз при запуске сервера ───────────────────────
@app.on_event("startup")
async def _startup():
    app.state.rag = RAGSearch()   # singleton внутри себя кэширует модель
    print("✅ RAGSearch загружен")

def get_rag():
    return app.state.rag

# ── Pydantic модель запроса ───────────────────────────────────────────────
class MenuRequest(BaseModel):
    allergies: str = ""
    general_prefs: str = ""
    today_prefs: str = ""
    budget: str = ""
    nutrition_goals: str = ""

# ── Роут ───────────────────────────────────────────────────────────────────
@app.post("/menu")
def generate_menu(payload: MenuRequest, rag: RAGSearch = Depends(get_rag)) -> Dict[str, Any]:
    try:
        dishes = dish_selector.select_dishes(
            allergies=payload.allergies,
            general_prefs=payload.general_prefs,
            today_prefs=payload.today_prefs,
            budget=payload.budget,
            nutrition_goals=payload.nutrition_goals,
        )

        menu = menu_builder.build_menu(dishes, rag)
        enriched = product_matcher.enrich_products(menu)
        return enriched

    except Exception as exc:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))
