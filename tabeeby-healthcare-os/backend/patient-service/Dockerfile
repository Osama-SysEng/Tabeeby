FROM python:3.11-slim
WORKDIR /app
COPY backend/patient-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/patient-service/ .
EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--workers", "4"]
