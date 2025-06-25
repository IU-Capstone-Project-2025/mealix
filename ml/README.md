Mealix is an AI-powered FastAPI service that generates personalized daily meal plans using YandexGPT and a recipe retrieval system based on semantic search (RAG). The system supports food preferences, allergy restrictions, and automatic matching of ingredients to a local product catalog.
- Generates breakfast, lunch, and dinner using natural language prompts
- Retrieval-Augmented Generation (RAG) using FAISS and SentenceTransformers
- Powered by YandexGPT API for text generation
- Fuzzy matching and morphological analysis for ingredient mapping
- Automatically maps ingredients to products in a dataset

| Component         | Description                                  |
|------------------|----------------------------------------------|
| **FastAPI**       | RESTful API framework                        |
| **YandexGPT**     | External LLM for recipe generation           |
| **FAISS**         | Vector similarity search for recipe retrieval|
| **SentenceTransformers** | Embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) |
| **pandas**        | Working with CSV product and recipe datasets |
| **pymorphy2**     | Russian language morphological analyzer      |
| **rapidfuzz**     | Fast fuzzy string matching                   |


fastapi-app/
├── app/
│   ├── __pycache__/
│   │   ├── __init__.cpython-310.pyc
│   │   └── main.cpython-310.pyc
│   ├── clients/
│   │   ├── __init__.py
│   │   └── yandex_gpt.py
│   │   ├── __pycache__/
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── yandex_gpt.cpython-310.pyc
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── __pycache__/
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── settings.cpython-310.pyc
│   ├── services/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── dish_selector.py
│   │   ├── menu_builder.py
│   │   ├── product_matcher.py
│   │   └── rag_search.py
│   ├── main.py
│   └── __init__.py
├── datasets/
│   ├── data.csv
│   └── recipes.csv
├── info/
│   ├── allergies.txt
│   ├── general_prefs.txt
│   └── today_prefs.txt
├── rag_data/
│   ├── rag_embeddings.npy
│   ├── rag_ids.npy
│   └── rag_texts.txt
└── requirements.txt
.env
build_csv.py
Dockerfile
find_products.py
generate_menu.py
README.md

## Getting Started (Local)

### 1. Clone the repository

git clone https://github.com/yourname/mealix.git
cd mealix/fastapi-app

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

Create a .env file in app/:
YANDEX_API_KEY=your_yandex_api_key
YANDEX_FOLDER_ID=your_yandex_folder_id

Run the API
uvicorn app.main:app --reload
