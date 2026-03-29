"""
Bayesian inference engine for hiker truthfulness scoring.

Computes P(hiker | evidence) using naive Bayes with 6 evidence signals,
each modeled as a Beta distribution likelihood.
"""

from __future__ import annotations

import math
from datetime import datetime
from itertools import combinations

import numpy as np
from scipy.stats import beta as beta_dist
from scipy.stats import lognorm

from app.config import settings
from app.models.domain import Answer, MatchedMountain, ScoreBreakdown, ScoringResult
from app.services.mountain_db import MountainDB


# Beta distribution parameters: (alpha_hiker, beta_hiker, alpha_non, beta_non)
LIKELIHOOD_PARAMS = {
    "mountain_validity": (8, 2, 3, 4),
    "timing_naturalness": (6, 2, 2, 3),
    "geographic_coherence": (5, 2, 2, 4),
    "obscurity_mix": (4, 2, 2, 5),
    "spelling_authenticity": (5, 2, 2, 3),
    # input_authenticity is NOT in the Bayesian model — it acts as a hard cap
    # on the posterior instead, because copy-paste evidence should not be
    # outvotable by other signals
}


def _timing_score_single(seconds: float) -> float:
    """Score a single answer's response time.

    Log-normal distribution centered around 5 seconds.
    Real hikers recall from memory in ~3-8s.
    Too fast (<1s) = copy-paste, too slow (>20s) = googling.
    """
    if seconds <= 0:
        return 0.01
    peak = lognorm.pdf(5.0, s=0.6, scale=5.0)
    if peak == 0:
        return 0.5
    return float(np.clip(lognorm.pdf(seconds, s=0.6, scale=5.0) / peak, 0.01, 1.0))


def _geo_coherence(avg_distance_km: float) -> float:
    """Convert average pairwise distance to a coherence score.

    0-500km = very coherent (same region)
    500-2000km = moderate
    2000km+ = low (scattered worldwide)
    """
    return 1.0 / (1.0 + math.exp((avg_distance_km - 800) / 300))


def _obscurity_score(popularity_ranks: list[int]) -> float:
    """Score the mix of famous vs obscure mountains.

    All top-10 famous = suspicious (score ~0.4)
    Mix of well-known and obscure = authentic (score ~0.8-0.9)
    All extremely obscure = unusual but possible (score ~0.6)
    """
    if not popularity_ranks:
        return 0.1

    ranks = np.array(popularity_ranks, dtype=float)
    mean_rank = float(np.mean(ranks))
    std_rank = float(np.std(ranks))

    # Ideal mean rank around 120-300 (knows some popular + some regional)
    peak = lognorm.pdf(200, s=0.8, scale=200)
    mean_score = float(lognorm.pdf(mean_rank, s=0.8, scale=200) / peak) if peak > 0 else 0.5

    # Variety bonus: std > 80 means a healthy mix
    variety_score = min(1.0, std_rank / 120)

    return float(np.clip(0.6 * mean_score + 0.4 * variety_score, 0.01, 0.99))


def _spelling_score(exact_matches: int, fuzzy_matches: int, total: int) -> float:
    """Score spelling patterns.

    All exact = slightly suspicious (copy-paste from a list)
    Mostly exact + a couple fuzzy = authentic (knows them but types casually)
    Mostly fuzzy = less certain
    No matches = not a hiker
    """
    if total == 0:
        return 0.1

    matched = exact_matches + fuzzy_matches
    if matched == 0:
        return 0.1

    exact_ratio = exact_matches / total

    # Perfect 5/5 exact is slightly suspicious
    if exact_ratio == 1.0 and total >= 5:
        return 0.75
    elif exact_ratio >= 0.6:
        return 0.90
    elif exact_ratio >= 0.3:
        return 0.70
    else:
        # Mostly fuzzy matches — could be sloppy typing or half-knowledge
        return 0.40 + 0.2 * (matched / total)


