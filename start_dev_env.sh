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
    
    # Check/Install Java (Required for Emulator)
    if ! java -version 2>&1 | grep -q "openjdk"; then
        echo '[VM] Installing OpenJDK 11 (Required for Firestore Emulator)...'
        sudo apt-get update > /dev/null
        sudo apt-get install -y openjdk-11-jre-headless > /dev/null
    fi

    echo '------------------------------------------'

    # --- 2. Start Firestore Emulator ---
    echo '[VM] Initializing Firestore Emulator...'
    (
        cd /vagrant/backend &&
        # Ensure node is available for firebase-tools
        source ~/.nvm/nvm.sh &&
        nvm use --lts > /dev/null &&
        
        if ! command -v firebase &> /dev/null; then
            echo '[Emulator] Installing Firebase CLI...'
            npm install -g firebase-tools
        fi

        echo '[Emulator] Starting Firestore Emulator (Project: demo-hiveinvestor)...'
        # Start emulator in background, listening on all interfaces so host can access if needed
        # Using --project demo-hiveinvestor to avoid login requirement
        firebase emulators:start --only firestore --project demo-hiveinvestor
    ) >> /log/web_service.log 2>&1 &
    echo '[VM] Firestore Emulator process started in background.'
    echo '------------------------------------------'

    # --- 3. Start Backend Service ---
    echo '[VM] Initializing FastAPI backend server...'
    (
        cd /vagrant/backend &&
        echo '[Backend] Activating Python virtual environment...' &&
        source /vagrant/backend/.venv/bin/activate &&
        
        # Configure Backend to use Emulator
        export FIRESTORE_EMULATOR_HOST="localhost:8081"
        export GCLOUD_PROJECT="demo-hiveinvestor"
        
        echo '[Backend] Starting Uvicorn server...' &&
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ) >> /log/web_service.log 2>&1 &
    echo '[VM] Backend server process started in background.'
    echo '------------------------------------------'

    # --- 4. Start Frontend Service ---
    echo '[VM] Initializing Vue.js frontend server...'
    (
        cd /vagrant/frontend &&
        echo '[Frontend] Setting Node.js version via NVM...' &&
        source ~/.nvm/nvm.sh &&
        nvm use --lts > /dev/null &&
        echo '[Frontend] Installing dependencies from package.json (if needed)...' &&
        npm install --quiet &&
        echo '[Frontend] Starting Vite dev server...' &&
        npm run dev -- --host 0.0.0.0 --port 8080
    ) >> /log/web_service.log 2>&1 &
    echo '[VM] Frontend server process started in background.'
    echo '------------------------------------------'

    # --- 5. Monitor Logs ---
    echo '✅ All services started.'
    echo '👀 Tailing combined log file: /log/web_service.log'
    echo '   (Press Ctrl+C to stop tailing logs and exit)'
    tail -f /log/web_service.log
"

# Execute the commands within the running Vagrant VM.
vagrant ssh -c "$VAGRANT_CMD"

echo "🛑 Development environment script finished."
