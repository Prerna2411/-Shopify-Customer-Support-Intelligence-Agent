from app.rag.embeddings import embed_queries, rerank
from app.rag.ingest import ingest_policies
from app.rag.vector_store import get_policy_collection


def ensure_vector_store_ready() -> None:
    collection = get_policy_collection()
    if collection.count() == 0:
        ingest_policies(reset=False)


def retrieve_policies(query: str, k: int = 4, fetch_k: int = 12, use_reranker: bool = True) -> list[dict]:
    ensure_vector_store_ready()
    collection = get_policy_collection()
    query_embedding = embed_queries([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=fetch_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    candidates = []
    for chunk_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
        candidates.append(
            {
                "id": chunk_id,
                "source": metadata.get("source"),
                "content": content,
                "metadata": metadata,
                "distance": round(float(distance), 4),
                "score": round(1 / (1 + float(distance)), 4),
            }
        )

    if use_reranker and candidates:
        scores = rerank(query, [candidate["content"] for candidate in candidates])
        for candidate, score in zip(candidates, scores):
            candidate["rerank_score"] = round(score, 4)
        candidates.sort(key=lambda item: item["rerank_score"], reverse=True)
    else:
        candidates.sort(key=lambda item: item["score"], reverse=True)

    return candidates[:k]
