from pathlib import Path

import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

def rebuild_rag(
    csv_path: Path,
    rag_dir: Path,
    model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
):
    df = pd.read_csv(csv_path)
    texts = (
        df["name"].fillna("").astype(str)
        + ". " + df["category"].fillna("").astype(str)
        + ". Ингредиенты: " + df["ingredients"].fillna("").astype(str)
        + ". Приготовление: " + df["instructions"].fillna("").astype(str)
    ).tolist()

    ids = df["id"].values
    rag_dir.mkdir(parents=True, exist_ok=True)

    with open(rag_dir / "rag_texts.txt", "w", encoding="utf-8") as f:
        for txt in texts:
            f.write(txt.replace("\n", " ") + "\n")

    print("[RAG BUILD] Загружаем модель…")
    encoder = SentenceTransformer(model_name)
    print("[RAG BUILD] Кодирование эмбеддингов…")
    embeddings = encoder.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        batch_size=32
    )
    faiss.normalize_L2(embeddings)
    np.save(rag_dir / "rag_ids.npy", ids)
    np.save(rag_dir / "rag_embeddings.npy", embeddings)

    print(f"[RAG BUILD] Сохранено {len(ids)} записей в {rag_dir}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Rebuild RAG index data from recipes.csv"
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/recipes.csv"),
        help="Путь к recipes.csv"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("rag_data"),
        help="Папка для rag_texts.txt, rag_ids.npy, rag_embeddings.npy"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="paraphrase-multilingual-MiniLM-L12-v2",
        help="Имя модели SentenceTransformer"
    )
    args = parser.parse_args()

    rebuild_rag(args.csv, args.out, args.model)
