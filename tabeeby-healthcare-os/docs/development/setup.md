# Development Setup

## Requirements
- Docker >= 24.0
- Docker Compose >= 2.20
- Python >= 3.11
- Node.js >= 20
- Flutter >= 3.16

## Quick Start
```bash
# Clone repository
git clone https://github.com/tabeeby/healthcare-os.git
cd healthcare-os

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Access services
# API Gateway: http://localhost:8000
# Web: http://localhost:3000
# Grafana: http://localhost:3001
```

## Development Mode
```bash
# Start only databases
docker-compose up -d postgres timescaledb neo4j qdrant redis

# Run services locally
 cd backend/api-gateway && uvicorn main:app --reload
```

## Testing
```bash
# Run all tests
pytest tests/

# Run specific service tests
pytest backend/diagnostic-ai/tests/
```
