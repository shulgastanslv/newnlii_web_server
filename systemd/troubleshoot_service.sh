#!/bin/bash

echo "=========================================="
echo "Devsy Web Server Service Troubleshooting"
echo "=========================================="
echo ""

# Check service status
echo "1. Checking service status..."
sudo systemctl status devsy-web-server.service --no-pager -l
echo ""

# Check recent logs
echo "2. Checking recent journal logs..."
sudo journalctl -u devsy-web-server.service -n 50 --no-pager
echo ""

# Check if paths exist
echo "3. Checking if required paths exist..."
if [ -d "/root/Projects/devsy_web_server" ]; then
    echo "✓ Working directory exists"
else
    echo "✗ Working directory missing: /root/Projects/devsy_web_server"
fi

if [ -d "/root/Projects/devsy_web_server/.venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "✗ Virtual environment missing: /root/Projects/devsy_web_server/.venv"
fi

if [ -f "/root/Projects/devsy_web_server/.venv/bin/uvicorn" ]; then
    echo "✓ uvicorn executable exists"
else
    echo "✗ uvicorn executable missing"
fi

if [ -f "/root/Projects/devsy_web_server/app/main.py" ]; then
    echo "✓ Main application file exists"
else
    echo "✗ Main application file missing"
fi
echo ""

# Check permissions
echo "4. Checking permissions..."
ls -la /root/Projects/devsy_web_server/.venv/bin/uvicorn 2>/dev/null || echo "Cannot check uvicorn permissions"
echo ""

echo "5. Checking Python interpreter and uvicorn module..."
if [ -f "/root/Projects/devsy_web_server/.venv/bin/python" ]; then
    echo "✓ Python interpreter exists"
    if /root/Projects/devsy_web_server/.venv/bin/python -c "import uvicorn" 2>/dev/null; then
        echo "✓ uvicorn module can be imported"
    else
        echo "✗ Cannot import uvicorn module"
        echo "  Attempting to import uvicorn..."
        /root/Projects/devsy_web_server/.venv/bin/python -c "import uvicorn" 2>&1 | head -5
    fi
else
    echo "✗ Python interpreter missing: /root/Projects/devsy_web_server/.venv/bin/python"
fi
echo ""

echo "6. Attempting to start the service..."
sudo systemctl start devsy-web-server.service
sleep 2
echo ""

echo "7. Service status after start attempt..."
sudo systemctl status devsy-web-server.service --no-pager -l
echo ""

if ! sudo systemctl is-active --quiet devsy-web-server.service; then
    echo "8. Latest error logs..."
    sudo journalctl -u devsy-web-server.service -n 20 --no-pager
fi

