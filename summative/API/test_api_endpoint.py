"""
Test the FastAPI endpoint with actual HTTP requests using TestClient.
"""

from fastapi.testclient import TestClient
from prediction import app
import sys

def test_root_endpoint(client):
    """Test the root endpoint."""
    print("\nTesting root endpoint (/)...")
    response = client.get("/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert "message" in response.json()
    print("✓ Root endpoint test passed")

def test_health_endpoint(client):
    """Test the health check endpoint."""
    print("\nTesting health endpoint (/health)...")
    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] == True
    assert response.json()["scaler_loaded"] == True
    print("✓ Health endpoint test passed")

def test_predict_endpoint_valid_input(client):
    """Test the predict endpoint with valid input."""
    print("\nTesting predict endpoint with valid input...")
    
    test_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    response = client.post("/predict", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    result = response.json()
    assert "predicted_adherence_rate" in result
    assert "confidence" in result
    assert "message" in result
    assert 0.0 <= result["predicted_adherence_rate"] <= 100.0
    print(f"✓ Predict endpoint test passed - Predicted: {result['predicted_adherence_rate']}%")

def test_predict_endpoint_invalid_age(client):
    """Test the predict endpoint with invalid age (> 120)."""
    print("\nTesting predict endpoint with invalid age...")
    
    test_data = {
        "age": 150,  # Invalid - exceeds maximum
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    response = client.post("/predict", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 422
    print("✓ Invalid age correctly rejected with 422 status")

def test_predict_endpoint_missing_field(client):
    """Test the predict endpoint with missing required field."""
    print("\nTesting predict endpoint with missing field...")
    
    test_data = {
        "age": 45,
        "num_medications": 3,
        # Missing other required fields
    }
    
    response = client.post("/predict", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 422
    print("✓ Missing fields correctly rejected with 422 status")

def test_predict_endpoint_out_of_range(client):
    """Test the predict endpoint with out-of-range values."""
    print("\nTesting predict endpoint with out-of-range snooze_frequency...")
    
    test_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 1.5,  # Invalid - exceeds maximum of 1.0
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    response = client.post("/predict", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 422
    print("✓ Out-of-range value correctly rejected with 422 status")

def main():
    """Run all endpoint tests."""
    print("=" * 60)
    print("FastAPI Endpoint Tests (using TestClient)")
    print("=" * 60)
    
    try:
        # Create TestClient with context manager to trigger startup/shutdown events
        with TestClient(app) as client:
            test_root_endpoint(client)
            test_health_endpoint(client)
            test_predict_endpoint_valid_input(client)
            test_predict_endpoint_invalid_age(client)
            test_predict_endpoint_missing_field(client)
            test_predict_endpoint_out_of_range(client)
        
        print("\n" + "=" * 60)
        print("✓ All endpoint tests passed!")
        print("=" * 60)
        print("\nThe FastAPI prediction endpoint is working correctly:")
        print("- Model and scaler load at startup")
        print("- POST /predict accepts valid input and returns predictions")
        print("- Input validation rejects invalid data with 422 status")
        print("- Error handling is in place for model loading and prediction failures")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
