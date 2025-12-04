from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock firestore before importing main
with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.api.deps import get_current_user, get_db

client = TestClient(app)

def mock_get_current_user():
    return {"id": "test_user_id", "email": "test@example.com"}

app.dependency_overrides[get_current_user] = mock_get_current_user

def test_cancel_transaction_success():
    mock_db = MagicMock()
    mock_doc_ref = MagicMock()
    mock_doc_snapshot = MagicMock()
    
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {
        "id": "tx123",
        "user_id": "test_user_id",
        "status": "PENDING"
    }
    
    mock_doc_ref.get.return_value = mock_doc_snapshot
    mock_db.collection.return_value.document.return_value = mock_doc_ref
    
    # Override get_db
    app.dependency_overrides[get_db] = lambda: mock_db
    
    try:
        response = client.post("/api/v1/transactions/tx123/cancel")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Transaction cancelled successfully"
        mock_doc_ref.update.assert_called_with({"status": "CANCELLED"})
    finally:
        del app.dependency_overrides[get_db]

def test_cancel_transaction_not_pending():
    mock_db = MagicMock()
    mock_doc_ref = MagicMock()
    mock_doc_snapshot = MagicMock()
    
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {
        "id": "tx123",
        "user_id": "test_user_id",
        "status": "EXECUTED"
    }
    
    mock_doc_ref.get.return_value = mock_doc_snapshot
    mock_db.collection.return_value.document.return_value = mock_doc_ref
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    try:
        response = client.post("/api/v1/transactions/tx123/cancel")
        
        assert response.status_code == 400
    finally:
        del app.dependency_overrides[get_db]
