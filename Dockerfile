FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y wget gnupg unzip && \
    apt-get install -y chromium chromium-driver

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]