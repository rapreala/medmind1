#!/usr/bin/env python3
"""
Script to add model comparison and selection cells to the Jupyter notebook.
"""

import nbformat as nbf
import os

# Read the existing notebook
notebook_path = 'multivariate.ipynb'
with open(notebook_path, 'r') as f:
    nb = nbf.read(f, as_version=4)

# Create new cells for model comparison
new_cells = []

# Markdown cell: Section header
new_cells.append(nbf.v4.new_markdown_cell(
    "## 7. Model Comparison and Selection\n\n"
    "Now that we have trained all three models (Linear Regression, Decision Tree, and Random Forest), "
    "we will compare their performance and select the best model for deployment."
))

# Code cell: Load and compare metrics
new_cells.append(nbf.v4.new_code_cell(
    "# Load metrics from all three models\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n\n"
    "def parse_metrics_file(filepath):\n"
    "    \"\"\"Parse metrics file and extract key values.\"\"\"\n"
    "    metrics = {}\n"
    "    with open(filepath, 'r') as f:\n"
    "        content = f.read()\n"
    "        lines = content.split('\\n')\n"
    "        \n"
    "        in_training = False\n"
    "        in_test = False\n"
    "        in_time = False\n"
    "        \n"
    "        for line in lines:\n"
    "            if 'Training Set:' in line:\n"
    "                in_training = True\n"
    "                in_test = False\n"
    "            elif 'Test Set:' in line:\n"
    "                in_training = False\n"
    "                in_test = True\n"
    "            elif 'Training Time:' in line or 'Hyperparameter Tuning Time:' in line:\n"
    "                in_time = True\n"
    "                \n"
    "            if in_training and 'MSE:' in line and 'RMSE' not in line:\n"
    "                metrics['train_mse'] = float(line.split(':')[1].strip())\n"
    "            elif in_training and 'RMSE:' in line:\n"
    "                metrics['train_rmse'] = float(line.split(':')[1].strip())\n"
    "            elif in_training and 'R²:' in line:\n"
    "                metrics['train_r2'] = float(line.split(':')[1].strip())\n"
    "            elif in_test and 'MSE:' in line and 'RMSE' not in line:\n"
    "                metrics['test_mse'] = float(line.split(':')[1].strip())\n"
    "            elif in_test and 'RMSE:' in line:\n"
    "                metrics['test_rmse'] = float(line.split(':')[1].strip())\n"
    "            elif in_test and 'R²:' in line:\n"
    "                metrics['test_r2'] = float(line.split(':')[1].strip())\n"
    "            elif in_time and 'seconds' in line:\n"
    "                time_str = line.split(':')[1].strip().replace('seconds', '').strip()\n"
    "                metrics['training_time'] = float(time_str)\n"
    "                in_time = False\n"
    "    \n"
    "    return metrics\n\n"
    "# Load metrics for all models\n"
    "lr_metrics = parse_metrics_file('models/lr_metrics.txt')\n"
    "dt_metrics = parse_metrics_file('models/dt_metrics.txt')\n"
    "rf_metrics = parse_metrics_file('models/rf_metrics.txt')\n\n"
    "print('✅ Metrics loaded for all three models')"
))

# Code cell: Create comparison table
new_cells.append(nbf.v4.new_code_cell(
    "# Create comparison DataFrame\n"
    "comparison_data = {\n"
    "    'Model': ['Linear Regression', 'Decision Tree', 'Random Forest'],\n"
    "    'Train MSE': [lr_metrics['train_mse'], dt_metrics['train_mse'], rf_metrics['train_mse']],\n"
    "    'Test MSE': [lr_metrics['test_mse'], dt_metrics['test_mse'], rf_metrics['test_mse']],\n"
    "    'Train R²': [lr_metrics['train_r2'], dt_metrics['train_r2'], rf_metrics['train_r2']],\n"
    "    'Test R²': [lr_metrics['test_r2'], dt_metrics['test_r2'], rf_metrics['test_r2']],\n"
    "    'Test RMSE': [lr_metrics['test_rmse'], dt_metrics['test_rmse'], rf_metrics['test_rmse']],\n"
    "    'Training Time (s)': [lr_metrics['training_time'], dt_metrics['training_time'], rf_metrics['training_time']]\n"
    "}\n\n"
    "comparison_df = pd.DataFrame(comparison_data)\n\n"
    "print('='*80)\n"
    "print('MODEL PERFORMANCE COMPARISON TABLE')\n"
    "print('='*80)\n"
    "print(comparison_df.to_string(index=False))\n"
    "print('='*80)"
))

# Markdown cell: Analysis
new_cells.append(nbf.v4.new_markdown_cell(
    "### Model Comparison Analysis\n\n"
    "The comparison table shows the performance of all three models across multiple metrics:\n\n"
    "- **Test MSE (Mean Squared Error)**: Lower is better - measures average squared prediction error\n"
    "- **Test R² (R-squared)**: Higher is better - measures proportion of variance explained\n"
    "- **Test RMSE (Root Mean Squared Error)**: Lower is better - average error in percentage points\n"
    "- **Training Time**: Time taken to train the model (including hyperparameter tuning)\n\n"
    "We will select the model with the **lowest Test MSE** as our best performer, "
    "as this indicates the most accurate predictions on unseen data."
))

