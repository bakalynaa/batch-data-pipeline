# src/utils/validation.py

from pathlib import Path
from pyspark.sql import DataFrame


def check_file_exists(path: str) -> None:
    if not Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")


def check_input_files_exist(paths: list[str]) -> None:
    for path in paths:
        check_file_exists(path)


def validate_required_columns(
    df: DataFrame,
    required_columns: list[str],
    dataset_name: str,
) -> None:
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: {sorted(missing_columns)}"
        )


def validate_output_not_empty(df: DataFrame) -> None:
    if df.count() == 0:
        raise ValueError("Output dataframe is empty")