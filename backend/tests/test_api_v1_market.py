from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.market import StockQuote

# Mock firestore before importing main
with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.api.deps import get_current_user

client = TestClient(app)

def mock_get_current_user():
    return {"id": "test_user_id", "email": "test@example.com"}

app.dependency_overrides[get_current_user] = mock_get_current_user

def test_get_quote_endpoint_success():
    mock_quote = StockQuote(
        symbol="AAPL",
        price=150.0,
        change=1.5,
        percent_change=1.0
    )
    
    # Patch the function where it is USED
    with patch("app.api.v1.endpoints.market.get_real_time_quote", new_callable=AsyncMock) as mock_service:
        mock_service.return_value = mock_quote
        
        response = client.get("/api/v1/market/quote/AAPL")
        
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["price"] == 150.0

def test_get_quote_endpoint_not_found():
    # We simulate the service raising HTTPException(404)
    # Note: We need to import HTTPException inside or mock side_effect
    from fastapi import HTTPException
    
    with patch("app.api.v1.endpoints.market.get_real_time_quote", new_callable=AsyncMock) as mock_service:
        mock_service.side_effect = HTTPException(status_code=404, detail="Symbol INVALID not found")
        
        response = client.get("/api/v1/market/quote/INVALID")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Symbol INVALID not found"
