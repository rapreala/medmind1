"""
Pytest configuration and fixtures for API tests.
"""

import pytest
from fastapi.testclient import TestClient
from prediction import app


@pytest.fixture
def client():
    """Create a TestClient for testing the FastAPI application."""
    with TestClient(app) as test_client:
        yield test_client
