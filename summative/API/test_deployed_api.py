"""
Test script for deployed API.

Usage:
    python test_deployed_api.py <API_URL>

Example:
    python test_deployed_api.py https://medmind-adherence-api.onrender.com
"""

import sys
import requests
import json
from typing import Dict, Any

def test_root_endpoint(base_url: str) -> bool:
    """Test the root endpoint."""
    print("\n" + "=" * 60)
    print("Testing Root Endpoint (GET /)")
    print("=" * 60)
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Root endpoint working")
            return True
        else:
            print("❌ Root endpoint failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_endpoint(base_url: str) -> bool:
    """Test the health check endpoint."""
    print("\n" + "=" * 60)
    print("Testing Health Endpoint (GET /health)")
    print("=" * 60)
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy" and data.get("model_loaded") and data.get("scaler_loaded"):
                print("✅ Health check passed - Model and scaler loaded")
                return True
            else:
                print("❌ Health check failed - Model or scaler not loaded")
                return False
        else:
            print("❌ Health endpoint failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_valid_input(base_url: str) -> bool:
    """Test prediction with valid input."""
    print("\n" + "=" * 60)
    print("Testing Prediction Endpoint - Valid Input (POST /predict)")
    print("=" * 60)
    
    valid_input = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Input: {json.dumps(valid_input, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=valid_input,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if "predicted_adherence_rate" in data:
                rate = data["predicted_adherence_rate"]
                if 0 <= rate <= 100:
                    print(f"✅ Prediction successful: {rate}%")
                    return True
                else:
                    print(f"❌ Prediction out of range: {rate}")
                    return False
            else:
                print("❌ Response missing predicted_adherence_rate")
                return False
        else:
            print("❌ Prediction failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_invalid_age(base_url: str) -> bool:
    """Test prediction with invalid age (should return 422)."""
    print("\n" + "=" * 60)
    print("Testing Prediction Endpoint - Invalid Age (POST /predict)")
    print("=" * 60)
    
    invalid_input = {
        "age": 150,  # Invalid: > 120
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Input: {json.dumps(invalid_input, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=invalid_input,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 422:
            print("✅ Validation error correctly returned (422)")
            return True
        else:
            print(f"❌ Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_missing_field(base_url: str) -> bool:
    """Test prediction with missing required field (should return 422)."""
    print("\n" + "=" * 60)
    print("Testing Prediction Endpoint - Missing Field (POST /predict)")
    print("=" * 60)
    
    invalid_input = {
        "age": 45,
        "num_medications": 3,
        # Missing other required fields
    }
    
    print(f"Input: {json.dumps(invalid_input, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=invalid_input,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 422:
            print("✅ Validation error correctly returned (422)")
            return True
        else:
            print(f"❌ Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_swagger_ui(base_url: str) -> bool:
    """Test that Swagger UI is accessible."""
    print("\n" + "=" * 60)
    print("Testing Swagger UI (GET /docs)")
    print("=" * 60)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Swagger UI is accessible")
            print(f"   Visit: {base_url}/docs")
            return True
        else:
            print("❌ Swagger UI not accessible")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_response_time(base_url: str) -> bool:
    """Test that API responds within 5 seconds."""
    print("\n" + "=" * 60)
    print("Testing Response Time (< 5 seconds)")
    print("=" * 60)
    
    valid_input = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    try:
        import time
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/predict",
            json=valid_input,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response_time < 5.0:
            print(f"✅ Response time within limit (< 5 seconds)")
            return True
        else:
            print(f"⚠️  Response time exceeds 5 seconds")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all API tests."""
    if len(sys.argv) < 2:
        print("Usage: python test_deployed_api.py <API_URL>")
        print("Example: python test_deployed_api.py https://medmind-adherence-api.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("=" * 60)
    print("MedMind API - Deployment Testing")
    print("=" * 60)
    print(f"Testing API at: {base_url}")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("Valid Prediction", test_predict_valid_input),
        ("Invalid Age Validation", test_predict_invalid_age),
        ("Missing Field Validation", test_predict_missing_field),
        ("Swagger UI", test_swagger_ui),
        ("Response Time", test_response_time),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func(base_url)
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
        print("\nNext steps:")
        print("1. Document the public URL in README files")
        print("2. Update Flutter app to use this API URL")
        print("3. Create video demonstration")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
