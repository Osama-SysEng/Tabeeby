#!/bin/bash
SERVICES=(
  "http://localhost:8000/health"
  "http://localhost:8001/health"
  "http://localhost:8002/health"
  "http://localhost:8003/health"
  "http://localhost:8004/health"
  "http://localhost:8005/health"
)

echo "🏥 TABEEBY Health Check"
echo "======================="

for url in "${SERVICES[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" $url)
  if [ "$status" == "200" ]; then
    echo "✅ $url - OK"
  else
    echo "❌ $url - FAILED ($status)"
  fi
done
