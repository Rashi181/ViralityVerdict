from fastapi import APIRouter, Depends, Request, status

from app.repositories.audience import AudienceRepository
from app.routes.auth import current_user
from app.schemas.audience import AudienceImportRequest, AudienceImportResponse, AudiencePersonaResponse, PersonaFeedbackRequest

router = APIRouter()


def repository(request: Request) -> AudienceRepository:
    return request.app.state.audience_repository


@router.post("/audience/import", response_model=AudienceImportResponse, status_code=status.HTTP_201_CREATED)
def import_audience(payload: AudienceImportRequest, user: dict = Depends(current_user), repo: AudienceRepository = Depends(repository)) -> AudienceImportResponse:
    limitations = ["User-supplied aggregate audience data; Verdict has not API-verified it."]
    if not payload.consent_confirmed:
        limitations.append("Creator consent was not confirmed.")
    record = repo.create(user["_id"], [item.model_dump(mode="json") for item in payload.aggregates], limitations)
    return AudienceImportResponse(id=record["_id"], aggregate_count=len(record["aggregates"]), created_at=record["created_at"], limitations=record["limitations"])


@router.post("/audience/personas/feedback", status_code=status.HTTP_204_NO_CONTENT)
def save_feedback(payload: PersonaFeedbackRequest, user: dict = Depends(current_user), repo: AudienceRepository = Depends(repository)) -> None:
    repo.save_feedback(user["_id"], payload.note)


@router.get("/audience/personas/current", response_model=AudiencePersonaResponse)
def current_persona(request: Request, user: dict = Depends(current_user), repo: AudienceRepository = Depends(repository)) -> AudiencePersonaResponse:
    audience = repo.latest_for_owner(user["_id"])
    feedback = repo.latest_feedback(user["_id"])
    onboarding = user.get("onboarding") or {}
    formats = request.app.state.import_repository.list_for_owner(user["_id"])
    imported_types = sorted({item["media_type"] for record in formats for item in record["media"]})
    format_basis = ", ".join(imported_types) if imported_types else "no imported content formats"

    if audience is None:
        return AudiencePersonaResponse(
            id="provisional-content-planning-lens", status="provisional", label="Provisional content-planning lens",
            intended_use="A synthetic planning aid while current aggregate audience statistics are unavailable.",
            observed_evidence=[], inferred_interests=[], likely_motivations=[], content_preferences=[],
            suggested_hooks=["Treat hook choices as experiments until audience evidence is available."],
            pacing_considerations=["No audience-backed pacing preference is available."],
            cta_preferences=["No audience-backed CTA preference is available."],
            unknowns=["Current aggregate audience demographics and geography are unavailable.", "No demographic-to-content-performance cross-tabulation is available."],
            confidence="low", data_coverage=f"No audience aggregates imported. Creator-history context: {format_basis}. User goal context: {', '.join(onboarding.get('content_goals', [])) or 'not provided'}.",
            freshness=None, feedback_note=feedback["note"] if feedback else None,
        )

    evidence = audience["aggregates"]
    freshness = max(item["as_of"] for item in evidence)
    return AudiencePersonaResponse(
        id="audience-informed-planning-lens", status="observed", label="Audience-informed planning lens",
        intended_use="A synthetic planning aid grounded in the listed aggregate audience evidence, not an individual viewer profile.",
        observed_evidence=evidence,
        inferred_interests=[], likely_motivations=[],
        content_preferences=[f"Hypothesis: test {format_basis} formats first because they are the imported creator-history context, not because a demographic segment is proven to prefer them."],
        suggested_hooks=["Hypothesis: compare a direct value-first opening against the current creator style."],
        pacing_considerations=["Hypothesis: test pacing as an experiment; supplied aggregates do not establish retention preferences."],
        cta_preferences=["Hypothesis: test one clear, low-friction CTA; supplied aggregates do not establish CTA preference."],
        unknowns=["No demographic-to-content-performance cross-tabulation was supplied.", "Interests, motivations, and individual viewer behavior remain unknown."],
        confidence="medium", data_coverage=f"{len(evidence)} user-imported aggregate audience fields; creator-history context: {format_basis}.",
        freshness=freshness, feedback_note=feedback["note"] if feedback else None,
    )
