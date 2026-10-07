FROM python:3.11-slim
WORKDIR /app
COPY backend/national-health/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/national-health/ .
EXPOSE 8014
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8014", "--workers", "4"]
