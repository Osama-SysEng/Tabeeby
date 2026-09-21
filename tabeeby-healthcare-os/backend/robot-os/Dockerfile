FROM python:3.11-slim
WORKDIR /app
COPY backend/robot-os/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/robot-os/ .
EXPOSE 8010
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--workers", "4"]
