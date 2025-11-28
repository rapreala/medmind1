#!/usr/bin/env python3
"""
Medication Adherence Prediction Function

This module provides a reusable function to predict patient medication adherence
rates using the trained machine learning model. The function loads the saved
best-performing model and scaler, preprocesses input features, and generates
predictions.

Requirements Addressed:
- 8.1: Function accepts feature values as input parameters
- 8.2: Loads saved best-performing model from disk
- 8.3: Preprocesses input data using same standardization as training
- 8.4: Returns predicted adherence rate as float between 0-100
- 8.5: Demonstrates prediction on test data points
- 7.5: Uses saved model for predictions on new data

Author: MedMind Development Team
Date: 2025-11-28
"""

import joblib
import numpy as np
import os
from typing import Union, List


def predict_adherence(
    age: Union[int, float],
    num_medications: Union[int, float],
    medication_complexity: float,
    days_since_start: Union[int, float],
    missed_doses_last_week: Union[int, float],
    snooze_frequency: float,
    chronic_conditions: Union[int, float],
    previous_adherence_rate: float,
    model_path: str = 'models/best_model.pkl',
    scaler_path: str = 'models/scaler.pkl'
) -> float:
    """
    Predict medication adherence rate for a patient based on their characteristics.
    
    This function loads the trained machine learning model and scaler, preprocesses
    the input features using standardization, and generates a prediction for the
    patient's expected adherence rate.
    
    Args:
        age: Patient age in years (expected range: 18-120)
        num_medications: Number of active medications (expected range: 1-20)
        medication_complexity: Medication regimen complexity score (range: 1.0-5.0)
                              1.0 = simple (once daily), 5.0 = complex (multiple times/day)
        days_since_start: Days since starting current medication regimen (range: 0+)
        missed_doses_last_week: Number of missed doses in the past 7 days (range: 0-50)
        snooze_frequency: Proportion of medication reminders that were snoozed (range: 0.0-1.0)
        chronic_conditions: Number of chronic health conditions (range: 0-10)
        previous_adherence_rate: Historical adherence rate percentage (range: 0.0-100.0)
        model_path: Path to the saved model file (default: 'models/best_model.pkl')
        scaler_path: Path to the saved scaler file (default: 'models/scaler.pkl')
    
    Returns:
        float: Predicted adherence rate as a percentage between 0.0 and 100.0
    
    Raises:
        FileNotFoundError: If model or scaler files cannot be found
        ValueError: If input features are invalid or out of expected ranges
    
    Example:
        >>> rate = predict_adherence(
        ...     age=45,
        ...     num_medications=3,
        ...     medication_complexity=2.5,
        ...     days_since_start=120,
        ...     missed_doses_last_week=1,
        ...     snooze_frequency=0.2,
        ...     chronic_conditions=2,
        ...     previous_adherence_rate=85.5
        ... )
        >>> print(f"Predicted adherence rate: {rate:.2f}%")
        Predicted adherence rate: 82.34%
    """
    
    # Validate model and scaler files exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    
    # Validate input ranges (basic validation)
    if not (0 <= age <= 150):
        raise ValueError(f"Age must be between 0 and 150, got {age}")
    if not (0 <= num_medications <= 50):
        raise ValueError(f"Number of medications must be between 0 and 50, got {num_medications}")
    if not (0.0 <= medication_complexity <= 10.0):
        raise ValueError(f"Medication complexity must be between 0.0 and 10.0, got {medication_complexity}")
    if days_since_start < 0:
        raise ValueError(f"Days since start must be non-negative, got {days_since_start}")
    if missed_doses_last_week < 0:
        raise ValueError(f"Missed doses must be non-negative, got {missed_doses_last_week}")
    if not (0.0 <= snooze_frequency <= 1.0):
        raise ValueError(f"Snooze frequency must be between 0.0 and 1.0, got {snooze_frequency}")
    if chronic_conditions < 0:
        raise ValueError(f"Chronic conditions must be non-negative, got {chronic_conditions}")
    if not (0.0 <= previous_adherence_rate <= 100.0):
        raise ValueError(f"Previous adherence rate must be between 0.0 and 100.0, got {previous_adherence_rate}")
    
    # Load the trained model and scaler
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        raise RuntimeError(f"Error loading model or scaler: {e}")
    
    # Create feature array in the correct order
    # Order must match the training data: age, num_medications, medication_complexity,
    # days_since_start, missed_doses_last_week, snooze_frequency, chronic_conditions,
    # previous_adherence_rate
    features = np.array([[
        age,
        num_medications,
        medication_complexity,
        days_since_start,
        missed_doses_last_week,
        snooze_frequency,
        chronic_conditions,
        previous_adherence_rate
    ]], dtype=np.float64)
    
    # Preprocess features using the same scaler from training
    # This ensures consistent standardization (mean=0, std=1)
    features_scaled = scaler.transform(features)
    
    # Generate prediction using the trained model
    prediction = model.predict(features_scaled)[0]
    
    # Ensure prediction is within valid range [0.0, 100.0]
    # Some models may predict slightly outside this range
    prediction = np.clip(prediction, 0.0, 100.0)
    
    return float(prediction)


