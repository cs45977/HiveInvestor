# Deployment Guide: HiveInvestor on Google Cloud Platform

This guide outlines the steps to deploy the HiveInvestor application to Google Cloud Platform (GCP) using the primary domain `chaperone.cloud`.

The deployment is divided into two phases:
1.  **Initial Infrastructure Setup**: One-time setup of GCP resources (Networking, Load Balancers, SSL, Databases).
2.  **Iterative Deployment**: Routine build and deployment of application code (Frontend and Backend).

## Configuration
- **Primary Domain**: `chaperone.cloud`
- **Secondary Domain**: `cryptomaison.com`
- **GCP Project ID**: `gen-lang-client-0437257621`
- **Region**: `us-central1`

---

## Part 1: Initial Infrastructure Setup

Run the `setup_infra.sh` script to provision the following resources. This only needs to be done once.

### 1. Prerequisites
Ensure you have the Google Cloud SDK installed and authenticated:
```bash
gcloud auth login
gcloud config set project gen-lang-client-0437257621
```

### 2. Resources Provisioned
The setup script will:
1.  **Enable APIs**: Cloud Run, Cloud Build, Firestore, Compute Engine, Certificate Manager, Cloud Storage, Cloud CDN, Cloud Functions, Cloud Scheduler, Cloud Pub/Sub, Secret Manager.
2.  **Network & Security**:
    - Reserve a Global Static IP Address.
    - Create a Google-managed SSL Certificate for `cryptomaison.com`.
3.  **Storage**:
    - Create a GCS Bucket for the Frontend (`gs://hiveinvestor-frontend-gen-lang-client-0437257621`).
    - Make the bucket public.
4.  **Load Balancing**:
    - Create a Global External HTTPS Load Balancer.
    - Map the Load Balancer to the Frontend Bucket.
    - Attach the SSL Certificate.
5.  **Database**:
    - Create the Firestore Database (if not exists).

### 3. DNS Configuration (Manual Step)
After running `setup_infra.sh`, the script will output a **Global Static IP Address**.
You must update your DNS provider for **both** domains (`cryptomaison.com` and `chaperone.cloud`):
- **Type**: A Record
- **Host**: @ (root)
- **Value**: [The Output IP Address]

*Note: SSL Certificates may take up to 60 minutes to provision after DNS propagation.*

---

## Part 2: Iterative Deployment

Run the `deploy_app.sh` script to build and deploy the latest code.

### Usage
```bash
./deploy_app.sh [flags]
```

**Flags:**
- `--backend-only`: Deploy only the backend.
- `--frontend-only`: Deploy only the frontend.
- `--skip-tests`: Skip unit tests (not recommended).

### Workflow
1.  **Backend Deployment**:
    - Builds the Docker image for `hiveinvestor-backend` using the `Dockerfile` in the backend project root.
    - Pushes to Google Container Registry (GCR).
    - Deploys to Cloud Run, configuring environment variables and secrets.
2.  **Frontend Deployment**:
    - Fetches the latest Backend URL from the deployed Cloud Run service.
    - Updates `.env.production` with the API URL.
    - Builds the Vue.js application (`npm run build`) from the frontend project root.
    - Uploads `dist/` to the GCS Bucket (`gs://hiveinvestor-frontend-gen-lang-client-0437257621`).
    - Invalidates Cloud CDN cache (optional/if configured).

### 5.6. Enforce HTTPS Redirect
The setup script automatically configures an HTTP-to-HTTPS redirect.
1.  **URL Map**: A dedicated URL Map `hiveinvestor-https-redirect` is created using `https-redirect.yaml`.
2.  **HTTP Proxy**: The `target-http-proxy` (port 80) uses this redirect map instead of the backend bucket.
3.  **Result**: Any request to `http://...` receives a `301 Moved Permanently` response pointing to `https://...`.

## 6. Portfolio Evaluator Deployment (Cloud Functions/Cloud Run Jobs)

Choose either Cloud Functions or Cloud Run Jobs for the periodic portfolio evaluation.

##### Option A: Cloud Functions

1.  **Create a Python function for evaluation logic.**
    Example `main.py`:
    ```python
    # main.py for Cloud Function
    from google.cloud import firestore
    import functions_framework

    @functions_framework.cloud_event
    def evaluate_portfolios(cloud_event):
        # Your portfolio evaluation logic here
        # Access Firestore, recalculate PPG, update leaderboards
        print("Running portfolio evaluation...")
        db = firestore.Client()
        # ... implement logic ...
        print("Portfolio evaluation complete.")
    ```
2.  **Deploy the Cloud Function:**
    ```bash
    gcloud functions deploy evaluate-portfolios \
        --runtime python39 \
        --trigger-topic portfolio-evaluation-topic \
        --entry-point evaluate_portfolios \
        --region us-central1 \
        --set-env-vars GOOGLE_CLOUD_PROJECT=gen-lang-client-0437257621
    ```

##### Option B: Cloud Run Jobs

1.  **Containerize your evaluation script.**
    Create a `Dockerfile` for your evaluation job (similar to backend, but `CMD` runs the script).
2.  **Build and Push Docker Image:**
    ```bash
    gcloud builds submit --tag gcr.io/gen-lang-client-0437257621/hiveinvestor-evaluator-job
    ```
3.  **Deploy as a Cloud Run Job:**
    ```bash
gcloud run jobs create hiveinvestor-evaluator-job \
        --image gcr.io/gen-lang-client-0437257621/hiveinvestor-evaluator-job \
        --region us-central1 \
        --set-env-vars GOOGLE_CLOUD_PROJECT=gen-lang-client-0437257621
    ```

##### Schedule with Cloud Scheduler (for both options)

1.  **Create a Pub/Sub Topic (if not already created for Cloud Function trigger):**
    ```bash
    gcloud pubsub topics create portfolio-evaluation-topic
    ```
2.  **Create a Cloud Scheduler Job:**
    ```bash
gcloud scheduler jobs create pubsub daily-portfolio-evaluation \
        --schedule "0 0 * * *" \
        --topic portfolio-evaluation-topic \
        --message-body "run_evaluation" \
        --location us-central1
    ```
    This example schedules the job to run daily at midnight UTC.

#### Secrets Management (Google Secret Manager)

1.  **Store your secrets:**
    ```bash
    echo -n "your-api-key-value" | gcloud secrets create API_KEY --data-file=-
    ```
2.  **Grant access to Cloud Run Service Account:**
    Ensure the Cloud Run service account (`PROJECT_NUMBER-compute@developer.gserviceaccount.com`) has the `Secret Manager Secret Accessor` role.

---

## 3. Manual Verification

### Backend
- Verify Cloud Run service is active: https://console.cloud.google.com/run
- Check logs: https://console.cloud.google.com/logs

### Frontend
- Visit `https://cryptomaison.com` and `https://chaperone.cloud`
- Verify SSL is valid (padlock icon) for both.
- Verify API calls to backend are successful.

### Database
- Verify Firestore collections: https://console.cloud.google.com/firestore
