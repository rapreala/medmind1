#!/usr/bin/env python3
"""
Script to add Random Forest model cells to the Jupyter notebook.
"""

import json

# Load the existing notebook
with open('multivariate.ipynb', 'r') as f:
    notebook = json.load(f)

# Random Forest cells to add
rf_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5.3 Random Forest Model\n",
            "\n",
            "Random Forest is an ensemble learning method that constructs multiple decision trees and combines their predictions for improved accuracy and robustness.\n",
            "\n",
            "**How Random Forest Works:**\n",
            "1. Create multiple decision trees (100-300 trees)\n",
            "2. Each tree is trained on a random subset of data (bootstrap sampling)\n",
            "3. Each tree considers only a random subset of features at each split\n",
            "4. Final prediction is the average of all tree predictions\n",
            "5. This \"wisdom of crowds\" approach reduces overfitting\n",
            "\n",
            "**Advantages:**\n",
            "- Highly accurate and robust\n",
            "- Reduces overfitting compared to single decision trees\n",
            "- Handles non-linear relationships and feature interactions\n",
            "- Provides feature importance scores\n",
            "- Works well with high-dimensional data\n",
            "- Less sensitive to hyperparameters than single trees\n",
            "\n",
            "**Limitations:**\n",
            "- Slower training and prediction than single models\n",
            "- Less interpretable than linear regression or single trees\n",
            "- Requires more memory (stores multiple trees)\n",
            "- Can be overkill for simple linear relationships\n",
            "\n",
            "**Hyperparameters to Tune:**\n",
            "- `n_estimators`: Number of trees in the forest (more trees = better performance but slower)\n",
            "- `max_depth`: Maximum depth of each tree\n",
            "- `min_samples_split`: Minimum samples required to split a node\n",
            "- `min_samples_leaf`: Minimum samples required at leaf nodes"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Import RandomForestRegressor from scikit-learn\n",
            "from sklearn.ensemble import RandomForestRegressor\n",
            "\n",
            "print(\"=\"*70)\n",
            "print(\"RANDOM FOREST MODEL TRAINING\")\n",
            "print(\"=\"*70)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Define hyperparameter grid for Random Forest tuning\n",
            "print(\"\\nSetting up hyperparameter grid for Random Forest...\")\n",
            "\n",
            "rf_param_grid = {\n",
            "    'n_estimators': [100, 200, 300],\n",
            "    'max_depth': [10, 15, 20, None],\n",
            "    'min_samples_split': [2, 5, 10],\n",
            "    'min_samples_leaf': [1, 2, 4]\n",
            "}\n",
            "\n",
            "total_rf_combinations = (len(rf_param_grid['n_estimators']) * \n",
            "                         len(rf_param_grid['max_depth']) * \n",
            "                         len(rf_param_grid['min_samples_split']) * \n",
            "                         len(rf_param_grid['min_samples_leaf']))\n",
            "\n",
            "print(f\"✅ Grid defined: {total_rf_combinations} combinations to test\")\n",
            "print(f\"\\nHyperparameters to tune:\")\n",
            "print(f\"  - n_estimators: {rf_param_grid['n_estimators']}\")\n",
            "print(f\"  - max_depth: {rf_param_grid['max_depth']}\")\n",
            "print(f\"  - min_samples_split: {rf_param_grid['min_samples_split']}\")\n",
            "print(f\"  - min_samples_leaf: {rf_param_grid['min_samples_leaf']}\")\n",
            "print(f\"\\nNote: This will take 2-5 minutes due to the large search space...\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Initialize Random Forest and perform hyperparameter tuning\n",
            "print(\"\\nPerforming hyperparameter tuning with 5-fold cross-validation...\")\n",
            "\n",
            "rf_base = RandomForestRegressor(random_state=42, n_jobs=-1)\n",
            "rf_grid_search = GridSearchCV(\n",
            "    estimator=rf_base,\n",
            "    param_grid=rf_param_grid,\n",
            "    cv=5,\n",
            "    scoring='neg_mean_squared_error',\n",
            "    n_jobs=-1,\n",
            "    verbose=1\n",
            ")\n",
            "\n",
            "rf_start_time = time.time()\n",
            "rf_grid_search.fit(X_train, y_train)\n",
            "rf_tuning_time = time.time() - rf_start_time\n",
            "\n",
            "print(f\"\\n✅ Hyperparameter tuning complete in {rf_tuning_time:.2f} seconds\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Get the best Random Forest model\n",
            "rf_model = rf_grid_search.best_estimator_\n",
            "rf_best_params = rf_grid_search.best_params_\n",
            "rf_best_cv_mse = -rf_grid_search.best_score_\n",
            "rf_best_cv_rmse = np.sqrt(rf_best_cv_mse)\n",
            "\n",
            "print(\"\\n\" + \"=\"*70)\n",
            "print(\"BEST HYPERPARAMETERS FOUND\")\n",
            "print(\"=\"*70)\n",
            "print(f\"\\nBest parameters:\")\n",
            "for param, value in rf_best_params.items():\n",
            "    print(f\"  - {param}: {value}\")\n",
            "\n",
            "print(f\"\\nCross-validation performance:\")\n",
            "print(f\"  - Best CV MSE: {rf_best_cv_mse:.4f}\")\n",
            "print(f\"  - Best CV RMSE: {rf_best_cv_rmse:.4f}\")\n",
            "\n",
            "print(f\"\\nBest model configuration:\")\n",
            "print(f\"  - Number of trees: {rf_model.n_estimators}\")\n",
            "print(f\"  - Max depth: {rf_model.max_depth}\")\n",
            "print(f\"  - Min samples split: {rf_model.min_samples_split}\")\n",
            "print(f\"  - Min samples leaf: {rf_model.min_samples_leaf}\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Make predictions with Random Forest\n",
            "print(\"\\nGenerating predictions...\")\n",
            "y_train_pred_rf = rf_model.predict(X_train)\n",
            "y_test_pred_rf = rf_model.predict(X_test)\n",
            "print(\"✅ Predictions complete\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate evaluation metrics for Random Forest\n",
            "train_mse_rf = mean_squared_error(y_train, y_train_pred_rf)\n",
            "train_rmse_rf = np.sqrt(train_mse_rf)\n",
            "train_r2_rf = r2_score(y_train, y_train_pred_rf)\n",
            "\n",
            "test_mse_rf = mean_squared_error(y_test, y_test_pred_rf)\n",
            "test_rmse_rf = np.sqrt(test_mse_rf)\n",
            "test_r2_rf = r2_score(y_test, y_test_pred_rf)\n",
            "\n",
            "print(\"\\n\" + \"=\"*70)\n",
            "print(\"RANDOM FOREST MODEL PERFORMANCE\")\n",
            "print(\"=\"*70)\n",
            "print(f\"\\n{'Metric':<25} {'Training Set':<20} {'Test Set':<20}\")\n",
            "print(\"-\"*70)\n",
            "print(f\"{'Mean Squared Error':<25} {train_mse_rf:>15.4f}     {test_mse_rf:>15.4f}\")\n",
            "print(f\"{'Root Mean Squared Error':<25} {train_rmse_rf:>15.4f}     {test_rmse_rf:>15.4f}\")\n",
            "print(f\"{'R-squared (R²)':<25} {train_r2_rf:>15.4f}     {test_r2_rf:>15.4f}\")\n",
            "print(\"=\"*70)\n",
            "\n",
            "print(\"\\nMetric Interpretations:\")\n",
            "print(f\"\\n1. Mean Squared Error (MSE): {test_mse_rf:.4f}\")\n",
            "print(\"   - Average squared difference between actual and predicted values\")\n",
            "print(\"   - Lower is better (0 = perfect predictions)\")\n",
            "print(f\"   - RMSE of {test_rmse_rf:.2f} means predictions are off by ~{test_rmse_rf:.1f} percentage points on average\")\n",
            "\n",
            "print(f\"\\n2. R-squared (R²): {test_r2_rf:.4f}\")\n",
            "print(f\"   - Proportion of variance in adherence rate explained by the model\")\n",
            "print(f\"   - Range: 0 to 1 (1 = perfect fit)\")\n",
            "print(f\"   - This model explains {test_r2_rf*100:.2f}% of the variance in adherence rates\")\n",
            "\n",
            "print(f\"\\n3. Overfitting Analysis:\")\n",
            "print(f\"   - Training R²: {train_r2_rf:.4f}\")\n",
            "print(f\"   - Test R²: {test_r2_rf:.4f}\")\n",
            "print(f\"   - Difference: {abs(train_r2_rf - test_r2_rf):.4f}\")\n",
            "if abs(train_r2_rf - test_r2_rf) < 0.05:\n",
            "    print(\"   - ✅ Minimal overfitting - model generalizes excellently\")\n",
            "elif abs(train_r2_rf - test_r2_rf) < 0.10:\n",
            "    print(\"   - ⚠️  Slight overfitting - acceptable for most applications\")\n",
            "else:\n",
            "    print(\"   - ⚠️  Significant overfitting detected\")\n",
            "\n",
            "print(f\"\\n4. Training Time: {rf_tuning_time:.2f} seconds\")\n",
            "print(\"   - Random Forest takes longer to train but often provides better accuracy\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5.3.1 Random Forest Feature Importance"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Extract and display feature importance\n",
            "feature_importance_rf = rf_model.feature_importances_\n",
            "\n",
            "# Create DataFrame for better visualization\n",
            "rf_importance_df = pd.DataFrame({\n",
            "    'Feature': feature_cols,\n",
            "    'Importance': feature_importance_rf\n",
            "}).sort_values('Importance', ascending=False)\n",
            "\n",
            "print(\"\\n\" + \"=\"*70)\n",
            "print(\"RANDOM FOREST FEATURE IMPORTANCE\")\n",
            "print(\"=\"*70)\n",
            "print(f\"\\n{'Rank':<6} {'Feature':<30} {'Importance':<15} {'Percentage'}\")\n",
            "print(\"-\"*70)\n",
            "\n",
            "for idx, (_, row) in enumerate(rf_importance_df.iterrows(), 1):\n",
            "    print(f\"{idx:<6} {row['Feature']:<30} {row['Importance']:>10.4f}      {row['Importance']*100:>6.2f}%\")\n",
            "\n",
            "print(\"=\"*70)\n",
            "print(f\"\\nTop 3 features account for {rf_importance_df.head(3)['Importance'].sum()*100:.1f}% of total importance\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Visualize Random Forest feature importance\n",
            "plt.figure(figsize=(12, 8))\n",
            "bars = plt.barh(rf_importance_df['Feature'], rf_importance_df['Importance'], \n",
            "                color='forestgreen', edgecolor='black')\n",
            "\n",
            "# Color the top 3 features differently\n",
            "for i in range(min(3, len(bars))):\n",
            "    bars[i].set_color('coral')\n",
            "\n",
            "plt.xlabel('Feature Importance Score', fontsize=12, fontweight='bold')\n",
            "plt.ylabel('Features', fontsize=12, fontweight='bold')\n",
            "plt.title('Random Forest: Feature Importance Scores\\n(Higher = More Important for Predictions)', \n",
            "          fontsize=14, fontweight='bold', pad=20)\n",
            "plt.gca().invert_yaxis()  # Highest importance at top\n",
            "plt.grid(axis='x', alpha=0.3)\n",
            "\n",
            "# Add value labels on bars\n",
            "for i, (_, row) in enumerate(rf_importance_df.iterrows()):\n",
            "    plt.text(row['Importance'] + 0.005, i, f\"{row['Importance']:.4f}\", \n",
            "             va='center', fontsize=10, fontweight='bold')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('plots/rf_feature_importance.png', dpi=300, bbox_inches='tight')\n",
            "plt.show()\n",
            "\n",
            "print(\"✅ Feature importance plot saved: plots/rf_feature_importance.png\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5.3.2 Random Forest Visualization: Actual vs Predicted"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create scatter plot of actual vs predicted values for Random Forest\n",
            "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))\n",
            "fig.suptitle('Random Forest: Actual vs Predicted Adherence Rates', \n",
            "             fontsize=16, fontweight='bold', y=1.02)\n",
            "\n",
            "# Training set plot\n",
            "ax1.scatter(y_train, y_train_pred_rf, alpha=0.5, s=30, color='darkgreen', \n",
            "            edgecolors='black', linewidth=0.5)\n",
            "ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], \n",
            "         'r--', linewidth=2, label='Perfect Prediction Line')\n",
            "ax1.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
            "ax1.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
            "ax1.set_title(f'Training Set\\nR² = {train_r2_rf:.4f}, RMSE = {train_rmse_rf:.2f}', \n",
            "              fontsize=13, fontweight='bold')\n",
            "ax1.legend(fontsize=10)\n",
            "ax1.grid(alpha=0.3)\n",
            "ax1.set_xlim([0, 100])\n",
            "ax1.set_ylim([0, 100])\n",
            "\n",
            "# Test set plot\n",
            "ax2.scatter(y_test, y_test_pred_rf, alpha=0.5, s=30, color='lime', \n",
            "            edgecolors='black', linewidth=0.5)\n",
            "ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], \n",
            "         'r--', linewidth=2, label='Perfect Prediction Line')\n",
            "ax2.set_xlabel('Actual Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
            "ax2.set_ylabel('Predicted Adherence Rate (%)', fontsize=12, fontweight='bold')\n",
            "ax2.set_title(f'Test Set\\nR² = {test_r2_rf:.4f}, RMSE = {test_rmse_rf:.2f}', \n",
            "              fontsize=13, fontweight='bold')\n",
            "ax2.legend(fontsize=10)\n",
            "ax2.grid(alpha=0.3)\n",
            "ax2.set_xlim([0, 100])\n",
            "ax2.set_ylim([0, 100])\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('plots/rf_actual_vs_predicted.png', dpi=300, bbox_inches='tight')\n",
            "plt.show()\n",
            "\n",
            "print(\"✅ Actual vs Predicted plot saved: plots/rf_actual_vs_predicted.png\")\n",
            "print(\"\\nInterpretation:\")\n",
            "print(\"- Points close to the red line indicate accurate predictions\")\n",
            "print(\"- Random Forest typically shows tighter clustering around the line than Linear Regression\")\n",
            "print(\"- Similar patterns in training and test sets indicate good generalization\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5.3.3 Random Forest Summary\n",
            "\n",
            "**Model Performance:**\n",
            "- The Random Forest model has been successfully trained with hyperparameter tuning\n",
            "- Ensemble of multiple decision trees provides robust predictions\n",
            "- Performance metrics calculated for both training and test sets\n",
            "\n",
            "**Key Strengths:**\n",
            "- Captures non-linear relationships and feature interactions\n",
            "- Reduces overfitting through ensemble averaging\n",
            "- Provides reliable feature importance scores\n",
            "- Generally achieves best performance among the three models\n",
            "\n",
            "**Considerations:**\n",
            "- Longer training time due to multiple trees and hyperparameter tuning\n",
            "- Less interpretable than Linear Regression\n",
            "- Requires more memory to store multiple trees\n",
            "\n",
            "**Next Steps:**\n",
            "- Compare all three models (Linear Regression, Decision Tree, Random Forest)\n",
            "- Select the best-performing model based on test set MSE\n",
            "- Save the best model for deployment"
        ]
    }
]

print("Adding Random Forest cells to notebook...")
print(f"Current notebook has {len(notebook['cells'])} cells")

# Add the cells to the notebook
notebook['cells'].extend(rf_cells)

# Save the updated notebook
with open('multivariate.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"✅ Random Forest section added to notebook successfully!")
print(f"   Notebook now has {len(notebook['cells'])} cells")
print("   Note: Run the notebook or use run_random_forest.py to execute the training")
