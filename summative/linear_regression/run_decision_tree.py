#!/usr/bin/env python3
"""
Script to execute Decision Tree model training and evaluation.
This script runs the Decision Tree section with hyperparameter tuning.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
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
print("DECISION TREE MODEL TRAINING WITH HYPERPARAMETER TUNING")
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

# Define hyperparameter grid for tuning
print("\n6. Setting up hyperparameter grid...")
param_grid = {
    'max_depth': [3, 5, 7, 10, 15, 20, None],
    'min_samples_split': [2, 5, 10, 20],
    'min_samples_leaf': [1, 2, 4, 8]
}
total_combinations = len(param_grid['max_depth']) * len(param_grid['min_samples_split']) * len(param_grid['min_samples_leaf'])
print(f"   ✅ Grid defined: {total_combinations} combinations to test")
print(f"      max_depth: {param_grid['max_depth']}")
print(f"      min_samples_split: {param_grid['min_samples_split']}")
print(f"      min_samples_leaf: {param_grid['min_samples_leaf']}")

# Initialize Decision Tree and GridSearchCV
print("\n7. Performing hyperparameter tuning with 5-fold cross-validation...")
print("   (This may take 1-2 minutes...)")
dt_base = DecisionTreeRegressor(random_state=42)
grid_search = GridSearchCV(
    estimator=dt_base,
    param_grid=param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    verbose=0
)

start_time = time.time()
grid_search.fit(X_train, y_train)
tuning_time = time.time() - start_time
print(f"   ✅ Hyperparameter tuning complete in {tuning_time:.2f} seconds")

# Get the best model
dt_model = grid_search.best_estimator_
best_params = grid_search.best_params_
best_cv_mse = -grid_search.best_score_
best_cv_rmse = np.sqrt(best_cv_mse)

print("\n" + "="*70)
print("BEST HYPERPARAMETERS FOUND")
print("="*70)
print(f"\nBest parameters:")
for param, value in best_params.items():
    print(f"  - {param}: {value}")
print(f"\nCross-validation performance:")
print(f"  - Best CV MSE: {best_cv_mse:.4f}")
print(f"  - Best CV RMSE: {best_cv_rmse:.4f}")
print(f"\nBest model configuration:")
print(f"  - Tree depth: {dt_model.get_depth()}")
print(f"  - Number of leaf nodes: {dt_model.get_n_leaves()}")

# Make predictions
print("\n8. Generating predictions...")
y_train_pred_dt = dt_model.predict(X_train)
y_test_pred_dt = dt_model.predict(X_test)
print(f"   ✅ Predictions generated")

# Calculate metrics
print("\n9. Calculating evaluation metrics...")
train_mse_dt = mean_squared_error(y_train, y_train_pred_dt)
train_rmse_dt = np.sqrt(train_mse_dt)
train_r2_dt = r2_score(y_train, y_train_pred_dt)

test_mse_dt = mean_squared_error(y_test, y_test_pred_dt)
test_rmse_dt = np.sqrt(test_mse_dt)
test_r2_dt = r2_score(y_test, y_test_pred_dt)

print("\n" + "="*70)
print("DECISION TREE MODEL PERFORMANCE")
print("="*70)
print(f"\n{'Metric':<25} {'Training Set':<20} {'Test Set':<20}")
print("-"*70)
print(f"{'Mean Squared Error':<25} {train_mse_dt:>15.4f}     {test_mse_dt:>15.4f}")
print(f"{'Root Mean Squared Error':<25} {train_rmse_dt:>15.4f}     {test_rmse_dt:>15.4f}")
print(f"{'R-squared (R²)':<25} {train_r2_dt:>15.4f}     {test_r2_dt:>15.4f}")
print("="*70)

# Load Linear Regression metrics for comparison
print("\n10. Comparing with Linear Regression baseline...")
try:
    with open('models/lr_metrics.txt', 'r') as f:
        lr_content = f.read()
        # Extract test MSE and R² from LR metrics
        in_test = False
        for line in lr_content.split('\n'):
            if 'Test Set:' in line:
                in_test = True
            elif in_test and 'MSE:' in line:
                test_mse_lr = float(line.split(':')[1].strip())
            elif in_test and 'R²:' in line:
                test_r2_lr = float(line.split(':')[1].strip())
                break
    
    print("\n" + "="*70)
    print("MODEL COMPARISON: DECISION TREE vs LINEAR REGRESSION")
    print("="*70)
    print(f"\n{'Metric':<25} {'Linear Reg':<15} {'Decision Tree':<15} {'Winner'}")
    print("-"*70)
    
    # MSE comparison
    mse_winner = "Decision Tree" if test_mse_dt < test_mse_lr else "Linear Reg"
    mse_improvement = abs(test_mse_dt - test_mse_lr) / test_mse_lr * 100
    mse_direction = "better" if test_mse_dt < test_mse_lr else "worse"
    print(f"{'Test MSE':<25} {test_mse_lr:>10.4f}      {test_mse_dt:>10.4f}      {mse_winner} ({mse_improvement:.1f}% {mse_direction})")
    
    # R² comparison
    r2_winner = "Decision Tree" if test_r2_dt > test_r2_lr else "Linear Reg"
    r2_improvement = abs(test_r2_dt - test_r2_lr) / test_r2_lr * 100
    r2_direction = "better" if test_r2_dt > test_r2_lr else "worse"
    print(f"{'Test R²':<25} {test_r2_lr:>10.4f}      {test_r2_dt:>10.4f}      {r2_winner} ({r2_improvement:.1f}% {r2_direction})")
    
    print("="*70)
    
    # Overfitting analysis
    print("\nOverfitting Analysis:")
    print("-"*70)
    dt_overfit = abs(train_r2_dt - test_r2_dt)
    print(f"Decision Tree - Train R²: {train_r2_dt:.4f}, Test R²: {test_r2_dt:.4f}, Gap: {dt_overfit:.4f}")
    
    if dt_overfit < 0.05:
        print("✅ Minimal overfitting - model generalizes well")
    elif dt_overfit < 0.10:
        print("⚠️  Slight overfitting - acceptable for most applications")
    else:
        print("⚠️  Significant overfitting detected")
        print("   Hyperparameter tuning helped, but consider further regularization")
    
except FileNotFoundError:
    print("   ⚠️  Linear Regression metrics not found. Run run_linear_regression.py first.")

# Feature importance
print("\n11. Analyzing feature importance...")
feature_importance_dt = dt_model.feature_importances_

# Create DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': feature_importance_dt
}).sort_values('Importance', ascending=False)

print("\n" + "="*70)
print("DECISION TREE FEATURE IMPORTANCE")
print("="*70)
print(f"\n{'Rank':<6} {'Feature':<30} {'Importance':<15} {'Percentage'}")
print("-"*70)

for idx, (_, row) in enumerate(importance_df.iterrows(), 1):
    print(f"{idx:<6} {row['Feature']:<30} {row['Importance']:>10.4f}      {row['Importance']*100:>6.2f}%")

print("="*70)
print(f"\nTop 3 features account for {importance_df.head(3)['Importance'].sum()*100:.1f}% of total importance")

# Create visualizations
print("\n12. Creating visualizations...")
os.makedirs('plots', exist_ok=True)

# Plot 1: Feature Importance
plt.figure(figsize=(12, 8))
bars = plt.barh(importance_df['Feature'], importance_df['Importance'], color='steelblue', edgecolor='black')

# Color the top 3 features differently
for i in range(min(3, len(bars))):
    bars[i].set_color('coral')

plt.xlabel('Feature Importance Score', fontsize=12, fontweight='bold')
plt.ylabel('Features', fontsize=12, fontweight='bold')
plt.title('Decision Tree: Feature Importance Scores\n(Higher = More Important for Predictions)', 
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()  # Highest importance at top
plt.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, (_, row) in enumerate(importance_df.iterrows()):
    plt.text(row['Importance'] + 0.005, i, f"{row['Importance']:.4f}", 
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/dt_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Feature importance plot saved: plots/dt_feature_importance.png")

# Plot 2: Actual vs Predicted
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Decision Tree: Actual vs Predicted Adherence Rates', 
             fontsize=16, fontweight='bold', y=1.02)

# Training set
ax1.scatter(y_train, y_train_pred_dt, alpha=0.5, s=30, color='purple', edgecolors='black', linewidth=0.5)
ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 
         'r--', linewidth=2, label='Perfect Prediction Line')
ax1.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title(f'Training Set\nR² = {train_r2_dt:.4f}, RMSE = {train_rmse_dt:.2f}', 
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3)
ax1.set_xlim([0, 100])
ax1.set_ylim([0, 100])

# Test set
ax2.scatter(y_test, y_test_pred_dt, alpha=0.5, s=30, color='orange', edgecolors='black', linewidth=0.5)
ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', linewidth=2, label='Perfect Prediction Line')
ax2.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title(f'Test Set\nR² = {test_r2_dt:.4f}, RMSE = {test_rmse_dt:.2f}', 
              fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
ax2.set_xlim([0, 100])
ax2.set_ylim([0, 100])

plt.tight_layout()
plt.savefig('plots/dt_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Actual vs Predicted plot saved: plots/dt_actual_vs_predicted.png")

# Save metrics to file
print("\n13. Saving metrics to file...")
os.makedirs('models', exist_ok=True)
with open('models/dt_metrics.txt', 'w') as f:
    f.write("DECISION TREE MODEL METRICS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Best Hyperparameters:\n")
    for param, value in best_params.items():
        f.write(f"  {param}: {value}\n")
    f.write(f"\nModel Structure:\n")
    f.write(f"  Tree depth: {dt_model.get_depth()}\n")
    f.write(f"  Number of leaf nodes: {dt_model.get_n_leaves()}\n\n")
    f.write(f"Training Set:\n")
    f.write(f"  MSE:  {train_mse_dt:.4f}\n")
    f.write(f"  RMSE: {train_rmse_dt:.4f}\n")
    f.write(f"  R²:   {train_r2_dt:.4f}\n\n")
    f.write(f"Test Set:\n")
    f.write(f"  MSE:  {test_mse_dt:.4f}\n")
    f.write(f"  RMSE: {test_rmse_dt:.4f}\n")
    f.write(f"  R²:   {test_r2_dt:.4f}\n\n")
    f.write(f"Hyperparameter Tuning Time: {tuning_time:.2f} seconds\n\n")
    f.write("Feature Importance:\n")
    for _, row in importance_df.iterrows():
        f.write(f"  {row['Feature']:<30} {row['Importance']:>10.4f}\n")

print("   ✅ Metrics saved: models/dt_metrics.txt")

# Summary
print("\n" + "="*70)
print("DECISION TREE TRAINING COMPLETE ✅")
print("="*70)
print(f"\nModel Performance Summary:")
print(f"  - Test R²: {test_r2_dt:.4f} ({test_r2_dt*100:.2f}% variance explained)")
print(f"  - Test RMSE: {test_rmse_dt:.2f} (average error in percentage points)")
print(f"  - Hyperparameter Tuning Time: {tuning_time:.2f} seconds")
print(f"\nBest Hyperparameters:")
for param, value in best_params.items():
    print(f"  - {param}: {value}")
print(f"\nTop 3 Most Important Features:")
for idx, (_, row) in enumerate(importance_df.head(3).iterrows(), 1):
    print(f"  {idx}. {row['Feature']}: {row['Importance']:.4f}")
print(f"\nFiles Created:")
print(f"  - plots/dt_feature_importance.png")
print(f"  - plots/dt_actual_vs_predicted.png")
print(f"  - models/dt_metrics.txt")
print("\n" + "="*70)
