from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings
from app.services.mountain_db import mountain_db
from app.services.quiz_service import quiz_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    mountain_db.load()
    quiz_service.start_cleanup_task()
    yield
    quiz_service.stop_cleanup_task()


app = FastAPI(
    title=settings.app_name,
    description="Prove you're a real hiker. Get a discount.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok", "mountains_loaded": mountain_db.count()}
