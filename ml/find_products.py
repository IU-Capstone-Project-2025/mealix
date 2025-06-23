import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pymorphy3
import re

morph = pymorphy3.MorphAnalyzer()


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
    
    def lemmatize_text(text):
        if not isinstance(text, str):
            return ""
        
        words = re.findall(r'\w+', text.lower())
        
        # Lemmatize each word
        lemmatized_words = [morph.parse(word)[0].normal_form for word in words]
        
        return ' '.join(lemmatized_words)

    try:
        df = pd.read_csv(csv_file)
        
        if not {'name', 'type'}.issubset(df.columns):
            print("CSV file must contain 'name' and 'type' columns")
            return []
        
        lemmatized_query = lemmatize_text(product_name)
        
        matches = []
        
        for idx, row in df.iterrows():
            lemmatized_type = lemmatize_text(str(row['type']))
            lemmatized_name = lemmatize_text(str(row['name']))
            
            # Calculate score for 'type' (higher weight) and 'name' using lemmatized texts
            type_score = fuzz.partial_ratio(lemmatized_query, lemmatized_type) * 0.6
            name_score = fuzz.partial_ratio(lemmatized_query, lemmatized_name) * 0.4
            
            total_score = type_score + name_score
            
            matches.append({
                'score': total_score,
                'data': row.tolist()
            })
        
        matches = sorted(matches, key=lambda x: x['score'], reverse=True)
        
        # Extract top_n results
        top_matches = [match['data'] for match in matches[:top_n] if match['score'] > 50]
        
        return top_matches
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        return []
    except Exception as e:
        print(f"Error occurred: {str(e)}")
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

# product = input()
# while product != "стоп":
#     print(f"\nSearching for: {product}")
#     results = find_top_products(product)
#     if results:
#         print(f"Top 3 matches for '{product}':")
#         print(results)
#     product = input()