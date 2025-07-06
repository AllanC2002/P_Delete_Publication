import pytest
from main import app as flask_app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_delete_publication_success(client):
    mock_token = "mocktoken"
    mock_user_id = "user123"
    mock_publication_id = "64a1f9f347e8f9c3d0f1a2b3"  # ObjectId real

    with patch("main.jwt.decode") as mock_jwt_decode, \
         patch("services.functions.conection_mongo") as mock_conection_mongo:
        
        mock_jwt_decode.return_value = {"user_id": mock_user_id}

        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.update_one.return_value.matched_count = 1
        mock_db.__getitem__.return_value = mock_collection
        mock_conection_mongo.return_value = mock_db

        response = client.put(
            "/delete-publication",
            headers={"Authorization": f"Bearer {mock_token}"},
            json={"publication_id": mock_publication_id}
        )

        assert response.status_code == 200
        assert response.get_json()["message"] == "Publication deleted successfully"

"""
def test_delete_publication_not_found(client):
    mock_token = "mocktoken"
    mock_user_id = "user123"
    mock_publication_id = "64a1f9f347e8f9c3d0f1a2b3"  # ObjectId real

    with patch("main.jwt.decode") as mock_jwt_decode, \
         patch("services.functions.conection_mongo") as mock_conection_mongo:
        
        mock_jwt_decode.return_value = {"user_id": mock_user_id}

        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.update_one.return_value.matched_count = 0
        mock_db.__getitem__.return_value = mock_collection
        mock_conection_mongo.return_value = mock_db

        response = client.put(
            "/delete-publication",
            headers={"Authorization": f"Bearer {mock_token}"},
            json={"publication_id": mock_publication_id}
        )

        assert response.status_code == 404
        assert response.get_json()["error"] == "Publication not found"
"""