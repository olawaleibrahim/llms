from abc import ABC

from pydantic import UUID4, Field

from digital_research_assistant.domain.types import DataCategory

from .base import VectorBaseDocument


class EmbeddedChunk(VectorBaseDocument, ABC):
    content: str
    embedding: list[float] | None
    filetype: str
    document_id: UUID4
    author_id: UUID4
    author_full_name: str
    metadata: dict = Field(default_factory=dict)

    @classmethod
    def to_context(cls, chunks: list["EmbeddedChunk"]) -> str:
        context = ""
        for i, chunk in enumerate(chunks):
            context += f"""
            Chunk {i + 1}:
            Type: {chunk.__class__.__name__}
            Filetype: {chunk.filetype}
            Author: {chunk.author_full_name}
            Content: {chunk.content}\n
            """

        return context


class EmbeddedPDFChunk(EmbeddedChunk):
    class Config:
        name = "embedded_pdfs"
        category = DataCategory.PDFS
        use_vector_index = True


class EmbeddedWordChunk(EmbeddedChunk):
    link: str

    class Config:
        name = "embedded_docx"
        category = DataCategory.DOCX
        use_vector_index = True
