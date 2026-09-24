variable "aws_region" {
  description = "AWS region for all infrastructure resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "cloudmart"
}

variable "redshift_admin_username" {
  description = "Master username for Redshift Serverless"
  type        = string
  default     = "admin"
}

variable "redshift_admin_password" {
  description = "Master password for Redshift Serverless"
  type        = string
  sensitive   = true
  default     = "CloudMart123Secure!"
}

variable "bedrock_model_id" {
  description = "Default Bedrock Foundation Model ID"
  type        = string
  default     = "anthropic.claude-3-haiku-20240307-v1:0"
}
