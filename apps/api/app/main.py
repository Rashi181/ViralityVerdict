from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pymongo import MongoClient

from app.core.config import Settings
from app.repositories.users import MongoUserRepository
from app.repositories.imports import InMemoryImportRepository, MongoImportRepository, ImportRepository
from app.repositories.audience import AudienceRepository, InMemoryAudienceRepository, MongoAudienceRepository
from app.repositories.trends import TrendRepository, InMemoryTrendRepository, MongoTrendRepository
from app.repositories.opportunities import OpportunityRepository, InMemoryOpportunityRepository, MongoOpportunityRepository
from app.repositories.videos import VideoRepository, InMemoryVideoRepository, MongoVideoRepository
from app.repositories.planner import InMemoryPlannerRepository, MongoPlannerRepository
from app.repositories.connections import ConnectionRepository, InMemoryConnectionRepository, MongoConnectionRepository
from app.routes.auth import router as auth_router
from app.routes.imports import router as imports_router
from app.routes.instagram import router as instagram_router
from app.routes.creator import router as creator_router
from app.routes.audience import router as audience_router
from app.routes.trends import router as trends_router
from app.routes.opportunities import router as opportunities_router
from app.routes.videos import router as videos_router
from app.routes.optimization import router as optimization_router
from app.routes.planner import router as planner_router
from app.routes.strategist import router as strategist_router
from app.routes.publishing import router as publishing_router
from app.routes.system import router as system_router
from app.services.auth import AuthService


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cache-Control"] = "no-store"
        return response


def create_app(auth_service: AuthService | None = None, import_repository: ImportRepository | None = None, audience_repository: AudienceRepository | None = None, trend_repository: TrendRepository | None = None, opportunity_repository: OpportunityRepository | None = None, video_repository: VideoRepository | None = None, settings: Settings | None = None, connection_repository: ConnectionRepository | None = None) -> FastAPI:
    app = FastAPI(title="Verdict API", version="0.1.0", openapi_url="/api/v1/openapi.json")
    configured_settings = settings or Settings.from_environment()
    app.add_middleware(CORSMiddleware, allow_origins=list(configured_settings.web_origins), allow_credentials=True, allow_methods=["GET", "POST", "PUT"], allow_headers=["Content-Type"])
    app.add_middleware(SecurityHeadersMiddleware)
    if auth_service is None:
        app.state.settings = configured_settings
        if not configured_settings.mongodb_uri or not configured_settings.session_secret:
            app.state.auth_service = None
        else:
            client = MongoClient(configured_settings.mongodb_uri, serverSelectionTimeoutMS=2000)
            app.state.auth_service = AuthService(MongoUserRepository(client.verdict.users), configured_settings.session_secret)
            app.state.import_repository = MongoImportRepository(client.verdict.imports)
            app.state.audience_repository = MongoAudienceRepository(client.verdict.audience_aggregates, client.verdict.audience_feedback)
            app.state.trend_repository = MongoTrendRepository(client.verdict.trend_signals)
            app.state.opportunity_repository = MongoOpportunityRepository(client.verdict.opportunities)
            app.state.video_repository = MongoVideoRepository(client.verdict.video_jobs)
            app.state.planner_repository = MongoPlannerRepository(client.verdict.plans)
            app.state.connection_repository = MongoConnectionRepository(client.verdict.instagram_connections, client.verdict.instagram_audit)
    else:
        app.state.auth_service = auth_service
        app.state.settings = settings or Settings(None, "test-session-secret-that-is-at-least-32-chars")
    if import_repository is not None: app.state.import_repository = import_repository
    elif not hasattr(app.state, "import_repository"): app.state.import_repository = InMemoryImportRepository()
    if audience_repository is not None: app.state.audience_repository = audience_repository
    elif not hasattr(app.state, "audience_repository"): app.state.audience_repository = InMemoryAudienceRepository()
    if trend_repository is not None: app.state.trend_repository = trend_repository
    elif not hasattr(app.state, "trend_repository"): app.state.trend_repository = InMemoryTrendRepository()
    if opportunity_repository is not None: app.state.opportunity_repository = opportunity_repository
    elif not hasattr(app.state, "opportunity_repository"): app.state.opportunity_repository = InMemoryOpportunityRepository()
    if video_repository is not None: app.state.video_repository = video_repository
    elif not hasattr(app.state, "video_repository"): app.state.video_repository = InMemoryVideoRepository()
    if connection_repository is not None: app.state.connection_repository = connection_repository
    elif not hasattr(app.state, "connection_repository"): app.state.connection_repository = InMemoryConnectionRepository()
    if not hasattr(app.state,"planner_repository"): app.state.planner_repository=InMemoryPlannerRepository()
    app.include_router(system_router, prefix="/api/v1", tags=["system"])
    app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
    app.include_router(imports_router, prefix="/api/v1", tags=["imports"])
    app.include_router(instagram_router, prefix="/api/v1", tags=["instagram"])
    app.include_router(creator_router, prefix="/api/v1", tags=["creator"])
    app.include_router(audience_router, prefix="/api/v1", tags=["audience"])
    app.include_router(trends_router, prefix="/api/v1", tags=["trends"])
    app.include_router(opportunities_router, prefix="/api/v1", tags=["opportunities"])
    app.include_router(videos_router, prefix="/api/v1", tags=["videos"])
    app.include_router(optimization_router, prefix="/api/v1", tags=["optimization"])
    app.include_router(planner_router,prefix="/api/v1",tags=["planner"])
    app.include_router(strategist_router,prefix="/api/v1",tags=["strategist"])
    app.include_router(publishing_router,prefix="/api/v1",tags=["publishing"])
    return app


app = create_app()
