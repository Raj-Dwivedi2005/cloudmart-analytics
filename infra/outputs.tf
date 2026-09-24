output "s3_raw_bucket_name" {
  description = "Name of the raw zone S3 bucket"
  value       = aws_s3_bucket.raw.id
}

output "s3_curated_bucket_name" {
  description = "Name of the curated zone S3 bucket"
  value       = aws_s3_bucket.curated.id
}

output "glue_database_name" {
  description = "AWS Glue Catalog Database Name"
  value       = aws_glue_catalog_database.cloudmart_db.name
}

output "redshift_serverless_endpoint" {
  description = "Redshift Serverless Workgroup Endpoint"
  value       = aws_redshiftserverless_workgroup.cloudmart_workgroup.endpoint[0].address
}

output "athena_workgroup_name" {
  description = "Athena Workgroup Name"
  value       = aws_athena_workgroup.cloudmart_wg.name
}
