from zenml import pipeline

from steps.etl import extract_documents, get_or_create_user


@pipeline
def extract_data_etl(user_full_name: str) -> str:
    user = get_or_create_user(user_full_name)
    last_step = extract_documents(user, user_full_name)

    return last_step.invocation_id
