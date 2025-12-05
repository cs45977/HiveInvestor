#!/bin/bash
set -e

PROJECT_ID="gen-lang-client-0437257621"
REGION="us-central1"
BACKEND_SERVICE_NAME="hiveinvestor-backend"
BACKEND_IMAGE="gcr.io/${PROJECT_ID}/${BACKEND_SERVICE_NAME}"
FRONTEND_BUCKET="hiveinvestor-frontend-${PROJECT_ID}"
FIRESTORE_DATABASE="hiveinvestor"

DEPLOY_BACKEND=true
DEPLOY_FRONTEND=true
SKIP_TESTS=false

# Parse flags
for arg in "$@"
do
    case $arg in
        --backend-only)
        DEPLOY_BACKEND=true
        DEPLOY_FRONTEND=false
        shift
        ;;
        --frontend-only)
        DEPLOY_BACKEND=false
        DEPLOY_FRONTEND=true
        shift
        ;;
        --skip-tests)
        SKIP_TESTS=true
        shift
        ;;
    esac
done

echo "========================================================"
echo "Starting Application Deployment"
echo "Project: ${PROJECT_ID}"
echo "Deploy Backend: ${DEPLOY_BACKEND}"
echo "Deploy Frontend: ${DEPLOY_FRONTEND}"
echo "========================================================"

gcloud config set project $PROJECT_ID

# Backend Deployment
if [ "$DEPLOY_BACKEND" = true ]; then
    echo "[Backend] Building and Deploying..."
    cd backend
    
    echo "  - Submitting Build..."
    gcloud builds submit --tag $BACKEND_IMAGE

    # Load API Key from .env
    if [ -f backend/.env ]; then
        export $(grep FINNHUB_API_KEY backend/.env | xargs)
    fi

    echo "  - Deploying to Cloud Run..."
    gcloud run deploy $BACKEND_SERVICE_NAME \
        --image $BACKEND_IMAGE \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --port 8000 \
        --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,FIRESTORE_DATABASE=$FIRESTORE_DATABASE,FINNHUB_API_KEY=$FINNHUB_API_KEY
    
    cd ..
else
    echo "[Backend] Skipping..."
fi

# Fetch Backend URL (Needed for Frontend)
echo "Fetching Backend URL..."
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)' 2>/dev/null || echo "")
echo "Backend URL: $BACKEND_URL"

# Frontend Deployment
if [ "$DEPLOY_FRONTEND" = true ]; then
    echo "[Frontend] Building and Deploying..."
    cd frontend

    if [ ! -z "$BACKEND_URL" ]; then
        echo "  - Updating .env.production..."
        # Use relative path for API since we have a Load Balancer rule for /api/*
        echo "VITE_API_URL=" > .env.production
    fi

    echo "  - Installing Dependencies..."
    echo "  - Installing Dependencies (Clean Install)..."
    # Fix for @rollup/rollup-darwin-x64 error
    rm -rf node_modules package-lock.json
    npm install

    echo "  - Building..."
    npm run build

    echo "  - Uploading to GCS..."
    gcloud storage cp -r dist/* gs://${FRONTEND_BUCKET}/
    
    # Set cache control for index.html to ensure updates are seen
    gcloud storage cp dist/index.html gs://${FRONTEND_BUCKET}/index.html --cache-control="no-cache,max-age=0"

    cd ..
else
    echo "[Frontend] Skipping..."
fi

echo "========================================================"
echo "Deployment Complete!"
echo "Frontend: https://chaperone.cloud"
echo "Backend: $BACKEND_URL"
echo "========================================================"
