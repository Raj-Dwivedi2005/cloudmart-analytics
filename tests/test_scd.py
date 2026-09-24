from etl.transform.scd_handler import SCD2Handler


def test_scd2_initial_load(spark):
    """Tests SCD Type 2 initial dimension load when existing dimension is empty."""
    updates_data = [
        ("CUST_001", "John", "Doe", "VIP", "US"),
        ("CUST_002", "Jane", "Smith", "Standard", "CA")
    ]
    cols = ["customer_id", "first_name", "last_name", "customer_segment", "country"]
    updates_df = spark.createDataFrame(updates_data, cols)

    scd_df = SCD2Handler.process_scd2(
        existing_dim_df=None,
        updates_df=updates_df,
        natural_key="customer_id",
        tracked_attributes=["customer_segment", "country"],
        effective_date_str="2026-01-01"
    )

    results = scd_df.collect()
    assert len(results) == 2
    for r in results:
        assert r["is_current"] == True
        assert str(r["end_date"]) == "9999-12-31"
        assert r["version"] == 1


def test_scd2_update_tracking(spark):
    """Tests SCD Type 2 updates expire previous active records and create new active records."""
    # Existing active dimension
    existing_data = [
        ("CUST_001", "John", "Doe", "Standard", "US", "2025-01-01", "9999-12-31", True, 1)
    ]
    existing_cols = ["customer_id", "first_name", "last_name", "customer_segment", "country", "effective_date", "end_date", "is_current", "version"]
    existing_df = spark.createDataFrame(existing_data, existing_cols)

    # Incoming update: Customer segment upgraded from Standard to VIP
    updates_data = [
        ("CUST_001", "John", "Doe", "VIP", "US")
    ]
    update_cols = ["customer_id", "first_name", "last_name", "customer_segment", "country"]
    updates_df = spark.createDataFrame(updates_data, update_cols)

    scd_df = SCD2Handler.process_scd2(
        existing_dim_df=existing_df,
        updates_df=updates_df,
        natural_key="customer_id",
        tracked_attributes=["customer_segment", "country"],
        effective_date_str="2026-09-01"
    )

    results = scd_df.collect()
    assert len(results) == 2

    # Verify expired record
    expired = next(r for r in results if not r["is_current"])
    assert expired["customer_segment"] == "Standard"
    assert str(expired["end_date"]) == "2026-09-01"

    # Verify new active record
    active = next(r for r in results if r["is_current"])
    assert active["customer_segment"] == "VIP"
    assert str(active["effective_date"]) == "2026-09-01"
    assert active["version"] == 2
