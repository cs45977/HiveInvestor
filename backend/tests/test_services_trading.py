import pytest
from fastapi import HTTPException
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.trading import validate_and_calculate_buy, validate_and_calculate_sell

def test_validate_and_calculate_buy_success():
    portfolio = {
        "cash_balance": 2000.0,
        "holdings": []
    }
    price = 150.0
    quantity = 10
    
    updated_portfolio, total_cost = validate_and_calculate_buy(portfolio, "AAPL", quantity, price)
    
    assert updated_portfolio["cash_balance"] == 490.0
    assert total_cost == 1510.0
    holding = next(h for h in updated_portfolio["holdings"] if h["symbol"] == "AAPL")
    assert holding["quantity"] == 10

def test_validate_and_calculate_buy_insufficient_funds():
    portfolio = {
        "cash_balance": 100.0,
        "holdings": []
    }
    price = 150.0
    quantity = 10
    
    with pytest.raises(HTTPException) as exc:
        validate_and_calculate_buy(portfolio, "AAPL", quantity, price)
    
    assert exc.value.status_code == 400
    assert "Insufficient funds" in exc.value.detail

def test_validate_and_calculate_sell_success():
    portfolio = {
        "cash_balance": 100.0,
        "holdings": [{"symbol": "AAPL", "quantity": 10, "average_price": 100.0}]
    }
    price = 150.0
    quantity = 5
    # Proceeds = (150*5) - 10 = 740. Cash = 840.
    
    updated_portfolio, total_amount = validate_and_calculate_sell(portfolio, "AAPL", quantity, price)
    
    assert updated_portfolio["cash_balance"] == 840.0
    assert total_amount == 740.0
    holding = next(h for h in updated_portfolio["holdings"] if h["symbol"] == "AAPL")
    assert holding["quantity"] == 5

def test_validate_and_calculate_sell_insufficient_holdings():
    portfolio = {
        "cash_balance": 100.0,
        "holdings": [{"symbol": "AAPL", "quantity": 2}]
    }
    price = 150.0
    quantity = 5
    
    with pytest.raises(HTTPException) as exc:
        validate_and_calculate_sell(portfolio, "AAPL", quantity, price)
    
    assert exc.value.status_code == 400
    assert "Insufficient holdings" in exc.value.detail
