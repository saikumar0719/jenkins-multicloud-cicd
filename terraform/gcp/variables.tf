variable "project_id" {
  description = "GCP project ID (the owner puts their own project ID here)"
  type        = string
  default     = "my-demo-project"
}

variable "region" {
  description = "GCP region for the bucket"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Name of the GCS bucket for app artifacts (must be globally unique)"
  type        = string
  default     = "sai-shop-artifacts-gcp-demo"
}
