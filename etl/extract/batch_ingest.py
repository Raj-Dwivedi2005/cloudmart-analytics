from pyspark.sql import DataFrame, SparkSession

from etl.common.logger import get_logger

logger = get_logger("BatchIngest")


class BatchIngestor:
    """Ingests raw CSV/JSON batch drop files from S3 raw landing zone."""

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_csv(self, path: str, header: bool = True, infer_schema: bool = True) -> DataFrame:
        """Reads raw CSV dataset into a PySpark DataFrame."""
        logger.info(f"Reading CSV batch drop from path: {path}")
        return self.spark.read.option("header", str(header)).option("inferSchema", str(infer_schema)).csv(path)

    def read_json(self, path: str, multiline: bool = False) -> DataFrame:
        """Reads raw JSON dataset into a PySpark DataFrame."""
        logger.info(f"Reading JSON batch drop from path: {path}")
        return self.spark.read.option("multiline", str(multiline)).json(path)
