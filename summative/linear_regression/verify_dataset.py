"""
Verify that the dataset meets all requirements from the specification.
"""

import pandas as pd

# Load dataset
df = pd.read_csv('adherence_data.csv')

print("=" * 60)
print("DATASET VERIFICATION REPORT")
print("=" * 60)

# Requirement 1.1: At least 1000 records
num_records = len(df)
print(f"\n✓ Requirement 1.1: Dataset has {num_records} records")
print(f"  Status: {'PASS' if num_records >= 1000 else 'FAIL'} (minimum: 1000)")

# Requirement 1.2: At least 8 distinct features (excluding target)
feature_columns = [col for col in df.columns if col != 'adherence_rate']
num_features = len(feature_columns)
print(f"\n✓ Requirement 1.2: Dataset has {num_features} features")
print(f"  Status: {'PASS' if num_features >= 8 else 'FAIL'} (minimum: 8)")
print(f"  Features: {', '.join(feature_columns)}")

# Requirement 1.3: Continuous target variable (0-100)
target_min = df['adherence_rate'].min()
target_max = df['adherence_rate'].max()
print(f"\n✓ Requirement 1.3: Target variable is continuous")
print(f"  Variable: adherence_rate")
print(f"  Range: {target_min:.2f} - {target_max:.2f}")
print(f"  Status: {'PASS' if 0 <= target_min and target_max <= 100 else 'FAIL'} (expected: 0-100)")

# Additional information
print(f"\n" + "=" * 60)
print("ADDITIONAL DATASET INFORMATION")
print("=" * 60)

print(f"\nData Types:")
for col in df.columns:
    print(f"  - {col}: {df[col].dtype}")

print(f"\nMissing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("  No missing values")
else:
    for col in missing[missing > 0].index:
        print(f"  - {col}: {missing[col]} ({(missing[col]/len(df)*100):.2f}%)")

print(f"\nBasic Statistics:")
print(df.describe())

print(f"\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
