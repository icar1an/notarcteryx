from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Mountain:
    name: str
    aliases: list[str]
    latitude: float
    longitude: float
    elevation_m: int
    region: str
    country: str
    state_province: str
    popularity_rank: int


@dataclass
class Answer:
    mountain_name: str
    answered_at: datetime
    keystroke_count: int | None = None
    paste_detected: bool | None = None
    focus_lost_ms: int | None = None


@dataclass
class MatchedMountain:
    """Result of fuzzy-matching a user answer against the mountain database."""
    answer_text: str
    matched: bool
    mountain: Mountain | None = None
    match_score: float = 0.0  # rapidfuzz similarity (0-100)
    exact_match: bool = False


@dataclass
class ScoreBreakdown:
    mountain_validity: float
    timing_naturalness: float
    geographic_coherence: float
    obscurity_mix: float
    spelling_authenticity: float
    input_authenticity: float


@dataclass
class ScoringResult:
    truthfulness_score: float
    breakdown: ScoreBreakdown


@dataclass
class QuizSession:
    session_id: str
    product_id: str
    started_at: datetime
    expires_at: datetime
    answers: list[Answer] | None = None
    result: ScoringResult | None = None
    final_price: float | None = None


@dataclass
class Product:
    id: str
    name: str
    category: str
    base_price: float
    description: str
    colors: list[str] = field(default_factory=list)
    image_url: str = ""
