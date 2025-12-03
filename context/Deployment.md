# Deployment Guide: HiveInvestor on Google Cloud Platform

This guide outlines the steps to deploy the HiveInvestor application to Google Cloud Platform (GCP). The deployment strategy leverages Cloud Storage/CDN for the frontend, Cloud Run for the backend API, Firestore for the database, and Cloud Functions/Cloud Run Jobs for portfolio evaluation.

## 1. Prerequisites

Before you begin, ensure you have the following:

*   **GCP Project:** A Google Cloud Project with billing enabled.
*   **Google Cloud SDK:** Installed and authenticated on your local machine. If not, follow the instructions [here](https://cloud.google.com/sdk/docs/install).
*   **Required APIs Enabled:** Ensure the following APIs are enabled in your GCP project:
    *   Cloud Run API
    *   Cloud Storage API
    *   Cloud CDN API
    *   Firestore API
    *   Cloud Functions API (if using Cloud Functions for evaluator)
    *   Cloud Scheduler API
    *   Cloud Pub/Sub API
    *   Secret Manager API
*   **Container Registry/Artifact Registry:** Enabled for storing Docker images.

## 2. Setup Google Cloud Project

1.  **Set your GCP Project ID:**
    ```bash
    gcloud config set project YOUR_GCP_PROJECT_ID
    ```
2.  **Set your default compute region:**
    ```bash
    gcloud config set compute/region YOUR_GCP_REGION # e.g., us-central1
    ```

## 3. Database Setup (Firestore)

1.  **Create a Firestore Database:**
    Navigate to the Firestore section in the GCP Console and create a new database in "Native mode". Choose a suitable location.

## 4. Backend Deployment (FastAPI on Cloud Run)

### 4.1. Containerize the FastAPI Application

Create a `Dockerfile` in your backend project root (e.g., `/backend/Dockerfile`):

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run uvicorn to serve the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create a `requirements.txt` file in your backend project root:

```
fastapi
uvicorn[standard]
google-cloud-firestore
# Add any other Python dependencies here
```

### 4.2. Build and Push Docker Image

1.  Navigate to your backend directory:
    ```bash
    cd /Users/cwserna/code/gemini-demo/backend
    ```
2.  Build the Docker image:
    ```bash
    gcloud builds submit --tag gcr.io/YOUR_GCP_PROJECT_ID/hiveinvestor-backend
    ```
    (Replace `gcr.io` with `REGION-docker.pkg.dev/YOUR_GCP_PROJECT_ID/REPOSITORY` if using Artifact Registry)

### 4.3. Deploy to Cloud Run

```bash
gcloud run deploy hiveinvestor-backend \
    --image gcr.io/YOUR_GCP_PROJECT_ID/hiveinvestor-backend \
    --platform managed \
    --region YOUR_GCP_REGION \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID \
    --update-secrets API_KEY=API_KEY:latest # Example for external API key
```

*   Replace `YOUR_GCP_PROJECT_ID` and `YOUR_GCP_REGION`.
*   `--allow-unauthenticated` is for public APIs. Adjust if authentication is required at the Cloud Run level.
*   `--update-secrets` is used to inject secrets from Google Secret Manager. Ensure your secrets are configured there.

## 5. Frontend Deployment (Vue.js on Cloud Storage with Cloud CDN)

### 5.1. Build the Vue.js Application

1.  Navigate to your frontend directory:
    ```bash
    cd /Users/cwserna/code/gemini-demo/frontend
    ```
2.  Build your Vue.js application for production:
    ```bash
    npm run build
    ```
    This will create a `dist` directory (or similar) containing your static assets.

### 5.2. Create a Cloud Storage Bucket

```bash
gcloud storage buckets create gs://YOUR_FRONTEND_BUCKET_NAME \
    --project=YOUR_GCP_PROJECT_ID \
    --uniform-bucket-level-access \
    --location=YOUR_GCP_REGION
```

*   Choose a unique bucket name (e.g., `hiveinvestor-frontend-yourprojectid`).

### 5.3. Upload Frontend Assets to Cloud Storage

```bash
gcloud storage cp -r dist/* gs://YOUR_FRONTEND_BUCKET_NAME/
```

### 5.4. Configure Public Access

Make the bucket content publicly readable:

```bash
gcloud storage buckets add-iam-policy-binding gs://YOUR_FRONTEND_BUCKET_NAME \
    --member=allUsers \
    --role=roles/storage.objectViewer
```

### 5.5. Configure Cloud CDN (Optional, but Recommended)

1.  **Create a Load Balancer Backend Bucket:**
    ```bash
    gcloud compute backend-buckets create hiveinvestor-frontend-backend \
        --gcs-bucket-name=YOUR_FRONTEND_BUCKET_NAME \
        --enable-cdn
    ```
2.  **Create a URL Map:**
    ```bash
    gcloud compute url-maps create hiveinvestor-frontend-url-map \
        --default-backend-bucket=hiveinvestor-frontend-backend
    ```
3.  **Create an SSL Certificate (Managed by Google):**
    ```bash
    gcloud compute ssl-certificates create hiveinvestor-frontend-cert \
        --domains=YOUR_CUSTOM_DOMAIN \
        --global
    ```
    *   Replace `YOUR_CUSTOM_DOMAIN` with your actual domain (e.g., `app.hiveinvestor.com`). DNS records must point to the load balancer's IP.
4.  **Create a Global External IP Address:**
    ```bash
    gcloud compute addresses create hiveinvestor-frontend-ip \
        --ip-version=IPV4 \
        --global
    ```
    Note the IP address returned.
5.  **Create a Target HTTPS Proxy:**
    ```bash
    gcloud compute target-https-proxies create hiveinvestor-frontend-proxy \
        --url-map=hiveinvestor-frontend-url-map \
        --ssl-certificates=hiveinvestor-frontend-cert
    ```
6.  **Create a Global Forwarding Rule:**
    ```bash
    gcloud compute forwarding-rules create hiveinvestor-frontend-https-rule \
        --address=hiveinvestor-frontend-ip \
        --global \
        --target-https-proxy=hiveinvestor-frontend-proxy \
        --ports=443
    ```
    Update your DNS `A` record for `YOUR_CUSTOM_DOMAIN` to point to `hiveinvestor-frontend-ip`.

## 6. Portfolio Evaluator Deployment (Cloud Functions/Cloud Run Jobs)

Choose either Cloud Functions or Cloud Run Jobs for the periodic portfolio evaluation.

### Option A: Cloud Functions

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
        --region YOUR_GCP_REGION \
        --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
    ```

### Option B: Cloud Run Jobs

1.  **Containerize your evaluation script.**
    Create a `Dockerfile` for your evaluation job (similar to backend, but `CMD` runs the script).
2.  **Build and Push Docker Image:**
    ```bash
    gcloud builds submit --tag gcr.io/YOUR_GCP_PROJECT_ID/hiveinvestor-evaluator-job
    ```
3.  **Deploy as a Cloud Run Job:**
    ```bash
gcloud run jobs create hiveinvestor-evaluator-job \
        --image gcr.io/YOUR_GCP_PROJECT_ID/hiveinvestor-evaluator-job \
        --region YOUR_GCP_REGION \
        --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
    ```

### 6.1. Schedule with Cloud Scheduler (for both options)

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
        --location YOUR_GCP_REGION
    ```
    This example schedules the job to run daily at midnight UTC.

## 7. Secrets Management (Google Secret Manager)

### 7.1 Finnhub API Setup
HiveInvestor uses **Finnhub.io** for real-time stock quotes. You must obtain an API key and configure it for the application to function correctly in production.

1.  **Obtain API Key:**
    *   Register at [Finnhub.io](https://finnhub.io/).
    *   Get your free or paid API key from the dashboard.

2.  **Store the API Key in Secret Manager:**
    ```bash
    echo -n "YOUR_FINNHUB_API_KEY" | gcloud secrets create FINNHUB_API_KEY --data-file=-
    ```

### 7.2 Other Secrets
1.  **Store other secrets (e.g., JWT Secret):**
    ```bash
    echo -n "your-jwt-secret-value" | gcloud secrets create SECRET_KEY --data-file=-
    ```

2.  **Grant access to Cloud Run Service Account:**
    Ensure the Cloud Run service account (`PROJECT_NUMBER-compute@developer.gserviceaccount.com`) has the `Secret Manager Secret Accessor` role.

## 8. Continuous Integration/Continuous Deployment (CI/CD)

### Updated Backend Deployment Command
When deploying the backend to Cloud Run, ensure you inject the secrets as environment variables:

```bash
gcloud run deploy hiveinvestor-backend \
    --image gcr.io/YOUR_GCP_PROJECT_ID/hiveinvestor-backend \
    --platform managed \
    --region YOUR_GCP_REGION \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID \
    --update-secrets FINNHUB_API_KEY=FINNHUB_API_KEY:latest,SECRET_KEY=SECRET_KEY:latest
```

Consider using Cloud Build to automate the build, test, and deployment process for both frontend and backend. This typically involves creating `cloudbuild.yaml` files in your repositories.

This completes the deployment guide for HiveInvestor on Google Cloud Platform.
