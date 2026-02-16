#!/bin/bash

echo "========================================"
echo " Multicloud Mapper - Setup and Start"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create .env from .env.example and configure Azure OpenAI credentials"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the Flask server
echo ""
echo "========================================"
echo "Starting Multicloud Mapper API Server"
echo "========================================"
echo ""
echo "API will be available at: http://localhost:5000"
echo "Frontend: Open index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
