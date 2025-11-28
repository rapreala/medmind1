#!/usr/bin/env python3
"""
Script to execute Linear Regression model training and evaluation.
This script runs the Linear Regression section of the notebook programmatically.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import time
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

print("="*70)
print("LINEAR REGRESSION MODEL TRAINING AND EVALUATION")
print("="*70)

# Load the dataset
print("\n1. Loading dataset...")
df = pd.read_csv('adherence_data.csv')
print(f"   ✅ Dataset loaded: {df.shape[0]} records, {df.shape[1]} columns")

# Handle missing values
print("\n2. Handling missing values...")
df_clean = df.dropna()
print(f"   ✅ Clean records: {len(df_clean)} (removed {len(df) - len(df_clean)} rows)")

# Separate features and target
print("\n3. Preparing features and target...")
target_col = 'adherence_rate'
feature_cols = [col for col in df_clean.columns if col != target_col]
X = df_clean[feature_cols]
y = df_clean[target_col]
print(f"   ✅ Features: {X.shape[1]}, Target: {target_col}")

# Standardize features
print("\n4. Standardizing features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"   ✅ Features standardized (mean ≈ 0, std ≈ 1)")

# Train-test split
print("\n5. Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"   ✅ Training: {len(X_train)} samples, Testing: {len(X_test)} samples")

# Train Linear Regression model
print("\n6. Training Linear Regression model...")
lr_model = LinearRegression()
start_time = time.time()
lr_model.fit(X_train, y_train)
training_time = time.time() - start_time
print(f"   ✅ Training complete in {training_time:.4f} seconds")

# Make predictions
print("\n7. Generating predictions...")
y_train_pred_lr = lr_model.predict(X_train)
y_test_pred_lr = lr_model.predict(X_test)
print(f"   ✅ Predictions generated")

# Calculate metrics
print("\n8. Calculating evaluation metrics...")
train_mse_lr = mean_squared_error(y_train, y_train_pred_lr)
train_rmse_lr = np.sqrt(train_mse_lr)
train_r2_lr = r2_score(y_train, y_train_pred_lr)

test_mse_lr = mean_squared_error(y_test, y_test_pred_lr)
test_rmse_lr = np.sqrt(test_mse_lr)
test_r2_lr = r2_score(y_test, y_test_pred_lr)

print("\n" + "="*70)
print("LINEAR REGRESSION MODEL PERFORMANCE")
print("="*70)
print(f"\n{'Metric':<25} {'Training Set':<20} {'Test Set':<20}")
print("-"*70)
print(f"{'Mean Squared Error':<25} {train_mse_lr:>15.4f}     {test_mse_lr:>15.4f}")
print(f"{'Root Mean Squared Error':<25} {train_rmse_lr:>15.4f}     {test_rmse_lr:>15.4f}")
print(f"{'R-squared (R²)':<25} {train_r2_lr:>15.4f}     {test_r2_lr:>15.4f}")
print("="*70)

# Display feature coefficients
print("\n9. Feature Coefficients (Impact on Adherence Rate):")
print("="*70)
print(f"{'Feature':<30} {'Coefficient':<15} {'Impact'}")
print("-"*70)

coef_pairs = list(zip(feature_cols, lr_model.coef_))
coef_pairs_sorted = sorted(coef_pairs, key=lambda x: abs(x[1]), reverse=True)

for feature, coef in coef_pairs_sorted:
    impact = "Increases adherence" if coef > 0 else "Decreases adherence"
    print(f"{feature:<30} {coef:>+10.4f}      {impact}")
print("="*70)

# Create visualizations
print("\n10. Creating visualizations...")

# Create plots directory
os.makedirs('plots', exist_ok=True)

# Plot 1: Actual vs Predicted
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Linear Regression: Actual vs Predicted Adherence Rates', 
             fontsize=16, fontweight='bold', y=1.02)

# Training set
ax1.scatter(y_train, y_train_pred_lr, alpha=0.5, s=30, color='blue', edgecolors='black', linewidth=0.5)
ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 
         'r--', linewidth=2, label='Perfect Prediction Line')
ax1.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title(f'Training Set\nR² = {train_r2_lr:.4f}, RMSE = {train_rmse_lr:.2f}', 
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3)
ax1.set_xlim([0, 100])
ax1.set_ylim([0, 100])

# Test set
ax2.scatter(y_test, y_test_pred_lr, alpha=0.5, s=30, color='green', edgecolors='black', linewidth=0.5)
ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', linewidth=2, label='Perfect Prediction Line')
ax2.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title(f'Test Set\nR² = {test_r2_lr:.4f}, RMSE = {test_rmse_lr:.2f}', 
              fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
ax2.set_xlim([0, 100])
ax2.set_ylim([0, 100])

plt.tight_layout()
plt.savefig('plots/lr_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Actual vs Predicted plot saved: plots/lr_actual_vs_predicted.png")

# Plot 2: Residual Analysis
train_residuals_lr = y_train - y_train_pred_lr
test_residuals_lr = y_test - y_test_pred_lr

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Linear Regression: Residual Analysis', fontsize=16, fontweight='bold', y=1.00)

# Residuals vs Predicted (Training)
axes[0, 0].scatter(y_train_pred_lr, train_residuals_lr, alpha=0.5, s=20, color='blue')
axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Predicted Adherence Rate (%)', fontsize=11)
axes[0, 0].set_ylabel('Residuals (Actual - Predicted)', fontsize=11)
axes[0, 0].set_title('Training Set: Residuals vs Predicted Values', fontsize=12, fontweight='bold')
axes[0, 0].grid(alpha=0.3)

# Residuals vs Predicted (Test)
axes[0, 1].scatter(y_test_pred_lr, test_residuals_lr, alpha=0.5, s=20, color='green')
axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('Predicted Adherence Rate (%)', fontsize=11)
axes[0, 1].set_ylabel('Residuals (Actual - Predicted)', fontsize=11)
axes[0, 1].set_title('Test Set: Residuals vs Predicted Values', fontsize=12, fontweight='bold')
axes[0, 1].grid(alpha=0.3)

# Residual Distribution (Training)
axes[1, 0].hist(train_residuals_lr, bins=30, color='blue', alpha=0.7, edgecolor='black')
axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Residuals', fontsize=11)
axes[1, 0].set_ylabel('Frequency', fontsize=11)
axes[1, 0].set_title(f'Training Set: Residual Distribution\nMean: {train_residuals_lr.mean():.4f}, Std: {train_residuals_lr.std():.4f}', 
                     fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)

# Residual Distribution (Test)
axes[1, 1].hist(test_residuals_lr, bins=30, color='green', alpha=0.7, edgecolor='black')
axes[1, 1].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Residuals', fontsize=11)
axes[1, 1].set_ylabel('Frequency', fontsize=11)
axes[1, 1].set_title(f'Test Set: Residual Distribution\nMean: {test_residuals_lr.mean():.4f}, Std: {test_residuals_lr.std():.4f}', 
                     fontsize=12, fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('plots/lr_residuals.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Residual analysis plot saved: plots/lr_residuals.png")

# Save metrics to file
print("\n11. Saving metrics to file...")
os.makedirs('models', exist_ok=True)
with open('models/lr_metrics.txt', 'w') as f:
    f.write("LINEAR REGRESSION MODEL METRICS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Training Set:\n")
    f.write(f"  MSE:  {train_mse_lr:.4f}\n")
    f.write(f"  RMSE: {train_rmse_lr:.4f}\n")
    f.write(f"  R²:   {train_r2_lr:.4f}\n\n")
    f.write(f"Test Set:\n")
    f.write(f"  MSE:  {test_mse_lr:.4f}\n")
    f.write(f"  RMSE: {test_rmse_lr:.4f}\n")
    f.write(f"  R²:   {test_r2_lr:.4f}\n\n")
    f.write(f"Training Time: {training_time:.4f} seconds\n\n")
    f.write("Feature Coefficients:\n")
    for feature, coef in coef_pairs_sorted:
        f.write(f"  {feature:<30} {coef:>+10.4f}\n")

print("   ✅ Metrics saved: models/lr_metrics.txt")

# Summary
print("\n" + "="*70)
print("LINEAR REGRESSION TRAINING COMPLETE ✅")
print("="*70)
print(f"\nModel Performance Summary:")
print(f"  - Test R²: {test_r2_lr:.4f} ({test_r2_lr*100:.2f}% variance explained)")
print(f"  - Test RMSE: {test_rmse_lr:.2f} (average error in percentage points)")
print(f"  - Training Time: {training_time:.4f} seconds")
print(f"\nFiles Created:")
print(f"  - plots/lr_actual_vs_predicted.png")
print(f"  - plots/lr_residuals.png")
print(f"  - models/lr_metrics.txt")
print("\n" + "="*70)
