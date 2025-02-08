from functools import cached_property
from pathlib import Path
from typing import Optional

import numpy as np
from loguru import logger
from numpy.typing import NDArray
from sentence_transformers.SentenceTransformer import SentenceTransformer
from sentence_transformers.cross_encoder import CrossEncoder
from transformers import AutoTokenizer

from digital_research_assistant.settings import settings

from .base import SingletonMeta


class EmbeddingModelSingleton(metaclass=SingletonMeta):
    """
    A singleton class that provides a pre-trained transformer model for generating embeddings of input text.
    """

    def __init__(
        self,
        model_id: str = settings.TEXT_EMBEDDING_MODEL_ID,
        device: str = settings.RAG_MODEL_DEVICE,
        cache_dir: Optional[Path] = None,
    ) -> None:
        self._model_id = model_id
        self._device = device

        self._model = SentenceTransformer(
            self._model_id,
            device=self._device,
            cache_folder=str(cache_dir) if cache_dir else None,
        )
        self._model.eval()

    @property
    def model_id(self) -> str:
        """
        Returns the identifier of the pre-trained transformer model to use.

        Returns:
            str: The identifier of the pre-trained transformer model to use.
        """

        return self._model_id

    @cached_property
    def embedding_size(self) -> int:
        """
        Returns the size of the embeddings generated by the pre-trained transformer model.

        Returns:
            int: The size of the embeddings generated by the pre-trained transformer model.
        """

        dummy_embedding = self._model.encode("")

        return dummy_embedding.shape[0]

    @property
    def max_input_length(self) -> int:
        """
        Returns the maximum length of input text to tokenize.

        Returns:
            int: The maximum length of input text to tokenize.
        """

        return self._model.max_seq_length

    @property
    def tokenizer(self) -> AutoTokenizer:
        """
        Returns the tokenizer used to tokenize input text.

        Returns:
            AutoTokenizer: The tokenizer used to tokenize input text.
        """

        return self._model.tokenizer

    def __call__(
        self, input_text: str | list[str], to_list: bool = True
    ) -> NDArray[np.float32] | list[float] | list[list[float]]:
        """
        Generates embeddings for the input text using the pre-trained transformer model.

        Args:
            input_text (str): The input text to generate embeddings for.
            to_list (bool): Whether to return the embeddings as a list or numpy array. Defaults to True.

        Returns:
            Union[np.ndarray, list]: The embeddings generated for the input text.
        """

        try:
            embeddings = self._model.encode(input_text)
        except Exception:
            logger.error(
                f"Error generating embeddings for {self._model_id=} and {input_text=}")

            return [] if to_list else np.array([])

        if to_list:
            embeddings = embeddings.tolist()

        return embeddings


class CrossEncoderModelSingleton(metaclass=SingletonMeta):
    def __init__(
        self,
        model_id: str = settings.RERANKING_CROSS_ENCODER_MODEL_ID,
        device: str = settings.RAG_MODEL_DEVICE,
    ) -> None:
        """
        A singleton class that provides a pre-trained cross-encoder model for scoring pairs of input text.
        """

        self._model_id = model_id
        self._device = device

        self._model = CrossEncoder(
            model_name=self._model_id,
            device=self._device,
        )
        self._model.model.eval()

    def __call__(self, pairs: list[tuple[str, str]], to_list: bool = True) -> NDArray[np.float32] | list[float]:
        scores = self._model.predict(pairs)

        if to_list:
            scores = scores.tolist()

        return scores
