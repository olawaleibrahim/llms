from zenml import pipeline

from steps import feature_engineering as fe


@pipeline
def feature_engineering(user_full_name: list[str], wait_for: str | list[str] | None = None) -> list[str]:
    retrieved_user_documents = fe.query_data_warehouse(
        user_full_name, after=wait_for)
    cleaned_documents = fe.clean_documents(retrieved_user_documents)
    populate_cleaned_step = fe.populate_vector_db(cleaned_documents)

    embedded_documents = fe.chunk_and_embed(cleaned_documents)
    populate_embedded_step = fe.populate_vector_db(embedded_documents)

    assert type(populate_embedded_step) == type(populate_cleaned_step)
