from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, portfolios, market, trade, transactions, leaderboard

app = FastAPI()

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(portfolios.router, prefix="/api/v1/portfolios", tags=["portfolios"])
app.include_router(market.router, prefix="/api/v1/market", tags=["market"])
app.include_router(trade.router, prefix="/api/v1/trade", tags=["trade"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(leaderboard.router, prefix="/api/v1/leaderboard", tags=["leaderboard"])

@app.get("/")
def read_root():
    return {"Hello": "Brave New World"}

@app.get("/api/status")
def get_status():
    from app.db.firestore import get_db
    from google.cloud import firestore
    
    db_status = "Disconnected"
    try:
        db = get_db()
        # Attempt a lightweight operation to verify connection
        # We just check if we can get a collection reference (client initialization check)
        # For a deeper check, we'd try to read a doc, but client init is usually enough to catch config errors
        # To be sure, let's try to list collections (might be empty, that's fine)
        # Note: list_collections is a generator.
        # Simply initializing the client often doesn't throw until a request is made.
        # We will try to access a dummy document.
        doc_ref = db.collection("health").document("ping")
        doc = doc_ref.get()
        db_status = "Connected" 
    except Exception as e:
        # If it fails (e.g. auth error, connection refused), we catch it
        db_status = f"Disconnected: {str(e)}"

    return {
        "backend_status": "Connected",
        "db_status": db_status
    }
