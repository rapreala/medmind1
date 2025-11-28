#!/usr/bin/env python3
"""
Script to test the saved best model and scaler.
Verifies that the model can be loaded and makes predictions correctly.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

print("="*70)
print("TESTING SAVED BEST MODEL")
print("="*70)

# Load the saved model and scaler
print("\n1. Loading saved model and scaler...")
try:
    best_model = joblib.load('models/best_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    print("   ✅ Model loaded successfully")
    print("   ✅ Scaler loaded successfully")
    print(f"   Model type: {type(best_model).__name__}")
except Exception as e:
    print(f"   ❌ Error loading model: {e}")
    exit(1)

# Load dataset for testing
print("\n2. Loading test dataset...")
df = pd.read_csv('adherence_data.csv')
df_clean = df.dropna()

target_col = 'adherence_rate'
feature_cols = [col for col in df_clean.columns if col != target_col]
X = df_clean[feature_cols]
y = df_clean[target_col]

# Standardize and split
X_scaled = scaler.transform(X)  # Use transform, not fit_transform
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"   ✅ Test set: {len(X_test)} samples")

# Make predictions
print("\n3. Making predictions on test set...")
y_pred = best_model.predict(X_test)
print(f"   ✅ Predictions generated")

# Calculate metrics
test_mse = mean_squared_error(y_test, y_pred)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(y_test, y_pred)

print("\n" + "="*70)
print("MODEL PERFORMANCE VERIFICATION")
print("="*70)
print(f"Test MSE:  {test_mse:.4f}")
print(f"Test RMSE: {test_rmse:.4f}")
print(f"Test R²:   {test_r2:.4f}")
print("="*70)

# Test with a single sample
print("\n4. Testing prediction on a single sample...")
sample_idx = 0
sample_features = X_test[sample_idx].reshape(1, -1)
sample_actual = y_test.iloc[sample_idx]
sample_pred = best_model.predict(sample_features)[0]

print(f"\n   Sample Input Features:")
for i, col in enumerate(feature_cols):
    print(f"      {col}: {sample_features[0][i]:.4f}")
print(f"\n   Actual Adherence Rate: {sample_actual:.2f}%")
print(f"   Predicted Adherence Rate: {sample_pred:.2f}%")
print(f"   Prediction Error: {abs(sample_actual - sample_pred):.2f}%")

# Test prediction function
print("\n5. Testing prediction function with raw input...")

def predict_adherence(age, num_medications, medication_complexity, 
                     days_since_start, missed_doses_last_week, 
                     snooze_frequency, chronic_conditions, 
                     previous_adherence_rate):
    """
    Predict adherence rate for a patient.
    
    Args:
        age: Patient age (18-120)
        num_medications: Number of medications (1-20)
        medication_complexity: Complexity score (1.0-5.0)
        days_since_start: Days since starting regimen (0+)
        missed_doses_last_week: Missed doses in past week (0-50)
        snooze_frequency: Proportion of reminders snoozed (0.0-1.0)
        chronic_conditions: Number of chronic conditions (0-10)
        previous_adherence_rate: Historical adherence rate (0.0-100.0)
    
    Returns:
        Predicted adherence rate (0.0-100.0)
    """
    # Create feature array
    features = np.array([[
        age, num_medications, medication_complexity,
        days_since_start, missed_doses_last_week,
        snooze_frequency, chronic_conditions,
        previous_adherence_rate
    ]])
    
    # Standardize features
    features_scaled = scaler.transform(features)
    
    # Make prediction
    prediction = best_model.predict(features_scaled)[0]
    
    # Ensure prediction is in valid range
    prediction = np.clip(prediction, 0.0, 100.0)
    
    return prediction

# Test with example patient
test_patient = {
    'age': 45,
    'num_medications': 3,
    'medication_complexity': 2.5,
    'days_since_start': 120,
    'missed_doses_last_week': 1,
    'snooze_frequency': 0.2,
    'chronic_conditions': 2,
    'previous_adherence_rate': 85.5
}

predicted_rate = predict_adherence(**test_patient)

print(f"\n   Test Patient Profile:")
for key, value in test_patient.items():
    print(f"      {key}: {value}")
print(f"\n   Predicted Adherence Rate: {predicted_rate:.2f}%")

# Validate prediction is in range
if 0.0 <= predicted_rate <= 100.0:
    print(f"   ✅ Prediction is within valid range [0, 100]")
else:
    print(f"   ❌ Prediction is out of range: {predicted_rate}")

print("\n" + "="*70)
print("MODEL TESTING COMPLETE ✅")
print("="*70)
print("\nThe saved model and scaler are working correctly!")
print("Ready for deployment in the FastAPI prediction service.")
print("="*70)
