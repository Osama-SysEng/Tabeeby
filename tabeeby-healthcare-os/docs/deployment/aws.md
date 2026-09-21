# AWS Deployment Guide

## Prerequisites
- AWS CLI configured
- kubectl + eksctl
- Terraform >= 1.5.0

## Steps

1. Initialize Terraform:
```bash
cd infrastructure/terraform
terraform init
```

2. Plan deployment:
```bash
terraform plan -var="aws_region=us-east-1"
```

3. Apply:
```bash
terraform apply
```

4. Configure kubectl:
```bash
aws eks update-kubeconfig --region us-east-1 --name tabeeby-aws
```

5. Deploy services:
```bash
kubectl apply -f infrastructure/kubernetes/
```

## Instance Types
- p4d.24xlarge: Ultra IQ Engine (GPU)
- c7i.48xlarge: API Gateway, Auth Service
- r6i.32xlarge: Patient Service, Diagnostic AI
- inf2.48xlarge: NLP + RAG inference
