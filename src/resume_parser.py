import fitz


def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF resume.

    Accepts Streamlit UploadedFile objects and file-like objects.
    Raises ValueError with a user-friendly message for unreadable PDFs.
    """
    if hasattr(pdf_file, "getvalue"):
        pdf_bytes = pdf_file.getvalue()
    else:
        current_position = None
        try:
            current_position = pdf_file.tell()
            pdf_file.seek(0)
        except (AttributeError, OSError):
            pass

        pdf_bytes = pdf_file.read()

        if current_position is not None:
            try:
                pdf_file.seek(current_position)
            except (AttributeError, OSError):
                pass

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise ValueError(
                    "This PDF is password-protected. Please upload an unlocked PDF."
                )

            extracted_pages = [page.get_text() for page in pdf]
    except ValueError:
        raise
    except (fitz.FileDataError, fitz.EmptyFileError, RuntimeError) as error:
        raise ValueError(
            "Unable to read this PDF. Please upload a valid, uncorrupted PDF."
        ) from error

    return "\n".join(extracted_pages).strip()
