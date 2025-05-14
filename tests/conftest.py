import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.core.security import JWTBearer


# Mock JWTBearer dependency for testing
async def mock_jwt_bearer():
    return {"admin": "admin123"}

app.dependency_overrides[JWTBearer] = mock_jwt_bearer

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
