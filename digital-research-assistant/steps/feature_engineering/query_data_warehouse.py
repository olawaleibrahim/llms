from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step

from digital_research_assistant.domain.base.nosql import NoSQLBaseDocument
from digital_research_assistant.domain.documents import Document, PDFDocument, UserDocument, WordDocument


@step
def query_data_warehouse(
    user_full_names: list[str],
) -> Annotated[list, "raw_documents"]:
    documents = []
    authors = []
    for user_full_name in user_full_names:
        logger.info(f"Querying data warehouse for user: {user_full_name}")

        user_full_name = user_full_name.split("_")
        first_name, last_name = user_full_name[0], user_full_name[1]
        logger.info(f"First name: {first_name}, Last name: {last_name}")
        user = UserDocument.get_or_create(
            first_name=first_name, last_name=last_name)
        authors.append(user)

        results = fetch_all_data(user)
        user_documents = [doc for query_result in results.values()
                          for doc in query_result]

        documents.extend(user_documents)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="raw_documents", metadata=_get_metadata(documents))

    return documents


def fetch_all_data(user: UserDocument) -> dict[str, list[NoSQLBaseDocument]]:
    user_id = str(user.id)
    with ThreadPoolExecutor() as executor:
        future_to_query = {
            executor.submit(__fetch_pdfs, user_id): "pdfs",
            executor.submit(__fetch_docx, user_id): "docx",
        }

        results = {}
        for future in as_completed(future_to_query):
            query_name = future_to_query[future]
            try:
                results[query_name] = future.result()
            except Exception:
                logger.exception(f"'{query_name}' request failed.")

                results[query_name] = []

    return results


def __fetch_pdfs(user_id) -> list[NoSQLBaseDocument]:
    return PDFDocument.bulk_find(author_id=user_id)


def __fetch_docx(user_id) -> list[NoSQLBaseDocument]:
    return WordDocument.bulk_find(author_id=user_id)


def _get_metadata(documents: list[Document]) -> dict:
    metadata = {
        "num_documents": len(documents),
    }
    for document in documents:
        collection = document.get_collection_name()
        if collection not in metadata:
            metadata[collection] = {}
        if "authors" not in metadata[collection]:
            metadata[collection]["authors"] = list()

        metadata[collection]["num_documents"] = metadata[collection].get(
            "num_documents", 0) + 1
        metadata[collection]["authors"].append(document.author_full_name)

    for value in metadata.values():
        if isinstance(value, dict) and "authors" in value:
            value["authors"] = list(set(value["authors"]))

    return metadata
