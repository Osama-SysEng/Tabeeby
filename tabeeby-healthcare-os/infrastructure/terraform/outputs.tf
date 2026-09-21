output "eks_cluster_endpoint" { value = module.eks.cluster_endpoint }
output "gke_cluster_endpoint" { value = module.gke.cluster_endpoint }
output "aks_cluster_endpoint" { value = module.aks.cluster_endpoint }
output "database_endpoints" { value = module.database.endpoints }
