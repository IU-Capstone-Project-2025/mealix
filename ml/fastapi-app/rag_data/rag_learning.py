
from pathlib import Path
import argparse
from typing import List

import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer


def build_text(row: pd.Series) -> str:
    parts: List[str] = [
        str(row["name"]),
        f"Категория: {row['category']}",
        f"Ингредиенты: {row['ingredients']}",
        f"Инструкции: {row['instructions']}",
        f"Пищевая ценность: {row['nutrition']}",
    ]
    return "\n".join(parts)


def main(csv_path: Path, out_dir: Path, model_name: str) -> None:
    print("читаем CSV")
    df = pd.read_csv(csv_path)

    print("собираем тексты")
    texts = [build_text(row) for _, row in df.iterrows()]
    ids = df["id"].to_numpy()

    print(f"загружаем SentenceTransformer: {model_name}")
    model = SentenceTransformer(model_name)

    print("кодируем эмбеддинги")
    embeddings = model.encode(
        texts,
        batch_size=64,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "rag_embeddings.npy", embeddings)
    np.save(out_dir / "rag_ids.npy", ids)
    with open(out_dir / "rag_texts.txt", "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t.replace("\n", " ") + "\n")

    print(f"cохранено: {len(ids)} рецептов → {out_dir.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Сгенерировать файлы rag_embeddings.npy, rag_ids.npy, rag_texts.txt"
    )
    parser.add_argument("--csv", required=True, help="Путь к recipes.csv")
    parser.add_argument("--out", default="rag_data", help="Выходная директория")
    parser.add_argument(
        "--model",
        default="paraphrase-multilingual-MiniLM-L12-v2",
        help="SentenceTransformer model id",
    )
    args = parser.parse_args()

    main(Path(args.csv), Path(args.out), args.model)
