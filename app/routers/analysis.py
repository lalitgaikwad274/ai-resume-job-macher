
from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.services.analysis_service import (
    analyze_complete_resume,
)

router = APIRouter(
    prefix="/analysis",
    tags=["Complete Analysis"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/full")
async def full_resume_analysis(
    file: UploadFile = File(...),

    job_title: str = Form(
        ...,
        min_length=2,
        max_length=150,
    ),

    job_description: str = Form(
        ...,
        min_length=30,
        max_length=15000,
    ),

    include_ai: bool = Form(True),
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
        file_bytes = await file.read(
            MAX_FILE_SIZE + 1
        )

        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Maximum file size is 5 MB.",
            )

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        try:
            result = await analyze_complete_resume(
                filename=filename,
                file_bytes=file_bytes,
                job_title=job_title,
                job_description=job_description,
                include_ai=include_ai,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=str(exc),
            ) from exc

        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Resume analysis failed. Check the AI provider configuration and service logs.",
            ) from exc

        return result

    finally:
        await file.close()
