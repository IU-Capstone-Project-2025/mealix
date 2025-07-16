from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
import pymorphy3

from app.core.settings import settings

# ─────────── Глобальные singletons / кэш ──────────────────────────────────
_morph = pymorphy3.MorphAnalyzer()
_vectorizer: TfidfVectorizer | None = None
_tfidf_matrix = None
_catalog_df: pd.DataFrame | None = None

_SCORE_THRESHOLD = 0.1

# ──────────────────────────────────────────────────────────────────────────
def _lemmatize(text: str) -> str:
    words = re.findall(r"\w+", str(text).lower())
    return " ".join(_morph.parse(w)[0].normal_form for w in words)

def _prepare_tfidf(df: pd.DataFrame) -> Tuple[TfidfVectorizer, Any]:
    texts = (
        df["name"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["composition"].fillna("")
    ).apply(_lemmatize).tolist()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

def _ensure_loaded(catalog_path: Path) -> Tuple[pd.DataFrame, TfidfVectorizer, Any]:
    global _catalog_df, _vectorizer, _tfidf_matrix
    if _catalog_df is None:
        _catalog_df = pd.read_csv(catalog_path)
        _vectorizer, _tfidf_matrix = _prepare_tfidf(_catalog_df)
        print(f"[MATCHER] TF-IDF индекс построен для {len(_catalog_df)} товаров.")
    return _catalog_df, _vectorizer, _tfidf_matrix

def _search_catalog(query: str,
                    df: pd.DataFrame,
                    vectorizer: TfidfVectorizer,
                    tfidf_matrix,
                    top_n: int = 1) -> List[pd.Series]:
    query_vec = vectorizer.transform([_lemmatize(query)])
    sims = cosine_similarity(query_vec, tfidf_matrix)[0]

    df = df.copy()
    df["similarity"] = sims
    matches = df[df["similarity"] >= _SCORE_THRESHOLD] \
              .sort_values("similarity", ascending=False) \
              .head(top_n)
    return [row for _, row in matches.iterrows()]

# ──────────────────────────────────────────────────────────────────────────
def enrich_products(menu: Dict[str, Any],
                    catalog_path: Path | None = None) -> Dict[str, Any]:
    catalog_path = catalog_path or (settings.data_dir / "data.csv")
    df, vec, mat = _ensure_loaded(catalog_path)

    for meal in menu.get("meals", []):
        for ing in meal.get("ingredients", []):
            match_rows = _search_catalog(ing["name"], df, vec, mat)
            if not match_rows:
                continue
            row = match_rows[0]
            ing["product_name"] = row["name"]
            if pd.notna(row.get("article", None)):
                ing["article"] = row["article"]

    return menu
