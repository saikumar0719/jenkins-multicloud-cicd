output "bucket_name" {
  description = "The GCS bucket that receives app artifacts"
  value       = google_storage_bucket.artifacts.name
}
