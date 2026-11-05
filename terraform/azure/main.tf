terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "app" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Project = "jenkins-multicloud-cicd"
    Owner   = "sai"
  }
}

# Storage account names: lowercase letters and numbers only, 3-24 chars.
resource "azurerm_storage_account" "artifacts" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.app.name
  location                 = azurerm_resource_group.app.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Project = "jenkins-multicloud-cicd"
    Owner   = "sai"
  }
}

resource "azurerm_storage_container" "artifacts" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.artifacts.name
  container_access_type = "private"
}
