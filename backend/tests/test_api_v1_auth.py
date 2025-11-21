from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock firestore before importing main
with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.db.firestore import get_db

client = TestClient(app)

def test_login_success():
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    
    # Simulate user found in DB
    mock_user_doc = MagicMock()
    mock_user_doc.to_dict.return_value = {
        "email": "user@example.com",
        "username": "user@example.com",
        "hashed_password": "hashed_secret",
        "id": "123"
    }
    # Mock streaming results
    # The query chain is where().limit().stream()
    mock_query = mock_collection.where.return_value
    mock_query.limit.return_value.stream.return_value = [mock_user_doc]
    # Fallback for where().stream() if limit is not used (good practice for robust mocks)
    mock_query.stream.return_value = [mock_user_doc]
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    payload = {
        "username": "user@example.com",
        "password": "password"
    }
    
    with patch("app.core.security.verify_password", return_value=True):
        with patch("app.core.security.create_access_token", return_value="mock_token"):
            response = client.post("/api/v1/users/login", data=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "mock_token"
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    
    mock_user_doc = MagicMock()
    mock_user_doc.to_dict.return_value = {
        "email": "user@example.com",
        "hashed_password": "hashed_secret"
    }
    mock_collection.where.return_value.limit.return_value.stream.return_value = [mock_user_doc]
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    payload = {
        "username": "user@example.com",
        "password": "wrongpassword"
    }
    
    with patch("app.core.security.verify_password", return_value=False):
        response = client.post("/api/v1/users/login", data=payload)
    
    assert response.status_code == 401


def test_login_non_existent_user():
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    mock_collection.where.return_value.limit.return_value.stream.return_value = []
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    payload = {
        "username": "unknown@example.com",
        "password": "password"
    }
    
    response = client.post("/api/v1/users/login", data=payload)
    
    assert response.status_code == 401
