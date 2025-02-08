from docx import Document
from loguru import logger

from digital_research_assistant.domain.documents import WordDocument


def extract_text_from_word(doc_path):
    document = Document(doc_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()


class WordExtractor():
    model = WordDocument

    def extract(self, filepath: str, **kwargs) -> None:
        old_model = self.model.find(filepath=filepath)
        if old_model is not None:
            logger.info(f"Word doc already exists in the database: {filepath}")

            return

        logger.info(f"Starting extracting word: {filepath}")
        content = extract_text_from_word(filepath)

        data = {
            "Title": filepath,
            "Content": content
        }

        user = kwargs["user"]
        user_full_name = kwargs["user_full_name"]
        instance = self.model(
            filetype="docx",
            content=data,
            filepath=filepath,
            author_id=user.id,
            author_full_name=user_full_name,
        )

        instance.save()

        logger.info(f"Successfully extracted and saved file: {filepath}")

        return content
