#!/bin/bash

# A script to start the local development environment for HiveInvestor.
# This script executes commands within the Vagrant VM to start the backend and frontend services.
# Logs for both services are combined and streamed to /log/web_service.log inside the VM.

echo "🚀 Starting HiveInvestor local development environment..."

# Define the sequence of commands to be executed inside the Vagrant VM.
VAGRANT_CMD="
    # --- 1. Environment Setup ---
    echo '[VM] Setting up log directory...'
    sudo mkdir -p /log
    sudo chmod -R 777 /log
    echo '[VM] Clearing previous logs...'
    > /log/web_service.log
    echo '[VM] Log file ready at /log/web_service.log'
    echo '------------------------------------------'

    # --- 2. Start Backend Service ---
    echo '[VM] Initializing FastAPI backend server...'
    (
        cd /vagrant/backend &&
        echo '[Backend] Activating Python virtual environment...' &&
        source venv/bin/activate &&
        echo '[Backend] Starting Uvicorn server...' &&
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ) >> /log/web_service.log 2>&1 &
    echo '[VM] Backend server process started in background.'
    echo '------------------------------------------'

    # --- 3. Start Frontend Service ---
    echo '[VM] Initializing Vue.js frontend server...'
    (
        cd /vagrant/frontend &&
        echo '[Frontend] Setting Node.js version via NVM...' &&
        source ~/.nvm/nvm.sh &&
        nvm use --lts &&
        echo '[Frontend] Installing dependencies from package.json (if needed)...' &&
        npm install --quiet &&
        echo '[Frontend] Starting Vite dev server...' &&
        npm run dev -- --host 0.0.0.0 --port 8080
    ) >> /log/web_service.log 2>&1 &
    echo '[VM] Frontend server process started in background.'
    echo '------------------------------------------'

    # --- 4. Monitor Logs ---
    echo '✅ All services started.'
    echo '👀 Tailing combined log file: /log/web_service.log'
    echo '   (Press Ctrl+C to stop tailing logs and exit)'
    tail -f /log/web_service.log
"

# Execute the commands within the running Vagrant VM.
vagrant ssh -c "$VAGRANT_CMD"

echo "🛑 Development environment script finished."
