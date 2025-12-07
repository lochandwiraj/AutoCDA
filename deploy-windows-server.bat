@echo off
REM Self-Hosted Deployment for Windows Server
REM Run this as Administrator

echo ========================================
echo AutoCDA Windows Server Deployment
echo ========================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Please run as Administrator
    pause
    exit /b 1
)

REM Set API Key
set /p OPENROUTER_API_KEY="Enter your OpenRouter API Key: "
echo OPENROUTER_API_KEY=%OPENROUTER_API_KEY% > .env

REM Install Python dependencies
echo.
echo Installing Python dependencies...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

REM Build React frontend
echo.
echo Building React frontend...
cd client
call npm install
call npm run build
cd ..

REM Create startup script for backend
echo.
echo Creating startup scripts...
(
echo @echo off
echo cd /d "%~dp0"
echo call venv\Scripts\activate
echo set OPENROUTER_API_KEY=%OPENROUTER_API_KEY%
echo python backend/api.py
) > start-backend.bat

REM Install as Windows Service (optional)
echo.
echo To run as Windows Service, install NSSM:
echo 1. Download NSSM from https://nssm.cc/download
echo 2. Run: nssm install AutoCDA-Backend "%CD%\start-backend.bat"
echo.

REM Setup IIS (if available)
echo.
echo For production, configure IIS:
echo 1. Install IIS with URL Rewrite and ARR modules
echo 2. Create a new site pointing to: %CD%\client\dist
echo 3. Add reverse proxy rule for /api/* to http://localhost:5000
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Run: start-backend.bat
echo 2. Open browser to: http://localhost
echo.
echo For production with IIS, configure as described above.
echo.
pause