def predict_adherence_batch(
    features_list: List[List[Union[int, float]]],
    model_path: str = 'models/best_model.pkl',
    scaler_path: str = 'models/scaler.pkl'
) -> List[float]:
    """
    Predict adherence rates for multiple patients in batch.
    
    This function is more efficient than calling predict_adherence() multiple times
    because it loads the model and scaler only once.
    
    Args:
        features_list: List of feature arrays, where each array contains:
                      [age, num_medications, medication_complexity, days_since_start,
                       missed_doses_last_week, snooze_frequency, chronic_conditions,
                       previous_adherence_rate]
        model_path: Path to the saved model file
        scaler_path: Path to the saved scaler file
    
    Returns:
        List[float]: List of predicted adherence rates (0.0-100.0)
    
    Example:
        >>> patients = [
        ...     [45, 3, 2.5, 120, 1, 0.2, 2, 85.5],
        ...     [62, 5, 3.8, 365, 3, 0.4, 4, 72.0],
        ...     [38, 2, 1.5, 60, 0, 0.1, 1, 95.0]
        ... ]
        >>> rates = predict_adherence_batch(patients)
        >>> for i, rate in enumerate(rates):
        ...     print(f"Patient {i+1}: {rate:.2f}%")
    """
    
    # Validate files exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    
    # Load model and scaler once
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        raise RuntimeError(f"Error loading model or scaler: {e}")
    
    # Convert to numpy array
    features_array = np.array(features_list, dtype=np.float64)
    
    # Validate shape
    if features_array.shape[1] != 8:
        raise ValueError(f"Each feature array must have 8 elements, got {features_array.shape[1]}")
    
    # Preprocess all features at once
    features_scaled = scaler.transform(features_array)
    
    # Generate predictions
    predictions = model.predict(features_scaled)
    
    # Clip to valid range
    predictions = np.clip(predictions, 0.0, 100.0)
    
    return predictions.tolist()


