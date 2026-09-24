from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    coalesce,
    col,
    dayofmonth,
    lit,
    month,
    quarter,
    to_timestamp,
    year,
)
from pyspark.sql.functions import round as spark_round

from etl.common.logger import get_logger

logger = get_logger("CleanSales")


class SalesTransformer:
    """Transforms raw e-commerce sales transactions into cleansed analytical datasets."""

    @staticmethod
    def clean_orders(df: DataFrame) -> DataFrame:
        """Cleans and standardizes raw sales transaction records.

        Performs:
        - Timestamp formatting
        - Price & Quantity validation (quantity > 0, unit_price >= 0)
        - Net Revenue computation: (quantity * unit_price) - discount_amount
        - Partition column additions (year, month)
        """
        logger.info("Starting Sales Orders cleaning transformation...")

        cleaned_df = (
            df.withColumn("order_timestamp", to_timestamp(col("order_timestamp")))
            .withColumn("quantity", col("quantity").cast("integer"))
            .withColumn("unit_price", col("unit_price").cast("decimal(10,2)"))
            .withColumn("discount_amount", coalesce(col("discount_amount").cast("decimal(10,2)"), lit(0.00)))
            .filter((col("quantity") > 0) & (col("unit_price") >= 0))
            .withColumn(
                "gross_amount",
                spark_round(col("quantity") * col("unit_price"), 2)
            )
            .withColumn(
                "net_amount",
                spark_round((col("quantity") * col("unit_price")) - col("discount_amount"), 2)
            )
            .withColumn("order_year", year(col("order_timestamp")))
            .withColumn("order_month", month(col("order_timestamp")))
            .withColumn("order_quarter", quarter(col("order_timestamp")))
            .withColumn("order_day", dayofmonth(col("order_timestamp")))
        )

        logger.info("Sales Orders cleaning transformation completed successfully.")
        return cleaned_df
