FROM nvidia/cuda:12.1-devel-ubuntu22.04
WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
COPY backend/diagnostic-ai/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY backend/diagnostic-ai/ .
EXPOSE 8005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "4"]
