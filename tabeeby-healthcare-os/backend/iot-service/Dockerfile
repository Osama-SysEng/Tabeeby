FROM python:3.11-slim
WORKDIR /app
COPY backend/iot-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/iot-service/ .
EXPOSE 8011
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011", "--workers", "4"]
