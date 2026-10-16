from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


PROJECT_ROOT = "/opt/airflow"


def check_input_data():
    required_files = [
        f"{PROJECT_ROOT}/data/raw/users.csv",
        f"{PROJECT_ROOT}/data/raw/orders.csv",
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Missing input file: {file_path}")


def validate_output_data():
    output_path = Path(f"{PROJECT_ROOT}/data/curated/daily_revenue_by_country")

    if not output_path.exists():
        raise FileNotFoundError(f"Output folder not found: {output_path}")

    parquet_files = list(output_path.rglob("*.parquet"))

    if not parquet_files:
        raise ValueError("No Parquet files found in output folder")


default_args = {
    "owner": "student",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="ecommerce_daily_revenue_pipeline",
    default_args=default_args,
    description="Batch pipeline: CSV -> PySpark -> Parquet",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["ecommerce", "pyspark", "parquet"],
) as dag:

    check_input_data_task = PythonOperator(
        task_id="check_input_data",
        python_callable=check_input_data,
    )

    run_spark_job_task = BashOperator(
        task_id="run_spark_job",
        bash_command=(
            "cd /opt/airflow && "
            "PYTHONPATH=/opt/airflow "
            "python src/jobs/daily_revenue_by_country.py"
        ),
    )

    validate_output_data_task = PythonOperator(
        task_id="validate_output_data",
        python_callable=validate_output_data,
    )

    check_input_data_task >> run_spark_job_task >> validate_output_data_task