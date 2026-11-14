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

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            mongodb_uri=os.getenv("MONGODB_URI") or None,
            session_secret=os.getenv("VERDICT_SESSION_SECRET") or None,
        )
