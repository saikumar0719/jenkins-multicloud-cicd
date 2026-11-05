variable "region" {
  description = "AWS region for the artifacts bucket"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for app artifacts (must be globally unique)"
  type        = string
  default     = "sai-shop-artifacts-aws-demo"
}
