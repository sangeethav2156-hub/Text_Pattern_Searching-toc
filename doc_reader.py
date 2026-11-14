"""doc_reader.py - extracts plain text from a DOCX (or PDF) document."""
import sys


def read_document(path):
    """Return the text of the document; every paragraph becomes one line."""
    if path.lower().endswith(".docx"):
        from docx import Document              # pip install python-docx
        return "\n".join(p.text for p in Document(path).paragraphs)
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader            # pip install pypdf
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(path).pages)
    sys.exit("Unsupported file type (use .docx or .pdf)")


def locate(text, offset):
    """Convert a character offset into (line number, column), both 1-based."""
    line = text.count("\n", 0, offset) + 1
    col = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, col