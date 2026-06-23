from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Shopify Customer Support Intelligence"
    environment: str = "development"
    log_level: str = "INFO"
    data_dir: Path = Path("data")
    policy_dir: Path = Path("data/policies")
    orders_path: Path = Path("data/orders/orders.json")
    tickets_dir: Path = Path("data/tickets")
    chroma_dir: Path = Path("data/embeddings/chroma")
    chroma_collection: str = "shopify_support_policies"
    embedding_model_name: str = "BAAI/bge-small-en-v1.5"
    reranker_model_name: str = "BAAI/bge-reranker-base"
    rag_chunk_size: int = 700
    rag_chunk_overlap: int = 120
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    google_api_key: str | None = None
    shopify_store_url: str | None = None
    shopify_access_token: str | None = None
    auto_reply_confidence_threshold: float = 0.72

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
