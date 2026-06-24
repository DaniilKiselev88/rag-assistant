from fastapi import APIRouter

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}