from loguru import logger
import os
from tqdm import tqdm
from pathlib import Path
from typing_extensions import Annotated
from zenml import get_step_context, step

from digital_research_assistant.domain.documents import UserDocument


@step
def crawl_paperlinks(user: UserDocument, user_full_name: str) -> Annotated[list[str], "crawl_paperlinks"]:

    logger.info(f"Starting to append user filepaths ")

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    # ROOT_DIR = "/home/olawale/Desktop/PROJECTS/llms/digital-research-assistant/data/input/"
    username = f"/data/input/{user_full_name}/"
    dir_path = str(ROOT_DIR) + username
    filepaths = os.listdir(dir_path)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="crawl_paperlinks", metadata=_get_metadata(user_full_name, filepaths))
    print("filepaths", filepaths)

    return filepaths


def _get_metadata(user_full_name: str, filepaths: list) -> dict:
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "filepaths": filepaths,
        },
    }
