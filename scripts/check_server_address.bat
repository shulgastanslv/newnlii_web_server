@echo off
setlocal enabledelayedexpansion
echo ========================================
echo Determining addresses for access to the server
echo ========================================
echo.

echo [1] Local access (from this computer):
echo     http://localhost:8000
echo     http://127.0.0.1:8000
echo.

echo [2] Access from local network:
echo     Checking IP addresses...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo     http://!IP!:8000
)
echo.

echo [3] External IP address (for internet access):
echo     Checking through external service...
for /f %%i in ('powershell -Command "(Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing).Content"') do set EXTERNAL_IP=%%i
echo     http://!EXTERNAL_IP!:8000
echo     (Use this IP after setting up Port Forwarding in the router)
echo.

echo [4] Check port 8000 availability:
netstat -an | findstr :8000 >nul
if !errorlevel! equ 0 (
    echo     [OK] Port 8000 is active - server is running
    netstat -an | findstr :8000
) else (
    echo     [X] Port 8000 is not listening - server is not running
    echo     Start: run_production.bat
)
echo.

echo ========================================
echo Instructions:
echo - For local access: use localhost:8000
echo - For access from local network: use IP from point [2]
echo - For access from internet: set up Port Forwarding and use IP from point [3]
echo - Or use ngrok for quick testing
echo ========================================
pause
