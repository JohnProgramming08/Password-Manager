FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV database_uri="postgresql+psycopg2://postgres:postgres@postgres_db:5432/mydb"

EXPOSE 8000

CMD ["python", "app.py"]
