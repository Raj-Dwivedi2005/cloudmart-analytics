resource "aws_glue_catalog_database" "cloudmart_db" {
  name        = "${var.project_name}_db"
  description = "Glue Catalog database for CloudMart analytics"
}

resource "aws_glue_crawler" "curated_crawler" {
  database_name = aws_glue_catalog_database.cloudmart_db.name
  name          = "${var.project_name}-curated-crawler"
  role          = aws_iam_role.glue_service_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.curated.bucket}/tables/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }
}

resource "aws_glue_job" "sales_etl_job" {
  name     = "${var.project_name}-sales-etl"
  role_arn = aws_iam_role.glue_service_role.arn

  command {
    script_location = "s3://${aws_s3_bucket.scripts.bucket}/etl/transform/clean_sales.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"                    = "python"
    "--job-bookmark-option"             = "job-bookmark-enable"
    "--enable-metrics"                  = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--RAW_BUCKET"                      = aws_s3_bucket.raw.bucket
    "--CURATED_BUCKET"                  = aws_s3_bucket.curated.bucket
  }

  glue_version = "4.0"
  worker_type  = "G.1X"
  number_of_workers = 2
}
