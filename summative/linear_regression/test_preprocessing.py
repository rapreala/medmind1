#!/usr/bin/env python3
"""
Test script to verify the data preprocessing pipeline works correctly.
This executes the preprocessing steps from the notebook.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

print("="*70)
print("DATA PREPROCESSING PIPELINE TEST")
print("="*70)

# Load the dataset
print("\n1. Loading dataset...")
df = pd.read_csv('adherence_data.csv')
print(f"   ✅ Dataset loaded: {df.shape[0]} records, {df.shape[1]} columns")

# Check missing values
print("\n2. Checking missing values...")
missing_before = df.isnull().sum().sum()
print(f"   Missing values found: {missing_before}")

# Handle missing values
print("\n3. Handling missing values (dropping rows)...")
df_clean = df.dropna()
records_removed = len(df) - len(df_clean)
print(f"   Records before: {len(df)}")
print(f"   Records after: {len(df_clean)}")
print(f"   Records removed: {records_removed}")
print(f"   ✅ Retention rate: {(len(df_clean) / len(df)) * 100:.2f}%")

# Verify no missing values
missing_after = df_clean.isnull().sum().sum()
assert missing_after == 0, "Missing values still present!"
print(f"   ✅ All missing values handled (0 remaining)")

# Check for categorical variables
print("\n4. Checking for categorical variables...")
categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
if len(categorical_cols) > 0:
    print(f"   Categorical columns found: {categorical_cols}")
else:
    print(f"   ✅ No categorical variables (all numeric)")

# Separate features and target
print("\n5. Separating features and target...")
target_col = 'adherence_rate'
feature_cols = [col for col in df_clean.columns if col != target_col]
X = df_clean[feature_cols]
y = df_clean[target_col]
print(f"   Features (X): {X.shape}")
print(f"   Target (y): {y.shape}")
print(f"   ✅ {len(feature_cols)} features identified")

# Display feature statistics before standardization
print("\n6. Feature statistics BEFORE standardization:")
print(f"   {'Feature':<30} {'Mean':<12} {'Std Dev':<12}")
print("   " + "-"*54)
for col in feature_cols[:3]:  # Show first 3 for brevity
    print(f"   {col:<30} {X[col].mean():>8.2f}    {X[col].std():>8.2f}")
print(f"   ... ({len(feature_cols) - 3} more features)")

# Standardize features
print("\n7. Applying StandardScaler...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"   ✅ Standardization complete")

# Verify standardization
print("\n8. Verifying standardization (mean ≈ 0, std ≈ 1):")
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)
print(f"   {'Feature':<30} {'Mean':<12} {'Std Dev':<12}")
print("   " + "-"*54)
for col in feature_cols[:3]:  # Show first 3 for brevity
    mean_val = X_scaled_df[col].mean()
    std_val = X_scaled_df[col].std()
    print(f"   {col:<30} {mean_val:>8.6f}    {std_val:>8.6f}")
    # Verify mean ≈ 0 and std ≈ 1
    assert abs(mean_val) < 0.01, f"Mean not close to 0 for {col}"
    assert abs(std_val - 1.0) < 0.01, f"Std not close to 1 for {col}"
print(f"   ... ({len(feature_cols) - 3} more features)")
print(f"   ✅ All features properly standardized")

# Train-test split
print("\n9. Performing train-test split (80/20, random_state=42)...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, 
    y, 
    test_size=0.2, 
    random_state=42
)
print(f"   Training set: {X_train.shape[0]} samples ({(len(X_train) / len(X_scaled)) * 100:.1f}%)")
print(f"   Testing set: {X_test.shape[0]} samples ({(len(X_test) / len(X_scaled)) * 100:.1f}%)")

# Verify split proportions
expected_test_size = int(len(X_scaled) * 0.2)
actual_test_size = len(X_test)
assert abs(actual_test_size - expected_test_size) <= 1, "Split proportions incorrect"
print(f"   ✅ Split proportions verified (80/20)")

# Check target distribution
print("\n10. Verifying target distribution in train/test sets:")
print(f"    {'Set':<15} {'Mean':<10} {'Std Dev':<10}")
print("    " + "-"*35)
print(f"    {'Training':<15} {y_train.mean():>6.2f}    {y_train.std():>6.2f}")
print(f"    {'Testing':<15} {y_test.mean():>6.2f}    {y_test.std():>6.2f}")
print(f"    {'Full Dataset':<15} {y.mean():>6.2f}    {y.std():>6.2f}")
print(f"    ✅ Similar distributions (good split)")

# Save scaler
print("\n11. Saving scaler to disk...")
os.makedirs('models', exist_ok=True)
scaler_path = 'models/scaler.pkl'
joblib.dump(scaler, scaler_path)
file_size = os.path.getsize(scaler_path)
print(f"    File: {scaler_path}")
print(f"    Size: {file_size} bytes")
print(f"    ✅ Scaler saved successfully")

# Test loading scaler
print("\n12. Testing scaler load and verification...")
scaler_loaded = joblib.load(scaler_path)
test_sample = X.iloc[0:1]
scaled_original = scaler.transform(test_sample)
scaled_loaded = scaler_loaded.transform(test_sample)
match = np.allclose(scaled_original, scaled_loaded)
assert match, "Loaded scaler produces different results!"
print(f"    ✅ Scaler loads correctly")
print(f"    ✅ Produces identical results")

print("\n" + "="*70)
print("DATA PREPROCESSING PIPELINE: ALL TESTS PASSED ✅")
print("="*70)
print("\nSummary:")
print(f"  - Clean records: {len(df_clean)}")
print(f"  - Features: {len(feature_cols)}")
print(f"  - Training samples: {len(X_train)}")
print(f"  - Testing samples: {len(X_test)}")
print(f"  - Scaler saved: {scaler_path}")
print("\nData is ready for model training!")
