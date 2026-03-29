from datetime import datetime, timedelta, timezone

from app.models.domain import Answer
from app.services.bayesian_scorer import BayesianScorer
from app.services.mountain_db import mountain_db


def _make_answers(
    names: list[str],
    start: datetime,
    interval_seconds: float = 5.0,
    uniform: bool = False,
) -> list[Answer]:
    """Helper: create answers with timestamps.

    By default adds deterministic jitter to simulate natural human cadence.
    Set uniform=True for robotic/scripted timing tests.
    """
    # Deterministic per-answer jitter to simulate natural typing variance
    jitter = [0.0, 0.0, 0.0, 0.0, 0.0] if uniform else [-0.8, 1.2, -0.3, 0.9, -0.5]
    answers = []
    t = start + timedelta(seconds=interval_seconds)
    for i, name in enumerate(names):
        offset = 0.0 if uniform else jitter[i % len(jitter)]
        answers.append(Answer(mountain_name=name, answered_at=t + timedelta(seconds=offset)))
        t += timedelta(seconds=interval_seconds)
    return answers


def test_authentic_pnw_hiker():
    """A real PNW hiker naming regional peaks with natural timing."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    answers = _make_answers(
        ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"],
        start,
        interval_seconds=5.0,
    )
    result, matches = scorer.score(answers, start)

    assert result.truthfulness_score > 0.6
    assert result.breakdown.mountain_validity > 0.8
    assert result.breakdown.geographic_coherence > 0.5
    assert all(m.matched for m in matches)


def test_obvious_faker():
    """Someone who names gibberish — all signals should be low."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    answers = _make_answers(
        ["Xylophone", "Banana Sundae", "My Backyard", "Couch Potato", "Fluffy Clouds"],
        start,
        interval_seconds=25.0,  # slow = googling
    )
    result, matches = scorer.score(answers, start)

    assert result.truthfulness_score < 0.4
    # Most shouldn't match
    matched_count = sum(1 for m in matches if m.matched)
    assert matched_count <= 2


def test_famous_only_picker():
    """Someone who only names the most famous peaks globally — suspicious mix."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    answers = _make_answers(
        ["Mount Everest", "K2", "Mont Blanc", "Kilimanjaro", "Mount Fuji"],
        start,
        interval_seconds=4.0,
    )
    result, matches = scorer.score(answers, start)

    # All should match, but geographic coherence should be low (scattered worldwide)
    assert result.breakdown.mountain_validity > 0.8
    assert result.breakdown.geographic_coherence < 0.3
    # Overall score should be low — naming only the world's most famous peaks
    # from different continents screams "I googled famous mountains"
    assert result.truthfulness_score < 0.5


def test_copy_paste_speed():
    """Answers submitted impossibly fast — suspicious timing."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    answers = _make_answers(
        ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"],
        start,
        interval_seconds=0.5,  # half a second per answer = copy-paste
        uniform=True,
    )
    result, _ = scorer.score(answers, start)

    assert result.breakdown.timing_naturalness < 0.5


# --- Copy-paste / cheating detection tests ---


def test_paste_event_detected():
    """Frontend reports paste events — should tank input_authenticity."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    names = ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"]
    t = start + timedelta(seconds=5)
    answers = []
    for name in names:
        answers.append(Answer(
            mountain_name=name,
            answered_at=t,
            paste_detected=True,
            keystroke_count=2,  # just Ctrl+V
        ))
        t += timedelta(seconds=5)

    result, _ = scorer.score(answers, start)

    assert result.breakdown.input_authenticity < 0.1
    # Even with correct mountains, pasting should destroy the overall score
    assert result.truthfulness_score < 0.3


def test_low_keystroke_ratio():
    """Keystroke count far below text length = pasted text."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    names = ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"]
    t = start + timedelta(seconds=5)
    answers = []
    for name in names:
        answers.append(Answer(
            mountain_name=name,
            answered_at=t,
            keystroke_count=2,  # 2 keystrokes for 10+ char names
            paste_detected=False,
        ))
        t += timedelta(seconds=5)

    result, _ = scorer.score(answers, start)

    assert result.breakdown.input_authenticity < 0.1


def test_tab_away_heavy():
    """User tabbed away 3+ times — was googling."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    answers = _make_answers(
        ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"],
        start,
        interval_seconds=8.0,
    )
    result, _ = scorer.score(answers, start, tab_away_count=4)

    assert result.breakdown.input_authenticity < 0.1


def test_bulk_submission():
    """All 5 answers arrive within 2 seconds — server-side bulk paste detection."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    answers = _make_answers(
        ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"],
        start,
        interval_seconds=0.3,  # 1.5s total for all 5
        uniform=True,
    )
    result, _ = scorer.score(answers, start)

    assert result.breakdown.input_authenticity <= 0.1


def test_robotic_timing():
    """Perfectly uniform intervals — suspiciously robotic."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    # Exactly 4.000 seconds between each — no human types this precisely
    names = ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"]
    t = start + timedelta(seconds=4.0)
    answers = []
    for name in names:
        answers.append(Answer(mountain_name=name, answered_at=t))
        t += timedelta(seconds=4.0)

    result, _ = scorer.score(answers, start)

    # CV = 0 for perfectly uniform — should flag as robotic
    assert result.breakdown.input_authenticity < 0.15


def test_clean_typed_input():
    """Real typing with frontend metadata confirming no paste — high score."""
    scorer = BayesianScorer(mountain_db)
    start = datetime.now(timezone.utc)
    names = ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"]
    intervals = [4.2, 5.8, 3.9, 6.1, 4.5]  # natural variation
    t = start + timedelta(seconds=intervals[0])
    answers = []
    for i, name in enumerate(names):
        answers.append(Answer(
            mountain_name=name,
            answered_at=t,
            keystroke_count=len(name) + 2,  # typed with a couple corrections
            paste_detected=False,
            focus_lost_ms=0,
        ))
        if i + 1 < len(intervals):
            t += timedelta(seconds=intervals[i + 1])

    result, _ = scorer.score(answers, start, tab_away_count=0)

    assert result.breakdown.input_authenticity > 0.8
