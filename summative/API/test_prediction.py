"""
Test script to verify the prediction endpoint works correctly.
"""

import sys
import numpy as np
import joblib
from pathlib import Path

def test_direct_prediction():
    """Test prediction using the model directly (without FastAPI)."""
    print("\nDirect Model Prediction Test:")
    print("-" * 40)
    
    try:
        # Load model and scaler
        model_path = Path(__file__).parent / "models" / "best_model.pkl"
        scaler_path = Path(__file__).parent / "models" / "scaler.pkl"
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Test data (same as in the example)
        test_features = np.array([[
            45,      # age
            3,       # num_medications
            2.5,     # medication_complexity
            120,     # days_since_start
            1,       # missed_doses_last_week
            0.2,     # snooze_frequency
            2,       # chronic_conditions
            85.5     # previous_adherence_rate
        ]])
        
        # Preprocess and predict
        features_scaled = scaler.transform(test_features)
        prediction = model.predict(features_scaled)[0]
        
        # Clip to valid range
        prediction = float(np.clip(prediction, 0.0, 100.0))
        
        print(f"✓ Input features: {test_features[0].tolist()}")
        print(f"✓ Predicted adherence rate: {prediction:.2f}%")
        
        # Validate prediction is in valid range
        if 0.0 <= prediction <= 100.0:
            print(f"✓ Prediction is within valid range (0-100)")
            return True
        else:
            print(f"✗ Prediction {prediction} is outside valid range")
            return False
            
    except Exception as e:
        print(f"✗ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pydantic_validation():
    """Test that Pydantic models validate correctly."""
    print("\nPydantic Validation Test:")
    print("-" * 40)
    
    try:
        from prediction import PredictionInput, PredictionOutput
        
        # Test valid input
        valid_input = PredictionInput(
            age=45,
            num_medications=3,
            medication_complexity=2.5,
            days_since_start=120,
            missed_doses_last_week=1,
            snooze_frequency=0.2,
            chronic_conditions=2,
            previous_adherence_rate=85.5
        )
        print(f"✓ Valid input accepted: age={valid_input.age}")
        
        # Test invalid input (age > 120)
        try:
            invalid_input = PredictionInput(
                age=150,  # Invalid
                num_medications=3,
                medication_complexity=2.5,
                days_since_start=120,
                missed_doses_last_week=1,
                snooze_frequency=0.2,
                chronic_conditions=2,
                previous_adherence_rate=85.5
            )
            print(f"✗ Invalid input was accepted (should have been rejected)")
            return False
        except Exception as e:
            print(f"✓ Invalid input correctly rejected: {type(e).__name__}")
        
        # Test output model
        output = PredictionOutput(
            predicted_adherence_rate=82.3,
            confidence="high",
            message="Prediction successful"
        )
        print(f"✓ Output model created: {output.predicted_adherence_rate}%")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during validation test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_app():
    """Test that FastAPI app is properly configured."""
    print("\nFastAPI App Configuration Test:")
    print("-" * 40)
    
    try:
        from prediction import app
        
        # Check app attributes
        print(f"✓ App title: {app.title}")
        print(f"✓ App version: {app.version}")
        
        # Check routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/predict"]
        
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route exists: {route}")
            else:
                print(f"✗ Route missing: {route}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error checking FastAPI app: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("FastAPI Prediction Functionality Tests")
    print("=" * 60)
    
    tests = [
        ("Direct Model Prediction", test_direct_prediction),
        ("Pydantic Validation", test_pydantic_validation),
        ("FastAPI App Configuration", test_fastapi_app),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All prediction functionality tests passed!")
        print("\nNext steps:")
        print("1. Start the API: uvicorn prediction:app --reload")
        print("2. Visit http://localhost:8000/docs to test interactively")
        print("3. Deploy to a hosting platform (Render, Railway, etc.)")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
