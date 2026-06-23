from functools import lru_cache

from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import CrossEncoder, SentenceTransformer

from app.utils.config import get_settings


QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    settings = get_settings()
    return SentenceTransformer(settings.embedding_model_name)


@lru_cache
def get_reranker_model() -> CrossEncoder:
    settings = get_settings()
    return CrossEncoder(settings.reranker_model_name)


def embed_documents(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()


def embed_queries(texts: list[str]) -> list[list[float]]:
    prefixed = [QUERY_PREFIX + text for text in texts]
    return embed_documents(prefixed)


class BGEEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        return embed_documents(list(input))


def rerank(query: str, documents: list[str]) -> list[float]:
    if not documents:
        return []
    model = get_reranker_model()
    pairs = [(query, document) for document in documents]
    scores = model.predict(pairs, show_progress_bar=False)
    return [float(score) for score in scores]
