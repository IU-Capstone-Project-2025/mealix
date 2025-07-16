#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from pathlib import Path
from app.services.rag_search import RAGSearch

def main():

    rag_dir  = Path("rag_data")
    data_dir = Path("datasets")

    rag = RAGSearch(rag_dir=rag_dir, data_dir=data_dir)

    test_queries = [
        "курица с рисом",
        "веганская паста с томатами",
        "шоколадный торт"
    ]

    for q in test_queries:
        print("\n---\nЗапрос:", q)
        result = rag.find(q)
        print("Результат:", result)

if __name__ == "__main__":
    main()
