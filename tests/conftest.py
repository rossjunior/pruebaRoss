import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app



@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
