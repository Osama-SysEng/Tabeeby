provider "aws" { region = var.aws_region }
provider "azurerm" { features {} }
provider "google" { project = var.gcp_project, region = var.gcp_region }