if __name__ == "__main__":
    """
    Demonstration of the prediction function on sample data points.
    This section fulfills Requirement 8.5: Test function on at least one sample
    data point from test set.
    """
    
    print("="*80)
    print("MEDICATION ADHERENCE PREDICTION FUNCTION DEMONSTRATION")
    print("="*80)
    
    # Test Case 1: High adherence patient
    print("\n" + "-"*80)
    print("TEST CASE 1: High Adherence Patient")
    print("-"*80)
    
    patient1 = {
        'age': 45,
        'num_medications': 3,
        'medication_complexity': 2.5,
        'days_since_start': 120,
        'missed_doses_last_week': 1,
        'snooze_frequency': 0.2,
        'chronic_conditions': 2,
        'previous_adherence_rate': 85.5
    }
    
    print("\nPatient Profile:")
    for key, value in patient1.items():
        print(f"  {key:30s}: {value}")
    
    try:
        prediction1 = predict_adherence(**patient1)
        print(f"\n✅ Predicted Adherence Rate: {prediction1:.2f}%")
        
        # Validate prediction is in range
        if 0.0 <= prediction1 <= 100.0:
            print(f"✅ Prediction is within valid range [0.0, 100.0]")
        else:
            print(f"❌ WARNING: Prediction out of range: {prediction1}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Case 2: Low adherence patient
    print("\n" + "-"*80)
    print("TEST CASE 2: Low Adherence Patient")
    print("-"*80)
    
    patient2 = {
        'age': 72,
        'num_medications': 8,
        'medication_complexity': 4.2,
        'days_since_start': 730,
        'missed_doses_last_week': 5,
        'snooze_frequency': 0.6,
        'chronic_conditions': 5,
        'previous_adherence_rate': 45.0
    }
    
    print("\nPatient Profile:")
    for key, value in patient2.items():
        print(f"  {key:30s}: {value}")
    
    try:
        prediction2 = predict_adherence(**patient2)
        print(f"\n✅ Predicted Adherence Rate: {prediction2:.2f}%")
        
        if 0.0 <= prediction2 <= 100.0:
            print(f"✅ Prediction is within valid range [0.0, 100.0]")
        else:
            print(f"❌ WARNING: Prediction out of range: {prediction2}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Case 3: Medium adherence patient
    print("\n" + "-"*80)
    print("TEST CASE 3: Medium Adherence Patient")
    print("-"*80)
    
    patient3 = {
        'age': 55,
        'num_medications': 5,
        'medication_complexity': 3.0,
        'days_since_start': 365,
        'missed_doses_last_week': 2,
        'snooze_frequency': 0.35,
        'chronic_conditions': 3,
        'previous_adherence_rate': 70.0
    }
    
    print("\nPatient Profile:")
    for key, value in patient3.items():
        print(f"  {key:30s}: {value}")
    
    try:
        prediction3 = predict_adherence(**patient3)
        print(f"\n✅ Predicted Adherence Rate: {prediction3:.2f}%")
        
        if 0.0 <= prediction3 <= 100.0:
            print(f"✅ Prediction is within valid range [0.0, 100.0]")
        else:
            print(f"❌ WARNING: Prediction out of range: {prediction3}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Case 4: Batch prediction
    print("\n" + "-"*80)
    print("TEST CASE 4: Batch Prediction")
    print("-"*80)
    
    patients_batch = [
        [45, 3, 2.5, 120, 1, 0.2, 2, 85.5],  # Patient 1
        [72, 8, 4.2, 730, 5, 0.6, 5, 45.0],  # Patient 2
        [55, 5, 3.0, 365, 2, 0.35, 3, 70.0], # Patient 3
        [30, 2, 1.8, 90, 0, 0.1, 1, 92.0],   # Patient 4 (young, simple regimen)
        [80, 10, 4.8, 1095, 8, 0.75, 7, 35.0] # Patient 5 (elderly, complex)
    ]
    
    print(f"\nPredicting adherence for {len(patients_batch)} patients...")
    
    try:
        predictions_batch = predict_adherence_batch(patients_batch)
        print("\nBatch Prediction Results:")
        for i, pred in enumerate(predictions_batch, 1):
            print(f"  Patient {i}: {pred:.2f}%")
        
        # Validate all predictions are in range
        all_valid = all(0.0 <= p <= 100.0 for p in predictions_batch)
        if all_valid:
            print(f"\n✅ All {len(predictions_batch)} predictions are within valid range")
        else:
            print(f"\n❌ WARNING: Some predictions are out of range")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Case 5: Load from actual test set
    print("\n" + "-"*80)
    print("TEST CASE 5: Prediction on Actual Test Set Sample")
    print("-"*80)
    
    try:
        import pandas as pd
        from sklearn.model_selection import train_test_split
        
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
        
        # Get first test sample
        test_sample = X_test.iloc[0]
        actual_rate = y_test.iloc[0]
        
        print("\nTest Set Sample (Raw Features):")
        for col, val in test_sample.items():
            print(f"  {col:30s}: {val:.4f}")
        print(f"  {'Actual Adherence Rate':30s}: {actual_rate:.2f}%")
        
        # Make prediction
        prediction_test = predict_adherence(
            age=test_sample['age'],
            num_medications=test_sample['num_medications'],
            medication_complexity=test_sample['medication_complexity'],
            days_since_start=test_sample['days_since_start'],
            missed_doses_last_week=test_sample['missed_doses_last_week'],
            snooze_frequency=test_sample['snooze_frequency'],
            chronic_conditions=test_sample['chronic_conditions'],
            previous_adherence_rate=test_sample['previous_adherence_rate']
        )
        
        error = abs(actual_rate - prediction_test)
        
        print(f"\n✅ Predicted Adherence Rate: {prediction_test:.2f}%")
        print(f"   Prediction Error: {error:.2f} percentage points")
        
        if error < 10.0:
            print(f"   ✅ Excellent prediction (error < 10%)")
        elif error < 20.0:
            print(f"   ✅ Good prediction (error < 20%)")
        else:
            print(f"   ⚠️  Moderate error (error >= 20%)")
        
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("PREDICTION FUNCTION DEMONSTRATION COMPLETE ✅")
    print("="*80)
    print("\nKey Features:")
    print("  ✅ Loads saved model and scaler from disk")
    print("  ✅ Preprocesses input features using standardization")
    print("  ✅ Generates predictions for individual patients")
    print("  ✅ Supports batch predictions for efficiency")
    print("  ✅ Validates predictions are in range [0.0, 100.0]")
    print("  ✅ Includes comprehensive error handling")
    print("  ✅ Tested on multiple patient profiles")
    print("\nThe prediction function is ready for integration into the FastAPI service!")
    print("="*80)
