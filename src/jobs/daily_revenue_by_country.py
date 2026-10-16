from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def transform(users_df: DataFrame, orders_df: DataFrame) -> DataFrame:
    """
    Transform raw users and orders data into daily revenue by country.

    Expected output columns:
    - order_date
    - country
    - total_revenue
    - completed_orders_count
    - unique_customers_count
    - avg_order_value

    Hints:
    - Use only completed orders.
    - Join orders with users by user_id.
    - Aggregate by order_date and country.
    - Use PySpark functions, not pandas.
    """

    completed_orders_df = orders_df.filter(F.col("status") == "completed")

    joined_df = completed_orders_df.join(
        users_df.select("user_id", "country"), on="user_id", how="inner"
    )

    result_df = joined_df.groupBy("order_date", "country").agg(
        F.sum("amount").alias("total_revenue"),
        F.count("order_id").alias("completed_orders_count"),
        F.countDistinct("user_id").alias("unique_customers_count"),
    )

    result_df = result_df.withColumn(
        "avg_order_value",
        F.col("total_revenue") / F.col("completed_orders_count"),
    )

    return result_df.select(
        "order_date",
        "country",
        "total_revenue",
        "completed_orders_count",
        "unique_customers_count",
        "avg_order_value",
    )


def main() -> None:
    from pyspark.sql import SparkSession

    from src.utils.config import load_config
    from src.utils.validation import (
        check_input_files_exist,
        validate_output_not_empty,
        validate_required_columns,
    )

    config = load_config()
    paths = config["paths"]
    check_input_files_exist([paths["users"], paths["orders"]])

    spark = SparkSession.builder.appName("daily_revenue_by_country").getOrCreate()
    try:
        users_df = spark.read.csv(paths["users"], header=True, inferSchema=True)
        orders_df = spark.read.csv(paths["orders"], header=True, inferSchema=True)

        validate_required_columns(
            users_df, ["user_id", "country", "registration_date"], "users"
        )
        validate_required_columns(
            orders_df,
            ["order_id", "user_id", "order_date", "amount", "status"],
            "orders",
        )

        result_df = transform(users_df, orders_df)
        validate_output_not_empty(result_df)

        (
            result_df.write.mode("overwrite")
            .partitionBy("order_date")
            .parquet(paths["output"])
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
