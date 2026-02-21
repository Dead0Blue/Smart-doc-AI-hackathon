from typing import List, Dict, Any

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pages(
    pages: List[Dict[str, Any]],
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> List[Dict[str, Any]]:
    """Split pages into chunks while preserving page metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks: List[Dict[str, Any]] = []

    for page in pages:
        page_text = page.get("text", "")
        if not page_text.strip():
            continue
        texts = splitter.split_text(page_text)
        for i, text in enumerate(texts):
            chunks.append(
                {
                    "text": text,
                    "metadata": {
                        "page": page["page"],
                        "chunk_index": i,
                    },
                }
            )

    return chunks

