terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# One bucket that holds the packed app artifacts.
resource "aws_s3_bucket" "artifacts" {
  bucket = var.bucket_name

  tags = {
    Project = "jenkins-multicloud-cicd"
    Owner   = "sai"
  }
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}
