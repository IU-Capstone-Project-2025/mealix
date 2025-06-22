from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import faiss                   # type: ignore
import numpy as np             # type: ignore
import pandas as pd            # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore

from app.core.settings import settings

THRESHOLD: float = 0.60
TOP_K: int = 1


class RAGSearch:

    def __init__(
        self,
        rag_dir: Path | None = None,
        data_dir: Path | None = None,
    ) -> None:
        rag_dir = rag_dir or settings.rag_dir
        data_dir = data_dir or settings.data_dir

        self.embeddings = np.load(rag_dir / "rag_embeddings.npy")
        self.ids        = np.load(rag_dir / "rag_ids.npy")
        d = self.embeddings.shape[1]

        self.index = faiss.IndexFlatIP(d)
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

        print("[RAG] Загружаем SentenceTransformer…")
        self.encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        print("[RAG] Модель готова ✔︎")

        self.recipes_df = pd.read_csv(data_dir / "recipes.csv")
        print(f"[RAG] Эмбеддинги: {len(self.embeddings)}, рецептов: {len(self.recipes_df)}")

    def _encode(self, text: str) -> np.ndarray:
        print("[RAG]    → encode() start")
        vec = self.encoder.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(vec)
        print("[RAG]    ← encode() done")
        return vec

    def find(self, query: str) -> Dict[str, Any] | None:
        print(f"[RAG] ▶︎ Поиск для: {query!r}")

        query_vec = self._encode(query)
        D, I = self.index.search(query_vec, k=TOP_K)

        score = float(D[0][0])
        idx   = int(I[0][0])
        print(f"[RAG] • score={score:.3f}, idx={idx}")

        if score < THRESHOLD:
            print("[RAG] • ниже порога → None")
            return None

        recipe_id = self.ids[idx]
        row = self.recipes_df[self.recipes_df["id"] == recipe_id]
        if row.empty:
            print(f"[RAG] • id={recipe_id} нет в CSV → None")
            return None

        recipe = row.iloc[0].to_dict() | {"similarity": score}
        print(f"[RAG] • найден рецепт: {recipe.get('name', recipe_id)!r}")
        return recipe
