from fastapi import FastAPI
from routers.rag_router import router

app = FastAPI(title="RAG API")

app.include_router(router)