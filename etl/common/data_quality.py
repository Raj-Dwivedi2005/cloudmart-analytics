
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from etl.common.logger import get_logger

logger = get_logger("DataQuality")


class DataQualityException(Exception):
    """Custom exception raised when a Data Quality threshold is breached."""


class DataQualityValidator:
    """Production PySpark Data Quality Validator."""

    def __init__(self, df: DataFrame, name: str = "Dataset"):
        self.df = df
        self.name = name

    def check_non_empty(self) -> "DataQualityValidator":
        """Verifies that the DataFrame is not empty."""
        count_records = self.df.count()
        logger.info(f"[{self.name}] Record count check: {count_records} records.")
        if count_records == 0:
            raise DataQualityException(f"Data Quality Error: {self.name} is empty!")
        return self

    def check_required_columns(self, required_cols: list[str]) -> "DataQualityValidator":
        """Validates that mandatory columns exist in the DataFrame schema."""
        missing = [c for c in required_cols if c not in self.df.columns]
        if missing:
            raise DataQualityException(
                f"Data Quality Error: {self.name} missing required columns: {missing}"
            )
        logger.info(f"[{self.name}] All required columns present: {required_cols}")
        return self

    def check_null_threshold(
        self, primary_keys: list[str], max_null_pct: float = 0.0
    ) -> "DataQualityValidator":
        """Ensures specified columns do not exceed allowed null percentage threshold.

        Args:
            primary_keys (List[str]): Columns to check for null values.
            max_null_pct (float): Maximum acceptable ratio of nulls (0.0 = 0%).
        """
        total_count = self.df.count()
        if total_count == 0:
            return self

        for col_name in primary_keys:
            null_count = self.df.filter(
                col(col_name).isNull() | (col(col_name) == "")
            ).count()
            null_pct = null_count / total_count
            logger.info(
                f"[{self.name}] Null check for '{col_name}': {null_count} nulls ({null_pct:.2%})"
            )
            if null_pct > max_null_pct:
                raise DataQualityException(
                    f"Data Quality Error: Column '{col_name}' in {self.name} "
                    f"has {null_pct:.2%} nulls, exceeding allowed threshold of {max_null_pct:.2%}"
                )
        return self

    def check_duplicates(self, unique_keys: list[str]) -> "DataQualityValidator":
        """Validates uniqueness across specified key combinations."""
        duplicate_count = (
            self.df.groupBy(unique_keys)
            .count()
            .filter(col("count") > 1)
            .count()
        )
        if duplicate_count > 0:
            raise DataQualityException(
                f"Data Quality Error: Found {duplicate_count} duplicate groups on keys {unique_keys} in {self.name}"
            )
        logger.info(f"[{self.name}] Zero duplicate key groups found on {unique_keys}")
        return self

    def run_all_checks(
        self, required_cols: list[str], primary_keys: list[str]
    ) -> bool:
        """Executes all standard data quality assertions."""
        self.check_non_empty()
        self.check_required_columns(required_cols)
        self.check_null_threshold(primary_keys)
        self.check_duplicates(primary_keys)
        logger.info(f"[{self.name}] ALL DATA QUALITY CHECKS PASSED.")
        return True
