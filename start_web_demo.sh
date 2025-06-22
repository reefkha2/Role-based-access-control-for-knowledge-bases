#!/bin/bash

# Start the SecureKB web demo

echo "===== Starting SecureKB Web Demo ====="
echo ""

# Activate virtual environment
source .venv/bin/activate

# Update the web config
cd web
python update_config.py

# Start the web server
python -m http.server 8000 &
SERVER_PID=$!

# Open the web browser
echo "Opening web browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:8000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:8000
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    start http://localhost:8000
else
    echo "Please open a web browser and navigate to http://localhost:8000"
fi

echo "Web server started at http://localhost:8000"
echo "Press Ctrl+C to stop the server."

# Wait for user to press Ctrl+C
trap "kill $SERVER_PID; echo 'Server stopped.'; exit 0" INT
wait
