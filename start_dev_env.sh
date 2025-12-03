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
            # Create data directory if it doesn't exist
            mkdir -p firebase-data
            
            # Start emulator in background
            # Using --project demo-hiveinvestor to avoid login requirement
            # Added persistence: --import and --export-on-exit
            exec firebase emulators:start --only firestore --project demo-hiveinvestor --import=./firebase-data --export-on-exit=./firebase-data
        ) >> /log/web_service.log 2>&1 &
        EMULATOR_PID=\$!
        echo \"[VM] Firestore Emulator process started in background. PID: \$EMULATOR_PID\"
        echo '------------------------------------------'
    
        # --- 3. Start Backend Service ---
        echo '[VM] Initializing FastAPI backend server...'
        (
            cd /vagrant/backend &&
            
            # Ensure venv exists
            if [ ! -d ".venv" ]; then
                 echo '[Backend] Creating Python virtual environment...'
                 python3 -m venv .venv
            fi
    
            echo '[Backend] Activating Python virtual environment...' &&
            source .venv/bin/activate &&
    
            echo '[Backend] Installing/Updating dependencies...' &&
            pip install -r requirements.txt > /dev/null &&
            
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

    # --- 5. Monitor Logs & Handle Shutdown ---
    cleanup() {
        echo \"\"
        echo \"🛑 Stopping services...\"
        if [ -n \"\$EMULATOR_PID\" ]; then
            echo \"[VM] Sending SIGINT to Emulator PID: \$EMULATOR_PID to trigger data export...\"
            kill -SIGINT \"\$EMULATOR_PID\"
            wait \"\$EMULATOR_PID\"
            echo \"[VM] Emulator stopped and data exported.\"
        fi
        # Kill other background jobs (backend/frontend)
        pkill -P \$\$
    }

    trap cleanup EXIT SIGINT SIGTERM SIGHUP

    echo "*************************************************************************"
    echo '✅ All services started.'
    echo ''
    echo '🌐 Access the application at:'
    echo '   Frontend UI:           http://localhost:8080'
    echo '   Backend API Docs:      http://localhost:8000/docs'
    echo '   Firestore Emulator UI: http://localhost:4000'
    echo ''
    echo '👀 Tailing combined log file: /log/web_service.log'
    echo '   (Press Ctrl+C to stop tailing logs and exit gracefully)'
    echo "*************************************************************************"    
    
    tail -f /log/web_service.log &
    wait $!
"

# Execute the commands within the running Vagrant VM.
vagrant ssh -c "$VAGRANT_CMD"

echo "🛑 Development environment script finished."
