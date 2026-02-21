from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from backend.config import get_settings
from backend.services.vector_store import as_retriever


def _llm():
    """
    Prefer OpenAI chat model if OPENAI_API_KEY is set.
    Fallback to Gemini if GOOGLE_API_KEY is set.
    """
    settings = get_settings()
    if settings.openai_api_key:
        return ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key, temperature=0.2)
    if settings.google_api_key:
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.google_api_key,
            temperature=0.2,
        )
    raise RuntimeError("No LLM provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY.")


_PROMPT_TEMPLATE = """
You are SmartDoc AI, an assistant specialized in financial and regulatory PDF reports.

Use the following context to answer the question. Cite the most relevant passages.

Context:
{context}

Question: {question}

Answer in clear paragraphs.
"""


def ask_question(collection_name: str, question: str):
    """Simple RAG: retrieve context, format prompt, call LLM, return answer + sources."""
    retriever = as_retriever(collection_name)
    source_docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in source_docs)
    prompt = _PROMPT_TEMPLATE.format(context=context, question=question)

    llm = _llm()
    result = llm.invoke(prompt)
    answer = result.content if isinstance(result.content, str) else str(result.content)

    return {"result": answer, "source_documents": source_docs}

