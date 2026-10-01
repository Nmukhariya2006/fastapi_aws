FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install  -r requirements.txt

COPY app ./app
# ./data holds the SQLite file. Mount a volume/EFS access point here to persist it.
RUN mkdir -p /app/data \
    && useradd -m appuser \
    && chown -R appuser:appuser /app


USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]

