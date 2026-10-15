#!/bin/sh
set -eu

# Running a script by absolute path places /app/scripts on sys.path;
# add the application root so `from app.database import engine` works.
export PYTHONPATH="/app${PYTHONPATH:+:$PYTHONPATH}"
python /app/scripts/prepare_database.py
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
