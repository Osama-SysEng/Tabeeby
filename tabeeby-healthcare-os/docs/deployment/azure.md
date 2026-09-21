# Azure Deployment Guide

## Prerequisites
- Azure CLI
- kubectl
- Terraform >= 1.5.0

## Steps

1. Login:
```bash
az login
```

2. Deploy AKS:
```bash
terraform apply -target=module.aks
```

3. Get credentials:
```bash
az aks get-credentials --resource-group tabeeby-rg --name tabeeby-azure
```

## VM Sizes
- Standard_NC24s_v3: GPU workloads
- Standard_D64s_v5: General compute
- Standard_E64s_v5: Memory intensive
