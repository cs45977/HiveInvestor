from google.cloud import firestore
import os
from datetime import datetime, timezone

def init_db():
    print("Initializing Firestore...")
    
    # Use Application Default Credentials (gcloud auth application-default login)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0437257621")
    database_id = os.environ.get("FIRESTORE_DATABASE", "(default)")
    print(f"Connecting to Firestore project={project_id}, database={database_id}...")
    db = firestore.Client(project=project_id, database=database_id)
    
    # Create empty leaderboard documents to prevent 404s
    windows = ["1d", "7d", "30d", "90d"]
    print("Seeding Leaderboard documents...")
    
    for window in windows:
        doc_ref = db.collection("leaderboards").document(window)
        if not doc_ref.get().exists:
            doc_ref.set({
                "id": window,
                "entries": [],
                "updated_at": datetime.now(timezone.utc)
            })
            print(f"  - Created empty leaderboard for {window}")
        else:
            print(f"  - Leaderboard {window} already exists")

    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
