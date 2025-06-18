import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def find_top_products(product_name, csv_file="data.csv", top_n=3):
    """Args:
        product_name (str): The name of the product to search for (e.g., "яйцо куриное", "молоко").
        csv_file (str, optional): The file path to the CSV file containing product data. Defaults to "data.csv".
        top_n (int, optional): The number of top matching products to return. Defaults to 3.

    Returns:
        list: A nested list where each inner list contains all column values (e.g., name, weight/volume,
              calories, proteins, fats, carbohydrates, type, brand, manufacturer, article, composition,
              description, image_url, rating_score, price, category) for a matched product.
              Returns an empty list if no matches are found or an error occurs."""
    try:
        df = pd.read_csv(csv_file)
        # Extract product names from the 'name' column
        product_names = df['name'].tolist()
        
        # Find the top matches
        matches = process.extract(product_name, product_names, scorer=fuzz.partial_ratio, limit=top_n)

        result = []
        for match in matches:
            product_match = match[0]
            product_row = df[df['name'] == product_match].iloc[0]
            result.append(product_row.tolist())
        
        return result
    
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

# Test search
# test_products = [
#     "яйцо куриное",
#     "молоко",
#     "хлеб ржаной",
#     "хлеб пшеничный",
#     "кальмар охлажденный",
#     "мороженое пломбир",
#     "клубника замороженная",
#     "тесто слоеное",
#     "печень куриная",
#     "брокколи"
# ]

# for product in test_products:
#     print(f"\nSearching for: {product}")
#     results = find_top_products(product)
#     if results:
#         print(f"Top 3 matches for '{product}':")
#         print(results)
