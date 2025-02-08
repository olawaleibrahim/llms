from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from digital_research_assistant.domain.cleaned_documents import (
    CleanedDocument,
    CleanedPDFDocument,
    CleanedWordDocument,
)
from digital_research_assistant.domain.documents import (
    Document,
    PDFDocument,
    WordDocument,
)

from .operations import clean_text

DocumentT = TypeVar("DocumentT", bound=Document)
CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)


class CleaningDataHandler(ABC, Generic[DocumentT, CleanedDocumentT]):
    """
    Abstract class for all cleaning data handlers.
    All data transformations logic for the cleaning step is done here
    """

    @abstractmethod
    def clean(self, data_model: DocumentT) -> CleanedDocumentT:
        pass


class PDFCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: PDFDocument) -> CleanedPDFDocument:
        return CleanedPDFDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(data_model.content.values())),
            filetype=data_model.filetype,
            filepath=data_model.filepath,
            author_id=data_model.author_id,
            author_full_name=data_model.author_full_name,
        )


class WordCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: WordDocument) -> CleanedWordDocument:
        return CleanedWordDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(data_model.content.values())),
            filetype=data_model.filetype,
            filepath=data_model.filepath,
            author_id=data_model.author_id,
            author_full_name=data_model.author_full_name,
        )
