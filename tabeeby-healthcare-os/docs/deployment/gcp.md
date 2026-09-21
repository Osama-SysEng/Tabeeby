# GCP Deployment Guide

## Prerequisites
- gcloud CLI
- kubectl
- Terraform >= 1.5.0

## Steps

1. Set project:
```bash
gcloud config set project tabeeby-healthcare
```

2. Deploy GKE:
```bash
terraform apply -target=module.gke
```

3. Get credentials:
```bash
gcloud container clusters get-credentials tabeeby-gcp --zone us-central1
```

## Machine Types
- a2-highgpu-8g: GPU workloads
- n2-standard-64: General compute
- m2-ultramem-416: Memory intensive
