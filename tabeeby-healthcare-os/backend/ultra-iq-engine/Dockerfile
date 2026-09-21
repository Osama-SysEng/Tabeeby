FROM nvidia/cuda:12.1-devel-ubuntu22.04

WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

COPY backend/ultra-iq-engine/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY backend/ultra-iq-engine/ .
EXPOSE 8001

ENV CUDA_VISIBLE_DEVICES=0
ENV COGNITIVE_OPS_PER_SEC=300000000000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "8"]
