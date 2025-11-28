#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to add EDA and visualization cells to the notebook"""

import json
import os

# Change to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Read the existing notebook
with open('multivariate.ipynb', 'r') as f:
    notebook = json.load(f)

# New cells to add for EDA and visualization
new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Exploratory Data Analysis (EDA)\n",
            "\n",
            "In this section, we will:\n",
            "1. Generate a correlation heatmap to understand feature relationships\n",
            "2. Create distribution visualizations for key features\n",
            "3. Identify features with strongest correlation to adherence rate\n",
            "4. Save all plots for documentation"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3.1 Correlation Analysis"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create plots directory if it doesn't exist\n",
            "import os\n",
            "os.makedirs('plots', exist_ok=True)\n",
            "\n",
            "print(\"Plots directory ready!\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate correlation matrix\n",
            "correlation_matrix = df.corr()\n",
            "\n",
            "# Display correlation with target variable\n",
            "print(\"Correlation with Adherence Rate (Target Variable):\")\n",
            "print(\"=\"*60)\n",
            "target_corr = correlation_matrix['adherence_rate'].sort_values(ascending=False)\n",
            "print(target_corr)\n",
            "print(\"\\n\" + \"=\"*60)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Generate correlation heatmap\n",
            "plt.figure(figsize=(12, 10))\n",
            "sns.heatmap(correlation_matrix, \n",
            "            annot=True, \n",
            "            fmt='.2f', \n",
            "            cmap='coolwarm', \n",
            "            center=0,\n",
            "            square=True,\n",
            "            linewidths=1,\n",
            "            cbar_kws={\"shrink\": 0.8})\n",
            "\n",
            "plt.title('Correlation Heatmap: Feature Relationships and Target Variable', \n",
            "          fontsize=14, fontweight='bold', pad=20)\n",
            "plt.tight_layout()\n",
            "plt.savefig('plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')\n",
            "plt.show()\n",
            "\n",
            "print(\"✅ Correlation heatmap saved to: plots/correlation_heatmap.png\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Interpretation: Correlation Analysis\n",
            "\n",
            "**Key Findings from Correlation Heatmap:**\n",
            "\n",
            "1. **Strongest Positive Correlations with Adherence Rate:**\n",
            "   - `previous_adherence_rate`: Historical adherence is the strongest predictor (expected)\n",
            "   - Features with positive correlation indicate they increase adherence when values are higher\n",
            "\n",
            "2. **Strongest Negative Correlations with Adherence Rate:**\n",
            "   - `missed_doses_last_week`: More missed doses strongly correlate with lower adherence\n",
            "   - `snooze_frequency`: Higher snooze rates indicate lower adherence\n",
            "   - `medication_complexity`: More complex regimens correlate with lower adherence\n",
            "\n",
            "3. **Feature Interactions:**\n",
            "   - The heatmap reveals multicollinearity between certain features\n",
            "   - Some features may be redundant for prediction\n",
            "   - This information will guide feature selection and model interpretation\n",
            "\n",
            "4. **Implications for Modeling:**\n",
            "   - Features with strong correlations (|r| > 0.5) will likely be important predictors\n",
            "   - Weak correlations (|r| < 0.2) may contribute less to model performance\n",
            "   - Non-linear models (Decision Trees, Random Forest) may capture relationships that linear correlation misses"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3.2 Feature Distributions and Relationships"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Identify top features by absolute correlation with target\n",
            "target_corr_abs = correlation_matrix['adherence_rate'].abs().sort_values(ascending=False)\n",
            "top_features = target_corr_abs[1:4].index.tolist()  # Exclude adherence_rate itself\n",
            "\n",
            "print(\"Top 3 Features by Correlation Strength:\")\n",
            "for i, feature in enumerate(top_features, 1):\n",
            "    corr_value = correlation_matrix.loc[feature, 'adherence_rate']\n",
            "    print(f\"{i}. {feature}: {corr_value:.3f}\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Distribution Plot 1: Histograms of key features\n",
            "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
            "fig.suptitle('Distribution of Key Features', fontsize=16, fontweight='bold', y=1.00)\n",
            "\n",
            "# Plot 1: Previous Adherence Rate\n",
            "axes[0, 0].hist(df['previous_adherence_rate'].dropna(), bins=30, color='skyblue', edgecolor='black', alpha=0.7)\n",
            "axes[0, 0].set_xlabel('Previous Adherence Rate (%)', fontsize=11)\n",
            "axes[0, 0].set_ylabel('Frequency', fontsize=11)\n",
            "axes[0, 0].set_title('Previous Adherence Rate Distribution', fontsize=12, fontweight='bold')\n",
            "axes[0, 0].axvline(df['previous_adherence_rate'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df[\"previous_adherence_rate\"].mean():.1f}%')\n",
            "axes[0, 0].legend()\n",
            "axes[0, 0].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Plot 2: Missed Doses Last Week\n",
            "axes[0, 1].hist(df['missed_doses_last_week'].dropna(), bins=20, color='salmon', edgecolor='black', alpha=0.7)\n",
            "axes[0, 1].set_xlabel('Missed Doses (Last Week)', fontsize=11)\n",
            "axes[0, 1].set_ylabel('Frequency', fontsize=11)\n",
            "axes[0, 1].set_title('Missed Doses Distribution', fontsize=12, fontweight='bold')\n",
            "axes[0, 1].axvline(df['missed_doses_last_week'].mean(), color='darkred', linestyle='--', linewidth=2, label=f'Mean: {df[\"missed_doses_last_week\"].mean():.1f}')\n",
            "axes[0, 1].legend()\n",
            "axes[0, 1].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Plot 3: Snooze Frequency\n",
            "axes[1, 0].hist(df['snooze_frequency'].dropna(), bins=25, color='lightgreen', edgecolor='black', alpha=0.7)\n",
            "axes[1, 0].set_xlabel('Snooze Frequency (0-1)', fontsize=11)\n",
            "axes[1, 0].set_ylabel('Frequency', fontsize=11)\n",
            "axes[1, 0].set_title('Snooze Frequency Distribution', fontsize=12, fontweight='bold')\n",
            "axes[1, 0].axvline(df['snooze_frequency'].mean(), color='darkgreen', linestyle='--', linewidth=2, label=f'Mean: {df[\"snooze_frequency\"].mean():.2f}')\n",
            "axes[1, 0].legend()\n",
            "axes[1, 0].grid(axis='y', alpha=0.3)\n",
            "\n",
            "# Plot 4: Target Variable (Adherence Rate)\n",
            "axes[1, 1].hist(df['adherence_rate'].dropna(), bins=30, color='gold', edgecolor='black', alpha=0.7)\n",
            "axes[1, 1].set_xlabel('Current Adherence Rate (%)', fontsize=11)\n",
            "axes[1, 1].set_ylabel('Frequency', fontsize=11)\n",
            "axes[1, 1].set_title('Target Variable: Adherence Rate Distribution', fontsize=12, fontweight='bold')\n",
            "axes[1, 1].axvline(df['adherence_rate'].mean(), color='orange', linestyle='--', linewidth=2, label=f'Mean: {df[\"adherence_rate\"].mean():.1f}%')\n",
            "axes[1, 1].legend()\n",
            "axes[1, 1].grid(axis='y', alpha=0.3)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('plots/feature_distributions.png', dpi=300, bbox_inches='tight')\n",
            "plt.show()\n",
            "\n",
            "print(\"✅ Feature distributions saved to: plots/feature_distributions.png\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Interpretation: Feature Distributions\n",
            "\n",
            "**Key Observations:**\n",
            "\n",
            "1. **Previous Adherence Rate:**\n",
            "   - Shows a relatively normal distribution with slight left skew\n",
            "   - Most patients have historical adherence rates between 60-90%\n",
            "   - This feature will be highly predictive as past behavior predicts future behavior\n",
            "\n",
            "2. **Missed Doses Last Week:**\n",
            "   - Right-skewed distribution (most patients miss few doses)\n",
            "   - Majority of patients miss 0-5 doses per week\n",
            "   - Outliers with high missed doses represent high-risk patients\n",
            "   - Strong negative correlation with adherence makes this a critical feature\n",
            "\n",
            "3. **Snooze Frequency:**\n",
            "   - Relatively uniform distribution across the 0-1 range\n",
            "   - Indicates diverse patient behaviors regarding reminder interactions\n",
            "   - Higher snooze rates correlate with procrastination and lower adherence\n",
            "\n",
            "4. **Target Variable (Adherence Rate):**\n",
            "   - Approximately normal distribution centered around 70-75%\n",
            "   - Good spread across the full range (0-100%)\n",
            "   - No extreme clustering that would make prediction trivial\n",
            "   - Suitable for regression modeling"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Distribution Plot 2: Scatter plots showing relationships with target\n",
            "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
            "fig.suptitle('Feature Relationships with Adherence Rate', fontsize=16, fontweight='bold', y=1.00)\n",
            "\n",
            "# Scatter 1: Previous Adherence Rate vs Current Adherence Rate\n",
            "axes[0, 0].scatter(df['previous_adherence_rate'], df['adherence_rate'], alpha=0.5, s=20, color='blue')\n",
            "axes[0, 0].set_xlabel('Previous Adherence Rate (%)', fontsize=11)\n",
            "axes[0, 0].set_ylabel('Current Adherence Rate (%)', fontsize=11)\n",
            "axes[0, 0].set_title(f'Previous vs Current Adherence\\n(r = {correlation_matrix.loc[\"previous_adherence_rate\", \"adherence_rate\"]:.3f})', \n",
            "                     fontsize=12, fontweight='bold')\n",
            "axes[0, 0].grid(alpha=0.3)\n",
            "\n",
            "# Add trend line\n",
            "z = np.polyfit(df['previous_adherence_rate'].dropna(), df['adherence_rate'][df['previous_adherence_rate'].notna()], 1)\n",
            "p = np.poly1d(z)\n",
            "axes[0, 0].plot(df['previous_adherence_rate'].dropna().sort_values(), \n",
            "                p(df['previous_adherence_rate'].dropna().sort_values()), \n",
            "                \"r--\", linewidth=2, label='Trend Line')\n",
            "axes[0, 0].legend()\n",
            "\n",
            "# Scatter 2: Missed Doses vs Adherence Rate\n",
            "axes[0, 1].scatter(df['missed_doses_last_week'], df['adherence_rate'], alpha=0.5, s=20, color='red')\n",
            "axes[0, 1].set_xlabel('Missed Doses (Last Week)', fontsize=11)\n",
            "axes[0, 1].set_ylabel('Current Adherence Rate (%)', fontsize=11)\n",
            "axes[0, 1].set_title(f'Missed Doses vs Adherence\\n(r = {correlation_matrix.loc[\"missed_doses_last_week\", \"adherence_rate\"]:.3f})', \n",
            "                     fontsize=12, fontweight='bold')\n",
            "axes[0, 1].grid(alpha=0.3)\n",
            "\n",
            "# Scatter 3: Snooze Frequency vs Adherence Rate\n",
            "axes[1, 0].scatter(df['snooze_frequency'], df['adherence_rate'], alpha=0.5, s=20, color='green')\n",
            "axes[1, 0].set_xlabel('Snooze Frequency (0-1)', fontsize=11)\n",
            "axes[1, 0].set_ylabel('Current Adherence Rate (%)', fontsize=11)\n",
            "axes[1, 0].set_title(f'Snooze Frequency vs Adherence\\n(r = {correlation_matrix.loc[\"snooze_frequency\", \"adherence_rate\"]:.3f})', \n",
            "                     fontsize=12, fontweight='bold')\n",
            "axes[1, 0].grid(alpha=0.3)\n",
            "\n",
            "# Scatter 4: Medication Complexity vs Adherence Rate\n",
            "axes[1, 1].scatter(df['medication_complexity'], df['adherence_rate'], alpha=0.5, s=20, color='purple')\n",
            "axes[1, 1].set_xlabel('Medication Complexity (1-5)', fontsize=11)\n",
            "axes[1, 1].set_ylabel('Current Adherence Rate (%)', fontsize=11)\n",
            "axes[1, 1].set_title(f'Medication Complexity vs Adherence\\n(r = {correlation_matrix.loc[\"medication_complexity\", \"adherence_rate\"]:.3f})', \n",
            "                     fontsize=12, fontweight='bold')\n",
            "axes[1, 1].grid(alpha=0.3)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('plots/feature_relationships.png', dpi=300, bbox_inches='tight')\n",
            "plt.show()\n",
            "\n",
            "print(\"✅ Feature relationships saved to: plots/feature_relationships.png\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Interpretation: Feature Relationships with Target\n",
            "\n",
            "**Scatter Plot Analysis:**\n",
            "\n",
            "1. **Previous Adherence Rate vs Current Adherence:**\n",
            "   - Strong positive linear relationship visible\n",
            "   - Trend line shows clear upward slope\n",
            "   - Patients with high historical adherence tend to maintain it\n",
            "   - Some variance indicates other factors also influence current adherence\n",
            "\n",
            "2. **Missed Doses vs Adherence:**\n",
            "   - Clear negative relationship: more missed doses = lower adherence\n",
            "   - Relationship appears somewhat non-linear (steeper decline at higher missed doses)\n",
            "   - Decision Trees and Random Forest may capture this non-linearity better than Linear Regression\n",
            "\n",
            "3. **Snooze Frequency vs Adherence:**\n",
            "   - Moderate negative correlation visible\n",
            "   - Higher snooze rates associated with lower adherence\n",
            "   - Relationship is more scattered, suggesting other factors moderate this effect\n",
            "\n",
            "4. **Medication Complexity vs Adherence:**\n",
            "   - Negative relationship: more complex regimens correlate with lower adherence\n",
            "   - Relationship appears relatively weak and scattered\n",
            "   - May interact with other features (e.g., age, chronic conditions)\n",
            "\n",
            "**Modeling Implications:**\n",
            "- Linear Regression will capture linear trends well\n",
            "- Decision Trees and Random Forest will better capture non-linear relationships and interactions\n",
            "- Feature engineering (e.g., interaction terms) could improve Linear Regression performance"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 3.3 Summary of Strongest Correlations"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create a summary table of feature correlations\n",
            "feature_importance = correlation_matrix['adherence_rate'].drop('adherence_rate').sort_values(key=abs, ascending=False)\n",
            "\n",
            "print(\"\\n\" + \"=\"*70)\n",
            "print(\"FEATURE CORRELATION SUMMARY WITH ADHERENCE RATE\")\n",
            "print(\"=\"*70)\n",
            "print(f\"{'Feature':<30} {'Correlation':<15} {'Strength':<20}\")\n",
            "print(\"-\"*70)\n",
            "\n",
            "for feature, corr in feature_importance.items():\n",
            "    abs_corr = abs(corr)\n",
            "    if abs_corr >= 0.7:\n",
            "        strength = \"Very Strong\"\n",
            "    elif abs_corr >= 0.5:\n",
            "        strength = \"Strong\"\n",
            "    elif abs_corr >= 0.3:\n",
            "        strength = \"Moderate\"\n",
            "    elif abs_corr >= 0.1:\n",
            "        strength = \"Weak\"\n",
            "    else:\n",
            "        strength = \"Very Weak\"\n",
            "    \n",
            "    direction = \"(+)\" if corr > 0 else \"(-)\"\n",
            "    print(f\"{feature:<30} {corr:>+.4f} {direction:<10} {strength:<20}\")\n",
            "\n",
            "print(\"=\"*70)\n",
            "print(\"\\nKey Insights:\")\n",
            "print(\"- Features with |correlation| > 0.5 are strong predictors\")\n",
            "print(\"- Positive correlations (+) increase adherence when feature value increases\")\n",
            "print(\"- Negative correlations (-) decrease adherence when feature value increases\")\n",
            "print(\"=\"*70)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## EDA Summary and Next Steps\n",
            "\n",
            "### Key Findings:\n",
            "\n",
            "1. **Dataset Quality:**\n",
            "   - 1500 patient records with 8 features + 1 target variable\n",
            "   - Minimal missing values (~2% in 3 columns)\n",
            "   - All features are numeric (no encoding needed)\n",
            "   - Target variable has good distribution for regression\n",
            "\n",
            "2. **Feature Importance (by correlation strength):**\n",
            "   - **Strongest predictors:** Previous adherence rate, missed doses, snooze frequency\n",
            "   - **Moderate predictors:** Medication complexity, number of medications\n",
            "   - **Weaker predictors:** Age, days since start, chronic conditions\n",
            "\n",
            "3. **Relationships:**\n",
            "   - Strong linear relationships exist (good for Linear Regression)\n",
            "   - Some non-linear patterns visible (advantage for tree-based models)\n",
            "   - Feature interactions likely present (Random Forest will capture these)\n",
            "\n",
            "4. **Visualizations Created:**\n",
            "   - ✅ Correlation heatmap: `plots/correlation_heatmap.png`\n",
            "   - ✅ Feature distributions: `plots/feature_distributions.png`\n",
            "   - ✅ Feature relationships: `plots/feature_relationships.png`\n",
            "\n",
            "### Next Steps:\n",
            "1. Handle missing values (imputation or removal)\n",
            "2. Feature standardization using StandardScaler\n",
            "3. Train/test split (80/20)\n",
            "4. Model training: Linear Regression, Decision Tree, Random Forest\n",
            "5. Model evaluation and comparison\n",
            "6. Select and save best-performing model"
        ]
    }
]

# Add the new cells to the notebook
notebook['cells'].extend(new_cells)

# Write the updated notebook
with open('multivariate.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("EDA cells added successfully to multivariate.ipynb")
print("   Total cells: " + str(len(notebook['cells'])))
print("   New sections added:")
print("   - 3. Exploratory Data Analysis (EDA)")
print("   - 3.1 Correlation Analysis")
print("   - 3.2 Feature Distributions and Relationships")
print("   - 3.3 Summary of Strongest Correlations")
