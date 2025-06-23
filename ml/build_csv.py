import json, csv, pathlib, os
from typing import List, Dict

DATA_DIR   = pathlib.Path("datasets/recipes")
OUTPUT_CSV = pathlib.Path("recipes.csv")

def flatten_list(lst: List[str]) -> str:
    return "; ".join(s.strip() for s in lst)

def main() -> None:
    rows: List[Dict[str, str]] = []

    for json_path in DATA_DIR.glob("*.json"):
        
        print(json_path)
        category = json_path.stem
        with json_path.open(encoding="utf-8") as f:
            recipes = json.load(f)

        for idx, rec in enumerate(recipes, start=1):
            row = {
                "id":           f"{category}_{idx}",
                "name":         rec.get("name", "").strip(),
                "category":     category,
                "ingredients":  flatten_list(rec.get("ingredients", [])),
                "instructions": flatten_list(rec.get("instructions", [])),
                "nutrition":    json.dumps(rec.get("nutrition", {}), ensure_ascii=False)
            }
            rows.append(row)

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "name", "category",
                      "ingredients", "instructions", "nutrition"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Сохранён {OUTPUT_CSV} — {len(rows)} строк")

if __name__ == "__main__":
    main()
