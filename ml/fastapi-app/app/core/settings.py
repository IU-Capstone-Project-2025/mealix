from pydantic_settings import BaseSettings #type: ignore
from pydantic import Field #type: ignore


from pathlib import Path

class Settings(BaseSettings):
    yandex_api_key: str = Field(..., env="YANDEX_API_KEY")
    yandex_folder_id: str = Field(..., env="YANDEX_FOLDER_ID")

    data_dir: Path = Path(__file__).resolve().parent.parent.parent / "datasets"
    rag_dir: Path = Path(__file__).resolve().parent.parent.parent / "rag_data"

    class Config:
        env_file = ".env"

settings = Settings()