from pathlib import Path
from typing import List, Dict, Any

import fitz  # pymupdf


def extract_pdf_text_with_pages(path: Path) -> List[Dict[str, Any]]:
    """Extract text per page using PyMuPDF."""
    doc = fitz.open(path)
    pages: List[Dict[str, Any]] = []
    try:
        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            text = page.get_text("text")
            pages.append(
                {
                    "page": page_index + 1,
                    "text": text,
                }
            )
    finally:
        doc.close()
    return pages

