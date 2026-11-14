from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.schemas.auth import OnboardingRequest, OnboardingResponse, SignInRequest, SignUpRequest, UserResponse
from app.services.auth import AuthService, AuthenticationError
from app.repositories.users import EmailAlreadyExistsError

router = APIRouter()
SESSION_COOKIE = "verdict_session"


def get_auth_service(request: Request) -> AuthService:
    auth_service = request.app.state.auth_service
    if auth_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication is not configured")
    return auth_service


def user_response(user: dict) -> UserResponse:
    return UserResponse(id=user["_id"], email=user["email"], display_name=user["display_name"], created_at=user["created_at"], onboarding=user["onboarding"])


def current_user(request: Request, auth: AuthService = Depends(get_auth_service)) -> dict:
    try:
        return auth.current_user(request.cookies.get(SESSION_COOKIE))
    except AuthenticationError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required") from error


def set_session(request: Request, response: Response, auth: AuthService, user_id: str) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        auth.issue_session(user_id),
        httponly=True,
        samesite="lax",
        secure=request.app.state.settings.cookie_secure,
        max_age=auth.session_hours * 3600,
    )


@router.post("/auth/sign-up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(payload: SignUpRequest, request: Request, response: Response, auth: AuthService = Depends(get_auth_service)) -> UserResponse:
    try:
        user = auth.sign_up(email=str(payload.email), password=payload.password, display_name=payload.display_name)
    except EmailAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from error
    set_session(request, response, auth, user["_id"])
    return user_response(user)


@router.post("/auth/sign-in", response_model=UserResponse)
def sign_in(payload: SignInRequest, request: Request, response: Response, auth: AuthService = Depends(get_auth_service)) -> UserResponse:
    try:
        user = auth.sign_in(email=str(payload.email), password=payload.password)
    except AuthenticationError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") from error
    set_session(request, response, auth, user["_id"])
    return user_response(user)


@router.post("/auth/sign-out", status_code=status.HTTP_204_NO_CONTENT)
def sign_out(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE)


@router.get("/auth/me", response_model=UserResponse)
def me(user: dict = Depends(current_user)) -> UserResponse:
    return user_response(user)


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str, user: dict = Depends(current_user)) -> UserResponse:
    if user_id != user["_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-user access denied")
    return user_response(user)


@router.put("/onboarding", response_model=OnboardingResponse)
def update_onboarding(payload: OnboardingRequest, user: dict = Depends(current_user), auth: AuthService = Depends(get_auth_service)) -> OnboardingResponse:
    onboarding = payload.model_dump() | {"updated_at": datetime.now(UTC)}
    updated = auth.repository.set_onboarding(user["_id"], onboarding)
    return OnboardingResponse(**updated["onboarding"])


@router.get("/onboarding", response_model=OnboardingResponse)
def get_onboarding(user: dict = Depends(current_user)) -> OnboardingResponse:
    if user["onboarding"] is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Onboarding has not been completed")
    return OnboardingResponse(**user["onboarding"])
