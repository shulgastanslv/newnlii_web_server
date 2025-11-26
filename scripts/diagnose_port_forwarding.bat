@echo off
setlocal enabledelayedexpansion
echo ========================================
echo Diagnosis of port forwarding
echo ========================================
echo.

echo [1] Check if the server is running on port 8000:
netstat -an | findstr :8000 >nul
if !errorlevel! equ 0 (
    echo     [OK] Port 8000 is active
    echo     Active connections on port 8000:
    netstat -an | findstr :8000
) else (
    echo     [ERROR] Port 8000 is not listening - server is not running!
    echo     Start: run_production.bat
    echo.
    pause
    exit /b 1
)
echo.

echo [2] Check on which interface the server is listening:
netstat -an | findstr "0.0.0.0:8000" >nul
if !errorlevel! equ 0 (
    echo     [OK] Server is listening on 0.0.0.0:8000 (all interfaces)
) else (
    echo     [WARNING] Server may only listen on localhost
    netstat -an | findstr ":8000"
)
echo.

echo [3] Determine local IP address:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo     Local IP: !IP!
    set LOCAL_IP=!IP!
)
echo.

echo [4] Determine external IP address:
echo     Запрос к внешнему сервису...
for /f %%i in ('powershell -Command "try { (Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing -TimeoutSec 5).Content } catch { 'Не удалось определить' }"') do set EXTERNAL_IP=%%i
echo     External IP: !EXTERNAL_IP!
echo.

echo [5] Проверка правил брандмауэра Windows:
echo     Checking rules for port 8000...
netsh advfirewall firewall show rule name=all | findstr /i "8000" >nul
if !errorlevel! equ 0 (
    echo     [OK] Found firewall rules for port 8000
    netsh advfirewall firewall show rule name=all | findstr /i "8000"
) else (
    echo     [WARNING] Firewall rules for port 8000 not found
    echo     Ensure port 8000 is open in the Windows firewall
)
echo.

    echo [6] Check availability of local server:
echo     Testing http://localhost:8000...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -UseBasicParsing -TimeoutSec 3; Write-Host '     [OK] Local server is responding' } catch { Write-Host '     [ERROR] Local server is not responding' }"
echo.

echo [7] Check availability by local IP:
if defined LOCAL_IP (
    echo     Testing http://!LOCAL_IP!:8000...
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://!LOCAL_IP!:8000' -UseBasicParsing -TimeoutSec 3; Write-Host '     [OK] Server is accessible by local IP' } catch { Write-Host '     [ERROR] Server is not accessible by local IP' }"
)
echo.

echo ========================================
echo POSSIBLE REASONS FOR PROBLEMS:
echo ========================================
echo.
echo 1. HAIRPIN NAT (NAT Loopback):
echo    - Если вы обращаетесь по внешнему IP с того же компьютера,
echo      роутер может не поддерживать Hairpin NAT
echo    - РЕШЕНИЕ: Проверьте доступ с другого устройства/сети
echo.
echo 2. Неправильная настройка роутера:
echo    - Убедитесь, что внутренний IP в роутере: !LOCAL_IP!
echo    - Убедитесь, что внутренний порт: 8000
echo    - Убедитесь, что внешний порт: 8000 (или другой, если настроен)
echo    - Проверьте, что правило активно (Enabled)
echo.
echo 3. CGNAT (Carrier-Grade NAT):
echo    - Ваш провайдер может использовать CGNAT, что блокирует
echo      входящие соединения
echo    - РЕШЕНИЕ: Обратитесь к провайдеру или используйте VPN/ngrok
echo.
echo 4. Брандмауэр роутера:
echo    - Проверьте настройки брандмауэра на самом роутере
echo    - Убедитесь, что порт 8000 разрешен
echo.
echo 5. Динамический IP:
echo    - Если ваш внешний IP меняется, используйте DDNS сервис
echo.
echo ========================================
echo РЕКОМЕНДАЦИИ:
echo ========================================
echo.
echo 1. Проверьте доступ с другого устройства (не с этого компьютера)
echo 2. Проверьте настройки роутера еще раз:
echo    - Внутренний IP должен быть: !LOCAL_IP!
echo    - Внутренний порт: 8000
echo    - Внешний порт: 8000
echo 3. Попробуйте временно отключить брандмауэр Windows для теста
echo 4. Используйте онлайн-сервис для проверки открытости порта:
echo    https://www.yougetsignal.com/tools/open-ports/
echo    или
echo    https://canyouseeme.org/
echo.
pause

