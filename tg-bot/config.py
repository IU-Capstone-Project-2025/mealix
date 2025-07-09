import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_HOST = os.getenv("BACKEND_HOST", "http://localhost:8080")
MINIAPP_HOST = os.getenv("MINIAPP_HOST", "http://localhost:8082") 