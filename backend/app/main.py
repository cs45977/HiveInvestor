from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import users, auth, portfolios, market, trade, transactions, leaderboard

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

import os
from app.db.firestore import get_db

@app.get("/api/status")
def get_status():
    db_status = "Unknown"
    db_name = os.getenv("FIRESTORE_DATABASE", "(default)")
    try:
        db = get_db()
        # Simple check: try to get a reference, maybe list collections
        # Note: collections() returns a generator.
        collections = db.collections()
        # We just need to know if the call succeeds
        for _ in collections:
            break
        db_status = "Connected"
    except Exception as e:
        db_status = f"Failed: {str(e)}"

    return {
        "status": "Backend Connected",
        "database_status": db_status,
        "database_name": db_name
    }
