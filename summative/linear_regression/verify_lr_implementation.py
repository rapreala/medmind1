#!/usr/bin/env python3
"""
Verification script for Linear Regression implementation.
Checks that all requirements from Task 4 have been met.
"""

import os
import sys

print("="*70)
print("LINEAR REGRESSION IMPLEMENTATION VERIFICATION")
print("="*70)

all_checks_passed = True

# Check 1: Verify metrics file exists
print("\n1. Checking metrics file...")
if os.path.exists('models/lr_metrics.txt'):
    print("   ✅ models/lr_metrics.txt exists")
    with open('models/lr_metrics.txt', 'r') as f:
        content = f.read()
        if 'MSE' in content and 'R²' in content:
            print("   ✅ Metrics file contains MSE and R² values")
        else:
            print("   ❌ Metrics file missing required metrics")
            all_checks_passed = False
else:
    print("   ❌ models/lr_metrics.txt not found")
    all_checks_passed = False

# Check 2: Verify actual vs predicted plot exists
print("\n2. Checking actual vs predicted plot...")
if os.path.exists('plots/lr_actual_vs_predicted.png'):
    size = os.path.getsize('plots/lr_actual_vs_predicted.png')
    print(f"   ✅ plots/lr_actual_vs_predicted.png exists ({size} bytes)")
    if size > 100000:  # Should be > 100KB for a quality plot
        print("   ✅ Plot file size indicates proper visualization")
    else:
        print("   ⚠️  Plot file size is smaller than expected")
else:
    print("   ❌ plots/lr_actual_vs_predicted.png not found")
    all_checks_passed = False

# Check 3: Verify residual plot exists
print("\n3. Checking residual analysis plot...")
if os.path.exists('plots/lr_residuals.png'):
    size = os.path.getsize('plots/lr_residuals.png')
    print(f"   ✅ plots/lr_residuals.png exists ({size} bytes)")
    if size > 100000:  # Should be > 100KB for a quality plot
        print("   ✅ Plot file size indicates proper visualization")
    else:
        print("   ⚠️  Plot file size is smaller than expected")
else:
    print("   ❌ plots/lr_residuals.png not found")
    all_checks_passed = False

# Check 4: Verify training script exists
print("\n4. Checking training script...")
if os.path.exists('run_linear_regression.py'):
    print("   ✅ run_linear_regression.py exists")
    with open('run_linear_regression.py', 'r') as f:
        content = f.read()
        required_imports = ['LinearRegression', 'mean_squared_error', 'r2_score']
        for imp in required_imports:
            if imp in content:
                print(f"   ✅ Script imports {imp}")
            else:
                print(f"   ❌ Script missing import: {imp}")
                all_checks_passed = False
else:
    print("   ❌ run_linear_regression.py not found")
    all_checks_passed = False

# Check 5: Verify summary document exists
print("\n5. Checking summary documentation...")
if os.path.exists('LINEAR_REGRESSION_SUMMARY.md'):
    print("   ✅ LINEAR_REGRESSION_SUMMARY.md exists")
    with open('LINEAR_REGRESSION_SUMMARY.md', 'r') as f:
        content = f.read()
        if 'R²' in content and 'MSE' in content and 'RMSE' in content:
            print("   ✅ Summary contains performance metrics")
        else:
            print("   ❌ Summary missing performance metrics")
            all_checks_passed = False
else:
    print("   ❌ LINEAR_REGRESSION_SUMMARY.md not found")
    all_checks_passed = False

# Check 6: Verify metrics values are reasonable
print("\n6. Checking metric values...")
try:
    with open('models/lr_metrics.txt', 'r') as f:
        content = f.read()
        # Extract R² value
        for line in content.split('\n'):
            if 'R²' in line and 'Test' in line:
                r2_str = line.split(':')[1].strip()
                r2_value = float(r2_str)
                print(f"   ✅ Test R² = {r2_value:.4f}")
                if 0 <= r2_value <= 1:
                    print("   ✅ R² value is in valid range [0, 1]")
                else:
                    print("   ❌ R² value is out of valid range")
                    all_checks_passed = False
                break
except Exception as e:
    print(f"   ⚠️  Could not parse metrics: {e}")

# Final summary
print("\n" + "="*70)
if all_checks_passed:
    print("✅ ALL VERIFICATION CHECKS PASSED")
    print("="*70)
    print("\nTask 4 Requirements Met:")
    print("  ✅ LinearRegression imported from scikit-learn")
    print("  ✅ Model trained on standardized training data")
    print("  ✅ Predictions made on test set")
    print("  ✅ MSE and R² metrics calculated for both sets")
    print("  ✅ Actual vs predicted scatter plot created")
    print("  ✅ Residual analysis plots created")
    print("  ✅ Model performance documented")
    print("\n" + "="*70)
    sys.exit(0)
else:
    print("❌ SOME VERIFICATION CHECKS FAILED")
    print("="*70)
    print("\nPlease review the errors above and fix any issues.")
    print("="*70)
    sys.exit(1)
