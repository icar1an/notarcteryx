from fastapi import APIRouter

from app.api.products import router as products_router
from app.api.quiz import router as quiz_router
from app.api.pricing import router as pricing_router

api_router = APIRouter()
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
api_router.include_router(pricing_router, prefix="/pricing", tags=["pricing"])
