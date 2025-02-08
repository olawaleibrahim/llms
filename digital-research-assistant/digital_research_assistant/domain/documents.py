from abc import ABC

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory


class UserDocument(NoSQLBaseDocument):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Document(NoSQLBaseDocument, ABC):
    content: dict
    filetype: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")


class PDFDocument(Document):
    filepath: str

    class Settings:
        name = DataCategory.PDFS


class WordDocument(Document):
    filepath: str

    class Settings:
        name = DataCategory.DOCX
