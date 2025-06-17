import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.povarenok.ru/recipes/poisk/kasha-ovsyanaya"
HEADERS = {"User-Agent": "Mozilla/5.0"}

recipes = []

# Проходим по страницам 1–15
for page in range(1, 3):
    # Формируем URL для текущей страницы
    if page == 1:
        url = BASE_URL + "/?orderby=#searchformtop"
    else:
        url = f"{BASE_URL}/~{page}/?orderby=#searchformtop"

    print(f"\n📄 Обработка страницы {page}: {url}")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Получаем карточки рецептов
    cards = soup.select("article.item-bl")
    print(f"🔎 Найдено рецептов на странице: {len(cards)}")

    for i, card in enumerate(cards, 1):
        try:
            title_tag = card.select_one("h2 a")
            recipe_url = title_tag["href"]
            recipe_name = ' '.join(title_tag.get_text(strip=True).split())

            # Переход на страницу рецепта
            recipe_resp = requests.get(recipe_url, headers=HEADERS)
            recipe_soup = BeautifulSoup(recipe_resp.text, "html.parser")

            # Ингредиенты
            ingredients = [
                ' '.join(li.get_text(separator=' ', strip=True).split())
                for li in recipe_soup.select("div.ingredients-bl ul li")
            ]

            # Шаги приготовления
            steps = [
                ' '.join(p.get_text(separator=' ', strip=True).split())
                for li in recipe_soup.select("ul[itemprop='recipeInstructions'] li.cooking-bl")
                for p in li.select("div > p")
            ]

            # Пищевая ценность
            nutrition_block = recipe_soup.select_one("div[itemprop='nutrition']")
            calories = protein = fat = carbs = None

            if nutrition_block:
                calories_tag = nutrition_block.select_one("strong[itemprop='calories']")
                protein_tag = nutrition_block.select_one("strong[itemprop='proteinContent']")
                fat_tag = nutrition_block.select_one("strong[itemprop='fatContent']")
                carbs_tag = nutrition_block.select_one("strong[itemprop='carbohydrateContent']")

                if calories_tag:
                    calories = ' '.join(calories_tag.get_text(strip=True).split())
                if protein_tag:
                    protein = ' '.join(protein_tag.get_text(strip=True).split())
                if fat_tag:
                    fat = ' '.join(fat_tag.get_text(strip=True).split())
                if carbs_tag:
                    carbs = ' '.join(carbs_tag.get_text(strip=True).split())

            recipes.append({
                "name": recipe_name,
                "ingredients": ingredients,
                "instructions": steps,
                "url": recipe_url,
                "nutrition": {
                    "calories": calories,
                    "protein": protein,
                    "fat": fat,
                    "carbohydrates": carbs
                }
            })

            print(f"[{i}] ✅ {recipe_name}")
            time.sleep(1.0)  # Пауза между запросами к рецептам

        except Exception as e:
            print(f"[{i}] ❌ Ошибка: {e}")
            continue

    time.sleep(1.5)  # Пауза между страницами

# Сохраняем результат
with open("ovsyanaya_kasha.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=2)

print(f"\n✅ Всего сохранено {len(recipes)} рецептов в json")
