import sys
import os
from pathlib import Path
import pprint

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

try:
    from app.services.product_matcher_vectors import enrich_products
except ImportError as e:
    print("❌ Не удалось импортировать enrich_products. Исправьте путь импорта.")
    raise

def main():
    catalog_path = Path("datasets/data.csv")

    menu = {
        "meals": [
            {
                "name": "Завтрак",
                "ingredients": [
                    {"name": "яблоко"},
                    {"name": "груша"}
                ]
            },
            {
                "name": "Обед",
                "ingredients": [
                    {"name": "куриное филе"},
                    {"name": "рис"}
                ]
            }
        ]
    }

    print("🔍 Исходное меню:")
    pprint.pprint(menu)

    enriched = enrich_products(menu, catalog_path=catalog_path)

    print("\n✅ Обогащённое меню:")
    pprint.pprint(enriched)

if __name__ == "__main__":
    main()
