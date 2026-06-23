import hashlib
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.config import get_settings
from app.rag.vector_store import get_policy_collection, reset_vector_store


def load_policy_documents(policy_dir: Path | None = None) -> list[dict]:
    directory = policy_dir or get_settings().policy_dir
    documents: list[dict] = []
    for path in sorted(directory.glob("*.txt")):
        content = path.read_text(encoding="utf-8").strip()
        if content:
            documents.append(
                {
                    "source": path.name,
                    "path": str(path),
                    "document_type": infer_document_type(path.name),
                    "text": content,
                }
            )
    return documents


def infer_document_type(filename: str) -> str:
    if filename.startswith("faq_"):
        return "faq"
    if filename.startswith("product_manual_"):
        return "product_manual"
    if "policy" in filename or "shipping" in filename:
        return "policy"
    return "knowledge_base"


def build_text_splitter() -> RecursiveCharacterTextSplitter:
    settings = get_settings()
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.rag_chunk_size,
        chunk_overlap=settings.rag_chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def chunk_documents(documents: list[dict]) -> list[dict]:
    splitter = build_text_splitter()
    chunks: list[dict] = []
    for document in documents:
        split_texts = splitter.split_text(document["text"])
        total_chunks = len(split_texts)
        for index, text in enumerate(split_texts):
            chunk_id = stable_chunk_id(document["source"], index, text)
            chunks.append(
                {
                    "id": chunk_id,
                    "text": text,
                    "metadata": {
                        "source": document["source"],
                        "path": document["path"],
                        "document_type": document["document_type"],
                        "chunk_index": index,
                        "chunk_count": total_chunks,
                        "char_count": len(text),
                    },
                }
            )
    return chunks


def stable_chunk_id(source: str, index: int, text: str) -> str:
    digest = hashlib.sha1(f"{source}:{index}:{text}".encode("utf-8")).hexdigest()[:16]
    return f"{Path(source).stem}-{index}-{digest}"


def ingest_policies(reset: bool = True) -> dict:
    if reset:
        reset_vector_store()

    documents = load_policy_documents()
    chunks = chunk_documents(documents)
    collection = get_policy_collection()

    if chunks:
        collection.upsert(
            ids=[chunk["id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[chunk["metadata"] for chunk in chunks],
        )

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "collection_count": collection.count(),
    }


if __name__ == "__main__":
    result = ingest_policies(reset=True)
    print(
        "Ingested {documents} documents into {chunks} chunks. "
        "Chroma collection now has {collection_count} records.".format(**result)
    )
