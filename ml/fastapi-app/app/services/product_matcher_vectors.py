from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
import pymorphy3
_morph = pymorphy3.MorphAnalyzer()

from ..core.settings import settings

_morph = pymorphy3.MorphAnalyzer()
_SCORE_THRESHOLD = 0.1

def _lemmatize(text: str) -> str:
    words = re.findall(r"\w+", str(text).lower())
    return " ".join(_morph.parse(w)[0].normal_form for w in words)


def _prepare_tfidf(df: pd.DataFrame) -> tuple[TfidfVectorizer, Any, List[str]]:
    texts = (
        df["name"].fillna("") + " " +
        df["description"].fillna("") + " " +
        df["composition"].fillna("")
    ).apply(_lemmatize).tolist()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix, texts


def _search_catalog_tfidf(query: str,
                          df: pd.DataFrame,
                          vectorizer: TfidfVectorizer,
                          tfidf_matrix,
                          top_n: int = 1) -> List[pd.Series]:
    query_lem = _lemmatize(query)
    query_vec = vectorizer.transform([query_lem])
    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]

    df = df.copy()
    df["similarity"] = similarities
    filtered = df[df["similarity"] >= _SCORE_THRESHOLD]
    sorted_matches = filtered.sort_values("similarity", ascending=False)

    return [row for _, row in sorted_matches.head(top_n).iterrows()]


def enrich_products(menu: Dict[str, Any],
                    catalog_path: Path | None = None) -> Dict[str, Any]:
    catalog_path = catalog_path or (settings.data_dir / "data.csv")
    df = pd.read_csv(catalog_path)

    vectorizer, tfidf_matrix, _ = _prepare_tfidf(df)

    for meal in menu.get("meals", []):
        for ing in meal.get("ingredients", []):
            matches = _search_catalog_tfidf(ing["name"], df, vectorizer, tfidf_matrix, top_n=1)
            if matches:
                row = matches[0]
                ing["product_name"] = row["name"]

                article_val = row.get("article") or (row.iloc[9] if len(row) > 9 else None)
                if article_val:
                    ing["article"] = article_val
                elif len(row) > 9:
                    ing["article"] = row.iloc[9]

    return menu
