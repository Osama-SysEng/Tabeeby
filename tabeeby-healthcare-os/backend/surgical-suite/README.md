# surgical-suite

Tabeeby Healthcare OS — Surgical Suite - VR simulation, AR live assistance, robotic surgery control

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
