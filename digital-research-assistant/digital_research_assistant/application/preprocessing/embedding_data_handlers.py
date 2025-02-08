from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast

from digital_research_assistant.application.networks import EmbeddingModelSingleton
from digital_research_assistant.domain.chunks import Chunk, PDFChunk, WordChunk
from digital_research_assistant.domain.embedded_chunks import (
    EmbeddedChunk,
    EmbeddedPDFChunk,
    EmbeddedWordChunk,
)
from digital_research_assistant.domain.queries import EmbeddedQuery, Query

ChunkT = TypeVar("ChunkT", bound=Chunk)
EmbeddedChunkT = TypeVar("EmbeddedChunkT", bound=EmbeddedChunk)

embedding_model = EmbeddingModelSingleton()


class EmbeddingDataHandler(ABC, Generic[ChunkT, EmbeddedChunkT]):
    """
    Abstract class for all embedding data handlers.
    All data transformations logic for the embedding step is done here
    """

    def embed(self, data_model: ChunkT) -> EmbeddedChunkT:
        return self.embed_batch([data_model])[0]

    def embed_batch(self, data_model: list[ChunkT]) -> list[EmbeddedChunkT]:
        embedding_model_input = [
            data_model.content for data_model in data_model]
        embeddings = embedding_model(embedding_model_input, to_list=True)

        embedded_chunk = [
            self.map_model(data_model, cast(list[float], embedding))
            for data_model, embedding in zip(data_model, embeddings, strict=False)
        ]

        return embedded_chunk

    @abstractmethod
    def map_model(self, data_model: ChunkT, embedding: list[float]) -> EmbeddedChunkT:
        pass


class QueryEmbeddingHandler(EmbeddingDataHandler):
    def map_model(self, data_model: Query, embedding: list[float]) -> EmbeddedQuery:
        return EmbeddedQuery(
            id=data_model.id,
            author_id=data_model.author_id,
            author_full_name=data_model.author_full_name,
            content=data_model.content,
            embedding=embedding,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )


class PDFEmbeddingHandler(EmbeddingDataHandler):
    def map_model(self, data_model: PDFChunk, embedding: list[float]) -> EmbeddedPDFChunk:
        return EmbeddedPDFChunk(
            id=data_model.id,
            content=data_model.content,
            embedding=embedding,
            filetype=data_model.filetype,
            document_id=data_model.document_id,
            author_id=data_model.author_id,
            author_full_name=data_model.author_full_name,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )


class WordEmbeddingHandler(EmbeddingDataHandler):
    def map_model(self, data_model: WordChunk, embedding: list[float]) -> EmbeddedWordChunk:
        return EmbeddedWordChunk(
            id=data_model.id,
            content=data_model.content,
            embedding=embedding,
            filetype=data_model.filetype,
            link=data_model.filepath,
            document_id=data_model.document_id,
            author_id=data_model.author_id,
            author_full_name=data_model.author_full_name,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )