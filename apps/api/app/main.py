from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from app.core.config import Settings
from app.repositories.users import MongoUserRepository
from app.routes.auth import router as auth_router
from app.routes.system import router as system_router
from app.services.auth import AuthService


def create_app(auth_service: AuthService | None = None) -> FastAPI:
    app = FastAPI(title="Verdict API", version="0.1.0", openapi_url="/api/v1/openapi.json")
    app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type"])
    if auth_service is None:
        settings = Settings.from_environment()
        if not settings.mongodb_uri or not settings.session_secret:
            app.state.auth_service = None
        else:
            client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)
            app.state.auth_service = AuthService(MongoUserRepository(client.verdict.users), settings.session_secret)
    else:
        app.state.auth_service = auth_service
    app.include_router(system_router, prefix="/api/v1", tags=["system"])
    app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
    return app


app = create_app()
