from pyspark.sql import DataFrame

from etl.common.logger import get_logger

logger = get_logger("RedshiftLoader")


class RedshiftLoader:
    """Handles PySpark DataFrame writing to Amazon Redshift and S3 Curated Data Lake."""

    def __init__(self, redshift_url: str, temp_s3_dir: str):
        self.redshift_url = redshift_url
        self.temp_s3_dir = temp_s3_dir

    def save_to_s3_parquet(
        self, df: DataFrame, s3_target_path: str, mode: str = "overwrite", partition_cols: list | None = None
    ):
        """Writes PySpark DataFrame to S3 Curated Zone in Parquet format."""
        logger.info(f"Writing DataFrame to S3 Parquet target: {s3_target_path}")
        writer = df.write.mode(mode).format("parquet")
        if partition_cols:
            writer = writer.partitionBy(*partition_cols)
        writer.save(s3_target_path)
        logger.info("S3 Parquet write completed successfully.")

    def load_to_redshift_table(
        self,
        df: DataFrame,
        target_table: str,
        iam_role_arn: str,
        mode: str = "append"
    ):
        """Loads PySpark DataFrame directly into Redshift table using standard spark-redshift connector."""
        logger.info(f"Loading DataFrame into Redshift table: {target_table} (mode: {mode})")
        (
            df.write.format("io.github.spark_redshift_community.spark.redshift")
            .option("url", self.redshift_url)
            .option("dbtable", target_table)
            .option("tempdir", self.temp_s3_dir)
            .option("aws_iam_role", iam_role_arn)
            .mode(mode)
            .save()
        )
        logger.info(f"Successfully loaded data into Redshift table {target_table}.")
