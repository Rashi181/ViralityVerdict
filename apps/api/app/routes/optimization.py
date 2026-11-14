from fastapi import APIRouter, Depends
from app.routes.auth import current_user
from app.schemas.optimization import CaptionRecommendation, HashtagRecommendation, OptimizationRequest, OptimizationResponse

router=APIRouter()

@router.post("/optimize",response_model=OptimizationResponse)
def optimize(payload:OptimizationRequest,user:dict=Depends(current_user))->OptimizationResponse:
    opening=payload.draft_text.splitlines()[0][:120]
    keyword_tokens = [token.strip("#.,!?;:()[]{}\"'").lower() for token in payload.draft_text.split()]
    keywords = []
    for token in keyword_tokens:
        if token.isalnum() and len(token) >= 4 and token not in keywords:
            keywords.append(token)
        if len(keywords) == 3:
            break
    hashtags = [
        HashtagRecommendation(
            tag=f"#{keyword}",
            source="creator_provided_keyword",
            explanation="Derived from words in the creator-provided draft; not a claim that this hashtag is trending.",
        )
        for keyword in keywords
    ]
    prompt_note = " Your refinement instruction was recorded, but no model is configured to interpret it yet." if payload.refinement_prompt else ""
    return OptimizationResponse(source_tier="user_supplied",captions=[CaptionRecommendation(id="concise",text=f"{opening}\n\n{payload.call_to_action}"),CaptionRecommendation(id="context_first",text=f"Here is the context: {opening}\n\n{payload.call_to_action}"),CaptionRecommendation(id="question_led",text=f"Want to try this? {opening}\n\n{payload.call_to_action}")],hashtags=hashtags,suggestions=["These are deterministic caption structures based on the text you supplied; verify them against the actual edit.","Place the value proposition before the CTA if the opening currently delays it."],persona_reactions=[],limitations=[f"No transcript, scene analysis, OCR, or model analysis is available, so Verdict cannot provide timestamped findings or interpret a tone request.{prompt_note}","Persona reactions are unavailable rather than simulated without evidence-grounded draft analysis."])
