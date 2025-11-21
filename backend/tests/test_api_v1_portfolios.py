from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend directory to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock firestore before importing main
with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.db.firestore import get_db
    from app.api.deps import get_current_user

client = TestClient(app)

def get_mock_db():
    mock_db = MagicMock()
    return mock_db

def mock_get_current_user():
    return {"id": "test_user_id", "email": "test@example.com", "username": "testuser"}

# Override dependencies globally for this test file
app.dependency_overrides[get_current_user] = mock_get_current_user

def test_create_portfolio_success():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Setup mock: Portfolio document does NOT exist
    mock_portfolio_ref = MagicMock()
    mock_portfolio_ref.get.return_value.exists = False
    
    # When looking up 'portfolios' collection -> document 'test_user_id'
    mock_db.collection.return_value.document.return_value = mock_portfolio_ref

    response = client.post("/api/v1/portfolios/")
    
    assert response.status_code == 201
    data = response.json()
    assert data["cash_balance"] == 100000.0
    assert data["total_value"] == 100000.0
    assert data["user_id"] == "test_user_id"
    
    # Verify set() was called to save the portfolio
    assert mock_portfolio_ref.set.called

def test_create_portfolio_already_exists():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Setup mock: Portfolio document DOES exist
    mock_portfolio_ref = MagicMock()
    mock_portfolio_ref.get.return_value.exists = True
    
    mock_db.collection.return_value.document.return_value = mock_portfolio_ref

    response = client.post("/api/v1/portfolios/")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Portfolio already exists for this user"

def test_get_portfolio_success():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Setup mock: Portfolio document exists and returns data
    mock_portfolio_ref = MagicMock()
    mock_portfolio_ref.get.return_value.exists = True
    mock_portfolio_ref.get.return_value.to_dict.return_value = {
        "user_id": "test_user_id",
        "cash_balance": 100000.0,
        "total_value": 100000.0,
        "holdings": [],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }
    
    mock_db.collection.return_value.document.return_value = mock_portfolio_ref

    response = client.get("/api/v1/portfolios/me")
    
    assert response.status_code == 200
    data = response.json()
    assert data["cash_balance"] == 100000.0
    assert data["user_id"] == "test_user_id"

def test_get_portfolio_not_found():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Setup mock: Portfolio document does NOT exist
    mock_portfolio_ref = MagicMock()
    mock_portfolio_ref.get.return_value.exists = False
    
    mock_db.collection.return_value.document.return_value = mock_portfolio_ref

    response = client.get("/api/v1/portfolios/me")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Portfolio not found"
