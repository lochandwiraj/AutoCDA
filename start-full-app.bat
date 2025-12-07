@echo off
echo ========================================
echo Starting AutoCDA Full Application
echo ========================================
echo.

REM Set API Key
set OPENROUTER_API_KEY=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

echo Starting Backend API on port 5000...
start "AutoCDA Backend" cmd /k "set OPENROUTER_API_KEY=%OPENROUTER_API_KEY% && python backend/api.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend on port 5173...
start "AutoCDA Frontend" cmd /k "cd client && npm run dev"

echo.
echo ========================================
echo Both services are starting!
echo ========================================
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to stop all services...
pause >nul

taskkill /FI "WINDOWTITLE eq AutoCDA Backend*" /F
taskkill /FI "WINDOWTITLE eq AutoCDA Frontend*" /F
