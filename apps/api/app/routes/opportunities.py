from fastapi import APIRouter, Depends, Request, status

from app.repositories.opportunities import OpportunityRepository
from app.routes.auth import current_user
from app.schemas.opportunities import OpportunityRequest, OpportunityResponse
from app.services.scoring import confidence, opportunity_score

router = APIRouter()
SCORE_VERSION = "v1:0.35/0.30/0.20/0.15"


def repository(request: Request) -> OpportunityRepository: return request.app.state.opportunity_repository


def response(record: dict) -> OpportunityResponse:
    return OpportunityResponse(id=record["_id"], title=record["title"], angle=record["angle"], hook=record["hook"], format=record["format"], effort=record["effort"], evidence=record["evidence"], score_inputs=record["score_inputs"], score=record["score"], score_version=record["score_version"], confidence=record["confidence"], created_at=record["created_at"])


@router.post("/opportunities", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(payload: OpportunityRequest, user: dict = Depends(current_user), repo: OpportunityRepository = Depends(repository)) -> OpportunityResponse:
    data = payload.model_dump(mode="json")
    data |= {"score": opportunity_score(payload.score_inputs), "score_version": SCORE_VERSION, "confidence": confidence(payload.score_inputs)}
    return response(repo.create(user["_id"], data))


@router.get("/opportunities", response_model=list[OpportunityResponse])
def list_opportunities(user: dict = Depends(current_user), repo: OpportunityRepository = Depends(repository)) -> list[OpportunityResponse]:
    return [response(record) for record in repo.list_for_owner(user["_id"])]
