from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    id: str
    name: str
    pages: int


class UploadResponse(BaseModel):
    document: DocumentInfo


class Citation(BaseModel):
    page: int
    text: str
    source: str
    chunk_id: Optional[str] = None


class QueryRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]


class TableQueryRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None


class TableQueryResponse(BaseModel):
    rows: List[Dict[str, Any]]

