import pytest
from pyspark.sql import SparkSession

from src.jobs.daily_revenue_by_country import transform


@pytest.fixture(scope="session")
def spark():
    spark_session = (
        SparkSession.builder
        .master("local[1]")
        .appName("daily_revenue_tests")
        .getOrCreate()
    )

    yield spark_session

    spark_session.stop()


def collect_result(df):
    return {
        (row["order_date"], row["country"]): row.asDict()
        for row in df.collect()
    }


def test_revenue_calculation_for_completed_orders(spark):
    users_df = spark.createDataFrame(
        [
            (1, "Ukraine"),
            (2, "Poland"),
        ],
        ["user_id", "country"],
    )

    orders_df = spark.createDataFrame(
        [
            (101, 1, "2024-01-01", 100.0, "completed"),
            (102, 1, "2024-01-01", 50.0, "completed"),
            (103, 2, "2024-01-01", 70.0, "cancelled"),
        ],
        ["order_id", "user_id", "order_date", "amount", "status"],
    )

    result = collect_result(transform(users_df, orders_df))

    row = result[("2024-01-01", "Ukraine")]

    assert row["total_revenue"] == 150.0
    assert row["completed_orders_count"] == 2
    assert row["unique_customers_count"] == 1
    assert row["avg_order_value"] == 75.0


def test_cancelled_orders_are_ignored(spark):
    users_df = spark.createDataFrame(
        [(1, "Ukraine")],
        ["user_id", "country"],
    )

    orders_df = spark.createDataFrame(
        [
            (101, 1, "2024-01-01", 100.0, "cancelled"),
        ],
        ["order_id", "user_id", "order_date", "amount", "status"],
    )

    result_df = transform(users_df, orders_df)

    assert result_df.count() == 0


def test_orders_are_grouped_by_date_and_country(spark):
    users_df = spark.createDataFrame(
        [
            (1, "Ukraine"),
            (2, "Ukraine"),
            (3, "Poland"),
        ],
        ["user_id", "country"],
    )

    orders_df = spark.createDataFrame(
        [
            (101, 1, "2024-01-01", 100.0, "completed"),
            (102, 2, "2024-01-01", 200.0, "completed"),
            (103, 3, "2024-01-01", 300.0, "completed"),
            (104, 1, "2024-01-02", 50.0, "completed"),
        ],
        ["order_id", "user_id", "order_date", "amount", "status"],
    )

    result = collect_result(transform(users_df, orders_df))

    assert result[("2024-01-01", "Ukraine")]["total_revenue"] == 300.0
    assert result[("2024-01-01", "Poland")]["total_revenue"] == 300.0
    assert result[("2024-01-02", "Ukraine")]["total_revenue"] == 50.0


def test_unique_customers_count(spark):
    users_df = spark.createDataFrame(
        [
            (1, "Ukraine"),
            (2, "Ukraine"),
        ],
        ["user_id", "country"],
    )

    orders_df = spark.createDataFrame(
        [
            (101, 1, "2024-01-01", 100.0, "completed"),
            (102, 1, "2024-01-01", 150.0, "completed"),
            (103, 2, "2024-01-01", 200.0, "completed"),
        ],
        ["order_id", "user_id", "order_date", "amount", "status"],
    )

    result = collect_result(transform(users_df, orders_df))

    row = result[("2024-01-01", "Ukraine")]

    assert row["completed_orders_count"] == 3
    assert row["unique_customers_count"] == 2


def test_output_schema(spark):
    users_df = spark.createDataFrame(
        [(1, "Ukraine")],
        ["user_id", "country"],
    )

    orders_df = spark.createDataFrame(
        [(101, 1, "2024-01-01", 100.0, "completed")],
        ["order_id", "user_id", "order_date", "amount", "status"],
    )

    result_df = transform(users_df, orders_df)

    assert result_df.columns == [
        "order_date",
        "country",
        "total_revenue",
        "completed_orders_count",
        "unique_customers_count",
        "avg_order_value",
    ]