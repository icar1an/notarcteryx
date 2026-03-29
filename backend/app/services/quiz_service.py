"""Quiz session lifecycle management."""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.models.domain import Answer, QuizSession, ScoringResult


class QuizService:
    def __init__(self) -> None:
        self._sessions: dict[str, QuizSession] = {}
        self._cleanup_task: asyncio.Task | None = None

    def create_session(self, product_id: str) -> QuizSession:
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        session = QuizSession(
            session_id=session_id,
            product_id=product_id,
            started_at=now,
            expires_at=now + timedelta(seconds=settings.quiz_duration_seconds),
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> QuizSession | None:
        return self._sessions.get(session_id)

    def is_expired(self, session: QuizSession) -> bool:
        return datetime.now(timezone.utc) > session.expires_at

    def submit_answers(
        self, session: QuizSession, answers: list[Answer]
    ) -> None:
        session.answers = answers

    def save_result(
        self, session: QuizSession, result: ScoringResult, final_price: float
    ) -> None:
        session.result = result
        session.final_price = final_price

    def start_cleanup_task(self) -> None:
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    def stop_cleanup_task(self) -> None:
        if self._cleanup_task:
            self._cleanup_task.cancel()

    async def _cleanup_loop(self) -> None:
        while True:
            await asyncio.sleep(settings.session_cleanup_interval_seconds)
            now = datetime.now(timezone.utc)
            # Remove sessions that expired more than 10 minutes ago
            cutoff = now - timedelta(minutes=10)
            expired = [
                sid
                for sid, s in self._sessions.items()
                if s.expires_at < cutoff
            ]
            for sid in expired:
                del self._sessions[sid]


quiz_service = QuizService()
