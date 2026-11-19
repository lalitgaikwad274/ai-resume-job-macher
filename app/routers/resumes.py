
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.resume import (
    ResumeResponse,
    ResumeUpdate,
)

from app.services.resume_parser import (
    extract_resume_text,
)

from app.repositories.resume_repository import (
    create_resume,
    get_resume_by_id,
    get_user_resumes,
    update_resume,
    delete_resume,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/", response_model=ResumeResponse)
async def upload_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = file.filename or ""

    extension = (
        "." + filename.rsplit(".", 1)[-1].lower()
        if "." in filename
        else ""
    )

    if extension not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    try:
        file_bytes = await file.read(MAX_FILE_SIZE + 1)

        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Maximum file size is 5 MB.",
            )

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Empty file.",
            )

        try:
            extracted_text = extract_resume_text(
                filename,
                file_bytes,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=422,
                detail="Unable to parse the uploaded document.",
            ) from exc

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="No readable text found in resume.",
            )

        resume = create_resume(
            db=db,
            user_id=user_id,
            filename=filename,
            file_type=extension.lstrip("."),
            extracted_text=extracted_text,
        )

        return resume

    finally:
        await file.close()


@router.get("/", response_model=list[ResumeResponse])
def list_resumes(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_resumes(db, user_id)


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    resume = get_resume_by_id(
        db,
        resume_id,
        user_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    return resume


@router.patch("/{resume_id}", response_model=ResumeResponse)
def rename_resume(
    resume_id: int,
    user_id: int,
    request: ResumeUpdate,
    db: Session = Depends(get_db),
):
    resume = get_resume_by_id(
        db,
        resume_id,
        user_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    if request.filename is not None:
        if not request.filename.strip():
            raise HTTPException(
                status_code=422,
                detail="Filename cannot be empty.",
            )

        resume = update_resume(
            db,
            resume,
            request.filename.strip(),
        )

    return resume


@router.delete("/{resume_id}")
def remove_resume(
    resume_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    resume = get_resume_by_id(
        db,
        resume_id,
        user_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    delete_resume(db, resume)

    return {
        "message": "Resume deleted successfully.",
        "status": "success",
    }
