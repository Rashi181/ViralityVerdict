from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[4] / ".env")


@dataclass(frozen=True)
class Settings:
    mongodb_uri: str | None
    session_secret: str | None
    session_hours: int = 24
    cookie_secure: bool = False
    web_origins: tuple[str, ...] = ("http://localhost:3000", "http://127.0.0.1:3000")
    meta_app_id: str | None = None
    meta_app_secret: str | None = None
    meta_instagram_login_config_id: str | None = None  # Legacy Unified Login value; not used by Facebook Login.
    meta_redirect_uri: str | None = None
    meta_api_version: str = "v27.0"
    meta_token_encryption_key: str | None = None
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.8-flash"
    groq_api_key: str | None = None
    groq_reel_model: str = "qwen/qwen3.8-27b"
    xai_api_key: str | None = None
    xai_reel_model: str = "grok-4.7"
    reel_analysis_provider: str = "gemini"
    demo_mode: bool = False
    demo_fixture_path: str | None = None

    @classmethod
    def from_environment(cls) -> "Settings":
        web_origins = tuple(
            origin.strip()
            for origin in os.getenv("VERDICT_WEB_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
            if origin.strip()
        )
        return cls(
            mongodb_uri=os.getenv("MONGODB_URI") or None,
            session_secret=os.getenv("VERDICT_SESSION_SECRET") or None,
            cookie_secure=os.getenv("VERDICT_COOKIE_SECURE", "false").lower() == "true",
            web_origins=web_origins,
            meta_app_id=os.getenv("META_APP_ID") or None,
            meta_app_secret=os.getenv("META_APP_SECRET") or None,
            meta_instagram_login_config_id=os.getenv("META_INSTAGRAM_LOGIN_CONFIG_ID") or None,
            meta_redirect_uri=os.getenv("META_REDIRECT_URI") or None,
            meta_api_version=os.getenv("META_API_VERSION") or "v27.0",
            meta_token_encryption_key=os.getenv("META_TOKEN_ENCRYPTION_KEY") or None,
            gemini_api_key=os.getenv("GEMINI_API_KEY") or None,
            gemini_model=os.getenv("GEMINI_MODEL") or "gemini-3.8-flash",
            groq_api_key=os.getenv("GROQ_API_KEY") or None,
            groq_reel_model=os.getenv("GROQ_REEL_MODEL") or "qwen/qwen3.8-27b",
            xai_api_key=os.getenv("XAI_API_KEY") or None,
            xai_reel_model=os.getenv("XAI_REEL_MODEL") or "grok-4.7",
            reel_analysis_provider=os.getenv("VERDICT_REEL_ANALYSIS_PROVIDER") or "gemini",
            demo_mode=os.getenv("VERDICT_DEMO_MODE", "false").lower() == "true",
            demo_fixture_path=os.getenv("VERDICT_DEMO_FIXTURE_PATH") or None,
        )
