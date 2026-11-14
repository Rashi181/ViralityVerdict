import csv
from io import StringIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status

from app.repositories.imports import ImportRepository
from app.routes.auth import current_user
from app.schemas.imports import ImportedMedia, ImportRequest, ImportResponse

router = APIRouter()

def repository(request: Request) -> ImportRepository: return request.app.state.import_repository
def response(record: dict) -> ImportResponse: return ImportResponse(id=record["_id"], source=record["source"], status=record["status"], media_count=len(record["media"]), created_at=record["created_at"], limitations=record["limitations"])


@router.post("/imports", response_model=ImportResponse, status_code=status.HTTP_201_CREATED)
def create_import(payload: ImportRequest, user: dict = Depends(current_user), repo: ImportRepository = Depends(repository)) -> ImportResponse:
    limitations = ["User-supplied import; Verdict has not API-verified these metrics."]
    if not payload.consent_confirmed: limitations.append("Creator consent was not confirmed.")
    return response(repo.create(user["_id"], "user_import", [item.model_dump(mode="json") for item in payload.media], limitations))


@router.get("/imports", response_model=list[ImportResponse])
def list_imports(user: dict = Depends(current_user), repo: ImportRepository = Depends(repository)) -> list[ImportResponse]:
    return [response(record) for record in repo.list_for_owner(user["_id"])]


@router.post("/imports/csv", response_model=ImportResponse, status_code=status.HTTP_201_CREATED)
async def create_csv_import(file: UploadFile = File(...), consent_confirmed: bool = Form(...), user: dict = Depends(current_user), repo: ImportRepository = Depends(repository)) -> ImportResponse:
    if file.content_type not in {"text/csv", "application/vnd.ms-excel"}:
        raise HTTPException(status_code=422, detail="Upload a CSV file")
    try:
        rows = list(csv.DictReader(StringIO((await file.read()).decode("utf-8"))))
        media = [ImportedMedia(**{**row, "views": int(row["views"]), "likes": int(row["likes"]), "comments": int(row["comments"])}) for row in rows]
        payload = ImportRequest(consent_confirmed=consent_confirmed, media=media)
    except (KeyError, UnicodeDecodeError, ValueError) as error:
        raise HTTPException(status_code=422, detail="CSV must contain media_id,published_at,caption,media_type,views,likes,comments") from error
    return create_import(payload, user, repo)
