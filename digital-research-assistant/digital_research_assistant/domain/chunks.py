from abc import ABC

from pydantic import UUID4, Field

from digital_research_assistant.domain.base import VectorBaseDocument
from digital_research_assistant.domain.types import DataCategory


class Chunk(VectorBaseDocument, ABC):
    content: str
    filetype: str
    document_id: UUID4
    author_id: UUID4
    author_full_name: str
    metadata: dict = Field(default_factory=dict)


class PDFChunk(Chunk):
    filepath: str

    class Config:
        category = DataCategory.PDFS


class WordChunk(Chunk):
    filepath: str

    class Config:
        category = DataCategory.DOCX
