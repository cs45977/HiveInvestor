#!/bin/bash
# This script runs INSIDE the Vagrant VM to start services and manage logs/persistence.

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
    HOST_DATA_DIR="/vagrant/backend/firebase-data"
    VM_TEMP_EXPORT="/log/firebase-temp-export"
    ARGS="--only firestore --project=demo-project"
    
    # Ensure the host data directory exists (synced folder)
    mkdir -p "$HOST_DATA_DIR"
    
    if [ -f "$HOST_DATA_DIR/firebase-export-metadata.json" ]; then
        echo "[VM] Found existing Firestore data. Importing..."
        ARGS="$ARGS --import=$HOST_DATA_DIR"
    else
        echo "[VM] No existing data found. Starting with fresh database."
    fi
    
    # Start emulator
    # Note: We rely on firebase.json for host binding (0.0.0.0)
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
    
    # --- CONFIGURATION FOR EMULATOR ---
    # Force the client to use the local emulator
    export FIRESTORE_EMULATOR_HOST="127.0.0.1:8090"
    
    # Force the project ID to match the emulator's start command
    export FIRESTORE_PROJECT_ID="demo-project"
    export GOOGLE_CLOUD_PROJECT="demo-project"
    export GCLOUD_PROJECT="demo-project"
    
    # Unset variables that might cause the client to try real cloud authentication
    unset GOOGLE_APPLICATION_CREDENTIALS
    
    # Unset FIRESTORE_DATABASE to default to the (default) database.
    # This prevents "Database (hiveinvestor)" 403 errors if a named DB was accidentally set.
    unset FIRESTORE_DATABASE
    
    echo "[Backend] Env Vars: EMULATOR_HOST=$FIRESTORE_EMULATOR_HOST PROJECT_ID=$FIRESTORE_PROJECT_ID" &&
    
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
) >> /log/web_service.log 2>&1 &
echo '[VM] Backend server process started in background.'
echo '------------------------------------------'

# --- 3. Start Frontend Service ---
echo '[VM] Initializing Vue.js frontend server...'
(
    cd /vagrant/frontend &&
    echo '[Frontend] Setting Node.js version via NVM...' &&
    # Load NVM
    [ -s "$HOME/.nvm/nvm.sh" ] && source "$HOME/.nvm/nvm.sh"
    
    # Install NVM/Node if missing (failsafe)
    if ! command -v nvm &> /dev/null; then
        echo "[VM] NVM not found. Installing..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    fi

    nvm use --lts
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

# Define export function
export_data() {
    # 1. Export from Emulator to VM Temp Dir (Fast)
    # Using the hub port 4400 which we forwarded, but inside VM localhost:4400 is correct.
    curl -s -X POST http://localhost:4400/emulators/export -d '{"path":"/log/firebase-temp-export"}' > /log/export_status.log
    
    # 2. Sync VM Temp Dir to Host Synced Folder (Safe)
    if [ -d "/log/firebase-temp-export" ]; then
            # Only copy if export was successful (check if dir is not empty)
            cp -r /log/firebase-temp-export/* /vagrant/backend/firebase-data/
    fi
}

# Auto-save loop (every 10 seconds)
(
    while true; do
        sleep 10
        export_data
    done
) &
AUTOSAVE_PID=$!

# Function to handle exit signals
on_exit() {
    echo ''
    echo '💾 Saving Firestore data before exit...'
    export_data
    echo '✅ Data saved to backend/firebase-data'
    
    echo '🛑 Stopping log monitoring and auto-save...'
    kill $TAIL_PID 2>/dev/null
    kill $AUTOSAVE_PID 2>/dev/null
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap on_exit SIGINT SIGTERM

# Wait for tail to finish (it won't unless killed)
wait $TAIL_PID
