FROM python:3.11-slim
WORKDIR /app
COPY backend/emergency-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/emergency-service/ .
EXPOSE 8012
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8012", "--workers", "4"]
