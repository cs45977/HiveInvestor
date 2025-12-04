from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock firestore before importing main
with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.api.deps import get_current_user, get_db
    from app.models.market import StockQuote

client = TestClient(app)

def mock_get_current_user():
    return {"id": "test_user_id", "email": "test@example.com"}

def mock_get_db():
    return MagicMock()

app.dependency_overrides[get_current_user] = mock_get_current_user
app.dependency_overrides[get_db] = mock_get_db

def test_buy_stock_success():
    # Mock result from service
    mock_transaction_result = {
        "id": "tx_123",
        "user_id": "test_user_id",
        "symbol": "AAPL",
        "type": "BUY",
        "quantity": 10,
        "price_per_share": 150.0,
        "total_amount": 1510.0,
        "commission": 10.0,
        "timestamp": "2023-01-01T00:00:00Z"
    }

    # We assume the endpoint will exist at app.api.v1.endpoints.trade
    # And it will call execute_trade from app.services.trading
    with patch("app.services.trading.execute_trade", new_callable=AsyncMock) as mock_trade:
        mock_trade.return_value = mock_transaction_result
        
        payload = {"symbol": "AAPL", "quantity": 10, "type": "BUY"}
        response = client.post("/api/v1/trade/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_amount"] == 1510.0
        assert data["type"] == "BUY"
        
        mock_trade.assert_called_once()

def test_limit_order_valid():
    # Mock result for a limit order (which might be PENDING or Executed)
    mock_transaction_result = {
        "id": "tx_124",
        "user_id": "test_user_id",
        "symbol": "AAPL",
        "type": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "limit_price": 145.0,
        "status": "PENDING",
        "timestamp": "2023-01-01T00:00:00Z"
    }

    with patch("app.services.trading.execute_trade", new_callable=AsyncMock) as mock_trade:
        mock_trade.return_value = mock_transaction_result
        
        payload = {
            "symbol": "AAPL", 
            "quantity": 10, 
            "type": "BUY",
            "order_type": "LIMIT",
            "limit_price": 145.0,
            "time_in_force": "DAY"
        }
        response = client.post("/api/v1/trade/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["order_type"] == "LIMIT"
        assert data["limit_price"] == 145.0
        
        # Verify arguments passed to service
        call_args = mock_trade.call_args
        # We can inspect args if needed, but ensuring 200 OK and response data is good start

def test_limit_order_missing_price():
    # Should fail validation before service call
    payload = {
        "symbol": "AAPL", 
        "quantity": 10, 
        "type": "BUY",
        "order_type": "LIMIT",
        # Missing limit_price
        "time_in_force": "DAY"
    }
    response = client.post("/api/v1/trade/", json=payload)
    assert response.status_code == 422 # Validation error

def test_tif_invalid():
    payload = {
        "symbol": "AAPL", 
        "quantity": 10, 
        "type": "BUY",
        "order_type": "MARKET",
        "time_in_force": "FOREVER" # Invalid
    }
    response = client.post("/api/v1/trade/", json=payload)
    assert response.status_code == 422
