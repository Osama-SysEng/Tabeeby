FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/file-security/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/file-security/ ./
COPY backend/shared /app/shared
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8017
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8017", "--workers", "2"]
