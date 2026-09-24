from pyspark.sql import DataFrame
from pyspark.sql.functions import coalesce, col, concat_ws, lit, sha2, to_date

from etl.common.logger import get_logger

logger = get_logger("SCDHandler")


class SCD2Handler:
    """Implements Slowly Changing Dimension Type 2 (SCD2) logic in PySpark."""

    @staticmethod
    def process_scd2(
        existing_dim_df: DataFrame,
        updates_df: DataFrame,
        natural_key: str,
        tracked_attributes: list,
        effective_date_str: str = "2026-01-01"
    ) -> DataFrame:
        """Merges incoming updates with existing dimension table producing SCD Type 2 history.

        Args:
            existing_dim_df (DataFrame): Existing dimension table (may be empty).
            updates_df (DataFrame): Incoming incremental dataset.
            natural_key (str): Business key column name (e.g., 'customer_id' or 'product_id').
            tracked_attributes (list): List of attribute column names to monitor for changes.
            effective_date_str (str): Date of update batch.

        Returns:
            DataFrame: Updated dimension table with historical and active records (SCD2).
        """
        logger.info(f"Processing SCD Type 2 for natural key: {natural_key}")

        # Compute hash of tracked attributes to detect changes efficiently
        updates_with_hash = updates_df.withColumn(
            "attr_hash",
            sha2(concat_ws("||", *[col(c) for c in tracked_attributes]), 256)
        )

        if existing_dim_df is None or existing_dim_df.rdd.isEmpty():
            logger.info("Existing dimension is empty. Creating initial active SCD2 records.")
            initial_dim = (
                updates_with_hash
                .withColumn("effective_date", to_date(lit(effective_date_str)))
                .withColumn("end_date", to_date(lit("9999-12-31")))
                .withColumn("is_current", lit(True))
                .withColumn("version", lit(1))
            )
            return initial_dim

        # Compute hash on existing active dimension records
        existing_active = existing_dim_df.filter(col("is_current") == True).withColumn(
            "existing_attr_hash",
            sha2(concat_ws("||", *[col(c) for c in tracked_attributes]), 256)
        )
        existing_inactive = existing_dim_df.filter(col("is_current") == False)

        # Identify changed records
        joined = updates_with_hash.alias("u").join(
            existing_active.alias("e"),
            col(f"u.{natural_key}") == col(f"e.{natural_key}"),
            "left"
        )

        # Expired records (existing records that got updated)
        expired_records = (
            joined.filter(
                col("e.existing_attr_hash").isNotNull() &
                (col("u.attr_hash") != col("e.existing_attr_hash"))
            )
            .select("e.*")
            .withColumn("end_date", to_date(lit(effective_date_str)))
            .withColumn("is_current", lit(False))
            .drop("existing_attr_hash")
        )

        # New active records (brand new keys or updated keys with new effective date)
        new_active = (
            joined.filter(
                col("e.existing_attr_hash").isNull() |
                (col("u.attr_hash") != col("e.existing_attr_hash"))
            )
            .select("u.*")
            .withColumn("effective_date", to_date(lit(effective_date_str)))
            .withColumn("end_date", to_date(lit("9999-12-31")))
            .withColumn("is_current", lit(True))
            .withColumn(
                "version",
                coalesce(col("e.version"), lit(0)) + 1
            )
        )

        # Unchanged existing active records
        unchanged_active = (
            joined.filter(
                col("e.existing_attr_hash").isNotNull() &
                (col("u.attr_hash") == col("e.existing_attr_hash"))
            )
            .select("e.*")
            .drop("existing_attr_hash")
        )

        # Union all components to form complete SCD2 dimension
        final_dim = existing_inactive.unionByName(expired_records).unionByName(new_active).unionByName(unchanged_active)
        logger.info(f"SCD Type 2 processing completed. Final total rows: {final_dim.count()}")
        return final_dim
