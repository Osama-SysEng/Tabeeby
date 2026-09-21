FROM python:3.11-slim
WORKDIR /app
COPY backend/research-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/research-service/ .
EXPOSE 8013
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8013", "--workers", "4"]
