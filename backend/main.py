import sys
from pathlib import Path
from typing import List

# Ensure project root is on path when running from backend/
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.models.schemas import (
    UploadResponse,
    DocumentInfo,
    QueryRequest,
    QueryResponse,
    Citation,
    TableQueryRequest,
    TableQueryResponse,
)
from backend.services.extraction import extract_pdf_text_with_pages
from backend.services.chunking import chunk_pages
from backend.services.vector_store import add_documents
from backend.services.rag_engine import ask_question
from backend.services.tables import answer_table_query

app = FastAPI(title="SmartDoc AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()
app.mount("/static", StaticFiles(directory=settings.upload_dir), name="static")


@app.get("/")
async def root():
    return {"message": "Welcome to SmartDoc AI API"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    settings = get_settings()
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    dest: Path = settings.upload_dir / file.filename
    content = await file.read()
    dest.write_bytes(content)

    pages = extract_pdf_text_with_pages(dest)
    chunks_with_meta = chunk_pages(pages)

    texts: List[str] = [c["text"] for c in chunks_with_meta]
    metadatas = []
    for idx, c in enumerate(chunks_with_meta):
        meta = dict(c["metadata"])
        meta.update({"source": file.filename, "document_id": file.filename, "chunk_id": f"{file.filename}-{idx}"})
        metadatas.append(meta)

    add_documents(collection_name="smartdoc", texts=texts, metadatas=metadatas)

    document = DocumentInfo(id=file.filename, name=file.filename, pages=len(pages))
    return UploadResponse(document=document)


@app.post("/query", response_model=QueryResponse)
async def query_rag(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    result = ask_question(collection_name="smartdoc", question=payload.question)
    answer: str = result.get("result", "")
    source_docs = result.get("source_documents", []) or []

    citations: List[Citation] = []
    for doc in source_docs:
        meta = doc.metadata or {}
        citations.append(
            Citation(
                page=int(meta.get("page", 1)),
                text=doc.page_content[:300],
                source=str(meta.get("source", "")),
                chunk_id=meta.get("chunk_id"),
            )
        )

    return QueryResponse(answer=answer, citations=citations)


@app.websocket("/ws/query")
async def query_rag_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            question = (payload.get("question") or "").strip()
            if not question:
                await websocket.send_json({"error": "Question must not be empty."})
                continue
            result = ask_question(collection_name="smartdoc", question=question)
            answer: str = result.get("result", "")
            source_docs = result.get("source_documents", []) or []
            citations_payload = []
            for doc in source_docs:
                meta = doc.metadata or {}
                citations_payload.append(
                    {
                        "page": int(meta.get("page", 1)),
                        "text": doc.page_content[:300],
                        "source": str(meta.get("source", "")),
                        "chunk_id": meta.get("chunk_id"),
                    }
                )
            await websocket.send_json({"answer": answer, "citations": citations_payload})
    except WebSocketDisconnect:
        return


@app.post("/query/table", response_model=TableQueryResponse)
async def query_table(payload: TableQueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    rows = answer_table_query(collection_name="smartdoc", question=payload.question)
    return TableQueryResponse(rows=rows)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
