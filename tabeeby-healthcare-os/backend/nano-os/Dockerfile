FROM python:3.11-slim
WORKDIR /app
COPY backend/nano-os/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/nano-os/ .
EXPOSE 8008
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008", "--workers", "4"]
