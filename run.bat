@echo off
REM AI Copilot System Startup Script for Windows
REM Starts Flask backend and React frontend, then opens browser

setlocal enabledelayedexpansion

REM Project directories
set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%flask-ai-copilot"
set "FRONTEND_DIR=%SCRIPT_DIR%react-ai-copilot"

echo ==========================================
echo   AI Copilot System Startup
echo ==========================================
echo.

REM Check if directories exist
if not exist "%BACKEND_DIR%" (
    echo [ERROR] Backend directory not found: %BACKEND_DIR%
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo [ERROR] Frontend directory not found: %FRONTEND_DIR%
    exit /b 1
)

REM Check if .env exists
if not exist "%BACKEND_DIR%\.env" (
    echo [WARNING] .env file not found in backend directory
    echo Please create %BACKEND_DIR%\.env with your API keys
    echo See RUNNING_THE_PROJECT.md for details
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "!CONTINUE!"=="y" exit /b 1
)

REM Start Flask backend
echo [INFO] Starting Flask backend...
cd /d "%BACKEND_DIR%"

REM Check for virtual environment
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Start backend in new window
echo [INFO] Starting backend server...
start "AI Copilot Backend" cmd /k "python app.py"
timeout /t 2 /nobreak >nul

REM Wait for backend to be ready
echo [INFO] Waiting for backend to be ready...
set MAX_ATTEMPTS=30
set ATTEMPT=0
set BACKEND_READY=0

:check_backend
set /a ATTEMPT+=1
timeout /t 2 /nobreak >nul

curl -s http://localhost:5000/check-keys >nul 2>&1
if !errorlevel! equ 0 (
    set BACKEND_READY=1
    goto backend_ready
)

if !ATTEMPT! lss !MAX_ATTEMPTS! (
    echo|set /p="."
    goto check_backend
)

:backend_ready
echo.

if !BACKEND_READY! equ 1 (
    echo [OK] Backend is running on http://localhost:5000
    
    REM Check API keys
    curl -s http://localhost:5000/check-keys | findstr /C:"generator_initialized\":true" >nul
    if !errorlevel! equ 0 (
        echo [OK] API keys loaded and generator initialized
    ) else (
        echo [WARNING] Generator not initialized. Check API keys in .env file
    )
) else (
    echo [ERROR] Backend failed to start after !MAX_ATTEMPTS! attempts
    echo Check the backend window for errors
    exit /b 1
)

REM Start React frontend
echo [INFO] Starting React frontend...
cd /d "%FRONTEND_DIR%"

REM Check if node_modules exists
if not exist "node_modules" (
    echo [WARNING] node_modules not found. Installing dependencies...
    call npm install
)

REM Start frontend in new window
echo [INFO] Starting frontend server...
start "AI Copilot Frontend" cmd /k "npm run dev"
timeout /t 5 /nobreak >nul

REM Wait for frontend to be ready
echo [INFO] Waiting for frontend to be ready...
set MAX_ATTEMPTS=30
set ATTEMPT=0
set FRONTEND_READY=0

:check_frontend
set /a ATTEMPT+=1
timeout /t 2 /nobreak >nul

curl -s http://localhost:3000 >nul 2>&1
if !errorlevel! equ 0 (
    set FRONTEND_READY=1
    goto frontend_ready
)

if !ATTEMPT! lss !MAX_ATTEMPTS! (
    echo|set /p="."
    goto check_frontend
)

:frontend_ready
echo.

if !FRONTEND_READY! equ 1 (
    echo [OK] Frontend is running on http://localhost:3000
) else (
    echo [WARNING] Frontend may still be starting. Check the frontend window
)

REM Open browser
echo [INFO] Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:3000

echo.
echo ==========================================
echo [OK] AI Copilot System is running!
echo ==========================================
echo.
echo [INFO] Backend:  http://localhost:5000
echo [INFO] Frontend: http://localhost:3000
echo.
echo [INFO] Both servers are running in separate windows
echo [INFO] Close those windows to stop the servers
echo.
pause

