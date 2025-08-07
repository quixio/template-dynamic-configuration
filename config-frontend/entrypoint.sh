#!/bin/sh
set -e

echo "📦 Running config initialization..."
python /app/configuration_svc.py

echo "🚀 Starting Flet..."
exec python /app/main.py
