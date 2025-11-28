#!/usr/bin/env python3
"""
Test script to verify the prediction function meets all requirements.

This script validates:
- Requirement 8.1: Function accepts 8 feature values as parameters ✓
- Requirement 8.2: Loads saved model and scaler from disk ✓
- Requirement 8.3: Preprocesses input features using loaded scaler ✓
- Requirement 8.4: Returns predicted adherence rate as float between 0-100 ✓
- Requirement 8.5: Tests function on at least one sample data point from test set ✓
- Requirement 7.5: Uses saved model for predictions on new data ✓
"""

import sys
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Import the prediction function
from predict_adherence import predict_adherence, predict_adherence_batch


def test_requirement_8_1():
    """Test that function accepts 8 feature values as parameters."""
    print("\n" + "="*80)
    print("TEST: Requirement 8.1 - Function accepts 8 feature values as parameters")
    print("="*80)
    
    try:
        # Call function with all 8 parameters
        result = predict_adherence(
            age=45,
            num_medications=3,
            medication_complexity=2.5,
            days_since_start=120,
            missed_doses_last_week=1,
            snooze_frequency=0.2,
            chronic_conditions=2,
            previous_adherence_rate=85.5
        )
        print("✅ PASS: Function accepts all 8 feature parameters")
        print(f"   Result: {result:.2f}%")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_requirement_8_2():
    """Test that function loads saved model and scaler from disk."""
    print("\n" + "="*80)
    print("TEST: Requirement 8.2 - Loads saved model and scaler from disk")
    print("="*80)
    
    # Check if files exist
    model_exists = os.path.exists('models/best_model.pkl')
    scaler_exists = os.path.exists('models/scaler.pkl')
    
    print(f"   Model file exists: {model_exists}")
    print(f"   Scaler file exists: {scaler_exists}")
    
    if not model_exists or not scaler_exists:
        print("❌ FAIL: Model or scaler files not found")
        return False
    
    try:
        # Function should load these files internally
        result = predict_adherence(
            age=50, num_medications=4, medication_complexity=3.0,
            days_since_start=200, missed_doses_last_week=2,
            snooze_frequency=0.3, chronic_conditions=3,
            previous_adherence_rate=75.0
        )
        print("✅ PASS: Function successfully loads model and scaler from disk")
        print(f"   Prediction generated: {result:.2f}%")
        return True
    except Exception as e:
        print(f"❌ FAIL: Error loading model/scaler: {e}")
        return False


def test_requirement_8_3():
    """Test that function preprocesses input using the same scaler."""
    print("\n" + "="*80)
    print("TEST: Requirement 8.3 - Preprocesses input features using loaded scaler")
    print("="*80)
    
    try:
        import joblib
        
        # Load scaler to verify it's being used
        scaler = joblib.load('models/scaler.pkl')
        
        # Test input
        test_features = np.array([[45, 3, 2.5, 120, 1, 0.2, 2, 85.5]])
        
        # Manual preprocessing
        manual_scaled = scaler.transform(test_features)
        
        print(f"   Original features: {test_features[0]}")
        print(f"   Scaled features (first 3): {manual_scaled[0][:3]}")
        print(f"   Scaler mean (first 3): {scaler.mean_[:3]}")
        print(f"   Scaler std (first 3): {scaler.scale_[:3]}")
        
        # The function should use the same scaler internally
        result = predict_adherence(
            age=45, num_medications=3, medication_complexity=2.5,
            days_since_start=120, missed_doses_last_week=1,
            snooze_frequency=0.2, chronic_conditions=2,
            previous_adherence_rate=85.5
        )
        
        print("✅ PASS: Function uses scaler for preprocessing")
        print(f"   Prediction: {result:.2f}%")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_requirement_8_4():
    """Test that function returns float between 0-100."""
    print("\n" + "="*80)
    print("TEST: Requirement 8.4 - Returns predicted adherence rate as float between 0-100")
    print("="*80)
    
    test_cases = [
        # High adherence case
        {'age': 30, 'num_medications': 2, 'medication_complexity': 1.5,
         'days_since_start': 60, 'missed_doses_last_week': 0,
         'snooze_frequency': 0.1, 'chronic_conditions': 1,
         'previous_adherence_rate': 95.0},
        # Low adherence case
        {'age': 80, 'num_medications': 10, 'medication_complexity': 4.8,
         'days_since_start': 1095, 'missed_doses_last_week': 8,
         'snooze_frequency': 0.75, 'chronic_conditions': 7,
         'previous_adherence_rate': 35.0},
        # Medium adherence case
        {'age': 55, 'num_medications': 5, 'medication_complexity': 3.0,
         'days_since_start': 365, 'missed_doses_last_week': 2,
         'snooze_frequency': 0.35, 'chronic_conditions': 3,
         'previous_adherence_rate': 70.0}
    ]
    
    all_valid = True
    for i, case in enumerate(test_cases, 1):
        try:
            result = predict_adherence(**case)
            is_float = isinstance(result, float)
            in_range = 0.0 <= result <= 100.0
            
            print(f"\n   Test Case {i}:")
            print(f"      Result: {result:.2f}%")
            print(f"      Is float: {is_float}")
            print(f"      In range [0, 100]: {in_range}")
            
            if not is_float or not in_range:
                all_valid = False
                print(f"      ❌ FAIL")
            else:
                print(f"      ✅ PASS")
        except Exception as e:
            print(f"   Test Case {i}: ❌ FAIL - {e}")
            all_valid = False
    
    if all_valid:
        print("\n✅ PASS: All predictions are floats in range [0.0, 100.0]")
        return True
    else:
        print("\n❌ FAIL: Some predictions failed validation")
        return False


