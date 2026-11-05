output "container_url_part" {
  description = "Storage account and container that receive app artifacts"
  value       = "${azurerm_storage_account.artifacts.name}/${azurerm_storage_container.artifacts.name}"
}
