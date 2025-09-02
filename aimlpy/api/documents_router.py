from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED
from aimlpy.service.document_service import DocumentService
from aimlpy.repo.datasource import DataSource
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/document", tags=["Documents"])

@router.post("/post", status_code=HTTP_201_CREATED)
async def upload_document_api(
    title: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        service = DocumentService()
        document = await service.add_document(title, file)

        if document is None:
            raise HTTPException(
                status_code=409,
                detail="Plagiarism detected. Document not uploaded."
            )

        return {
            "message": "Document uploaded successfully.",
            "document": {
                "id": document.id,
                "title": document.title,
                "author": document.author,
                "filename": document.filename,
                "created_at": str(document.created_at),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list", response_class=JSONResponse)
async def list_documents(
    request: Request,
    author: str = Query(None),
    keyword: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    session: AsyncSession = Depends(DataSource.get_session_dependency),
):
    service = DocumentService()
    documents = await service.list_documents(author, keyword, date_from, date_to)
    serialized_docs = [
        {
            "id": doc.id,
            "title": doc.title,
            "author": doc.author,
            "keywords": doc.keywords,
            "summary": doc.summary,
            "created_at": str(doc.created_at),
            "filename": doc.filename,
        }
        for doc in documents
    ]

    return JSONResponse(content={"documents": serialized_docs})


@router.get("/search", response_class=JSONResponse)
def search_documents(
    query: str = Query("", description="Search term"),
    session: Session = Depends(DataSource.get_session_dependency),
):
    service = DocumentService(session=session)
    results = service.search_documents(query)

    serialized = [
        {
            "id": doc.id,
            "title": doc.title,
            "author": doc.author,
            "summary": doc.summary,
            "keywords": doc.keywords,
            "created_at": str(doc.created_at),
            "filename": doc.filename,
        }
        for doc in results
    ]

    return JSONResponse(content={
        "results": serialized,
        "query": query,
        "use_semantic": "hybrid"
    })