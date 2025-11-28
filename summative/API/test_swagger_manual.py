"""
Manual testing script for the FastAPI prediction endpoint.
This script tests various scenarios including valid inputs, invalid inputs,
out of range values, wrong types, and missing fields.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_test_header(test_name: str):
    """Print a formatted test header."""
    print("\n" + "=" * 80)
    print(f"TEST: {test_name}")
    print("=" * 80)


def print_response(response: requests.Response):
    """Print formatted response details."""
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    try:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Body: {response.text}")


def test_valid_input():
    """Test 1: Valid input - should return 200"""
    print_test_header("Valid Input - Expected: 200 OK")
    
    valid_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(valid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=valid_data)
    print_response(response)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "predicted_adherence_rate" in data
    assert "confidence" in data
    assert "message" in data
    assert 0 <= data["predicted_adherence_rate"] <= 100
    print("✓ Test PASSED")


def test_age_out_of_range_high():
    """Test 2: Age > 120 - should return 422"""
    print_test_header("Age Out of Range (>120) - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": 150,  # Invalid: > 120
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    data = response.json()
    assert "detail" in data
    print("✓ Test PASSED")


def test_age_out_of_range_low():
    """Test 3: Age < 0 - should return 422"""
    print_test_header("Age Out of Range (<0) - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": -5,  # Invalid: < 0
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Test PASSED")


def test_medication_complexity_out_of_range():
    """Test 4: Medication complexity > 5.0 - should return 422"""
    print_test_header("Medication Complexity Out of Range - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 7.5,  # Invalid: > 5.0
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Test PASSED")


def test_snooze_frequency_out_of_range():
    """Test 5: Snooze frequency > 1.0 - should return 422"""
    print_test_header("Snooze Frequency Out of Range - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 1.5,  # Invalid: > 1.0
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Test PASSED")


def test_wrong_type_age_string():
    """Test 6: Wrong type - age as string - should return 422"""
    print_test_header("Wrong Type (age as string) - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": "forty-five",  # Invalid: should be int
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Test PASSED")


def test_wrong_type_complexity_string():
    """Test 7: Wrong type - medication_complexity as string - should return 422"""
    print_test_header("Wrong Type (medication_complexity as string) - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": "medium",  # Invalid: should be float
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Test PASSED")


def test_missing_required_field_age():
    """Test 8: Missing required field (age) - should return 422"""
    print_test_header("Missing Required Field (age) - Expected: 422 Validation Error")
    
    invalid_data = {
        # "age": 45,  # Missing required field
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    data = response.json()
    assert "detail" in data
    # Check that the error mentions the missing field
    error_str = json.dumps(data["detail"]).lower()
    assert "age" in error_str
    print("✓ Test PASSED")


def test_missing_multiple_fields():
    """Test 9: Missing multiple required fields - should return 422"""
    print_test_header("Missing Multiple Required Fields - Expected: 422 Validation Error")
    
    invalid_data = {
        "age": 45,
        "num_medications": 3,
        # Missing: medication_complexity, days_since_start, missed_doses_last_week,
        #          snooze_frequency, chronic_conditions, previous_adherence_rate
    }
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) >= 6  # Should have errors for all missing fields
    print("✓ Test PASSED")


def test_empty_request_body():
    """Test 10: Empty request body - should return 422"""
    print_test_header("Empty Request Body - Expected: 422 Validation Error")
    
    invalid_data = {}
    
    print(f"Request Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print_response(response)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✓ Test PASSED")


def test_additional_valid_inputs():
    """Test 11: Additional valid inputs with different values - should return 200"""
    print_test_header("Additional Valid Input (Edge Case Values) - Expected: 200 OK")
    
    # Test with minimum valid values
    valid_data = {
        "age": 18,
        "num_medications": 1,
        "medication_complexity": 1.0,
        "days_since_start": 0,
        "missed_doses_last_week": 0,
        "snooze_frequency": 0.0,
        "chronic_conditions": 0,
        "previous_adherence_rate": 0.0
    }
    
    print(f"Request Data: {json.dumps(valid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=valid_data)
    print_response(response)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✓ Test PASSED")


def test_valid_input_max_values():
    """Test 12: Valid input with maximum values - should return 200"""
    print_test_header("Valid Input (Maximum Values) - Expected: 200 OK")
    
    valid_data = {
        "age": 120,
        "num_medications": 20,
        "medication_complexity": 5.0,
        "days_since_start": 3650,
        "missed_doses_last_week": 50,
        "snooze_frequency": 1.0,
        "chronic_conditions": 10,
        "previous_adherence_rate": 100.0
    }
    
    print(f"Request Data: {json.dumps(valid_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/predict", json=valid_data)
    print_response(response)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✓ Test PASSED")


def test_cors_headers():
    """Test 13: Verify CORS headers are present"""
    print_test_header("CORS Headers Verification - Expected: CORS headers present")
    
    valid_data = {
        "age": 45,
        "num_medications": 3,
        "medication_complexity": 2.5,
        "days_since_start": 120,
        "missed_doses_last_week": 1,
        "snooze_frequency": 0.2,
        "chronic_conditions": 2,
        "previous_adherence_rate": 85.5
    }
    
    # Include Origin header to trigger CORS
    headers = {"Origin": "http://localhost:3000"}
    response = requests.post(f"{BASE_URL}/predict", json=valid_data, headers=headers)
    
    # Check for CORS headers (case-insensitive)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    print(f"Response headers: {headers_lower}")
    assert "access-control-allow-origin" in headers_lower, "Missing CORS header"
    print(f"CORS Header: {headers_lower.get('access-control-allow-origin')}")
    print("✓ Test PASSED")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "=" * 80)
    print("STARTING API TESTING SUITE")
    print("=" * 80)
    
    tests = [
        test_valid_input,
        test_age_out_of_range_high,
        test_age_out_of_range_low,
        test_medication_complexity_out_of_range,
        test_snooze_frequency_out_of_range,
        test_wrong_type_age_string,
        test_wrong_type_complexity_string,
        test_missing_required_field_age,
        test_missing_multiple_fields,
        test_empty_request_body,
        test_additional_valid_inputs,
        test_valid_input_max_values,
        test_cors_headers,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 80)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")


if __name__ == "__main__":
    try:
        # First check if the API is running
        print("Checking if API is running...")
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"API Health Check: {response.json()}")
        
        # Run all tests
        run_all_tests()
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API at http://localhost:8000")
        print("Please ensure the API is running with: uvicorn prediction:app --reload")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
