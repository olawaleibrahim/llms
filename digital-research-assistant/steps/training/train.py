from zenml import step

from digital_research_assistant.model.finetuning.sagemaker import run_finetuning_on_sagemaker


@step
def train(
    finetuning_type: str,
    num_train_epochs: int,
    per_device_train_batch_size: int,
    learning_rate: float,
    dataset_huggingface_workspace: str = "olawaleibrahim",
    is_dummy: bool = False,
) -> None:
    run_finetuning_on_sagemaker(
        finetuning_type=finetuning_type,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        learning_rate=learning_rate,
        dataset_huggingface_workspace=dataset_huggingface_workspace,
        is_dummy=is_dummy,
    )
