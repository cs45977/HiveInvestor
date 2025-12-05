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

    # --- 1.5 Install Dependencies & Start Emulator ---
    echo '[VM] Checking system dependencies...'
    if ! command -v java &> /dev/null; then
        echo '[VM] Installing Java (required for Firebase Emulator)...'
        sudo apt-get update > /dev/null
        sudo apt-get install -y openjdk-11-jre-headless > /dev/null
    fi

    if ! command -v firebase &> /dev/null; then
        echo '[VM] Installing Firebase CLI...'
        curl -sL https://firebase.tools | bash
    fi

    echo '[VM] Starting Firebase Emulator...'
    (
        cd /vagrant
        
        # Persistence logic
        DATA_DIR=\"backend/firebase-data\"
        ARGS=\"--only firestore\"
        
        if [ -f \"$DATA_DIR/firebase-export-metadata.json\" ]; then
            echo \"[VM] Found existing Firestore data. Importing...\"
            ARGS=\"$ARGS --import=$DATA_DIR --export-on-exit\"
        else
            echo \"[VM] No existing data. Starting fresh (will export on exit)...\"
            ARGS=\"$ARGS --export-on-exit=$DATA_DIR\"
        fi
        
        firebase emulators:start $ARGS
    ) >> /log/web_service.log 2>&1 &
    echo '[VM] Firebase Emulator started in background.'
    echo '------------------------------------------'

    # --- 2. Start Backend Service ---
    echo '[VM] Initializing FastAPI backend server...'
    (
        cd /vagrant/backend &&
        echo '[Backend] Activating Python virtual environment...' &&
        source /vagrant/backend/.venv/bin/activate &&
        echo '[Backend] Installing dependencies...' &&
        pip uninstall -y google-cloud-firestore google-api-core protobuf grpcio-status &&
        pip install -r requirements.txt &&
        echo '[Backend] Starting Uvicorn server...' &&
        export FIRESTORE_EMULATOR_HOST="127.0.0.1:8090" &&
        export FIRESTORE_PROJECT_ID="demo-project" &&
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

    # --- 4. Monitor Logs & Handle Shutdown ---
    echo '✅ All services started.'
    echo '👀 Tailing combined log file: /log/web_service.log'
    echo '   (Press Ctrl+C to stop tailing logs and save data)'
    
    # Run tail in background so we can wait on it and trap signals
    tail -f /log/web_service.log &
    TAIL_PID=$!
    
    # Auto-save loop (every 5 seconds)
    (
        while true; do
            sleep 5
            curl -s -X POST http://localhost:4400/emulators/export -d '{\"path\":\"/vagrant/backend/firebase-data\"}' > /dev/null
        done
    ) &
    AUTOSAVE_PID=$!
    
    # Function to handle exit signals
    on_exit() {
        echo ''
        echo '💾 Saving Firestore data before exit...'
        # Trigger export via Emulator Hub
        curl -s -X POST http://localhost:4400/emulators/export -d '{\"path\":\"/vagrant/backend/firebase-data\"}'
        echo ''
        echo '🛑 Stopping log monitoring and auto-save...'
        kill $TAIL_PID
        kill $AUTOSAVE_PID
    }
    
    # Trap SIGINT (Ctrl+C) and SIGTERM
    trap on_exit SIGINT SIGTERM
    
    # Wait for tail to finish (it won't unless killed)
    wait $TAIL_PID
"

# Execute the commands within the running Vagrant VM.
vagrant ssh -c "$VAGRANT_CMD"

echo "🛑 Development environment script finished."
