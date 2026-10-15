#!/bin/sh
set -eu

python /app/scripts/prepare_database.py
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
