variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Resource group that holds the storage account"
  type        = string
  default     = "sai-shop-rg"
}

variable "storage_account_name" {
  description = "Storage account name (lowercase letters and numbers only)"
  type        = string
  default     = "saishopartifacts"
}

variable "container_name" {
  description = "Blob container for app artifacts"
  type        = string
  default     = "shop-artifacts"
}
