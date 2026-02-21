from pathlib import Path
from typing import List, Dict, Any

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from backend.config import get_settings
from backend.services.embeddings import get_embeddings


def _vector_store(collection_name: str) -> Chroma:
    settings = get_settings()
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(settings.chroma_persist_dir),
    )


def add_documents(
    collection_name: str,
    texts: List[str],
    metadatas: List[Dict[str, Any]],
) -> List[str]:
    vs = _vector_store(collection_name)
    docs = [Document(page_content=t, metadata=m) for t, m in zip(texts, metadatas)]
    ids = vs.add_documents(docs)
    vs.persist()
    return ids


def as_retriever(collection_name: str):
    vs = _vector_store(collection_name)
    return vs.as_retriever()

