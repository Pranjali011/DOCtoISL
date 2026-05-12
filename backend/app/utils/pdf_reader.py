import pdfplumber
from io import BytesIO

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract clean text from a PDF file.
    Works for multi-page, scanned, or partially readable PDFs.
    """

    text_parts = []

    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:

            # Simply iterate pages 
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    cleaned = text.replace("\n", " ").strip()
                    if cleaned:
                        text_parts.append(cleaned)

    except Exception as e:
        print(f"[PDF ERROR] Failed to read PDF: {e}")
        return ""

    if not text_parts:
        return ""

    full_text = " ".join(text_parts)
    return " ".join(full_text.split())
