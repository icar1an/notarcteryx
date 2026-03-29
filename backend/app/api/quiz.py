from fastapi import APIRouter, HTTPException

from app.api.products import PRODUCTS
from app.models.domain import Answer
from app.models.schemas import (
    QuizStartRequest,
    QuizStartResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
    ScoreBreakdownResponse,
)
from app.services.bayesian_scorer import BayesianScorer
from app.services.mountain_db import mountain_db
from app.services.pricing_service import calculate_price
from app.services.quiz_service import quiz_service

router = APIRouter()


@router.post("/start", response_model=QuizStartResponse, status_code=201)
async def start_quiz(req: QuizStartRequest):
    if req.product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")

    session = quiz_service.create_session(req.product_id)

    return QuizStartResponse(
        session_id=session.session_id,
        product_id=session.product_id,
        started_at=session.started_at,
        expires_at=session.expires_at,
    )


@router.post("/{session_id}/submit", response_model=QuizSubmitResponse)
async def submit_quiz(session_id: str, req: QuizSubmitRequest):
    session = quiz_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Quiz session not found")

    if session.result is not None:
        raise HTTPException(
            status_code=409, detail="Quiz already submitted for this session"
        )

    if quiz_service.is_expired(session):
        raise HTTPException(
            status_code=410, detail="Quiz session expired. Start a new one."
        )

    # Convert schema answers to domain answers (including input metadata)
    answers = [
        Answer(
            mountain_name=a.mountain_name,
            answered_at=a.answered_at,
            keystroke_count=a.keystroke_count,
            paste_detected=a.paste_detected,
            focus_lost_ms=a.focus_lost_ms,
        )
        for a in req.answers
    ]

    quiz_service.submit_answers(session, answers)

    # Score with Bayesian inference
    scorer = BayesianScorer(mountain_db)
    result, _matches = scorer.score(answers, session.started_at, req.tab_away_count)

    # Calculate price
    product = PRODUCTS[session.product_id]
    pricing = calculate_price(product.base_price, result.truthfulness_score)

    quiz_service.save_result(session, result, pricing["final_price"])

    return QuizSubmitResponse(
        session_id=session.session_id,
        truthfulness_score=result.truthfulness_score,
        score_breakdown=ScoreBreakdownResponse(
            mountain_validity=result.breakdown.mountain_validity,
            timing_naturalness=result.breakdown.timing_naturalness,
            geographic_coherence=result.breakdown.geographic_coherence,
            obscurity_mix=result.breakdown.obscurity_mix,
            spelling_authenticity=result.breakdown.spelling_authenticity,
            input_authenticity=result.breakdown.input_authenticity,
        ),
        final_price=pricing["final_price"],
        base_price=pricing["base_price"],
        surcharge_pct=pricing["surcharge_pct"],
        message=pricing["message"],
    )
