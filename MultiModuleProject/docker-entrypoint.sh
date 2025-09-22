#!/bin/bash

# Start Ollama service in background
ollama serve &

# Wait for Ollama to start
sleep 10

# Pull the model if not exists
ollama pull llama3:latest

# Run Django migrations
python manage.py migrate --settings=MultiModuleProject.settings_production

# Start Django application
exec gunicorn MultiModuleProject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100