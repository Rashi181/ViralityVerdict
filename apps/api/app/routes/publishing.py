from fastapi import APIRouter,Depends,Request
from app.routes.auth import current_user
router=APIRouter()
@router.get("/publishing/eligibility")
def eligibility(request:Request,user:dict=Depends(current_user))->dict:
 return {"eligible":False,"status":"manual_handoff_required","limitations":["No verified Meta publishing configuration, granted scopes, or App Review status is available.","Verdict has not published anything."],"handoff":{"steps":["Open Instagram with the approved draft.","Paste the creator-approved caption.","Publish manually and record observed results later."],"requires_creator_approval":True}}