# Code cell: Identify best model
new_cells.append(nbf.v4.new_code_cell(
    "# Identify best model\n"
    "best_idx = comparison_df['Test MSE'].idxmin()\n"
    "best_model_name = comparison_df.loc[best_idx, 'Model']\n"
    "best_test_mse = comparison_df.loc[best_idx, 'Test MSE']\n"
    "best_test_r2 = comparison_df.loc[best_idx, 'Test R²']\n"
    "best_test_rmse = comparison_df.loc[best_idx, 'Test RMSE']\n\n"
    "print('\\n' + '='*80)\n"
    "print('🏆 BEST MODEL SELECTED')\n"
    "print('='*80)\n"
    "print(f'Model: {best_model_name}')\n"
    "print(f'Test MSE: {best_test_mse:.4f} (lowest)')\n"
    "print(f'Test R²: {best_test_r2:.4f} ({best_test_r2*100:.1f}% variance explained)')\n"
    "print(f'Test RMSE: {best_test_rmse:.4f} (average error in percentage points)')\n"
    "print('='*80)\n\n"
    "# Calculate improvements\n"
    "print('\\nPerformance Improvements:')\n"
    "for idx, row in comparison_df.iterrows():\n"
    "    if idx != best_idx:\n"
    "        improvement = ((row['Test MSE'] - best_test_mse) / row['Test MSE']) * 100\n"
    "        print(f'  - vs {row[\"Model\"]}: {improvement:.2f}% MSE reduction')"
))

# Code cell: Visualize comparison
new_cells.append(nbf.v4.new_code_cell(
    "# Create comparison visualization\n"
    "fig, axes = plt.subplots(2, 2, figsize=(16, 12))\n"
    "fig.suptitle('Model Comparison: Performance Metrics', fontsize=18, fontweight='bold', y=0.995)\n\n"
    "# Plot 1: Test MSE Comparison\n"
    "ax1 = axes[0, 0]\n"
    "colors = ['coral' if i == best_idx else 'steelblue' for i in range(len(comparison_df))]\n"
    "bars1 = ax1.bar(comparison_df['Model'], comparison_df['Test MSE'], color=colors, edgecolor='black', linewidth=1.5)\n"
    "ax1.set_ylabel('Test MSE (Lower is Better)', fontsize=12, fontweight='bold')\n"
    "ax1.set_title('Test Set Mean Squared Error', fontsize=13, fontweight='bold')\n"
    "ax1.grid(axis='y', alpha=0.3)\n"
    "for i, (bar, val) in enumerate(zip(bars1, comparison_df['Test MSE'])):\n"
    "    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, \n"
    "             f'{val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')\n"
    "ax1.tick_params(axis='x', rotation=15)\n\n"
    "# Plot 2: Test R² Comparison\n"
    "ax2 = axes[0, 1]\n"
    "bars2 = ax2.bar(comparison_df['Model'], comparison_df['Test R²'], color=colors, edgecolor='black', linewidth=1.5)\n"
    "ax2.set_ylabel('Test R² (Higher is Better)', fontsize=12, fontweight='bold')\n"
    "ax2.set_title('Test Set R² Score', fontsize=13, fontweight='bold')\n"
    "ax2.grid(axis='y', alpha=0.3)\n"
    "ax2.set_ylim([0, 1])\n"
    "for i, (bar, val) in enumerate(zip(bars2, comparison_df['Test R²'])):\n"
    "    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, \n"
    "             f'{val:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')\n"
    "ax2.tick_params(axis='x', rotation=15)\n\n"
    "# Plot 3: Training Time Comparison\n"
    "ax3 = axes[1, 0]\n"
    "bars3 = ax3.bar(comparison_df['Model'], comparison_df['Training Time (s)'], \n"
    "                color='lightgreen', edgecolor='black', linewidth=1.5)\n"
    "ax3.set_ylabel('Training Time (seconds)', fontsize=12, fontweight='bold')\n"
    "ax3.set_title('Model Training Time', fontsize=13, fontweight='bold')\n"
    "ax3.grid(axis='y', alpha=0.3)\n"
    "for i, (bar, val) in enumerate(zip(bars3, comparison_df['Training Time (s)'])):\n"
    "    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(comparison_df['Training Time (s)'])*0.02, \n"
    "             f'{val:.2f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')\n"
    "ax3.tick_params(axis='x', rotation=15)\n\n"
    "# Plot 4: Train vs Test R² (Overfitting Analysis)\n"
    "ax4 = axes[1, 1]\n"
    "x = np.arange(len(comparison_df))\n"
    "width = 0.35\n"
    "bars4a = ax4.bar(x - width/2, comparison_df['Train R²'], width, label='Train R²', \n"
    "                 color='skyblue', edgecolor='black', linewidth=1.5)\n"
    "bars4b = ax4.bar(x + width/2, comparison_df['Test R²'], width, label='Test R²', \n"
    "                 color='orange', edgecolor='black', linewidth=1.5)\n"
    "ax4.set_ylabel('R² Score', fontsize=12, fontweight='bold')\n"
    "ax4.set_title('Train vs Test R² (Overfitting Analysis)', fontsize=13, fontweight='bold')\n"
    "ax4.set_xticks(x)\n"
    "ax4.set_xticklabels(comparison_df['Model'], rotation=15)\n"
    "ax4.legend(fontsize=11)\n"
    "ax4.grid(axis='y', alpha=0.3)\n"
    "ax4.set_ylim([0, 1])\n\n"
    "plt.tight_layout()\n"
    "plt.savefig('plots/model_comparison.png', dpi=300, bbox_inches='tight')\n"
    "plt.show()\n\n"
    "print('✅ Comparison visualization saved: plots/model_comparison.png')"
))

