@echo off
echo Starting AutoCDA with React Frontend
echo ========================================
echo.

REM Check if backend is running
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo Backend not running. Starting backend...
    echo.
    start "AutoCDA Backend" cmd /k "python backend\api.py"
    timeout /t 3 /nobreak >nul
    echo Backend started
) else (
    echo Backend already running
)

echo.
echo Starting React frontend...
cd client
npm run dev
