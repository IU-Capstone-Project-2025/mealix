from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd # type: ignore
from rapidfuzz import fuzz             # type: ignore
import pymorphy2                        # type: ignore

from app.core.settings import settings


_morph = pymorphy2.MorphAnalyzer()
_SCORE_THRESHOLD = 50.0


def _lemmatize(text: str) -> str:
    words = re.findall(r"\w+", str(text).lower())
    return " ".join(_morph.parse(w)[0].normal_form for w in words)


def _search_catalog(query: str,
                    df: pd.DataFrame,
                    top_n: int = 1) -> List[pd.Series]:
    q_lem = _lemmatize(query)
    scores: List[tuple[float, pd.Series]] = []

    for _, row in df.iterrows():
        type_score = fuzz.partial_ratio(q_lem, _lemmatize(row.get("type", ""))) * 0.6
        name_score = fuzz.partial_ratio(q_lem, _lemmatize(row.get("name", ""))) * 0.4
        total = type_score + name_score
        if total >= _SCORE_THRESHOLD:
            scores.append((total, row))

    scores.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scores[:top_n]]


def enrich_products(menu: Dict[str, Any],
                    catalog_path: Path | None = None) -> Dict[str, Any]:
    catalog_path = catalog_path or (settings.data_dir / "data.csv")
    df = pd.read_csv(catalog_path)

    for meal in menu.get("meals", []):
        for ing in meal.get("ingredients", []):
            matches = _search_catalog(ing["name"], df, top_n=1)
            if matches:
                row = matches[0]
                ing["product_name"] = row["name"]
                
                article_val = row.get("article") or (row.iloc[9] if len(row) > 9 else None)
                if article_val:
                    ing["article"] = article_val
                
                elif len(row) > 9:
                    ing["article"] = row.iloc[9]

    return menu
