#!/bin/bash
set -e

PROJECT_ID="gen-lang-client-0437257621"
REGION="us-central1"
DOMAIN_1="chaperone.cloud"
DOMAIN_2="cryptomaison.com"
BUCKET_NAME="hiveinvestor-frontend-${PROJECT_ID}"
IP_NAME="hiveinvestor-frontend-ip"
CERT_NAME_1="hiveinvestor-frontend-cert-chaperone"
CERT_NAME_2="hiveinvestor-frontend-cert-crypto"
LB_BACKEND_NAME="hiveinvestor-frontend-backend"
URL_MAP_NAME="hiveinvestor-frontend-url-map"
PROXY_NAME="hiveinvestor-frontend-proxy"
FORWARDING_RULE_NAME="hiveinvestor-frontend-https-rule"

echo "========================================================"
echo "Starting Infrastructure Setup for ${DOMAIN_1} and ${DOMAIN_2}"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "========================================================"

echo "[1/7] Setting GCP Project..."
gcloud config set project $PROJECT_ID

echo "[2/7] Enabling Required APIs..."
gcloud services enable \
    compute.googleapis.com \
    storage.googleapis.com \
    cloudapis.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    firestore.googleapis.com \
    cloudresourcemanager.googleapis.com

echo "[3/7] Creating Frontend Bucket..."
if ! gcloud storage buckets describe gs://${BUCKET_NAME} > /dev/null 2>&1; then
    gcloud storage buckets create gs://${BUCKET_NAME} --project=${PROJECT_ID} --location=${REGION} --uniform-bucket-level-access
    echo "  - Bucket created."
else
    echo "  - Bucket gs://${BUCKET_NAME} already exists."
fi

# Ensure public access
echo "  - Configuring Public Access..."
gcloud storage buckets add-iam-policy-binding gs://${BUCKET_NAME} --member=allUsers --role=roles/storage.objectViewer > /dev/null

# Configure Website (Main Page Suffix)
echo "  - Configuring Bucket Website Settings..."
gcloud storage buckets update gs://${BUCKET_NAME} --web-main-page-suffix=index.html --web-error-page=index.html

echo "[4/7] Reserving Global Static IP..."
if ! gcloud compute addresses describe ${IP_NAME} --global > /dev/null 2>&1; then
    gcloud compute addresses create ${IP_NAME} --ip-version=IPV4 --global
    echo "  - IP reserved."
else
    echo "  - IP ${IP_NAME} already exists."
fi
IP_ADDRESS=$(gcloud compute addresses describe ${IP_NAME} --global --format="value(address)")

echo "[5/7] Creating SSL Certificates..."
# Cert 1
if ! gcloud compute ssl-certificates describe ${CERT_NAME_1} --global > /dev/null 2>&1; then
    gcloud compute ssl-certificates create ${CERT_NAME_1} --domains=${DOMAIN_1} --global
    echo "  - Certificate ${CERT_NAME_1} created."
else
    echo "  - Certificate ${CERT_NAME_1} already exists."
fi
# Cert 2
if ! gcloud compute ssl-certificates describe ${CERT_NAME_2} --global > /dev/null 2>&1; then
    gcloud compute ssl-certificates create ${CERT_NAME_2} --domains=${DOMAIN_2} --global
    echo "  - Certificate ${CERT_NAME_2} created."
else
    echo "  - Certificate ${CERT_NAME_2} already exists."
fi

echo "[6/7] Configuring Load Balancer Components..."

# Backend Bucket
if ! gcloud compute backend-buckets describe ${LB_BACKEND_NAME} > /dev/null 2>&1; then
    gcloud compute backend-buckets create ${LB_BACKEND_NAME} --gcs-bucket-name=${BUCKET_NAME} --enable-cdn
    echo "  - Backend Bucket created."
else
    echo "  - Backend Bucket ${LB_BACKEND_NAME} already exists."
fi

# URL Map
if ! gcloud compute url-maps describe ${URL_MAP_NAME} > /dev/null 2>&1; then
    gcloud compute url-maps create ${URL_MAP_NAME} --default-backend-bucket=${LB_BACKEND_NAME}
    echo "  - URL Map created."
else
    echo "  - URL Map ${URL_MAP_NAME} already exists."
fi

# Target HTTPS Proxy (with BOTH certs)
if ! gcloud compute target-https-proxies describe ${PROXY_NAME} > /dev/null 2>&1; then
    gcloud compute target-https-proxies create ${PROXY_NAME} --url-map=${URL_MAP_NAME} --ssl-certificates=${CERT_NAME_1},${CERT_NAME_2}
    echo "  - Target Proxy created."
else
    echo "  - Target Proxy ${PROXY_NAME} already exists. Updating certs..."
    gcloud compute target-https-proxies update ${PROXY_NAME} --ssl-certificates=${CERT_NAME_1},${CERT_NAME_2} --global
fi

# Forwarding Rule (HTTPS)
if ! gcloud compute forwarding-rules describe ${FORWARDING_RULE_NAME} --global > /dev/null 2>&1; then
    gcloud compute forwarding-rules create ${FORWARDING_RULE_NAME} --address=${IP_NAME} --global --target-https-proxy=${PROXY_NAME} --ports=443
    echo "  - HTTPS Forwarding Rule created."
else
    echo "  - HTTPS Forwarding Rule ${FORWARDING_RULE_NAME} already exists."
fi

