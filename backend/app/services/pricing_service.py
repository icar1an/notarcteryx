"""Maps truthfulness scores to dynamic pricing.

Real hikers pay base price. Performative posers pay more.
"""

from __future__ import annotations

import math

from app.config import settings


FLAVOR_TEXT = [
    (0.8, "You pass. Base price — respect."),
    (0.5, "Passable trail knowledge. Small markup."),
    (0.2, "You hesitated. That costs extra."),
    (0.0, "Performance tax applied. Maybe try actually going outside."),
]


def calculate_price(
    base_price: float, truthfulness_score: float
) -> dict:
    """Map truthfulness score [0, 1] to a surcharge for posers.

    Real hikers (score ~1.0) pay base price.
    Posers (score ~0.0) pay up to 40% more.

    Uses an inverted sigmoid:
      score ~1.0 → 0% surcharge (you're legit)
      score ~0.5 → ~20% surcharge
      score ~0.0 → ~40% surcharge
    """
    max_surcharge = settings.max_surcharge_pct / 100.0

    # Inverted sigmoid: low score = high surcharge
    # Midpoint at 0.35 so real hikers (0.6+) stay near base price
    surcharge_fraction = max_surcharge / (
        1.0 + math.exp(12 * (truthfulness_score - 0.35))
    )

    surcharge_pct = round(surcharge_fraction * 100)
    final_price = round(base_price * (1 + surcharge_fraction), 2)

    # Select flavor text
    message = FLAVOR_TEXT[-1][1]
    for threshold, text in FLAVOR_TEXT:
        if truthfulness_score >= threshold:
            message = text
            break

    return {
        "base_price": base_price,
        "final_price": final_price,
        "surcharge_pct": surcharge_pct,
        "message": message,
    }
