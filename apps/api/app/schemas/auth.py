from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=1, max_length=80)


class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class OnboardingRequest(BaseModel):
    niche: str = Field(min_length=1, max_length=100)
    content_goals: list[str] = Field(min_length=1, max_length=8)
    posting_constraints: str = Field(min_length=1, max_length=500)
    preferred_language: str = Field(min_length=2, max_length=20)
    preferred_tone: str = Field(min_length=1, max_length=80)
    connection_preference: Literal["instagram", "manual_import", "demo"]


class OnboardingResponse(OnboardingRequest):
    updated_at: datetime


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    created_at: datetime
    onboarding: OnboardingResponse | None
