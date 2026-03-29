"""Maps truthfulness scores to dynamic pricing.

Real hikers pay base price. Performative posers pay more.
"""

from __future__ import annotations

import math

from app.config import settings


FLAVOR_TEXT = [
    (0.8, "You actually hike."),
    (0.5, "Almost eliteball trail knowledge."),
    (0.2, "Do you really hike"),
    (0.0, "You don't hike lmao"),
]


def calculate_price(
    base_price: float, truthfulness_score: float
) -> dict:
    """Map truthfulness score [0, 1] to a surcharge for posers.

    Real hikers (score ~0.8+) pay near base price.
    Posers (score ~0.0) pay up to 900% more.

    Uses an inverted sigmoid (midpoint 0.55, slope 8):
      score ~0.8 → ~2% surcharge
      score ~0.7 → ~10% surcharge
      score ~0.55 → 450% surcharge (inflection point)
      score ~0.0 → ~887% surcharge
    """
    max_surcharge = settings.max_surcharge_pct / 100.0

    # Inverted sigmoid: low score = high surcharge
    # Midpoint at 0.55 so real hikers (0.7+) stay near base price
    surcharge_fraction = max_surcharge / (
        1.0 + math.exp(8 * (truthfulness_score - 0.55))
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
