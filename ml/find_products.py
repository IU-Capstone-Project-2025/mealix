import pandas as pd
from fuzzywuzzy import fuzz

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
        
        if not {'name', 'type'}.issubset(df.columns):
            print("CSV file must contain 'name' and 'type' columns")
            return []
        
        matches = []
        
        for idx, row in df.iterrows():
            type_score = fuzz.WRatio(product_name, str(row['type']))
            name_score = fuzz.WRatio(product_name, str(row['name']))
            
            total_score = type_score + name_score
            
            matches.append({
                'score': total_score,
                'data': row.tolist()
            })
        
        matches = sorted(matches, key=lambda x: x['score'], reverse=True)
        top_matches = [match['data'] for match in matches[:top_n]]
        
        return top_matches
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        return []
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []

# product = input()
# while product != "":
#     print(f"\nSearching for: {product}")
#     results = find_top_products(product)
#     if results:
#         print(f"Top 3 matches for '{product}':")
#         print(results)
#     product = input()