from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ImportedMedia(BaseModel):
    media_id: str = Field(min_length=1, max_length=128)
    published_at: datetime
    caption: str = Field(max_length=2200)
    media_type: Literal["reel", "post"]
    views: int = Field(ge=0)
    likes: int = Field(ge=0)
    comments: int = Field(ge=0)


class ImportRequest(BaseModel):
    consent_confirmed: bool
    media: list[ImportedMedia] = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def unique_media_ids(self) -> "ImportRequest":
        if len({item.media_id for item in self.media}) != len(self.media):
            raise ValueError("media_id values must be unique")
        return self


class ImportResponse(BaseModel):
    id: str
    source: Literal["user_import"]
    status: Literal["completed"]
    media_count: int
    created_at: datetime
    limitations: list[str]
