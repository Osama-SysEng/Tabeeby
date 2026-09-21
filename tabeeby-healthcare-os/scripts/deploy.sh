#!/bin/bash
set -e

ENVIRONMENT=${1:-production}
echo "🚀 Deploying TABEEBY to $ENVIRONMENT"

if [ "$ENVIRONMENT" == "local" ]; then
    docker-compose -f infrastructure/docker/docker-compose.yml up -d
elif [ "$ENVIRONMENT" == "staging" ]; then
    kubectl apply -f infrastructure/kubernetes/ --namespace=tabeeby-staging
elif [ "$ENVIRONMENT" == "production" ]; then
    kubectl apply -f infrastructure/kubernetes/ --namespace=tabeeby-healthcare
    kubectl rollout status deployment/api-gateway -n tabeeby-healthcare
fi

echo "✅ Deployment complete"
