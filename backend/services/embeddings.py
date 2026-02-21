from typing import List

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config import get_settings


def get_embeddings():
    """
    Prefer OpenAI embeddings if OPENAI_API_KEY is set.
    Fallback to Gemini embeddings if GOOGLE_API_KEY is set.
    """
    settings = get_settings()
    if settings.openai_api_key:
        return OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.openai_api_key)
    if settings.google_api_key:
        return GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=settings.google_api_key,
        )
    raise RuntimeError("No embedding provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY.")


def embed_texts(texts: List[str]) -> List[List[float]]:
    embeddings = get_embeddings()
    return embeddings.embed_documents(texts)

