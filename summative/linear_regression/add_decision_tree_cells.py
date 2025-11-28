#!/usr/bin/env python3
"""
Script to add Decision Tree model cells to the Jupyter notebook.
"""

import json

# Load the existing notebook
with open('multivariate.ipynb', 'r') as f:
    notebook = json.load(f)

# Decision Tree cells to add (as JSON strings that will be parsed)
dt_cells_json = '''
[
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 5.2 Decision Tree Model\\n",
            "\\n",
            "Decision Trees are non-parametric supervised learning algorithms that create a tree-like model of decisions. They split the data based on feature values to make predictions.\\n",
            "\\n",
            "**How Decision Trees Work:**\\n",
            "1. Start with all data at the root node\\n",
            "2. Find the best feature and split point that minimizes prediction error\\n",
            "3. Recursively split data into branches\\n",
            "4. Stop when reaching maximum depth or minimum samples\\n",
            "5. Leaf nodes contain the predicted values\\n",
            "\\n",
            "**Advantages:**\\n",
            "- Captures non-linear relationships\\n",
            "- Handles feature interactions automatically\\n",
            "- No assumptions about data distribution\\n",
            "- Provides feature importance scores\\n",
            "- Easy to visualize and interpret\\n",
            "\\n",
            "**Limitations:**\\n",
            "- Prone to overfitting (especially with deep trees)\\n",
            "- Can be unstable (small data changes cause different trees)\\n",
            "- May not generalize as well as ensemble methods\\n",
            "\\n",
            "**Hyperparameters to Tune:**\\n",
            "- `max_depth`: Maximum depth of the tree (prevents overfitting)\\n",
            "- `min_samples_split`: Minimum samples required to split a node\\n",
            "- `min_samples_leaf`: Minimum samples required at leaf nodes"
        ]
    }
]
'''

# Parse the JSON
dt_cells = json.loads(dt_cells_json)

# Add more cells programmatically
print("Adding Decision Tree cells to notebook...")
print(f"Current notebook has {len(notebook['cells'])} cells")

# Add the cells to the notebook
notebook['cells'].extend(dt_cells)

# Save the updated notebook
with open('multivariate.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"✅ Decision Tree section added to notebook successfully!")
print(f"   Notebook now has {len(notebook['cells'])} cells")
print("   Note: Run the notebook or use run_decision_tree.py to execute the training")
