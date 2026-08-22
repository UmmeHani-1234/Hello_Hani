#!/usr/bin/env bash
# Installs deps (if needed) and runs the Vite dev server on http://localhost:5173
set -e
cd "$(dirname "$0")/frontend"

if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

echo "Starting frontend on http://localhost:5173 ..."
npm run dev
