#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to run EDA and generate visualizations"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Create plots directory
os.makedirs('plots', exist_ok=True)
print("Plots directory ready!")

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# Load the dataset
print("\nLoading dataset...")
df = pd.read_csv('adherence_data.csv')
print(f"Dataset loaded: {df.shape[0]} records, {df.shape[1]} columns")

# Calculate correlation matrix
print("\nCalculating correlations...")
correlation_matrix = df.corr()

# Display correlation with target variable
print("\nCorrelation with Adherence Rate (Target Variable):")
print("="*60)
target_corr = correlation_matrix['adherence_rate'].sort_values(ascending=False)
print(target_corr)
print("\n" + "="*60)

# Generate correlation heatmap
print("\nGenerating correlation heatmap...")
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, 
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm', 
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8})

plt.title('Correlation Heatmap: Feature Relationships and Target Variable', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: plots/correlation_heatmap.png")

# Identify top features
target_corr_abs = correlation_matrix['adherence_rate'].abs().sort_values(ascending=False)
top_features = target_corr_abs[1:4].index.tolist()

print("\nTop 3 Features by Correlation Strength:")
for i, feature in enumerate(top_features, 1):
    corr_value = correlation_matrix.loc[feature, 'adherence_rate']
    print(f"{i}. {feature}: {corr_value:.3f}")

# Distribution Plot 1: Histograms of key features
print("\nGenerating feature distributions...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Distribution of Key Features', fontsize=16, fontweight='bold', y=1.00)

# Plot 1: Previous Adherence Rate
axes[0, 0].hist(df['previous_adherence_rate'].dropna(), bins=30, color='skyblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Previous Adherence Rate (%)', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Previous Adherence Rate Distribution', fontsize=12, fontweight='bold')
axes[0, 0].axvline(df['previous_adherence_rate'].mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {df["previous_adherence_rate"].mean():.1f}%')
axes[0, 0].legend()
axes[0, 0].grid(axis='y', alpha=0.3)

# Plot 2: Missed Doses Last Week
axes[0, 1].hist(df['missed_doses_last_week'].dropna(), bins=20, color='salmon', edgecolor='black', alpha=0.7)
axes[0, 1].set_xlabel('Missed Doses (Last Week)', fontsize=11)
axes[0, 1].set_ylabel('Frequency', fontsize=11)
axes[0, 1].set_title('Missed Doses Distribution', fontsize=12, fontweight='bold')
axes[0, 1].axvline(df['missed_doses_last_week'].mean(), color='darkred', linestyle='--', linewidth=2, 
                   label=f'Mean: {df["missed_doses_last_week"].mean():.1f}')
axes[0, 1].legend()
axes[0, 1].grid(axis='y', alpha=0.3)

# Plot 3: Snooze Frequency
axes[1, 0].hist(df['snooze_frequency'].dropna(), bins=25, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Snooze Frequency (0-1)', fontsize=11)
axes[1, 0].set_ylabel('Frequency', fontsize=11)
axes[1, 0].set_title('Snooze Frequency Distribution', fontsize=12, fontweight='bold')
axes[1, 0].axvline(df['snooze_frequency'].mean(), color='darkgreen', linestyle='--', linewidth=2, 
                   label=f'Mean: {df["snooze_frequency"].mean():.2f}')
axes[1, 0].legend()
axes[1, 0].grid(axis='y', alpha=0.3)

# Plot 4: Target Variable
axes[1, 1].hist(df['adherence_rate'].dropna(), bins=30, color='gold', edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Current Adherence Rate (%)', fontsize=11)
axes[1, 1].set_ylabel('Frequency', fontsize=11)
axes[1, 1].set_title('Target Variable: Adherence Rate Distribution', fontsize=12, fontweight='bold')
axes[1, 1].axvline(df['adherence_rate'].mean(), color='orange', linestyle='--', linewidth=2, 
                   label=f'Mean: {df["adherence_rate"].mean():.1f}%')
axes[1, 1].legend()
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('plots/feature_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: plots/feature_distributions.png")

# Distribution Plot 2: Scatter plots
print("\nGenerating feature relationships scatter plots...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Feature Relationships with Adherence Rate', fontsize=16, fontweight='bold', y=1.00)

# Scatter 1: Previous Adherence Rate vs Current
axes[0, 0].scatter(df['previous_adherence_rate'], df['adherence_rate'], alpha=0.5, s=20, color='blue')
axes[0, 0].set_xlabel('Previous Adherence Rate (%)', fontsize=11)
axes[0, 0].set_ylabel('Current Adherence Rate (%)', fontsize=11)
axes[0, 0].set_title(f'Previous vs Current Adherence\n(r = {correlation_matrix.loc["previous_adherence_rate", "adherence_rate"]:.3f})', 
                     fontsize=12, fontweight='bold')
axes[0, 0].grid(alpha=0.3)

# Add trend line
z = np.polyfit(df['previous_adherence_rate'].dropna(), df['adherence_rate'][df['previous_adherence_rate'].notna()], 1)
p = np.poly1d(z)
axes[0, 0].plot(df['previous_adherence_rate'].dropna().sort_values(), 
                p(df['previous_adherence_rate'].dropna().sort_values()), 
                "r--", linewidth=2, label='Trend Line')
axes[0, 0].legend()

# Scatter 2: Missed Doses vs Adherence
axes[0, 1].scatter(df['missed_doses_last_week'], df['adherence_rate'], alpha=0.5, s=20, color='red')
axes[0, 1].set_xlabel('Missed Doses (Last Week)', fontsize=11)
axes[0, 1].set_ylabel('Current Adherence Rate (%)', fontsize=11)
axes[0, 1].set_title(f'Missed Doses vs Adherence\n(r = {correlation_matrix.loc["missed_doses_last_week", "adherence_rate"]:.3f})', 
                     fontsize=12, fontweight='bold')
axes[0, 1].grid(alpha=0.3)

# Scatter 3: Snooze Frequency vs Adherence
axes[1, 0].scatter(df['snooze_frequency'], df['adherence_rate'], alpha=0.5, s=20, color='green')
axes[1, 0].set_xlabel('Snooze Frequency (0-1)', fontsize=11)
axes[1, 0].set_ylabel('Current Adherence Rate (%)', fontsize=11)
axes[1, 0].set_title(f'Snooze Frequency vs Adherence\n(r = {correlation_matrix.loc["snooze_frequency", "adherence_rate"]:.3f})', 
                     fontsize=12, fontweight='bold')
axes[1, 0].grid(alpha=0.3)

# Scatter 4: Medication Complexity vs Adherence
axes[1, 1].scatter(df['medication_complexity'], df['adherence_rate'], alpha=0.5, s=20, color='purple')
axes[1, 1].set_xlabel('Medication Complexity (1-5)', fontsize=11)
axes[1, 1].set_ylabel('Current Adherence Rate (%)', fontsize=11)
axes[1, 1].set_title(f'Medication Complexity vs Adherence\n(r = {correlation_matrix.loc["medication_complexity", "adherence_rate"]:.3f})', 
                     fontsize=12, fontweight='bold')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('plots/feature_relationships.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: plots/feature_relationships.png")

# Summary of correlations
print("\n" + "="*70)
print("FEATURE CORRELATION SUMMARY WITH ADHERENCE RATE")
print("="*70)
print(f"{'Feature':<30} {'Correlation':<15} {'Strength':<20}")
print("-"*70)

feature_importance = correlation_matrix['adherence_rate'].drop('adherence_rate').sort_values(key=abs, ascending=False)

for feature, corr in feature_importance.items():
    abs_corr = abs(corr)
    if abs_corr >= 0.7:
        strength = "Very Strong"
    elif abs_corr >= 0.5:
        strength = "Strong"
    elif abs_corr >= 0.3:
        strength = "Moderate"
    elif abs_corr >= 0.1:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    direction = "(+)" if corr > 0 else "(-)"
    print(f"{feature:<30} {corr:>+.4f} {direction:<10} {strength:<20}")

print("="*70)

print("\n" + "="*70)
print("EDA COMPLETE - ALL VISUALIZATIONS GENERATED")
print("="*70)
print("\nGenerated files:")
print("  1. plots/correlation_heatmap.png")
print("  2. plots/feature_distributions.png")
print("  3. plots/feature_relationships.png")
print("\nKey findings:")
print("  - Identified features with strongest correlation to adherence rate")
print("  - Created comprehensive visualizations of feature distributions")
print("  - Analyzed relationships between features and target variable")
print("="*70)
