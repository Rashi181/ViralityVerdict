from fastapi import APIRouter, Depends
from app.routes.auth import current_user
from app.schemas.optimization import CaptionVariant, OptimizationRequest, OptimizationResponse

router=APIRouter()

@router.post("/optimize",response_model=OptimizationResponse)
def optimize(payload:OptimizationRequest,user:dict=Depends(current_user))->OptimizationResponse:
    opening=payload.draft_text.splitlines()[0][:120]
    return OptimizationResponse(source_tier="user_supplied",captions=[CaptionVariant(style="formal",text=f"{opening}\n\n{payload.call_to_action}"),CaptionVariant(style="sarcastic",text=f"Because apparently we all needed this: {opening}\n\n{payload.call_to_action}"),CaptionVariant(style="humorous-tech",text=f"Patch notes: {opening}\n\n{payload.call_to_action}"),CaptionVariant(style="humorous-non-tech",text=f"Tiny win of the day: {opening}\n\n{payload.call_to_action}")],suggestions=["This is deterministic guidance from your supplied text; verify it against the actual edit.","Place the value proposition before the CTA if the opening currently delays it."],persona_reactions=[],limitations=["No transcript, scene analysis, OCR, or model analysis is available, so Verdict cannot provide timestamped findings.","Persona reactions are unavailable rather than simulated without evidence-grounded draft analysis."])
