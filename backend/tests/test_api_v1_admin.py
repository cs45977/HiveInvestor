from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch("google.cloud.firestore.Client"):
    from app.main import app
    from app.db.firestore import get_db
    from app.api.deps import get_current_user

client = TestClient(app)


def mock_admin_user():
    return {"id": "admin_id", "email": "admin@example.com", "username": "admin", "role": "admin"}


def mock_regular_user():
    return {"id": "user_id", "email": "user@example.com", "username": "user", "role": "user"}


def mock_legacy_user_no_role_field():
    # Simulates a user created before the role field existed.
    return {"id": "legacy_id", "email": "legacy@example.com", "username": "legacy"}


@pytest.fixture(autouse=True)
def _clear_db_override():
    yield
    app.dependency_overrides.pop(get_db, None)


def test_admin_evaluate_blocked_for_regular_user():
    app.dependency_overrides[get_current_user] = mock_regular_user
    app.dependency_overrides[get_db] = lambda: MagicMock()
    response = client.post("/api/v1/leaderboard/admin/evaluate")
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_admin_evaluate_blocked_for_legacy_user_missing_role_field():
    app.dependency_overrides[get_current_user] = mock_legacy_user_no_role_field
    app.dependency_overrides[get_db] = lambda: MagicMock()
    response = client.post("/api/v1/leaderboard/admin/evaluate")
    assert response.status_code == 403


def test_admin_evaluate_allowed_for_admin():
    app.dependency_overrides[get_current_user] = mock_admin_user
    app.dependency_overrides[get_db] = lambda: MagicMock()
    with patch("app.api.v1.endpoints.leaderboard.update_all_portfolios_total_value", new_callable=AsyncMock) as mock_update, \
         patch("app.api.v1.endpoints.leaderboard.generate_leaderboards", new_callable=AsyncMock) as mock_gen:
        response = client.post("/api/v1/leaderboard/admin/evaluate")

    assert response.status_code == 200
    assert response.json()["message"] == "Evaluation triggered successfully"
    mock_update.assert_called_once()
    mock_gen.assert_called_once()


def test_list_users_blocked_for_regular_user():
    app.dependency_overrides[get_current_user] = mock_regular_user
    app.dependency_overrides[get_db] = lambda: MagicMock()
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 403


def test_list_users_allowed_for_admin():
    mock_db = MagicMock()
    doc1 = MagicMock()
    doc1.to_dict.return_value = {"id": "u1", "email": "a@x.com", "username": "a", "role": "user"}
    doc2 = MagicMock()
    doc2.to_dict.return_value = {"id": "u2", "email": "b@x.com", "username": "b", "role": "admin"}
    mock_db.collection.return_value.stream.return_value = [doc1, doc2]

    app.dependency_overrides[get_current_user] = mock_admin_user
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get("/api/v1/admin/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {u["role"] for u in data} == {"user", "admin"}


def test_update_user_role_blocked_for_regular_user():
    app.dependency_overrides[get_current_user] = mock_regular_user
    app.dependency_overrides[get_db] = lambda: MagicMock()
    response = client.patch("/api/v1/admin/users/some_id/role", json={"role": "admin"})
    assert response.status_code == 403


def test_update_user_role_promotes_user():
    mock_db = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = True
    mock_user_doc.to_dict.return_value = {"id": "target_id", "email": "t@x.com", "username": "t", "role": "admin"}
    mock_db.collection.return_value.document.return_value.get.return_value = mock_user_doc

    app.dependency_overrides[get_current_user] = mock_admin_user
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.patch("/api/v1/admin/users/target_id/role", json={"role": "admin"})

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_update_user_role_404_when_user_missing():
    mock_db = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = False
    mock_db.collection.return_value.document.return_value.get.return_value = mock_user_doc

    app.dependency_overrides[get_current_user] = mock_admin_user
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.patch("/api/v1/admin/users/nonexistent/role", json={"role": "admin"})

    assert response.status_code == 404


def test_cannot_demote_the_only_remaining_admin():
    mock_db = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = True
    mock_db.collection.return_value.document.return_value.get.return_value = mock_user_doc

    # Only one admin exists in the system: the admin making this request.
    admin_doc = MagicMock()
    mock_db.collection.return_value.where.return_value.stream.return_value = [admin_doc]

    app.dependency_overrides[get_current_user] = mock_admin_user
    app.dependency_overrides[get_db] = lambda: mock_db

    # admin_id matches mock_admin_user()'s own id -- self-demotion attempt.
    response = client.patch("/api/v1/admin/users/admin_id/role", json={"role": "user"})

    assert response.status_code == 400
    assert "only remaining admin" in response.json()["detail"]
