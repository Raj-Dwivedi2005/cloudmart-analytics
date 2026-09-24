resource "aws_s3_bucket" "raw" {
  bucket        = "${var.project_name}-raw-zone-${var.environment}"
  force_destroy = true
}

resource "aws_s3_bucket_lifecycle_configuration" "raw_lifecycle" {
  bucket = aws_s3_bucket.raw.id

  rule {
    id     = "archive-old-raw-data"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}

resource "aws_s3_bucket" "curated" {
  bucket        = "${var.project_name}-curated-zone-${var.environment}"
  force_destroy = true
}

resource "aws_s3_bucket" "scripts" {
  bucket        = "${var.project_name}-glue-scripts-${var.environment}"
  force_destroy = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw_encryption" {
  bucket = aws_s3_bucket.raw.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "curated_encryption" {
  bucket = aws_s3_bucket.curated.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
