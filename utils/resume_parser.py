"""
Resume text extraction utilities — supports PDF and DOCX files.
"""
import io
from pathlib import Path


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from a PDF file given its raw bytes."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n".join(pages).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {e}") from e


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract plain text from a DOCX file given its raw bytes."""
    try:
        from docx import Document

        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX: {e}") from e


def extract_resume_text(uploaded_file) -> str:
    """
    Accept a Streamlit UploadedFile object and return extracted plain text.
    Raises ValueError for unsupported file types.
    """
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {Path(filename).suffix}")
