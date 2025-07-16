import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

df = pd.read_csv('data.csv')

def find_products_tfidf(query, dataframe, top_n=3):
    texts = (dataframe['name'].fillna('') + " " + 
             dataframe['description'].fillna('') + " " + 
             dataframe['composition'].fillna('')).tolist()
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
    dataframe['similarity'] = similarities
    
    results = dataframe.sort_values('similarity', ascending=False).head(top_n)
    return results[['name', 'type', 'similarity']].to_dict('records')

search_queries = [
    # Овощи
    "помидоры", "красная острая фасоль", "брокколи", "морковь", "лук репчатый",
    
    # Фрукты
    "клубника", "яблоки", "бананы", "апельсины", "виноград",
    
    # Орехи
    "грецкие орехи", "миндаль", "кешью", "фисташки", "арахис",
    
    # Мясо
    "куриная грудка", "говядина", "свинина", "индейка", "баранина"
]

all_results = {}
for query in search_queries:
    all_results[query] = find_products_tfidf(query, df)

with open('product_search_results.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print("Результаты поиска сохранены в файл product_search_results.json")