class BayesianScorer:
    def __init__(self, mountain_db: MountainDB) -> None:
        self.mountain_db = mountain_db

    def score(
        self,
        answers: list[Answer],
        session_started_at: datetime,
        tab_away_count: int | None = None,
    ) -> tuple[ScoringResult, list[MatchedMountain]]:
        """Score a set of quiz answers and return truthfulness assessment."""

        # Step 1: Match each answer against the mountain database
        matches = [self.mountain_db.lookup(a.mountain_name) for a in answers]

        # Step 2: Extract evidence signals
        validity = self._compute_validity(matches)
        timing = self._compute_timing(answers, session_started_at)
        geo = self._compute_geographic_coherence(matches)
        obscurity = self._compute_obscurity(matches)
        spelling = self._compute_spelling(matches)
        input_auth = self._compute_input_authenticity(answers, session_started_at, tab_away_count)

        breakdown = ScoreBreakdown(
            mountain_validity=round(validity, 4),
            timing_naturalness=round(timing, 4),
            geographic_coherence=round(geo, 4),
            obscurity_mix=round(obscurity, 4),
            spelling_authenticity=round(spelling, 4),
            input_authenticity=round(input_auth, 4),
        )

        # Step 3: Bayesian posterior (content signals only — did they name real mountains?)
        evidence = {
            "mountain_validity": validity,
            "timing_naturalness": timing,
            "geographic_coherence": geo,
            "obscurity_mix": obscurity,
            "spelling_authenticity": spelling,
        }
        truthfulness = self._compute_posterior(evidence)

        # Step 4: Input authenticity acts as a hard cap — copy-paste evidence
        # can't be outvoted by good content. Knowing the right mountains
        # doesn't matter if you clearly googled them.
        if input_auth < 0.15:
            # Definitive cheating detected — cap score to near zero
            truthfulness = min(truthfulness, input_auth)
        elif input_auth < 0.40:
            # Suspicious input — cap score proportionally
            truthfulness = min(truthfulness, input_auth * 0.5)

        result = ScoringResult(
            truthfulness_score=round(truthfulness, 4),
            breakdown=breakdown,
        )

        return result, matches

    def _compute_validity(self, matches: list[MatchedMountain]) -> float:
        """Fraction of answers that matched a real mountain."""
        if not matches:
            return 0.01
        matched_count = sum(1 for m in matches if m.matched)
        return max(0.01, min(0.99, matched_count / len(matches)))

    def _compute_timing(
        self, answers: list[Answer], session_started_at: datetime
    ) -> float:
        """Score response timing pattern."""
        if not answers:
            return 0.01

        deltas = []
        prev = session_started_at
        for ans in answers:
            delta = (ans.answered_at - prev).total_seconds()
            # Server-side sanity: if timestamps are nonsensical, penalize
            if delta < 0:
                return 0.01
            deltas.append(delta)
            prev = ans.answered_at

        per_answer = [_timing_score_single(d) for d in deltas]

        # Geometric mean (more sensitive to outliers than arithmetic mean)
        log_scores = [math.log(max(s, 1e-10)) for s in per_answer]
        geo_mean = math.exp(sum(log_scores) / len(log_scores))

        return max(0.01, min(0.99, geo_mean))

    def _compute_geographic_coherence(
        self, matches: list[MatchedMountain]
    ) -> float:
        """Score how geographically clustered the matched mountains are."""
        matched_mountains = [m.mountain for m in matches if m.matched and m.mountain]

        if len(matched_mountains) < 2:
            # Can't compute pairwise distance with 0-1 mountains
            # Give a neutral score
            return 0.5

        # Compute all pairwise distances
        distances = []
        for m1, m2 in combinations(matched_mountains, 2):
            d = self.mountain_db.haversine_km(
                m1.latitude, m1.longitude, m2.latitude, m2.longitude
            )
            distances.append(d)

        avg_distance = sum(distances) / len(distances)
        score = _geo_coherence(avg_distance)

        return max(0.01, min(0.99, score))

    def _compute_obscurity(self, matches: list[MatchedMountain]) -> float:
        """Score the popularity mix of matched mountains."""
        ranks = [
            m.mountain.popularity_rank
            for m in matches
            if m.matched and m.mountain
        ]
        if not ranks:
            return 0.01

        return _obscurity_score(ranks)

    def _compute_spelling(self, matches: list[MatchedMountain]) -> float:
        """Score the spelling pattern (exact vs fuzzy vs unmatched)."""
        total = len(matches)
        if total == 0:
            return 0.01

        exact = sum(1 for m in matches if m.exact_match)
        fuzzy = sum(1 for m in matches if m.matched and not m.exact_match)

        return _spelling_score(exact, fuzzy, total)

    def _compute_input_authenticity(
        self,
        answers: list[Answer],
        session_started_at: datetime,
        tab_away_count: int | None = None,
    ) -> float:
        """Detect copy-paste, tab-switching, and robotic input patterns.

        Two layers:
        1. Frontend-reported signals (paste events, keystroke counts, focus loss)
        2. Server-side heuristics (timing regularity, bulk submission, suspiciously
           low character-to-time ratios) that work even without frontend cooperation
        """
        penalties: list[float] = []

        # === FRONTEND-REPORTED SIGNALS ===

        # Direct paste detection: if the browser reported a paste event, instant flag
        paste_count = sum(1 for a in answers if a.paste_detected is True)
        if paste_count > 0:
            # Each paste kills the score. 1 paste = 0.15, 2+ = 0.01
            penalties.append(max(0.01, 0.30 - paste_count * 0.15))

        # Keystroke count vs text length: typing "Mount Rainier" = ~14 keystrokes
        # (plus corrections). Pasting = 0-2 keystrokes (Ctrl+V).
        keystroke_ratios = []
        for a in answers:
            if a.keystroke_count is not None:
                text_len = len(a.mountain_name)
                if text_len > 0:
                    ratio = a.keystroke_count / text_len
                    keystroke_ratios.append(ratio)

        if keystroke_ratios:
            avg_ratio = sum(keystroke_ratios) / len(keystroke_ratios)
            # Real typing: ratio ~1.0-1.5 (some backspaces/corrections)
            # Paste: ratio ~0.0-0.2 (Ctrl+V = 2 keystrokes for any length)
            if avg_ratio < 0.3:
                penalties.append(0.01)  # almost certainly pasted
            elif avg_ratio < 0.5:
                penalties.append(0.15)  # probably pasted
            elif avg_ratio < 0.8:
                penalties.append(0.50)  # suspicious
            # ratio >= 0.8 = no penalty from this signal

        # Tab-away detection: leaving the page to look things up
        if tab_away_count is not None:
            if tab_away_count >= 3:
                penalties.append(0.05)   # heavily googling
            elif tab_away_count >= 1:
                penalties.append(0.30)   # at least one tab-away

        # Focus loss per input: time spent with the input blurred
        focus_losses = [a.focus_lost_ms for a in answers if a.focus_lost_ms is not None]
        if focus_losses:
            total_focus_lost_s = sum(focus_losses) / 1000.0
            if total_focus_lost_s > 30:
                penalties.append(0.10)  # 30+ seconds away from inputs
            elif total_focus_lost_s > 10:
                penalties.append(0.40)

        # === SERVER-SIDE HEURISTICS (no frontend cooperation needed) ===

        # Heuristic 1: Timing regularity — real typing has variable cadence,
        # copy-paste has suspiciously uniform intervals
        deltas = []
        prev = session_started_at
        for ans in answers:
            delta = (ans.answered_at - prev).total_seconds()
            if delta > 0:
                deltas.append(delta)
            prev = ans.answered_at

        if len(deltas) >= 3:
            mean_delta = sum(deltas) / len(deltas)
            if mean_delta > 0:
                # Coefficient of variation: std/mean
                # Real typing: CV ~0.3-0.8 (variable pace)
                # Robotic/scripted: CV < 0.1 (suspiciously uniform)
                variance = sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)
                cv = math.sqrt(variance) / mean_delta
                if cv < 0.08:
                    penalties.append(0.05)   # robotic precision
                elif cv < 0.15:
                    penalties.append(0.25)   # very uniform

        # Heuristic 2: Bulk submission — all 5 answers within 3 seconds total
        if deltas:
            total_time = sum(deltas)
            if total_time < 3.0:
                penalties.append(0.01)  # bulk paste, instant kill
            elif total_time < 6.0:
                penalties.append(0.10)

        # Heuristic 3: Character-per-second rate — typing speed ceiling
        # Average human types ~5-7 chars/sec. Anything above ~15 is paste.
        for i, ans in enumerate(answers):
            if i < len(deltas) and deltas[i] > 0:
                chars = len(ans.mountain_name)
                cps = chars / deltas[i]
                if cps > 30:
                    penalties.append(0.05)  # instant text appearance
                    break  # one is enough to flag
                elif cps > 15:
                    penalties.append(0.20)
                    break

        # === COMBINE ===
        if not penalties:
            # No signals fired — either no frontend metadata or clean input
            # Give benefit of the doubt but not full score (absence of evidence
            # isn't evidence of absence when frontend signals are missing)
            has_any_frontend_data = any(
                a.keystroke_count is not None
                or a.paste_detected is not None
                or a.focus_lost_ms is not None
                for a in answers
            )
            return 0.90 if has_any_frontend_data else 0.60

        # Take the harshest penalty — one smoking gun is enough
        return max(0.01, min(penalties))

    def _compute_posterior(self, evidence: dict[str, float]) -> float:
        """Compute P(hiker | evidence) via naive Bayes."""
        prior_hiker = settings.prior_hiker
        prior_non = 1.0 - prior_hiker

        log_likelihood_hiker = 0.0
        log_likelihood_non = 0.0

        for signal_name, value in evidence.items():
            params = LIKELIHOOD_PARAMS[signal_name]
            a_h, b_h, a_n, b_n = params

            # Clamp to (0.001, 0.999) to avoid Beta PDF edge issues
            v = max(0.001, min(0.999, value))

            pdf_h = beta_dist.pdf(v, a_h, b_h)
            pdf_n = beta_dist.pdf(v, a_n, b_n)

            # Use log-space to avoid underflow
            log_likelihood_hiker += math.log(max(pdf_h, 1e-30))
            log_likelihood_non += math.log(max(pdf_n, 1e-30))

        # Log-sum-exp for numerical stability
        log_numerator = math.log(prior_hiker) + log_likelihood_hiker
        log_denominator_terms = [
            math.log(prior_hiker) + log_likelihood_hiker,
            math.log(prior_non) + log_likelihood_non,
        ]
        max_log = max(log_denominator_terms)
        log_denominator = max_log + math.log(
            sum(math.exp(t - max_log) for t in log_denominator_terms)
        )

        posterior = math.exp(log_numerator - log_denominator)

        return max(0.0, min(1.0, posterior))
