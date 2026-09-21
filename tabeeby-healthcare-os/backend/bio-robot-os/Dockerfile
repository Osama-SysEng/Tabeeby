FROM python:3.11-slim
WORKDIR /app
COPY backend/bio-robot-os/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/bio-robot-os/ .
EXPOSE 8007
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007", "--workers", "4"]
