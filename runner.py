import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urlparse

# Category mapping for URLs
CATEGORY_MAP = {
    'https://www.povarenok.ru/recipes/destiny/5/': 'zavtraki',
    'https://www.povarenok.ru/recipes/category/2/': 'supy',
    'https://www.povarenok.ru/recipes/category/6/': 'hot_food',
    'https://www.povarenok.ru/recipes/category/12/': 'salaty',
    'https://www.povarenok.ru/recipes/category/30/': 'deserts',
    'https://www.povarenok.ru/recipes/category/7/': 'myaso_bludo',
    'https://www.povarenok.ru/recipes/category/8/': 'fish_bludo',
    'https://www.povarenok.ru/recipes/category/9/': 'chicken_bludo',
    'https://www.povarenok.ru/recipes/poisk/kasha/': 'kasha',
    'https://www.povarenok.ru/recipes/poisk/kasha-ovsyanaya/': 'ovsyanaya_kasha'
}

HEADERS = {"User-Agent": "Mozilla/5.0"}
recipes = []
recipe_counts = {category: 0 for category in CATEGORY_MAP.values()}

# Read URLs from links.txt
with open('clean_links.txt', 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

# Process each URL
for base_url in urls:
    # Get category from URL (remove query parameters for matching)
    parsed_url = urlparse(base_url)
    clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    category = CATEGORY_MAP.get(clean_url, 'unknown')

    print(f"\n🌐 Processing category: {category} ({base_url})")

    # Process pages 1-15 for each URL
    for page in range(1, 15):
        # Form URL for current page
        if page == 1:
            url = base_url
        else:
            url = f"{base_url.rstrip('/')}/~{page}/"
            if 'orderby=' in base_url:
                url += '?' + base_url.split('?')[-1]

        print(f"\n📄 Processing page {page}: {url}")
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Get recipe cards
            cards = soup.select("article.item-bl")
            print(f"🔎 Found {len(cards)} recipes on page")

            if not cards:  # Break if no recipes found
                print("No more recipes found, moving to next category")
                break

            for i, card in enumerate(cards, 1):
                try:
                    title_tag = card.select_one("h2 a")
                    recipe_url = title_tag["href"]
                    recipe_name = ' '.join(title_tag.get_text(strip=True).split())

                    # Increment recipe count for category
                    recipe_counts[category] += 1
                    recipe_id = f"{category}_{recipe_counts[category]}"

                    # Go to recipe page
                    recipe_resp = requests.get(recipe_url, headers=HEADERS)
                    recipe_resp.raise_for_status()
                    recipe_soup = BeautifulSoup(recipe_resp.text, "html.parser")

                    # Ingredients
                    ingredients = [
                        ' '.join(li.get_text(separator=' ', strip=True).split())
                        for li in recipe_soup.select("div.ingredients-bl ul li")
                    ]

                    # Instructions
                    steps = [
                        ' '.join(p.get_text(separator=' ', strip=True).split())
                        for li in recipe_soup.select("ul[itemprop='recipeInstructions'] li.cooking-bl")
                        for p in li.select("div > p")
                    ]

                    # Nutrition
                    nutrition_block = recipe_soup.select_one("div[itemprop='nutrition']")
                    calories = protein = fat = carbs = None

                    if nutrition_block:
                        calories_tag = nutrition_block.select_one("strong[itemprop='calories']")
                        protein_tag = nutrition_block.select_one("strong[itemprop='proteinContent']")
                        fat_tag = nutrition_block.select_one("strong[itemprop='fatContent']")
                        carbs_tag = nutrition_block.select_one("strong[itemprop='carbohydrateContent']")

                        calories = ' '.join(calories_tag.get_text(strip=True).split()) if calories_tag else ''
                        protein = ' '.join(protein_tag.get_text(strip=True).split()) if protein_tag else ''
                        fat = ' '.join(fat_tag.get_text(strip=True).split()) if fat_tag else ''
                        carbs = ' '.join(carbs_tag.get_text(strip=True).split()) if carbs_tag else ''

                    nutrition = f"Calories: {calories}, Protein: {protein}, Fat: {fat}, Carbohydrates: {carbs}"

                    # Image URL
                    image_tag = recipe_soup.select_one("img[itemprop='image']")
                    image_url = image_tag["src"] if image_tag and "src" in image_tag.attrs else ""

                    recipes.append({
                        "id": recipe_id,
                        "name": recipe_name,
                        "category": category,
                        "ingredients": ';'.join(ingredients),
                        "instructions": ';'.join(steps),
                        "nutrition": nutrition,
                        "image_url": image_url
                    })

                    print(f"[{i}] ✅ {recipe_id}: {recipe_name}")
                    time.sleep(1.0)  # Pause between recipe requests

                except Exception as e:
                    print(f"[{i}] ❌ Error: {e}")
                    continue

            time.sleep(1.5)  # Pause between pages

        except Exception as e:
            print(f"❌ Error processing page {page}: {e}")
            continue

# Save to CSV
with open('recepts.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'category', 'ingredients', 'instructions', 'nutrition', 'image_url'])
    writer.writeheader()
    writer.writerows(recipes)

print(f"\n✅ Saved {len(recipes)} recipes to recepts.csv")