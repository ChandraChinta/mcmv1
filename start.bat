@echo off
echo ========================================
echo  Multicloud Mapper - Setup and Start
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Please create .env from .env.example and configure Azure OpenAI credentials
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/update requirements
echo.
echo Installing dependencies...
pip install -q -r requirements.txt

REM Start the Flask server
echo.
echo ========================================
echo Starting Multicloud Mapper API Server
echo ========================================
echo.
echo API will be available at: http://localhost:5000
echo Frontend: Open index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