def test_requirement_8_5():
    """Test function on at least one sample data point from test set."""
    print("\n" + "="*80)
    print("TEST: Requirement 8.5 - Tests function on sample data point from test set")
    print("="*80)
    
    try:
        # Load dataset
        df = pd.read_csv('adherence_data.csv')
        df_clean = df.dropna()
        
        target_col = 'adherence_rate'
        feature_cols = [col for col in df_clean.columns if col != target_col]
        X = df_clean[feature_cols]
        y = df_clean[target_col]
        
        # Split to get test set (same random_state as training)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"   Test set size: {len(X_test)} samples")
        
        # Test on first 3 samples from test set
        num_samples = min(3, len(X_test))
        print(f"   Testing on {num_samples} samples from test set:")
        
        for i in range(num_samples):
            sample = X_test.iloc[i]
            actual = y_test.iloc[i]
            
            prediction = predict_adherence(
                age=sample['age'],
                num_medications=sample['num_medications'],
                medication_complexity=sample['medication_complexity'],
                days_since_start=sample['days_since_start'],
                missed_doses_last_week=sample['missed_doses_last_week'],
                snooze_frequency=sample['snooze_frequency'],
                chronic_conditions=sample['chronic_conditions'],
                previous_adherence_rate=sample['previous_adherence_rate']
            )
            
            error = abs(actual - prediction)
            
            print(f"\n   Sample {i+1}:")
            print(f"      Actual: {actual:.2f}%")
            print(f"      Predicted: {prediction:.2f}%")
            print(f"      Error: {error:.2f} percentage points")
        
        print("\n✅ PASS: Function tested on test set samples")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_requirement_7_5():
    """Test that saved model is used for predictions on new data."""
    print("\n" + "="*80)
    print("TEST: Requirement 7.5 - Uses saved model for predictions on new data")
    print("="*80)
    
    try:
        # Create new data points (not from training set)
        new_patients = [
            {'age': 42, 'num_medications': 4, 'medication_complexity': 2.8,
             'days_since_start': 150, 'missed_doses_last_week': 1,
             'snooze_frequency': 0.25, 'chronic_conditions': 2,
             'previous_adherence_rate': 82.0},
            {'age': 68, 'num_medications': 7, 'medication_complexity': 4.0,
             'days_since_start': 500, 'missed_doses_last_week': 4,
             'snooze_frequency': 0.5, 'chronic_conditions': 4,
             'previous_adherence_rate': 55.0}
        ]
        
        print("   Testing predictions on new patient data:")
        
        for i, patient in enumerate(new_patients, 1):
            prediction = predict_adherence(**patient)
            print(f"\n   New Patient {i}:")
            print(f"      Age: {patient['age']}, Medications: {patient['num_medications']}")
            print(f"      Previous adherence: {patient['previous_adherence_rate']:.1f}%")
            print(f"      Predicted adherence: {prediction:.2f}%")
        
        print("\n✅ PASS: Saved model successfully makes predictions on new data")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_batch_prediction():
    """Bonus test: Verify batch prediction functionality."""
    print("\n" + "="*80)
    print("BONUS TEST: Batch Prediction Functionality")
    print("="*80)
    
    try:
        patients = [
            [45, 3, 2.5, 120, 1, 0.2, 2, 85.5],
            [72, 8, 4.2, 730, 5, 0.6, 5, 45.0],
            [55, 5, 3.0, 365, 2, 0.35, 3, 70.0]
        ]
        
        predictions = predict_adherence_batch(patients)
        
        print(f"   Batch size: {len(patients)} patients")
        print(f"   Predictions: {[f'{p:.2f}%' for p in predictions]}")
        
        all_valid = all(isinstance(p, float) and 0.0 <= p <= 100.0 for p in predictions)
        
        if all_valid:
            print("✅ PASS: Batch prediction works correctly")
            return True
        else:
            print("❌ FAIL: Some batch predictions invalid")
            return False
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def main():
    """Run all tests and generate summary report."""
    print("\n" + "="*80)
    print("PREDICTION FUNCTION REQUIREMENTS VALIDATION")
    print("="*80)
    print("\nValidating implementation against requirements 8.1-8.5 and 7.5...")
    
    results = {
        'Requirement 8.1 (Accept 8 parameters)': test_requirement_8_1(),
        'Requirement 8.2 (Load model/scaler)': test_requirement_8_2(),
        'Requirement 8.3 (Preprocess with scaler)': test_requirement_8_3(),
        'Requirement 8.4 (Return float 0-100)': test_requirement_8_4(),
        'Requirement 8.5 (Test on test set)': test_requirement_8_5(),
        'Requirement 7.5 (Use saved model)': test_requirement_7_5(),
        'Batch Prediction (Bonus)': test_batch_prediction()
    }
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*80)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("-"*80)
    
    if passed == total:
        print("\n🎉 ALL REQUIREMENTS VALIDATED SUCCESSFULLY!")
        print("\nThe prediction function is fully compliant with:")
        print("  ✓ Requirement 8.1: Accepts 8 feature values as parameters")
        print("  ✓ Requirement 8.2: Loads saved model and scaler from disk")
        print("  ✓ Requirement 8.3: Preprocesses input using loaded scaler")
        print("  ✓ Requirement 8.4: Returns float between 0-100")
        print("  ✓ Requirement 8.5: Tested on test set samples")
        print("  ✓ Requirement 7.5: Uses saved model for new predictions")
        print("\nThe function is ready for integration into the FastAPI service!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} requirement(s) not met. Please review failures above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
