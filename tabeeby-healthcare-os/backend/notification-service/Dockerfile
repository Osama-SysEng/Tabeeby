FROM python:3.11-slim
WORKDIR /app
COPY backend/notification-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/notification-service/ .
EXPOSE 8015
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8015", "--workers", "4"]
