from zenml import step

from digital_research_assistant.model.evaluation.sagemaker import run_evaluation_on_sagemaker


@step
def evaluate(
    is_dummy: bool = False,
) -> None:
    run_evaluation_on_sagemaker(
        is_dummy=is_dummy,
    )
