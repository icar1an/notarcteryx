"""Mountain database with fuzzy matching for quiz answer validation."""

from __future__ import annotations

import json
import math
from pathlib import Path

from rapidfuzz import fuzz, process

from app.config import settings
from app.models.domain import MatchedMountain, Mountain


class MountainDB:
    def __init__(self) -> None:
        self._mountains: list[Mountain] = []
        self._name_index: dict[str, Mountain] = {}  # lowercase name/alias -> Mountain
        self._all_names: list[str] = []  # for rapidfuzz process.extractOne

    def load(self, path: Path | None = None) -> None:
        if path is None:
            path = Path(__file__).parent.parent / "data" / "mountains.json"

        with open(path) as f:
            raw = json.load(f)

        self._mountains = []
        self._name_index = {}
        self._all_names = []

        for entry in raw:
            m = Mountain(
                name=entry["name"],
                aliases=entry.get("aliases", []),
                latitude=entry["latitude"],
                longitude=entry["longitude"],
                elevation_m=entry["elevation_m"],
                region=entry["region"],
                country=entry["country"],
                state_province=entry.get("state_province", ""),
                popularity_rank=entry["popularity_rank"],
            )
            self._mountains.append(m)

            # Index by canonical name and all aliases (lowercased)
            for name in [m.name] + m.aliases:
                lower = name.lower().strip()
                self._name_index[lower] = m
                self._all_names.append(lower)

    def count(self) -> int:
        return len(self._mountains)

    def lookup(self, query: str) -> MatchedMountain:
        """Fuzzy-match a user-provided mountain name against the database."""
        query_clean = query.strip()
        query_lower = query_clean.lower()

        # 1. Exact match (case-insensitive)
        if query_lower in self._name_index:
            m = self._name_index[query_lower]
            return MatchedMountain(
                answer_text=query_clean,
                matched=True,
                mountain=m,
                match_score=100.0,
                exact_match=True,
            )

        # 2. Fuzzy match using rapidfuzz
        if not self._all_names:
            return MatchedMountain(answer_text=query_clean, matched=False)

        result = process.extractOne(
            query_lower,
            self._all_names,
            scorer=fuzz.WRatio,
            score_cutoff=settings.fuzzy_match_threshold,
        )

        if result is None:
            return MatchedMountain(answer_text=query_clean, matched=False)

        matched_name, score, _ = result
        m = self._name_index[matched_name]
        return MatchedMountain(
            answer_text=query_clean,
            matched=True,
            mountain=m,
            match_score=score,
            exact_match=False,
        )

    @staticmethod
    def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Great-circle distance between two points in kilometers."""
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# Singleton — loaded at app startup via lifespan
mountain_db = MountainDB()
