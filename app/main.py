from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import get_db

from app.services.resume_parser import extract_resume_text
from app.services.skill_extractor import (
    extract_skills,
    get_total_skills,
)

from app.services.resume_analyzer import (
    extract_experience,
    extract_education,
)
from app.routers.jobs import router as jobs_router
from app.routers.matching import router as matching_router
from app.routers.ai import router as ai_router
from app.routers.analysis import router as analysis_router
from app.routers.users import router as users_router
from app.routers.resumes import router as resumes_router
from app.routers.saved_jobs import router as saved_jobs_router


app = FastAPI(
    title="AI Resume & Job Match Analyzer",
    description="Analyze resumes against job descriptions.",
    version="1.0.0",
)

#  CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

app.include_router(jobs_router)
app.include_router(matching_router)
app.include_router(ai_router)
app.include_router(analysis_router)
app.include_router(users_router)
app.include_router(users_router)
app.include_router(resumes_router)
app.include_router(saved_jobs_router)

@app.get("/")
async def home():
    return {
        "message": "Welcome to AI Resume & Job Match Analyzer",
        "status": "success",
    }


# @app.get("/health/database")
# def database_health(db: Session = Depends(get_db)):

#     db.execute(text("SELECT 1"))

#     return {
#         "status": "connected",
#         "database": "postgresql",
#     }

@app.post("/resume/parse")
async def parse_resume(
    file: UploadFile = File(...)
):
    allowed_extensions = {".pdf", ".docx"}

    filename = file.filename or ""
    extension = (
        "." + filename.rsplit(".", 1)[-1].lower()
        if "." in filename
        else ""
    )

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    try:
        file_bytes = await file.read(MAX_FILE_SIZE + 1)

        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size must not exceed 5 MB.",
            )

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        try:
            extracted_text = extract_resume_text(
                filename,
                file_bytes,
            )

            skills = extract_skills(extracted_text)

            experience = extract_experience(extracted_text)

            education = extract_education(extracted_text)

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail="Unable to read this document. Check that it is a valid PDF or DOCX file.",
            ) from exc

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="No readable text found. The resume may be scanned or empty.",
            )

        return {
            "filename": filename,
            "word_count": len(extracted_text.split()),

            "skills": skills,
            "total_skills": get_total_skills(skills),

            "experience_mentions": experience,
            "education": education,

            "extracted_text": extracted_text,
            "status": "success",
        }

    finally:
        await file.close()