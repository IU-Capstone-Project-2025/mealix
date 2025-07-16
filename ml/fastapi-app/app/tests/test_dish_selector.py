# test_dish_selector.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.services import dish_selector

if __name__ == "__main__":
    dishes = dish_selector.select_dishes(
        allergies="орехи, молоко",
        general_prefs="люблю азиатскую кухню, острое",
        today_prefs="хочу легкий ужин",
        budget="до 400 рублей",
        nutrition_goals="2000 ккал, 100г белков, 50г жиров, 250г углеводов"
    )

    print("🍽 Блюда, подобранные LLM:")
    for i, dish in enumerate(dishes, 1):
        print(f"{i}. {dish}")