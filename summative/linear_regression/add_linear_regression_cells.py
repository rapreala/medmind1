#!/usr/bin/env python3
"""
Script to add Linear Regression model training cells to the Jupyter notebook.
This implements task 4 from the implementation plan.
"""

import json
import sys

def add_linear_regression_cells(notebook_path):
    """Add Linear Regression training and evaluation cells to the notebook."""
    
    # Read the existing notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Define the new cells for Linear Regression
    new_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Model Training and Evaluation\n",
                "\n",
                "In this section, we will:\n",
                "1. Train a Linear Regression model\n",
                "2. Train a Decision Tree model\n",
                "3. Train a Random Forest model\n",
                "4. Compare all three models\n",
                "5. Select and save the best-performing model\n",
                "\n",
                "For each model, we will:\n",
                "- Train on the training set\n",
                "- Make predictions on both training and test sets\n",
                "- Calculate MSE and R-squared metrics\n",
                "- Create visualizations (actual vs predicted, residuals, feature importance)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.1 Linear Regression Model\n",
                "\n",
                "Linear Regression is a fundamental algorithm that models the relationship between features and target as a linear equation:\n",
                "\n",
                "**y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ**\n",
                "\n",
                "Where:\n",
                "- y is the predicted adherence rate\n",
                "- β₀ is the intercept\n",
                "- β₁, β₂, ..., βₙ are the coefficients for each feature\n",
                "- x₁, x₂, ..., xₙ are the feature values\n",
                "\n",
                "**Advantages:**\n",
                "- Simple and interpretable\n",
                "- Fast training and prediction\n",
                "- Works well when relationships are linear\n",
                "- Provides coefficient values showing feature importance\n",
                "\n",
                "**Limitations:**\n",
                "- Assumes linear relationships\n",
                "- Cannot capture complex interactions\n",
                "- Sensitive to outliers"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Import LinearRegression from scikit-learn\n",
                "from sklearn.linear_model import LinearRegression\n",
                "import time\n",
                "\n",
                "print(\"=\"*70)\n",
                "print(\"LINEAR REGRESSION MODEL TRAINING\")\n",
                "print(\"=\"*70)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Initialize and train Linear Regression model\n",
                "print(\"\\nInitializing Linear Regression model...\")\n",
                "lr_model = LinearRegression()\n",
                "\n",
                "print(\"Training on standardized training data...\")\n",
                "start_time = time.time()\n",
                "lr_model.fit(X_train, y_train)\n",
                "training_time = time.time() - start_time\n",
                "\n",
                "print(f\"✅ Training complete in {training_time:.4f} seconds\")\n",
                "print(f\"\\nModel Parameters:\")\n",
                "print(f\"  - Intercept: {lr_model.intercept_:.4f}\")\n",
                "print(f\"  - Number of coefficients: {len(lr_model.coef_)}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Display feature coefficients\n",
                "print(\"\\nFeature Coefficients (Impact on Adherence Rate):\")\n",
                "print(\"=\"*70)\n",
                "print(f\"{'Feature':<30} {'Coefficient':<15} {'Impact'}\")\n",
                "print(\"-\"*70)\n",
                "\n",
                "# Create a list of (feature, coefficient) pairs and sort by absolute value\n",
                "coef_pairs = list(zip(feature_cols, lr_model.coef_))\n",
                "coef_pairs_sorted = sorted(coef_pairs, key=lambda x: abs(x[1]), reverse=True)\n",
                "\n",
                "for feature, coef in coef_pairs_sorted:\n",
                "    impact = \"Increases adherence\" if coef > 0 else \"Decreases adherence\"\n",
                "    print(f\"{feature:<30} {coef:>+10.4f}      {impact}\")\n",
                "\n",
                "print(\"=\"*70)\n",
                "print(\"\\nInterpretation:\")\n",
                "print(\"- Positive coefficients: Higher feature values increase predicted adherence\")\n",
                "print(\"- Negative coefficients: Higher feature values decrease predicted adherence\")\n",
                "print(\"- Larger absolute values indicate stronger influence on predictions\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Make predictions on both training and test sets\n",
                "print(\"\\nGenerating predictions...\")\n",
                "y_train_pred_lr = lr_model.predict(X_train)\n",
                "y_test_pred_lr = lr_model.predict(X_test)\n",
                "print(\"✅ Predictions complete\")\n",
                "\n",
                "print(f\"\\nPrediction Statistics:\")\n",
                "print(f\"  Training predictions - Min: {y_train_pred_lr.min():.2f}, Max: {y_train_pred_lr.max():.2f}, Mean: {y_train_pred_lr.mean():.2f}\")\n",
                "print(f\"  Test predictions     - Min: {y_test_pred_lr.min():.2f}, Max: {y_test_pred_lr.max():.2f}, Mean: {y_test_pred_lr.mean():.2f}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Calculate evaluation metrics for training set\n",
                "train_mse_lr = mean_squared_error(y_train, y_train_pred_lr)\n",
                "train_rmse_lr = np.sqrt(train_mse_lr)\n",
                "train_r2_lr = r2_score(y_train, y_train_pred_lr)\n",
                "\n",
                "# Calculate evaluation metrics for test set\n",
                "test_mse_lr = mean_squared_error(y_test, y_test_pred_lr)\n",
                "test_rmse_lr = np.sqrt(test_mse_lr)\n",
                "test_r2_lr = r2_score(y_test, y_test_pred_lr)\n",
                "\n",
                "print(\"\\n\" + \"=\"*70)\n",
                "print(\"LINEAR REGRESSION MODEL PERFORMANCE\")\n",
                "print(\"=\"*70)\n",
                "print(f\"\\n{'Metric':<25} {'Training Set':<20} {'Test Set':<20}\")\n",
                "print(\"-\"*70)\n",
                "print(f\"{'Mean Squared Error':<25} {train_mse_lr:>15.4f}     {test_mse_lr:>15.4f}\")\n",
                "print(f\"{'Root Mean Squared Error':<25} {train_rmse_lr:>15.4f}     {test_rmse_lr:>15.4f}\")\n",
                "print(f\"{'R-squared (R²)':<25} {train_r2_lr:>15.4f}     {test_r2_lr:>15.4f}\")\n",
                "print(\"=\"*70)\n",
                "\n",
                "print(\"\\nMetric Interpretations:\")\n",
                "print(f\"\\n1. Mean Squared Error (MSE): {test_mse_lr:.4f}\")\n",
                "print(\"   - Average squared difference between actual and predicted values\")\n",
                "print(\"   - Lower is better (0 = perfect predictions)\")\n",
                "print(f\"   - RMSE of {test_rmse_lr:.2f} means predictions are off by ~{test_rmse_lr:.1f} percentage points on average\")\n",
                "\n",
                "print(f\"\\n2. R-squared (R²): {test_r2_lr:.4f}\")\n",
                "print(f\"   - Proportion of variance in adherence rate explained by the model\")\n",
                "print(f\"   - Range: 0 to 1 (1 = perfect fit)\")\n",
                "print(f\"   - This model explains {test_r2_lr*100:.2f}% of the variance in adherence rates\")\n",
                "\n",
                "print(f\"\\n3. Overfitting Analysis:\")\n",
                "print(f\"   - Training R²: {train_r2_lr:.4f}\")\n",
                "print(f\"   - Test R²: {test_r2_lr:.4f}\")\n",
                "print(f\"   - Difference: {abs(train_r2_lr - test_r2_lr):.4f}\")\n",
                "if abs(train_r2_lr - test_r2_lr) < 0.05:\n",
                "    print(\"   - ✅ Minimal overfitting - model generalizes well\")\n",
                "elif abs(train_r2_lr - test_r2_lr) < 0.10:\n",
                "    print(\"   - ⚠️  Slight overfitting - acceptable for most applications\")\n",
                "else:\n",
                "    print(\"   - ❌ Significant overfitting - model may not generalize well\")\n",
                "\n",
                "print(f\"\\n4. Training Time: {training_time:.4f} seconds\")\n",
                "print(\"   - Linear Regression is very fast to train\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.1.1 Visualization: Actual vs Predicted Values"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Create scatter plot of actual vs predicted values with regression line\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))\n",
                "fig.suptitle('Linear Regression: Actual vs Predicted Adherence Rates', \n",
                "             fontsize=16, fontweight='bold', y=1.02)\n",
                "\n",
                "# Training set plot\n",
                "ax1.scatter(y_train, y_train_pred_lr, alpha=0.5, s=30, color='blue', edgecolors='black', linewidth=0.5)\n",
                "ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], \n",
                "         'r--', linewidth=2, label='Perfect Prediction Line')\n",
                "ax1.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
                "ax1.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
                "ax1.set_title(f'Training Set\\nR² = {train_r2_lr:.4f}, RMSE = {train_rmse_lr:.2f}', \n",
                "              fontsize=13, fontweight='bold')\n",
                "ax1.legend(fontsize=10)\n",
                "ax1.grid(alpha=0.3)\n",
                "ax1.set_xlim([0, 100])\n",
                "ax1.set_ylim([0, 100])\n",
                "\n",
                "# Test set plot\n",
                "ax2.scatter(y_test, y_test_pred_lr, alpha=0.5, s=30, color='green', edgecolors='black', linewidth=0.5)\n",
                "ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], \n",
                "         'r--', linewidth=2, label='Perfect Prediction Line')\n",
                "ax2.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
                "ax2.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
                "ax2.set_title(f'Test Set\\nR² = {test_r2_lr:.4f}, RMSE = {test_rmse_lr:.2f}', \n",
                "              fontsize=13, fontweight='bold')\n",
                "ax2.legend(fontsize=10)\n",
                "ax2.grid(alpha=0.3)\n",
                "ax2.set_xlim([0, 100])\n",
                "ax2.set_ylim([0, 100])\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('plots/lr_actual_vs_predicted.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()\n",
                "\n",
                "print(\"✅ Actual vs Predicted plot saved to: plots/lr_actual_vs_predicted.png\")\n",
                "print(\"\\nInterpretation:\")\n",
                "print(\"- Points close to the red line indicate accurate predictions\")\n",
                "print(\"- Scatter around the line shows prediction error\")\n",
                "print(\"- Similar patterns in training and test sets indicate good generalization\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.1.2 Visualization: Residual Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Calculate residuals (prediction errors)\n",
                "train_residuals_lr = y_train - y_train_pred_lr\n",
                "test_residuals_lr = y_test - y_test_pred_lr\n",
                "\n",
                "# Create residual plots\n",
                "fig, axes = plt.subplots(2, 2, figsize=(16, 12))\n",
                "fig.suptitle('Linear Regression: Residual Analysis', fontsize=16, fontweight='bold', y=1.00)\n",
                "\n",
                "# Plot 1: Residuals vs Predicted (Training)\n",
                "axes[0, 0].scatter(y_train_pred_lr, train_residuals_lr, alpha=0.5, s=20, color='blue')\n",
                "axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)\n",
                "axes[0, 0].set_xlabel('Predicted Adherence Rate (%)', fontsize=11)\n",
                "axes[0, 0].set_ylabel('Residuals (Actual - Predicted)', fontsize=11)\n",
                "axes[0, 0].set_title('Training Set: Residuals vs Predicted Values', fontsize=12, fontweight='bold')\n",
                "axes[0, 0].grid(alpha=0.3)\n",
                "\n",
                "# Plot 2: Residuals vs Predicted (Test)\n",
                "axes[0, 1].scatter(y_test_pred_lr, test_residuals_lr, alpha=0.5, s=20, color='green')\n",
                "axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)\n",
                "axes[0, 1].set_xlabel('Predicted Adherence Rate (%)', fontsize=11)\n",
                "axes[0, 1].set_ylabel('Residuals (Actual - Predicted)', fontsize=11)\n",
                "axes[0, 1].set_title('Test Set: Residuals vs Predicted Values', fontsize=12, fontweight='bold')\n",
                "axes[0, 1].grid(alpha=0.3)\n",
                "\n",
                "# Plot 3: Residual Distribution (Training)\n",
                "axes[1, 0].hist(train_residuals_lr, bins=30, color='blue', alpha=0.7, edgecolor='black')\n",
                "axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)\n",
                "axes[1, 0].set_xlabel('Residuals', fontsize=11)\n",
                "axes[1, 0].set_ylabel('Frequency', fontsize=11)\n",
                "axes[1, 0].set_title(f'Training Set: Residual Distribution\\nMean: {train_residuals_lr.mean():.4f}, Std: {train_residuals_lr.std():.4f}', \n",
                "                     fontsize=12, fontweight='bold')\n",
                "axes[1, 0].grid(axis='y', alpha=0.3)\n",
                "\n",
                "# Plot 4: Residual Distribution (Test)\n",
                "axes[1, 1].hist(test_residuals_lr, bins=30, color='green', alpha=0.7, edgecolor='black')\n",
                "axes[1, 1].axvline(x=0, color='red', linestyle='--', linewidth=2)\n",
                "axes[1, 1].set_xlabel('Residuals', fontsize=11)\n",
                "axes[1, 1].set_ylabel('Frequency', fontsize=11)\n",
                "axes[1, 1].set_title(f'Test Set: Residual Distribution\\nMean: {test_residuals_lr.mean():.4f}, Std: {test_residuals_lr.std():.4f}', \n",
                "                     fontsize=12, fontweight='bold')\n",
                "axes[1, 1].grid(axis='y', alpha=0.3)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('plots/lr_residuals.png', dpi=300, bbox_inches='tight')\n",
                "plt.show()\n",
                "\n",
                "print(\"✅ Residual analysis plot saved to: plots/lr_residuals.png\")\n",
                "print(\"\\nResidual Analysis Interpretation:\")\n",
                "print(\"\\n1. Residuals vs Predicted (Top Row):\")\n",
                "print(\"   - Ideally, residuals should be randomly scattered around zero\")\n",
                "print(\"   - Patterns indicate model bias or non-linear relationships\")\n",
                "print(\"   - Funnel shapes indicate heteroscedasticity (non-constant variance)\")\n",
                "\n",
                "print(\"\\n2. Residual Distribution (Bottom Row):\")\n",
                "print(\"   - Ideally, residuals should be normally distributed around zero\")\n",
                "print(\"   - Mean close to zero indicates unbiased predictions\")\n",
                "print(f\"   - Training residuals: Mean = {train_residuals_lr.mean():.4f}\")\n",
                "print(f\"   - Test residuals: Mean = {test_residuals_lr.mean():.4f}\")\n",
                "print(\"   - Similar distributions in train/test indicate good generalization\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5.1.3 Linear Regression Summary\n",
                "\n",
                "**Model Performance:**\n",
                "- The Linear Regression model has been successfully trained and evaluated\n",
                "- Performance metrics (MSE, RMSE, R²) calculated for both training and test sets\n",
                "- Visualizations created to assess prediction quality and residual patterns\n",
                "\n",
                "**Key Strengths:**\n",
                "- Fast training time (< 1 second)\n",
                "- Interpretable coefficients show feature importance\n",
                "- Simple baseline model for comparison\n",
                "\n",
                "**Potential Limitations:**\n",
                "- Assumes linear relationships between features and target\n",
                "- Cannot capture complex feature interactions\n",
                "- May underperform if relationships are non-linear\n",
                "\n",
                "**Next Steps:**\n",
                "- Train Decision Tree model (captures non-linear relationships)\n",
                "- Train Random Forest model (ensemble method for improved accuracy)\n",
                "- Compare all three models to select the best performer"
            ]
        }
    ]
    
    # Add the new cells to the notebook
    notebook['cells'].extend(new_cells)
    
    # Write the updated notebook back to file
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"✅ Successfully added Linear Regression cells to {notebook_path}")
    print(f"   Added {len(new_cells)} new cells")
    return True

if __name__ == "__main__":
    notebook_path = "multivariate.ipynb"
    try:
        success = add_linear_regression_cells(notebook_path)
        if success:
            print("\n✅ Linear Regression implementation complete!")
            print("   You can now run the notebook to train and evaluate the model.")
            sys.exit(0)
        else:
            print("\n❌ Failed to add cells")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
