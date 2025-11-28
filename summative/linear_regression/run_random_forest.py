#!/usr/bin/env python3
"""
Script to execute Random Forest model training and evaluation.
This script runs the Random Forest section with hyperparameter tuning.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
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
print("RANDOM FOREST MODEL TRAINING WITH HYPERPARAMETER TUNING")
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
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
total_combinations = (len(param_grid['n_estimators']) * 
                     len(param_grid['max_depth']) * 
                     len(param_grid['min_samples_split']) * 
                     len(param_grid['min_samples_leaf']))
print(f"   ✅ Grid defined: {total_combinations} combinations to test")
print(f"      n_estimators: {param_grid['n_estimators']}")
print(f"      max_depth: {param_grid['max_depth']}")
print(f"      min_samples_split: {param_grid['min_samples_split']}")
print(f"      min_samples_leaf: {param_grid['min_samples_leaf']}")

# Initialize Random Forest and GridSearchCV
print("\n7. Performing hyperparameter tuning with 5-fold cross-validation...")
print("   (This may take 2-5 minutes...)")
rf_base = RandomForestRegressor(random_state=42, n_jobs=-1)
grid_search = GridSearchCV(
    estimator=rf_base,
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
rf_model = grid_search.best_estimator_
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
print(f"  - Number of trees: {rf_model.n_estimators}")
print(f"  - Max depth: {rf_model.max_depth}")
print(f"  - Min samples split: {rf_model.min_samples_split}")
print(f"  - Min samples leaf: {rf_model.min_samples_leaf}")

# Make predictions
print("\n8. Generating predictions...")
y_train_pred_rf = rf_model.predict(X_train)
y_test_pred_rf = rf_model.predict(X_test)
print(f"   ✅ Predictions generated")

# Calculate metrics
print("\n9. Calculating evaluation metrics...")
train_mse_rf = mean_squared_error(y_train, y_train_pred_rf)
train_rmse_rf = np.sqrt(train_mse_rf)
train_r2_rf = r2_score(y_train, y_train_pred_rf)

test_mse_rf = mean_squared_error(y_test, y_test_pred_rf)
test_rmse_rf = np.sqrt(test_mse_rf)
test_r2_rf = r2_score(y_test, y_test_pred_rf)

print("\n" + "="*70)
print("RANDOM FOREST MODEL PERFORMANCE")
print("="*70)
print(f"\n{'Metric':<25} {'Training Set':<20} {'Test Set':<20}")
print("-"*70)
print(f"{'Mean Squared Error':<25} {train_mse_rf:>15.4f}     {test_mse_rf:>15.4f}")
print(f"{'Root Mean Squared Error':<25} {train_rmse_rf:>15.4f}     {test_rmse_rf:>15.4f}")
print(f"{'R-squared (R²)':<25} {train_r2_rf:>15.4f}     {test_r2_rf:>15.4f}")
print("="*70)

# Load previous model metrics for comparison
print("\n10. Comparing with previous models...")
try:
    # Load Linear Regression metrics
    with open('models/lr_metrics.txt', 'r') as f:
        lr_content = f.read()
        in_test = False
        for line in lr_content.split('\n'):
            if 'Test Set:' in line:
                in_test = True
            elif in_test and 'MSE:' in line:
                test_mse_lr = float(line.split(':')[1].strip())
            elif in_test and 'R²:' in line:
                test_r2_lr = float(line.split(':')[1].strip())
                break
    
    # Load Decision Tree metrics
    with open('models/dt_metrics.txt', 'r') as f:
        dt_content = f.read()
        in_test = False
        for line in dt_content.split('\n'):
            if 'Test Set:' in line:
                in_test = True
            elif in_test and 'MSE:' in line:
                test_mse_dt = float(line.split(':')[1].strip())
            elif in_test and 'R²:' in line:
                test_r2_dt = float(line.split(':')[1].strip())
                break
    
    print("\n" + "="*70)
    print("MODEL COMPARISON: ALL THREE MODELS")
    print("="*70)
    print(f"\n{'Metric':<20} {'Linear Reg':<15} {'Decision Tree':<15} {'Random Forest':<15} {'Best'}")
    print("-"*70)
    
    # MSE comparison
    mse_values = {'Linear Reg': test_mse_lr, 'Decision Tree': test_mse_dt, 'Random Forest': test_mse_rf}
    mse_best = min(mse_values, key=mse_values.get)
    print(f"{'Test MSE':<20} {test_mse_lr:>10.4f}      {test_mse_dt:>10.4f}      {test_mse_rf:>10.4f}      {mse_best}")
    
    # R² comparison
    r2_values = {'Linear Reg': test_r2_lr, 'Decision Tree': test_r2_dt, 'Random Forest': test_r2_rf}
    r2_best = max(r2_values, key=r2_values.get)
    print(f"{'Test R²':<20} {test_r2_lr:>10.4f}      {test_r2_dt:>10.4f}      {test_r2_rf:>10.4f}      {r2_best}")
    
    print("="*70)
    
    # Performance improvements
    print("\nRandom Forest Improvements:")
    print("-"*70)
    lr_improvement = ((test_mse_lr - test_mse_rf) / test_mse_lr) * 100
    dt_improvement = ((test_mse_dt - test_mse_rf) / test_mse_dt) * 100
    print(f"vs Linear Regression:  {lr_improvement:>6.2f}% MSE reduction")
    print(f"vs Decision Tree:      {dt_improvement:>6.2f}% MSE reduction")
    
    # Overfitting analysis
    print("\nOverfitting Analysis:")
    print("-"*70)
    rf_overfit = abs(train_r2_rf - test_r2_rf)
    print(f"Random Forest - Train R²: {train_r2_rf:.4f}, Test R²: {test_r2_rf:.4f}, Gap: {rf_overfit:.4f}")
    
    if rf_overfit < 0.05:
        print("✅ Minimal overfitting - model generalizes excellently")
    elif rf_overfit < 0.10:
        print("⚠️  Slight overfitting - acceptable for most applications")
    else:
        print("⚠️  Significant overfitting detected")
        print("   Consider: reducing max_depth, increasing min_samples_split")
    
except FileNotFoundError as e:
    print(f"   ⚠️  Could not load previous model metrics: {e}")
    print("   Run run_linear_regression.py and run_decision_tree.py first for comparison.")

# Feature importance
print("\n11. Analyzing feature importance...")
feature_importance_rf = rf_model.feature_importances_

# Create DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': feature_importance_rf
}).sort_values('Importance', ascending=False)

print("\n" + "="*70)
print("RANDOM FOREST FEATURE IMPORTANCE")
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
bars = plt.barh(importance_df['Feature'], importance_df['Importance'], color='forestgreen', edgecolor='black')

# Color the top 3 features differently
for i in range(min(3, len(bars))):
    bars[i].set_color('coral')

plt.xlabel('Feature Importance Score', fontsize=12, fontweight='bold')
plt.ylabel('Features', fontsize=12, fontweight='bold')
plt.title('Random Forest: Feature Importance Scores\n(Higher = More Important for Predictions)', 
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()  # Highest importance at top
plt.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, (_, row) in enumerate(importance_df.iterrows()):
    plt.text(row['Importance'] + 0.005, i, f"{row['Importance']:.4f}", 
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/rf_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Feature importance plot saved: plots/rf_feature_importance.png")

# Plot 2: Actual vs Predicted
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Random Forest: Actual vs Predicted Adherence Rates', 
             fontsize=16, fontweight='bold', y=1.02)

# Training set
ax1.scatter(y_train, y_train_pred_rf, alpha=0.5, s=30, color='darkgreen', edgecolors='black', linewidth=0.5)
ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 
         'r--', linewidth=2, label='Perfect Prediction Line')
ax1.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title(f'Training Set\nR² = {train_r2_rf:.4f}, RMSE = {train_rmse_rf:.2f}', 
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3)
ax1.set_xlim([0, 100])
ax1.set_ylim([0, 100])

# Test set
ax2.scatter(y_test, y_test_pred_rf, alpha=0.5, s=30, color='lime', edgecolors='black', linewidth=0.5)
ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', linewidth=2, label='Perfect Prediction Line')
ax2.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title(f'Test Set\nR² = {test_r2_rf:.4f}, RMSE = {test_rmse_rf:.2f}', 
              fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
ax2.set_xlim([0, 100])
ax2.set_ylim([0, 100])

plt.tight_layout()
plt.savefig('plots/rf_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Actual vs Predicted plot saved: plots/rf_actual_vs_predicted.png")

# Save metrics to file
print("\n13. Saving metrics to file...")
os.makedirs('models', exist_ok=True)
with open('models/rf_metrics.txt', 'w') as f:
    f.write("RANDOM FOREST MODEL METRICS\n")
    f.write("="*70 + "\n\n")
    f.write(f"Best Hyperparameters:\n")
    for param, value in best_params.items():
        f.write(f"  {param}: {value}\n")
    f.write(f"\nModel Configuration:\n")
    f.write(f"  Number of trees: {rf_model.n_estimators}\n")
    f.write(f"  Max depth: {rf_model.max_depth}\n")
    f.write(f"  Min samples split: {rf_model.min_samples_split}\n")
    f.write(f"  Min samples leaf: {rf_model.min_samples_leaf}\n\n")
    f.write(f"Training Set:\n")
    f.write(f"  MSE:  {train_mse_rf:.4f}\n")
    f.write(f"  RMSE: {train_rmse_rf:.4f}\n")
    f.write(f"  R²:   {train_r2_rf:.4f}\n\n")
    f.write(f"Test Set:\n")
    f.write(f"  MSE:  {test_mse_rf:.4f}\n")
    f.write(f"  RMSE: {test_rmse_rf:.4f}\n")
    f.write(f"  R²:   {test_r2_rf:.4f}\n\n")
    f.write(f"Hyperparameter Tuning Time: {tuning_time:.2f} seconds\n\n")
    f.write("Feature Importance:\n")
    for _, row in importance_df.iterrows():
        f.write(f"  {row['Feature']:<30} {row['Importance']:>10.4f}\n")

print("   ✅ Metrics saved: models/rf_metrics.txt")

# Summary
print("\n" + "="*70)
print("RANDOM FOREST TRAINING COMPLETE ✅")
print("="*70)
print(f"\nModel Performance Summary:")
print(f"  - Test R²: {test_r2_rf:.4f} ({test_r2_rf*100:.2f}% variance explained)")
print(f"  - Test RMSE: {test_rmse_rf:.2f} (average error in percentage points)")
print(f"  - Hyperparameter Tuning Time: {tuning_time:.2f} seconds")
print(f"\nBest Hyperparameters:")
for param, value in best_params.items():
    print(f"  - {param}: {value}")
print(f"\nTop 3 Most Important Features:")
for idx, (_, row) in enumerate(importance_df.head(3).iterrows(), 1):
    print(f"  {idx}. {row['Feature']}: {row['Importance']:.4f}")
print(f"\nFiles Created:")
print(f"  - plots/rf_feature_importance.png")
print(f"  - plots/rf_actual_vs_predicted.png")
print(f"  - models/rf_metrics.txt")
print("\n" + "="*70)
