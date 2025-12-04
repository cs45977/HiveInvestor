from app.models.trade import TradeRequest, TradeResponse
from app.services.market_data import get_real_time_quote
from fastapi import HTTPException, status
from datetime import datetime, timezone
import uuid
from google.cloud import firestore

COMMISSION_FEE = 10.0

def validate_and_calculate_buy(portfolio: dict, symbol: str, quantity: int, price: float):
    total_cost = (price * quantity) + COMMISSION_FEE
    
    if portfolio.get("cash_balance", 0) < total_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    
    updated_portfolio = portfolio.copy()
    updated_portfolio["cash_balance"] = round(updated_portfolio.get("cash_balance", 0) - total_cost, 2)
    
    holdings = list(updated_portfolio.get("holdings", []))
    existing_holding = next((h for h in holdings if h["symbol"] == symbol), None)
    
    if existing_holding:
        old_qty = existing_holding["quantity"]
        old_avg = existing_holding.get("average_price", 0.0)
        new_qty = old_qty + quantity
        new_avg = ((old_qty * old_avg) + (quantity * price)) / new_qty
        
        holdings.remove(existing_holding)
        holdings.append({
            "symbol": symbol,
            "quantity": new_qty,
            "average_price": round(new_avg, 2)
        })
    else:
        holdings.append({
            "symbol": symbol,
            "quantity": quantity,
            "average_price": price
        })
    
    updated_portfolio["holdings"] = holdings
    return updated_portfolio, total_cost

def validate_and_calculate_sell(portfolio: dict, symbol: str, quantity: int, price: float):
    holdings = list(portfolio.get("holdings", []))
    existing_holding = next((h for h in holdings if h["symbol"] == symbol), None)
    
    if not existing_holding or existing_holding["quantity"] < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient holdings"
        )
    
    proceeds = (price * quantity) - COMMISSION_FEE
    
    updated_portfolio = portfolio.copy()
    updated_portfolio["cash_balance"] = round(updated_portfolio.get("cash_balance", 0) + proceeds, 2)
    
    new_qty = existing_holding["quantity"] - quantity
    holdings.remove(existing_holding)
    
    if new_qty > 0:
        holdings.append({
            "symbol": symbol,
            "quantity": new_qty,
            "average_price": existing_holding.get("average_price", 0.0)
        })
    
    updated_portfolio["holdings"] = holdings
    return updated_portfolio, proceeds

@firestore.transactional
def update_in_transaction(transaction, portfolio_ref, trade_request, price):
    snapshot = portfolio_ref.get(transaction=transaction)
    if not snapshot.exists:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio = snapshot.to_dict()
    
    if trade_request.type == "BUY":
        updated_portfolio, amount = validate_and_calculate_buy(
            portfolio, trade_request.symbol, trade_request.quantity, price
        )
    else:
        updated_portfolio, amount = validate_and_calculate_sell(
            portfolio, trade_request.symbol, trade_request.quantity, price
        )
    
    transaction.update(portfolio_ref, updated_portfolio)
    return amount, updated_portfolio

async def execute_trade(user_id: str, trade_request: TradeRequest, db) -> dict:
    quote = await get_real_time_quote(trade_request.symbol)
    
    # Check Limit Order Condition
    if trade_request.order_type == "LIMIT":
        is_buy_marketable = trade_request.type == "BUY" and quote.price <= trade_request.limit_price
        is_sell_marketable = trade_request.type == "SELL" and quote.price >= trade_request.limit_price
        
        if not (is_buy_marketable or is_sell_marketable):
            # Order is not marketable, save as PENDING
            # In a real system, we'd reserve cash/inventory here. For MVP, we just log it.
            transaction_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "symbol": trade_request.symbol,
                "type": trade_request.type,
                "order_type": trade_request.order_type,
                "limit_price": trade_request.limit_price,
                "time_in_force": trade_request.time_in_force,
                "quantity": trade_request.quantity,
                "status": "PENDING",
                "timestamp": datetime.now(timezone.utc),
                "price_per_share": None,
                "total_amount": None,
                "commission": None
            }
            # Save to a 'pending_orders' collection ideally, or 'transactions' with status
            db.collection("transactions").document(transaction_data["id"]).set(transaction_data)
            return transaction_data

    transaction = db.transaction()
    portfolio_ref = db.collection("portfolios").document(user_id)
    
    # Execute transaction (Market or Marketable Limit)
    amount, updated_portfolio = update_in_transaction(transaction, portfolio_ref, trade_request, quote.price)
    
    transaction_data = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "symbol": trade_request.symbol,
        "type": trade_request.type,
        "order_type": trade_request.order_type,
        "limit_price": trade_request.limit_price if trade_request.order_type == "LIMIT" else None,
        "time_in_force": trade_request.time_in_force,
        "quantity": trade_request.quantity,
        "status": "EXECUTED",
        "price_per_share": quote.price,
        "total_amount": round(amount, 2),
        "commission": COMMISSION_FEE,
        "timestamp": datetime.now(timezone.utc)
    }
    
    db.collection("transactions").document(transaction_data["id"]).set(transaction_data)
    
    return transaction_data
