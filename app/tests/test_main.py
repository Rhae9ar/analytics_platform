from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token
from unittest.mock import patch
from app.database import get_unique_users

client = TestClient(app)

def test_create_event():
    token = create_access_token({"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/events/",
        headers=headers,
        json={
            "event_type": "click",
            "user_id": "123",
            "timestamp": "2025-02-27T12:00:00Z",
            "metadata": {"button": "buy"}
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_reports():
    token = create_access_token({"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        "/reports/?date_from=2025-02-20&date_to=2025-02-27&group_by=event_type",
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    from unittest.mock import patch
from app.database import get_unique_users

@patch('app.database.ch_client.execute')
def test_get_unique_users(mock_execute):
    mock_execute.return_value = [[10]]
    result = get_unique_users()
    assert result == 10