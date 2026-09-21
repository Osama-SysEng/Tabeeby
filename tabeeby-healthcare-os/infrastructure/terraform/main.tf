terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
  backend "s3" {
    bucket = "tabeeby-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

# Multi-cloud deployment: AWS + Azure + GCP simultaneous
provider "aws" { region = var.aws_region }
provider "azurerm" { features {} }
provider "google" { project = var.gcp_project, region = var.gcp_region }

module "vpc" {
  source = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
  azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

module "eks" {
  source = "./modules/eks"
  cluster_name = "tabeeby-aws"
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  node_count = 50
  instance_types = ["p4d.24xlarge", "c7i.48xlarge", "r6i.32xlarge"]
}

module "gke" {
  source = "./modules/gke"
  cluster_name = "tabeeby-gcp"
  location = "us-central1"
  node_count = 30
  machine_type = "a2-highgpu-8g"
}

module "aks" {
  source = "./modules/aks"
  cluster_name = "tabeeby-azure"
  resource_group = "tabeeby-rg"
  node_count = 30
  vm_size = "Standard_NC24s_v3"
}

module "database" {
  source = "./modules/database"
  postgres_enabled = true
  timescaledb_enabled = true
  neo4j_enabled = true
  qdrant_enabled = true
  redis_enabled = true
  minio_enabled = true
}

module "storage" {
  source = "./modules/storage"
  s3_enabled = true
  azure_blob_enabled = true
  gcs_enabled = true
}

module "security" {
  source = "./modules/security"
  encryption = "AES-256"
  compliance = ["HIPAA", "GDPR", "ISO27001"]
}
