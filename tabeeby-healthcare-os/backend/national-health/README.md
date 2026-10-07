# national-health

Tabeeby Healthcare OS — National Health System - Ministry dashboard, pharmacy network, FHIR integration

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoints

- GET /health - Health check
- POST /start - Start operation
- GET /list - List items
- GET /list/{id} - Get item
