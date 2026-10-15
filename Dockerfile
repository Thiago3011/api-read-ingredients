FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-por \
    && groupadd --system app && \
       useradd --system --gid app --create-home app && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

USER app

EXPOSE 8000

# Safely prepare or upgrade the database, then start the API.
# Local Docker Compose overrides this with --reload for development.
CMD ["sh", "/app/start.sh"]
