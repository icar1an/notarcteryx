from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "notarcteryx"
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    quiz_duration_seconds: int = 120  # 2 minutes
    num_answers_required: int = 5
    prior_hiker: float = 0.3
    max_surcharge_pct: float = 900.0  # posers pay up to 10x
    fuzzy_match_threshold: float = 75.0  # rapidfuzz score threshold (0-100)
    session_cleanup_interval_seconds: int = 60

    model_config = {"env_prefix": "NOTARC_"}


settings = Settings()
