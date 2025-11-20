from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, portfolios, market, trade, transactions

app = FastAPI()

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(portfolios.router, prefix="/api/v1/portfolios", tags=["portfolios"])
app.include_router(market.router, prefix="/api/v1/market", tags=["market"])
app.include_router(trade.router, prefix="/api/v1/trade", tags=["trade"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])

@app.get("/")
def read_root():
    return {"Hello": "Brave New World"}
