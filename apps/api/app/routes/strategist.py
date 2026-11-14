from fastapi import APIRouter, Depends, Request
from app.routes.auth import current_user

router=APIRouter()
@router.get("/strategist/tools")
def tools(request:Request,user:dict=Depends(current_user))->dict:
 owner=user["_id"]
 return {"status":"provider_unavailable","tools":{"creator_media_count":sum(len(x["media"]) for x in request.app.state.import_repository.list_for_owner(owner)),"audience_evidence_available":request.app.state.audience_repository.latest_for_owner(owner) is not None,"trend_signal_count":len(request.app.state.trend_repository.list_for_owner(owner)),"opportunity_count":len(request.app.state.opportunity_repository.list_for_owner(owner)),"video_job_count":len(request.app.state.video_repository.list_for_owner(owner)),"plan_count":len(request.app.state.planner_repository.list_for_owner(owner))},"limitations":["These are real, authenticated read-tool results.","No reasoning-model provider is configured, so Verdict has not generated a strategist response.","Planner writes require a separate explicit confirmation flow and are unavailable through this endpoint."]}