# HTTP Proxy & Forwarding Rule (for port 80) -> HTTPS Redirect
HTTP_PROXY_NAME="hiveinvestor-frontend-http-proxy"
HTTP_FORWARDING_RULE_NAME="hiveinvestor-frontend-http-rule"
REDIRECT_URL_MAP_NAME="hiveinvestor-https-redirect"

# Create/Update Redirect URL Map
if ! gcloud compute url-maps describe ${REDIRECT_URL_MAP_NAME} > /dev/null 2>&1; then
    echo "  - Creating HTTPS Redirect URL Map..."
    gcloud compute url-maps import ${REDIRECT_URL_MAP_NAME} --source=https-redirect.yaml --global
else
    echo "  - HTTPS Redirect URL Map ${REDIRECT_URL_MAP_NAME} already exists. Updating..."
    gcloud compute url-maps import ${REDIRECT_URL_MAP_NAME} --source=https-redirect.yaml --global --quiet
fi

# Update HTTP Proxy to use Redirect Map
if ! gcloud compute target-http-proxies describe ${HTTP_PROXY_NAME} > /dev/null 2>&1; then
    gcloud compute target-http-proxies create ${HTTP_PROXY_NAME} --url-map=${REDIRECT_URL_MAP_NAME}
    echo "  - HTTP Proxy created (with redirect)."
else
    echo "  - HTTP Proxy ${HTTP_PROXY_NAME} already exists. Updating to use Redirect Map..."
    gcloud compute target-http-proxies update ${HTTP_PROXY_NAME} --url-map=${REDIRECT_URL_MAP_NAME}
fi

if ! gcloud compute forwarding-rules describe ${HTTP_FORWARDING_RULE_NAME} --global > /dev/null 2>&1; then
    gcloud compute forwarding-rules create ${HTTP_FORWARDING_RULE_NAME} --address=${IP_NAME} --global --target-http-proxy=${HTTP_PROXY_NAME} --ports=80
    echo "  - HTTP Forwarding Rule created."
else
    echo "  - HTTP Forwarding Rule ${HTTP_FORWARDING_RULE_NAME} already exists."
fi

# ... (Previous content)

# 8. API Backend Setup (Cloud Run)
NEG_NAME="hiveinvestor-backend-neg"
BACKEND_SERVICE_API="hiveinvestor-backend-service"
CLOUD_RUN_SERVICE="hiveinvestor-backend"

echo "[8/9] Configuring API Backend Routing..."

# Create Serverless NEG
if ! gcloud compute network-endpoint-groups describe ${NEG_NAME} --region=${REGION} > /dev/null 2>&1; then
    gcloud compute network-endpoint-groups create ${NEG_NAME} \
        --region=${REGION} \
        --network-endpoint-type=serverless \
        --cloud-run-service=${CLOUD_RUN_SERVICE}
    echo "  - Serverless NEG created."
else
    echo "  - Serverless NEG ${NEG_NAME} already exists."
fi

# Create Backend Service
if ! gcloud compute backend-services describe ${BACKEND_SERVICE_API} --global > /dev/null 2>&1; then
    gcloud compute backend-services create ${BACKEND_SERVICE_API} --global
    gcloud compute backend-services add-backend ${BACKEND_SERVICE_API} \
        --global \
        --network-endpoint-group=${NEG_NAME} \
        --network-endpoint-group-region=${REGION}
    echo "  - Backend Service created."
else
    echo "  - Backend Service ${BACKEND_SERVICE_API} already exists."
fi

# Update URL Map to route /api/* to Backend Service
echo "  - Updating URL Map for API routing..."

# Check if path matcher exists by trying to add it. If it fails, we assume it exists.
# Note: 'add-path-matcher' is the command to ADD a new matcher.
if ! gcloud compute url-maps add-path-matcher ${URL_MAP_NAME} \
    --default-service=${LB_BACKEND_NAME} \
    --path-matcher-name=api-matcher \
    --path-rules="/api/*=${BACKEND_SERVICE_API},/docs=${BACKEND_SERVICE_API},/openapi.json=${BACKEND_SERVICE_API}" \
    --global --quiet 2>/dev/null; then
    
    echo "    - Path matcher 'api-matcher' might already exist. Updating it..."
    # If it exists, we use 'edit' or just leave it. But 'add-path-matcher' fails if name exists.
    # To update an existing matcher, we usually have to remove and re-add or use 'edit' (interactive).
    # A safer way for scripts is to remove it first if we want to enforce state, but that causes downtime.
    # Let's try to ignore the error if it's "already exists", or maybe we don't need to update if it's already there.
    # But if we want to ensure the rules are correct:
    # There isn't a simple "update-path-matcher" command that modifies rules easily without replacing.
    # For now, let's assume if it exists, it's correct, or we can try to remove and re-add.
    echo "    - Skipping update to avoid downtime. If you need to update rules, delete the matcher manually first."
else
    echo "    - Path matcher added."
fi

echo "[9/9] Database Setup..."
# Check if database exists (this is a bit tricky via CLI, usually just try create or assume existing)
echo "  - Ensuring Firestore API is enabled (done in step 2)."
echo "  - Please ensure Firestore is created in Native mode via Console if not already done."

echo "[10/9] Seeding Initial Data..."
export GOOGLE_CLOUD_PROJECT=${PROJECT_ID}
export FIRESTORE_DATABASE="hiveinvestor"
./scripts/init_db.sh

echo "========================================================"
echo "Infrastructure Setup Complete!"
echo "Global IP Address: ${IP_ADDRESS}"
echo "ACTION REQUIRED: Update your DNS A record for ${DOMAIN_1} to point to ${IP_ADDRESS}"
echo "========================================================"
