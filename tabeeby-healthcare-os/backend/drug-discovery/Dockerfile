FROM python:3.11-slim
WORKDIR /app
COPY backend/drug-discovery/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/drug-discovery/ .
EXPOSE 8006
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006", "--workers", "4"]
