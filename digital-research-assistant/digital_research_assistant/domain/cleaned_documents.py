from abc import ABC
from typing import Optional

from pydantic import UUID4

from .base import VectorBaseDocument
from .types import DataCategory


class CleanedDocument(VectorBaseDocument, ABC):
    content: str
    filepath: str
    filetype: str
    author_id: UUID4
    author_full_name: str


class CleanedPDFDocument(CleanedDocument):
    image: Optional[str] = None

    class Config:
        name = "cleaned_pdfs"
        category = DataCategory.PDFS
        use_vector_index = False


class CleanedWordDocument(CleanedDocument):
    image: Optional[str] = None

    class Config:
        name = "cleaned_docx"
        category = DataCategory.DOCX
        use_vector_index = False
