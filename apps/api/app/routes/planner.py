from fastapi import APIRouter,Depends,Request,status
from app.routes.auth import current_user
from app.schemas.planner import PlanRequest,PlanResponse
router=APIRouter()
def repo(r:Request):return r.app.state.planner_repository
def out(x):return PlanResponse(id=x["_id"],title=x["title"],planned_at=x.get("planned_at"),status=x["status"],created_at=x["created_at"])
@router.post("/plans",response_model=PlanResponse,status_code=status.HTTP_201_CREATED)
def create(p:PlanRequest,u:dict=Depends(current_user),r=Depends(repo)):return out(r.create(u["_id"],p.model_dump(mode="json")))
@router.get("/plans",response_model=list[PlanResponse])
def list_plans(u:dict=Depends(current_user),r=Depends(repo)):return [out(x) for x in r.list_for_owner(u["_id"])]
