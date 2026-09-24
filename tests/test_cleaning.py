from etl.transform.clean_sales import SalesTransformer


def test_clean_orders_computations(spark):
    """Tests that SalesTransformer correctly computes gross and net amounts and filters invalid rows."""
    raw_data = [
        ("ORD_001", "CUST_001", "PROD_001", "2026-09-24 10:00:00", 2, 50.00, 5.00),
        ("ORD_002", "CUST_002", "PROD_002", "2026-09-24 11:00:00", 0, 100.00, 0.00),  # invalid quantity=0
        ("ORD_003", "CUST_003", "PROD_003", "2026-09-24 12:00:00", 1, -10.00, 0.00),  # invalid unit_price<0
    ]
    columns = ["order_id", "customer_id", "product_id", "order_timestamp", "quantity", "unit_price", "discount_amount"]
    raw_df = spark.createDataFrame(raw_data, columns)

    cleaned_df = SalesTransformer.clean_orders(raw_df)
    results = cleaned_df.collect()

    # Verify invalid rows (quantity=0, price<0) were filtered out
    assert len(results) == 1

    row = results[0]
    assert row["order_id"] == "ORD_001"
    assert float(row["gross_amount"]) == 100.00  # 2 * 50.00
    assert float(row["net_amount"]) == 95.00     # 100.00 - 5.00
    assert row["order_year"] == 2026
    assert row["order_month"] == 9
