FROM python:3.11-slim
WORKDIR /app
COPY backend/billing-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/billing-service/ .
EXPOSE 8016
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8016", "--workers", "4"]
