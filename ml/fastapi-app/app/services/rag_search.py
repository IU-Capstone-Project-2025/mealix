from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import faiss  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore

from app.core.settings import settings

THRESHOLD: float = 0.85
TOP_K: int = 1


@lru_cache(maxsize=1)
def _get_encoder(model_name: str = "paraphrase-multilingual-MiniLM-L12-v2") -> SentenceTransformer:
    """Singleton-объект SentenceTransformer (экономит память и время)."""
    print("[RAG] Загружаем SentenceTransformer…")
    return SentenceTransformer(model_name)


class RAGSearch:
    """Поиск рецептов по косинусному сходству эмбеддингов."""

    def __init__(self, rag_dir: Path | None = None, data_dir: Path | None = None) -> None:
        rag_dir = rag_dir or settings.rag_dir
        data_dir = data_dir or settings.data_dir

        # ── Загружаем данные ──────────────────────────────────────────────────
        self.embeddings: np.ndarray = np.load(rag_dir / "rag_embeddings.npy")
        self.ids: np.ndarray = np.load(rag_dir / "rag_ids.npy", allow_pickle=True).astype(str)

        self.recipes_df: pd.DataFrame = pd.read_csv(data_dir / "recipes.csv")
        self.recipes_df["id"] = self.recipes_df["id"].astype(str)

        # ── FAISS индекс ──────────────────────────────────────────────────────
        d = self.embeddings.shape[1]
        faiss.normalize_L2(self.embeddings)
        self.index = faiss.IndexFlatIP(d)
        self.index.add(self.embeddings)

        # ── Модель ────────────────────────────────────────────────────────────
        self.encoder = _get_encoder()
        print(f"[RAG] Инициализировано: {len(self.embeddings)} векторов, "
              f"{len(self.recipes_df)} рецептов")

    # ──────────────────────────────────────────────────────────────────────────
    def _encode(self, text: str) -> np.ndarray:
        vec = self.encoder.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(vec)
        return vec

    # ──────────────────────────────────────────────────────────────────────────
    def find(self, query: str) -> Dict[str, Any] | None:
        """Возвращает dict рецепта + similarity или None, если ниже порога."""
        query_vec = self._encode(query)
        D, I = self.index.search(query_vec, k=TOP_K)

        score = float(D[0, 0])
        idx = int(I[0, 0])
        print(f"[RAG] '{query}' → score={score:.3f}")

        if score < THRESHOLD:
            return None

        recipe_id = self.ids[idx]
        row = self.recipes_df.loc[self.recipes_df["id"] == recipe_id]
        if row.empty:
            return None

        recipe = row.iloc[0].to_dict() | {"similarity": score}
        return recipe
