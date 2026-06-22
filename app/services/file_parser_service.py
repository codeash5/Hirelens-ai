from io import BytesIO

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file.
    """
    pdf_file = BytesIO(file_bytes)
    reader = PdfReader(pdf_file)

    extracted_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text.strip()


def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    Extracts text from a plain text file.
    """
    return file_bytes.decode("utf-8").strip()


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    """
    Detects file type using filename and extracts resume text.
    Supports PDF and TXT for now.
    """
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if filename_lower.endswith(".txt"):
        return extract_text_from_txt(file_bytes)

    raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")