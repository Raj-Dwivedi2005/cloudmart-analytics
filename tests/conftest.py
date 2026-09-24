import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Provides a local PySpark SparkSession fixture for testing ETL logic."""
    spark_session = (
        SparkSession.builder.master("local[2]")
        .appName("CloudMartETLTests")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark_session
    spark_session.stop()
