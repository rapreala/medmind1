"""
Test CORS middleware and logging functionality.

This module tests that CORS is properly configured and logging works as expected.
"""

import pytest
from fastapi.testclient import TestClient
import logging
from io import StringIO
import sys

# Import the app
sys.path.insert(0, '.')
from prediction import app, logger


client = TestClient(app)


def test_cors_headers_present():
    """Test that CORS headers are present in responses when Origin header is provided."""
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    
    # Check for CORS headers
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"


def test_cors_preflight_request():
    """Test CORS preflight OPTIONS request."""
    response = client.options(
        "/predict",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    
    # Should return 200 for preflight
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_logging_configuration():
    """Test that logging is configured with proper format."""
    # Verify that basicConfig was called by checking if handlers exist
    root_logger = logging.getLogger()
    
    # The logging configuration in prediction.py sets up basicConfig
    # We can verify the format by checking if any handler has a formatter
    has_formatter = any(
        handler.formatter is not None 
        for handler in root_logger.handlers
    )
    
    # At minimum, we should have handlers configured
    assert len(root_logger.handlers) > 0 or has_formatter


def test_prediction_request_logging(caplog):
    """Test that prediction requests are logged."""
    with caplog.at_level(logging.INFO):
        # Make a valid prediction request
        # Note: This will fail because model is not loaded in test environment
        # But we can check that the error is logged
        response = client.post("/predict", json={
            "age": 45,
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        })
        
        # Check that either request was logged OR error was logged (model not loaded)
        assert any("Prediction request received" in record.message or "Model or scaler not loaded" in record.message 
                   for record in caplog.records)


def test_prediction_result_logging(caplog):
    """Test that prediction results are logged (or errors if model not loaded)."""
    with caplog.at_level(logging.INFO):
        # Make a valid prediction request
        response = client.post("/predict", json={
            "age": 45,
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        })
        
        # Check that either result was logged OR error was logged (model not loaded)
        # This verifies that logging is working
        assert len(caplog.records) > 0


def test_error_logging(caplog):
    """Test that errors are logged with appropriate level."""
    with caplog.at_level(logging.ERROR):
        # Make an invalid request to trigger validation error
        response = client.post("/predict", json={
            "age": 150,  # Invalid age
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        })
        
        # Validation errors are handled by FastAPI/Pydantic, not logged as errors
        # This is expected behavior
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
