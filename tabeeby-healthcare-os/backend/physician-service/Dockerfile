FROM python:3.11-slim
WORKDIR /app
COPY backend/physician-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/physician-service/ .
EXPOSE 8004
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004", "--workers", "4"]
