from zenml import pipeline

from steps.etl import crawl_paperlinks, get_or_create_user


@pipeline
def digital_data_etl(user_full_name: str) -> str:
    user = get_or_create_user(user_full_name)
    last_step = crawl_paperlinks(user, user_full_name)

    return last_step.invocation_id
