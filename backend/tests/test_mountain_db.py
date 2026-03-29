from app.services.mountain_db import mountain_db


def test_loads_mountains():
    assert mountain_db.count() > 100


def test_exact_match():
    result = mountain_db.lookup("Mount Rainier")
    assert result.matched
    assert result.exact_match
    assert result.mountain is not None
    assert result.mountain.region == "Cascades"


def test_alias_match():
    result = mountain_db.lookup("Mt. Rainier")
    assert result.matched
    assert result.exact_match  # aliases count as exact
    assert result.mountain.name == "Mount Rainier"


def test_fuzzy_match():
    result = mountain_db.lookup("Mount Ranier")  # common misspelling
    assert result.matched
    assert not result.exact_match
    assert result.mountain.name == "Mount Rainier"


def test_no_match():
    result = mountain_db.lookup("qwzxjfkdls")
    assert not result.matched
    assert result.mountain is None


def test_haversine():
    # Seattle to Portland is ~233 km
    d = mountain_db.haversine_km(47.6, -122.3, 45.5, -122.7)
    assert 220 < d < 250
