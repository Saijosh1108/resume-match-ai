from io import BytesIO

import fitz
import pytest

from src.resume_parser import extract_text_from_pdf


def make_pdf(text):
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def test_extracts_text_from_pdf():
    uploaded_file = BytesIO(make_pdf("Python and machine learning"))

    result = extract_text_from_pdf(uploaded_file)

    assert "Python and machine learning" in result


def test_empty_pdf_upload_raises_clear_error():
    with pytest.raises(ValueError, match="empty"):
        extract_text_from_pdf(BytesIO(b""))


def test_invalid_pdf_raises_clear_error():
    with pytest.raises(ValueError, match="Unable to read"):
        extract_text_from_pdf(BytesIO(b"not a PDF"))


def test_streamlit_style_upload_object_is_supported():
    class UploadedFile:
        def getvalue(self):
            return make_pdf("Resume content")

    assert "Resume content" in extract_text_from_pdf(UploadedFile())
