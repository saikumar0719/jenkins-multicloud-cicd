output "bucket_name" {
  description = "The S3 bucket that receives app artifacts"
  value       = aws_s3_bucket.artifacts.bucket
}
