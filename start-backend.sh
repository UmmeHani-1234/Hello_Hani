#!/usr/bin/env bash
# Sets up and runs the FastAPI backend on http://localhost:8000
set -e
cd "$(dirname "$0")/backend"

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv --clear
fi

source .venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo ""
  echo "Created backend/.env from the example."
  echo "Add your GROQ_API_KEY to backend/.env before chatting will work."
  echo ""
fi

echo "Starting backend on http://localhost:8000 ..."
uvicorn app.main:app --reload --port 8000
