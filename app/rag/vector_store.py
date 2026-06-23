import shutil
from pathlib import Path

import chromadb

from app.rag.embeddings import BGEEmbeddingFunction
from app.utils.config import get_settings


def get_chroma_client(persist_dir: Path | None = None) -> chromadb.PersistentClient:
    settings = get_settings()
    directory = persist_dir or settings.chroma_dir
    directory.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(directory))


def get_policy_collection():
    settings = get_settings()
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=settings.chroma_collection,
        embedding_function=BGEEmbeddingFunction(),
        metadata={"description": "Shopify customer support policy and manual chunks"},
    )


def reset_vector_store() -> None:
    settings = get_settings()
    if settings.chroma_dir.exists():
        shutil.rmtree(settings.chroma_dir)


def collection_count() -> int:
    return get_policy_collection().count()
