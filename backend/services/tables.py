import json
from typing import Any, Dict, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from backend.config import get_settings
from backend.services.vector_store import as_retriever


def _table_llm():
    settings = get_settings()
    if settings.openai_api_key:
        return ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key, temperature=0.1)
    if settings.google_api_key:
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.google_api_key,
            temperature=0.1,
        )
    raise RuntimeError("No LLM provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY.")


def answer_table_query(collection_name: str, question: str) -> List[Dict[str, Any]]:
    """Return a JSON-table representation based on retrieved context."""
    retriever = as_retriever(collection_name)
    docs = retriever.invoke(question)
    context_snippets = "\n\n".join(d.page_content for d in docs)

    system_prompt = """
You are an assistant that extracts structured tables from financial and regulatory documents.

Given the question and the context, respond ONLY with a JSON array of rows.
Each row must be a JSON object with simple string or number values.
Do not include any explanatory text outside the JSON.
"""

    llm = _table_llm()
    msg = f"{system_prompt}\n\nQuestion:\n{question}\n\nContext:\n{context_snippets}\n\nJSON table:"
    result = llm.invoke(msg)
    content = result.content if isinstance(result.content, str) else str(result.content)
    try:
        parsed = json.loads(content)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        return []
    return []

