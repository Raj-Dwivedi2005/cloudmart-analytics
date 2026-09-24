import pytest

from etl.common.data_quality import DataQualityException, DataQualityValidator


def test_data_quality_null_check_pass(spark):
    """Tests that DataQualityValidator passes clean data with zero nulls."""
    data = [("CUST_001", "John"), ("CUST_002", "Jane")]
    df = spark.createDataFrame(data, ["customer_id", "name"])

    validator = DataQualityValidator(df, name="CustomerTest")
    assert validator.run_all_checks(required_cols=["customer_id", "name"], primary_keys=["customer_id"]) is True


def test_data_quality_null_check_fail(spark):
    """Tests that DataQualityValidator raises exception when nulls exceed threshold."""
    data = [("CUST_001", "John"), (None, "Jane")]
    df = spark.createDataFrame(data, ["customer_id", "name"])

    validator = DataQualityValidator(df, name="CustomerTest")
    with pytest.raises(DataQualityException):
        validator.check_null_threshold(primary_keys=["customer_id"], max_null_pct=0.0)


def test_data_quality_duplicate_check_fail(spark):
    """Tests that DataQualityValidator catches duplicate primary key values."""
    data = [("CUST_001", "John"), ("CUST_001", "Johnny")]
    df = spark.createDataFrame(data, ["customer_id", "name"])

    validator = DataQualityValidator(df, name="CustomerTest")
    with pytest.raises(DataQualityException):
        validator.check_duplicates(unique_keys=["customer_id"])
