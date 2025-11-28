#!/bin/bash

# MedMind Adherence Prediction - Submission Verification Script
# This script verifies that all submission requirements are met

echo "=========================================="
echo "MedMind Submission Verification"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
        return 1
    fi
}

# Function to check API endpoint
check_api() {
    echo -n "Testing API endpoint... "
    RESPONSE=$(curl -s -X POST "https://medmind-adherence-api.onrender.com/predict" \
        -H "Content-Type: application/json" \
        -d '{"age": 45, "num_medications": 3, "medication_complexity": 2.5, "days_since_start": 120, "missed_doses_last_week": 1, "snooze_frequency": 0.2, "chronic_conditions": 2, "previous_adherence_rate": 85.5}' \
        --max-time 30 2>&1)
    
    if echo "$RESPONSE" | grep -q "predicted_adherence_rate"; then
        echo -e "${GREEN}✓${NC} API is responding correctly"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} API is not responding correctly"
        echo "Response: $RESPONSE"
        ((FAILED++))
        return 1
    fi
}

echo "1. Checking Directory Structure"
echo "--------------------------------"
check_dir "summative/linear_regression" "Linear regression directory"
check_dir "summative/API" "API directory"
check_dir "summative/linear_regression/models" "Models directory"
check_dir "summative/linear_regression/plots" "Plots directory"
echo ""

echo "2. Checking ML Pipeline Files"
echo "------------------------------"
check_file "summative/linear_regression/multivariate.ipynb" "Jupyter notebook"
check_file "summative/linear_regression/adherence_data.csv" "Dataset"
check_file "summative/linear_regression/models/best_model.pkl" "Best model"
check_file "summative/linear_regression/models/scaler.pkl" "Scaler"
echo ""

echo "3. Checking Visualizations"
echo "--------------------------"
check_file "summative/linear_regression/plots/correlation_heatmap.png" "Correlation heatmap"
check_file "summative/linear_regression/plots/feature_distributions.png" "Feature distributions"
check_file "summative/linear_regression/plots/lr_actual_vs_predicted.png" "LR predictions plot"
check_file "summative/linear_regression/plots/dt_feature_importance.png" "DT feature importance"
check_file "summative/linear_regression/plots/rf_feature_importance.png" "RF feature importance"
check_file "summative/linear_regression/plots/model_comparison.png" "Model comparison"
echo ""

echo "4. Checking API Files"
echo "---------------------"
check_file "summative/API/prediction.py" "FastAPI application"
check_file "summative/API/requirements.txt" "Requirements file"
check_file "summative/API/models/best_model.pkl" "Deployed model"
check_file "summative/API/models/scaler.pkl" "Deployed scaler"
echo ""

echo "5. Checking Flutter Integration"
echo "--------------------------------"
check_file "lib/features/adherence/presentation/pages/adherence_prediction_page.dart" "Prediction page"
check_file "lib/features/adherence/presentation/services/prediction_service.dart" "Prediction service"
echo ""

echo "6. Checking Documentation"
echo "-------------------------"
check_file "summative/README.md" "Main README"
check_file "summative/SUBMISSION_CHECKLIST.md" "Submission checklist"
check_file "summative/VIDEO_DEMONSTRATION_GUIDE.md" "Video guide"
check_file "summative/SUBMISSION_PACKAGE.md" "Submission package"
echo ""

echo "7. Checking Test Files"
echo "----------------------"
check_file "summative/linear_regression/test_preprocessing.py" "Preprocessing tests"
check_file "summative/linear_regression/test_prediction_function.py" "Prediction tests"
check_file "summative/API/test_api_endpoint.py" "API endpoint tests"
check_file "test/features/adherence/presentation/prediction_service_test.dart" "Flutter service tests"
echo ""

echo "8. Testing Live API"
echo "-------------------"
check_api
echo ""

echo "9. Checking for YouTube URL"
echo "---------------------------"
if grep -q "YOUR_YOUTUBE_URL_HERE" summative/README.md; then
    echo -e "${YELLOW}⚠${NC} YouTube URL placeholder still present in README"
    echo "   Action required: Record video and update URL"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓${NC} YouTube URL has been updated"
    ((PASSED++))
fi
echo ""

echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED - READY FOR SUBMISSION${NC}"
    exit 0
elif [ $FAILED -eq 0 ]; then
    echo -e "${YELLOW}⚠ ALMOST READY - ADDRESS WARNINGS BEFORE SUBMISSION${NC}"
    exit 0
else
    echo -e "${RED}✗ SUBMISSION NOT READY - FIX FAILED CHECKS${NC}"
    exit 1
fi
