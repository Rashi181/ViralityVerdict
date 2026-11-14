from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.repositories.users import EmailAlreadyExistsError, UserRepository

PASSWORD_HASH = PasswordHash.recommended()


class AuthenticationError(Exception):
    pass


class AuthService:
    def __init__(self, repository: UserRepository, session_secret: str, session_hours: int = 24) -> None:
        if len(session_secret) < 32:
            raise ValueError("VERDICT_SESSION_SECRET must contain at least 32 characters")
        self.repository = repository
        self.session_secret = session_secret
        self.session_hours = session_hours

    def sign_up(self, *, email: str, password: str, display_name: str) -> dict:
        return self.repository.create(
            email=email, display_name=display_name, password_hash=PASSWORD_HASH.hash(password)
        )

    def sign_in(self, *, email: str, password: str) -> dict:
        user = self.repository.find_by_email(email)
        if user is None or not PASSWORD_HASH.verify(password, user["password_hash"]):
            raise AuthenticationError
        return user

    def issue_session(self, user_id: str) -> str:
        now = datetime.now(UTC)
        return jwt.encode(
            {"sub": user_id, "iat": now, "exp": now + timedelta(hours=self.session_hours)},
            self.session_secret, algorithm="HS256",
        )

    def current_user(self, token: str | None) -> dict:
        if not token:
            raise AuthenticationError
        try:
            claims = jwt.decode(token, self.session_secret, algorithms=["HS256"])
        except jwt.PyJWTError as error:
            raise AuthenticationError from error
        user = self.repository.find_by_id(claims["sub"])
        if user is None:
            raise AuthenticationError
        return user
