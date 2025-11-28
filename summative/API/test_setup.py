"""
Test script to verify FastAPI setup is correct.
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import sklearn
        import numpy
        import joblib
        print("✓ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_model_files():
    """Test that model and scaler files exist."""
    model_path = Path(__file__).parent / "models" / "best_model.pkl"
    scaler_path = Path(__file__).parent / "models" / "scaler.pkl"
    
    if not model_path.exists():
        print(f"✗ Model file not found: {model_path}")
        return False
    print(f"✓ Model file exists: {model_path}")
    
    if not scaler_path.exists():
        print(f"✗ Scaler file not found: {scaler_path}")
        return False
    print(f"✓ Scaler file exists: {scaler_path}")
    
    return True

def test_model_loading():
    """Test that model and scaler can be loaded."""
    try:
        import joblib
        from pathlib import Path
        
        model_path = Path(__file__).parent / "models" / "best_model.pkl"
        scaler_path = Path(__file__).parent / "models" / "scaler.pkl"
        
        model = joblib.load(model_path)
        print(f"✓ Model loaded successfully: {type(model).__name__}")
        
        scaler = joblib.load(scaler_path)
        print(f"✓ Scaler loaded successfully: {type(scaler).__name__}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading model/scaler: {e}")
        return False

def test_prediction_module():
    """Test that prediction module can be imported."""
    try:
        import prediction
        print("✓ Prediction module imported successfully")
        
        # Check that key components exist
        assert hasattr(prediction, 'app'), "FastAPI app not found"
        assert hasattr(prediction, 'PredictionInput'), "PredictionInput model not found"
        assert hasattr(prediction, 'PredictionOutput'), "PredictionOutput model not found"
        assert hasattr(prediction, 'predict_adherence'), "predict_adherence endpoint not found"
        
        print("✓ All required components found in prediction module")
        return True
    except Exception as e:
        print(f"✗ Error with prediction module: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("FastAPI Project Setup Verification")
    print("=" * 60)
    print()
    
    tests = [
        ("Package Imports", test_imports),
        ("Model Files", test_model_files),
        ("Model Loading", test_model_loading),
        ("Prediction Module", test_prediction_module),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ FastAPI project setup is complete and working!")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
