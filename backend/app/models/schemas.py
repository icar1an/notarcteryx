from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# --- Quiz ---


class QuizStartRequest(BaseModel):
    product_id: str


class QuizStartResponse(BaseModel):
    session_id: str
    product_id: str
    question: str = "Name 5 mountains you've hiked recently."
    num_answers_required: int = 5
    started_at: datetime
    expires_at: datetime


class AnswerItem(BaseModel):
    mountain_name: str = Field(min_length=1, max_length=200)
    answered_at: datetime
    # Frontend-reported input signals (optional — server detects cheating
    # even without these, but they make detection sharper)
    keystroke_count: int | None = None  # how many keystrokes to produce the text
    paste_detected: bool | None = None  # browser fired a paste event
    focus_lost_ms: int | None = None    # total ms the input was blurred (tabbed away)


class QuizSubmitRequest(BaseModel):
    answers: list[AnswerItem] = Field(min_length=5, max_length=5)
    # How many times the user tabbed away from the quiz page entirely
    tab_away_count: int | None = None


class ScoreBreakdownResponse(BaseModel):
    mountain_validity: float
    timing_naturalness: float
    geographic_coherence: float
    obscurity_mix: float
    spelling_authenticity: float
    input_authenticity: float


class QuizSubmitResponse(BaseModel):
    session_id: str
    truthfulness_score: float
    score_breakdown: ScoreBreakdownResponse
    final_price: float
    base_price: float
    surcharge_pct: int
    message: str


# --- Products ---


class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    base_price: float
    description: str
    colors: list[str]
    image_url: str


class ProductListResponse(BaseModel):
    products: list[ProductResponse]


# --- Pricing ---


class PricingResponse(BaseModel):
    session_id: str
    final_price: float
    base_price: float
    surcharge_pct: int
    truthfulness_score: float
    message: str
