from fastapi import APIRouter, HTTPException

from app.api.products import PRODUCTS
from app.models.schemas import PricingResponse
from app.services.pricing_service import FLAVOR_TEXT
from app.services.quiz_service import quiz_service

router = APIRouter()


@router.get("/{session_id}", response_model=PricingResponse)
async def get_pricing(session_id: str):
    session = quiz_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.result is None or session.final_price is None:
        raise HTTPException(
            status_code=404, detail="Quiz not yet completed for this session"
        )

    product = PRODUCTS.get(session.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    score = session.result.truthfulness_score
    message = FLAVOR_TEXT[-1][1]
    for threshold, text in FLAVOR_TEXT:
        if score >= threshold:
            message = text
            break

    return PricingResponse(
        session_id=session.session_id,
        final_price=session.final_price,
        base_price=product.base_price,
        surcharge_pct=round(
            (session.final_price / product.base_price - 1) * 100
        ),
        truthfulness_score=score,
        message=message,
    )
