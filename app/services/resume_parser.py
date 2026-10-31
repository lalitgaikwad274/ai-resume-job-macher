from io import BytesIO

import pymupdf
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""

    with pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    ) as pdf:
        pages = [
            page.get_text()
            for page in pdf
        ]

    return "\n".join(pages).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""

    document = Document(BytesIO(file_bytes))

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_resume_text(
    filename: str,
    file_bytes: bytes
) -> str:
    """Choose the correct parser based on file extension."""

    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":
        return extract_text_from_pdf(file_bytes)

    if extension == "docx":
        return extract_text_from_docx(file_bytes)

    raise ValueError(
        "Unsupported file format. Upload PDF or DOCX."
    )