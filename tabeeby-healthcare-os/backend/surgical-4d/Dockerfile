FROM python:3.11-slim
WORKDIR /app
COPY backend/surgical-4d/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/surgical-4d/ .
EXPOSE 8009
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009", "--workers", "4"]
