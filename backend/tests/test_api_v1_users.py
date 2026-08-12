from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend directory to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# We need to mock firestore before importing main, as it likely initializes the client
with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.db.firestore import get_db

client = TestClient(app)

def get_mock_db():
    mock_db = MagicMock()
    return mock_db

def test_register_user_success():
    mock_db = MagicMock()
    # Setup mock: email index doc does NOT exist -> registration proceeds
    mock_email_doc = MagicMock()
    mock_email_doc.exists = False
    mock_db.collection.return_value.document.return_value.get.return_value = mock_email_doc

    app.dependency_overrides[get_db] = lambda: mock_db

    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "strongpassword123"
    }

    response = client.post("/api/v1/users/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert "id" in data
    assert "password" not in data

def test_register_user_duplicate_email():
    mock_db = MagicMock()
    # Setup mock: email index doc DOES exist -> registration blocked
    mock_email_doc = MagicMock()
    mock_email_doc.exists = True
    mock_db.collection.return_value.document.return_value.get.return_value = mock_email_doc

    app.dependency_overrides[get_db] = lambda: mock_db

    payload = {
        "email": "existing@example.com",
        "username": "existing",
        "password": "password"
    }

    response = client.post("/api/v1/users/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_register_user_missing_fields():
    # Pydantic body validation for UserCreate happens in solve_dependencies
    # alongside other Depends() params — including get_db — so a DB mock is
    # still required here even though we expect a 422 before any Firestore
    # call actually happens. This was previously masked by the (now-fixed)
    # dependency_overrides leak from an earlier test in the suite.
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db

    payload = {
        "email": "incomplete@example.com",
        "username": "incomplete"
    }
    
    response = client.post("/api/v1/users/register", json=payload)
    
    assert response.status_code == 422

def test_read_users_me_success():
    # Endpoint requires auth. Without headers, should be 401.
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_read_users_me_with_mocked_user():
    from app.api.deps import get_current_user
    
    mock_user = {
        "id": "123",
        "username": "testuser",
        "email": "test@example.com"
    }
    
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    response = client.get("/api/v1/users/me", headers={"Authorization": "Bearer mocktoken"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"



