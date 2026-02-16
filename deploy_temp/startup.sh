#!/bin/bash
# Azure App Service startup script for Python Flask app

echo "Starting Multicloud Mapper on Azure App Service..."

# Azure App Service sets PORT environment variable
# Default to 8000 if not set
export PORT="${PORT:-8000}"

echo "Python version:"
python --version

echo "Installing requirements..."
pip install -r requirements.txt

echo "Starting gunicorn on port $PORT..."

# Start gunicorn with proper configuration
exec gunicorn --bind=0.0.0.0:$PORT --timeout 600 --workers=4 --threads=2 --worker-class=gthread app:app
