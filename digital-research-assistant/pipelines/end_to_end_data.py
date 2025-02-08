from zenml import pipeline

from .extract_data_etl import extract_data_etl
from .feature_engineering import feature_engineering
from .generate_datasets import generate_datasets


@pipeline
def end_to_end_data(
    author_names,  # : list[dict[str, str | list[str]]],
    test_split_size: float = 0.1,
    push_to_huggingface: bool = False,
    dataset_id: str | None = None,
    mock: bool = False,
) -> None:
    wait_for_ids = []
    for author_data in author_names:
        last_step_invocation_id = extract_data_etl(
            user_full_name=author_data["user_full_name"][0]
        )

        wait_for_ids.append(last_step_invocation_id)

    author_full_names = [author_data["user_full_name"][0]
                         for author_data in author_names]
    wait_for_ids = feature_engineering(
        user_full_name=author_full_names, wait_for=wait_for_ids)

    generate_datasets(
        test_split_size=test_split_size,
        push_to_huggingface=push_to_huggingface,
        dataset_id=dataset_id,
        mock=mock,
        wait_for=wait_for_ids,
    )
