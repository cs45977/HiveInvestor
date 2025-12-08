import os
from google.cloud import firestore

def get_db():
    # Prioritize emulator/local config, then standard GCP env var, then fallback
    project_id = os.getenv("FIRESTORE_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT") or "demo-project"
    database = os.getenv("FIRESTORE_DATABASE")
    
    if database:
        return firestore.Client(project=project_id, database=database)
    return firestore.Client(project=project_id)
