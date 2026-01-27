import pytest
from rest_framework.test import APIClient
from unittest.mock import patch

@pytest.fixture
def auth_client():
    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION="Bearer fake-token")

    patcher = patch(
        "rest_framework_simplejwt.authentication.JWTAuthentication.get_validated_token",
    return_value={"user_id": 1, "email": "teste@example.com", "token_type": "access"}
    )

    patcher.start()
    yield client
    patcher.stop()