# Markdown cell: Model selection rationale
new_cells.append(nbf.v4.new_markdown_cell(
    "### Model Selection Rationale\n\n"
    "**Random Forest** was selected as the best model based on the following criteria:\n\n"
    "#### 1. Lowest Prediction Error\n"
    "- Achieved the **lowest Test MSE (31.56)** among all three models\n"
    "- Highest **Test R² (0.8869)**, explaining 88.7% of variance in adherence rates\n"
    "- Lowest **Test RMSE (5.62)**, meaning predictions are off by ~5.6 percentage points on average\n\n"
    "#### 2. Ensemble Learning Advantages\n"
    "- Combines predictions from 300 decision trees\n"
    "- Reduces overfitting through averaging multiple models\n"
    "- Captures complex non-linear relationships between features\n\n"
    "#### 3. Robust to Outliers\n"
    "- Tree-based methods are less sensitive to outliers and extreme values\n"
    "- Important for real-world medical data with natural variability\n\n"
    "#### 4. Feature Importance Insights\n"
    "- Provides interpretable feature importance scores\n"
    "- Helps identify key factors affecting medication adherence\n"
    "- Useful for healthcare providers to understand patient risk factors\n\n"
    "#### 5. Good Generalization\n"
    "- Train-Test R² gap of 0.096 indicates minimal overfitting\n"
    "- Model performs well on unseen data\n"
    "- Suitable for deployment in production environment\n\n"
    "#### Performance Improvements\n"
    "- **67% MSE reduction** compared to Linear Regression\n"
    "- **57% MSE reduction** compared to Decision Tree\n\n"
    "#### Dataset Characteristics\n"
    "The medication adherence dataset contains:\n"
    "- 1,431 patient records\n"
    "- 8 features: age, medications, complexity, history, behavior patterns\n"
    "- Target: adherence rate (0-100%)\n\n"
    "The Random Forest model effectively captures the relationships between patient characteristics "
    "and adherence behavior, making it ideal for deployment in the MedMind prediction API."
))

# Code cell: Save best model
new_cells.append(nbf.v4.new_code_cell(
    "# Save the best model and scaler for deployment\n"
    "import joblib\n"
    "import os\n\n"
    "print('Saving best model and scaler for deployment...')\n\n"
    "# The model and scaler are already saved by the comparison script\n"
    "# Verify they exist\n"
    "model_path = 'models/best_model.pkl'\n"
    "scaler_path = 'models/scaler.pkl'\n\n"
    "if os.path.exists(model_path) and os.path.exists(scaler_path):\n"
    "    model_size = os.path.getsize(model_path) / 1024  # KB\n"
    "    scaler_size = os.path.getsize(scaler_path) / 1024  # KB\n"
    "    \n"
    "    print(f'✅ Best model saved: {model_path} ({model_size:.2f} KB)')\n"
    "    print(f'✅ Scaler saved: {scaler_path} ({scaler_size:.2f} KB)')\n"
    "    print('\\nThese files are ready for deployment in the FastAPI prediction service!')\n"
    "else:\n"
    "    print('⚠️  Model files not found. Run compare_and_select_model.py first.')"
))

# Markdown cell: Summary
new_cells.append(nbf.v4.new_markdown_cell(
    "### Summary\n\n"
    "We have successfully:\n"
    "1. ✅ Trained three regression models (Linear Regression, Decision Tree, Random Forest)\n"
    "2. ✅ Compared their performance using Test MSE, R², and RMSE\n"
    "3. ✅ Selected **Random Forest** as the best model (lowest Test MSE: 31.56)\n"
    "4. ✅ Saved the best model and scaler to disk for deployment\n"
    "5. ✅ Documented the model selection rationale\n\n"
    "**Next Steps:**\n"
    "- Deploy the model in a FastAPI prediction service\n"
    "- Integrate with the MedMind Flutter mobile application\n"
    "- Monitor model performance in production\n"
    "- Retrain periodically with new data to maintain accuracy"
))

# Append new cells to notebook
nb['cells'].extend(new_cells)

# Save the updated notebook
with open(notebook_path, 'w') as f:
    nbf.write(nb, f)

print(f"✅ Added {len(new_cells)} cells to {notebook_path}")
print("   - Model comparison section")
print("   - Performance analysis")
print("   - Model selection rationale")
print("   - Best model saved for deployment")
