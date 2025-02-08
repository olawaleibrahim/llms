import os
from pathlib import Path

from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from digital_research_assistant.domain.documents import UserDocument
from steps.etl import utils


@step
def extract_documents(user: UserDocument, user_full_name: str) -> Annotated[list[str], "extract_documents"]:

    logger.info("Starting to append user filepaths ")

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    user_dir = f"/data/input/{user_full_name}/"
    dir_path = str(ROOT_DIR) + user_dir
    filepaths = os.listdir(dir_path)

    for filepath in tqdm(filepaths):
        extractor = utils.use_extractor(filepath)
        filepath = dir_path + filepath
        content = extractor.extract(filepath=filepath, user=user,
                                    user_full_name=user_full_name)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="extract_documents", metadata=_get_metadata(user_full_name, filepaths, content))
    logger.info("filepaths", filepaths)

    return filepaths


def _get_metadata(user_full_name: str, filepaths: list, content: str) -> dict:
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "filepaths": filepaths,
            "content": content,
        },
    }
