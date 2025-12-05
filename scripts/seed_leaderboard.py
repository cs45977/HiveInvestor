import asyncio
import os
import sys

# Add backend directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.db.firestore import get_db
from app.services.evaluation import generate_leaderboards

async def main():
    print("Initializing Firestore...")
    db = get_db()
    
    print("Generating Leaderboards...")
    await generate_leaderboards(db)
    print("Done!")

if __name__ == "__main__":
    # Set env vars if needed
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        os.environ["GOOGLE_CLOUD_PROJECT"] = "gen-lang-client-0437257621"
    if not os.getenv("FIRESTORE_DATABASE"):
        os.environ["FIRESTORE_DATABASE"] = "hiveinvestor"
        
    asyncio.run(main())
