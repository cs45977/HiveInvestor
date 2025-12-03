import os
from google.cloud import firestore
from google.auth.credentials import AnonymousCredentials

def get_db():
    if os.environ.get("FIRESTORE_EMULATOR_HOST"):
        return firestore.Client(
            project=os.environ.get("GCLOUD_PROJECT", "demo-hiveinvestor"),
            credentials=AnonymousCredentials()
        )
    return firestore.Client()
