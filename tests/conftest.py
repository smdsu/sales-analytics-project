import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def fake_super_token():
    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxNiIsImV4cCI6MTczODY4MzgxMH0."
        "p-EPg8ZpTWL2JWPV-lom77hEXxt-su__yo3RzeBPFJE"
    )


@pytest.fixture
def client_with_super_token(fake_super_token):
    client = TestClient(app)
    client.cookies = {"users_access_token": fake_super_token}
    return client
