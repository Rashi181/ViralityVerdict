from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.system import router as system_router

app = FastAPI(title="Verdict API", version="0.1.0", openapi_url="/api/v1/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)
app.include_router(system_router, prefix="/api/v1", tags=["system"])
