from .pdf_loader import load_pdf
from .web_loader import load_web
from .txt_loader import load_text
from .docx_loader import load_docx

def load(source: str):
    source = source.strip()
    check = source.lower()

    if check.startswith("http://") or check.startswith("https://"):
        return load_web(source)
    elif check.endswith(".pdf"):
        return load_pdf(source)
    elif check.endswith(".docx"):
        return load_docx(source)
    elif check.endswith(".txt"):
        return load_text(source)
    else:
        raise ValueError(f"Unsupported file type: {source}")