"""
Generate a synthetic medication adherence dataset for training ML models.

This script creates a realistic dataset with 1500 patient records and 8+ features
that influence medication adherence rates.
"""

import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n_samples = 1500

# Generate features
data = {
    # Patient demographics
    'age': np.random.randint(18, 121, n_samples),
    
    # Medication characteristics
    'num_medications': np.random.randint(1, 21, n_samples),
    'medication_complexity': np.random.uniform(1.0, 5.0, n_samples),
    
    # Temporal factors
    'days_since_start': np.random.randint(0, 3651, n_samples),
    
    # Recent behavior
    'missed_doses_last_week': np.random.randint(0, 51, n_samples),
    'snooze_frequency': np.random.uniform(0.0, 1.0, n_samples),
    
    # Health factors
    'chronic_conditions': np.random.randint(0, 11, n_samples),
    'previous_adherence_rate': np.random.uniform(0.0, 100.0, n_samples),
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate target variable (adherence_rate) based on features
# This creates realistic relationships between features and adherence

# Base adherence rate
adherence_rate = 75.0

# Age effect: older patients tend to be more adherent (up to age 70, then slight decline)
age_effect = np.where(df['age'] < 70, 
                      (df['age'] - 18) * 0.15,  # Increase with age
                      (df['age'] - 70) * -0.05 + (70 - 18) * 0.15)  # Slight decline after 70

# Medication complexity: more complex = lower adherence
complexity_effect = -5.0 * (df['medication_complexity'] - 1.0)

# Number of medications: polypharmacy reduces adherence
num_meds_effect = -1.5 * (df['num_medications'] - 1)

# Days since start: adherence decreases over time
days_effect = -0.002 * df['days_since_start']

# Recent missed doses: strong negative predictor
missed_effect = -2.0 * df['missed_doses_last_week']

# Snooze frequency: procrastination reduces adherence
snooze_effect = -15.0 * df['snooze_frequency']

# Chronic conditions: more conditions = slightly better adherence (health awareness)
conditions_effect = 1.0 * df['chronic_conditions']

# Previous adherence: strongest predictor (regression to mean)
previous_effect = 0.4 * (df['previous_adherence_rate'] - 75.0)

# Combine all effects
df['adherence_rate'] = (
    adherence_rate +
    age_effect +
    complexity_effect +
    num_meds_effect +
    days_effect +
    missed_effect +
    snooze_effect +
    conditions_effect +
    previous_effect +
    np.random.normal(0, 5, n_samples)  # Add noise
)

# Clip to valid range [0, 100]
df['adherence_rate'] = df['adherence_rate'].clip(0, 100)

# Round to 2 decimal places
df['adherence_rate'] = df['adherence_rate'].round(2)

# Introduce some missing values (realistic scenario)
# Randomly set 2% of values to NaN across different columns
for col in ['medication_complexity', 'snooze_frequency', 'previous_adherence_rate']:
    mask = np.random.random(n_samples) < 0.02
    df.loc[mask, col] = np.nan

# Save to CSV
output_path = 'summative/linear_regression/adherence_data.csv'
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully!")
print(f"Saved to: {output_path}")
print(f"\nDataset Statistics:")
print(f"- Total records: {len(df)}")
print(f"- Number of features: {len(df.columns) - 1}")  # Exclude target
print(f"- Target variable: adherence_rate")
print(f"\nFeature columns:")
for col in df.columns:
    if col != 'adherence_rate':
        print(f"  - {col}")
print(f"\nTarget column:")
print(f"  - adherence_rate (range: {df['adherence_rate'].min():.2f} - {df['adherence_rate'].max():.2f})")
print(f"\nMissing values:")
print(df.isnull().sum())
