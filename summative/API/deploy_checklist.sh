#!/bin/bash

# Deployment Checklist Script
# This script helps you track deployment progress

echo "======================================================================"
echo "MedMind API - Deployment Checklist"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Step 1: Pre-Deployment Verification"
echo "----------------------------------------------------------------------"
echo "Running verification script..."
python verify_deployment_ready.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pre-deployment checks passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some checks failed. Review and fix before deploying.${NC}"
    exit 1
fi
echo ""

echo "Step 2: Git Status"
echo "----------------------------------------------------------------------"
git status --short
echo ""
read -p "Do you want to commit and push changes? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    read -p "Enter commit message: " commit_msg
    git commit -m "$commit_msg"
    git push origin main
    echo -e "${GREEN}✅ Changes committed and pushed${NC}"
else
    echo -e "${YELLOW}⚠️  Skipped git commit. Remember to push before deploying!${NC}"
fi
echo ""

echo "Step 3: Deployment Platform Selection"
echo "----------------------------------------------------------------------"
echo "Choose your deployment platform:"
echo "1) Render (Recommended - Free tier)"
echo "2) Railway (Free credit)"
echo "3) Heroku (Paid - $7/month minimum)"
echo ""
read -p "Enter choice (1-3): " platform_choice

case $platform_choice in
    1)
        echo ""
        echo "Deploying to Render:"
        echo "1. Go to https://render.com"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Configure:"
        echo "   - Name: medmind-adherence-api"
        echo "   - Root Directory: summative/API"
        echo "   - Build: pip install -r requirements.txt"
        echo "   - Start: uvicorn prediction:app --host 0.0.0.0 --port \$PORT"
        echo "   - Instance: Free"
        echo "6. Click 'Create Web Service'"
        echo ""
        echo "See DEPLOYMENT_QUICK_START.md for detailed steps"
        ;;
    2)
        echo ""
        echo "Deploying to Railway:"
        echo "1. Go to https://railway.app"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Select your repository"
        echo "5. Configure in Settings:"
        echo "   - Root Directory: summative/API"
        echo "   - Start: uvicorn prediction:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md Section 'Option 2' for details"
        ;;
    3)
        echo ""
        echo "Deploying to Heroku:"
        echo "1. Install Heroku CLI: brew install heroku"
        echo "2. Login: heroku login"
        echo "3. Create app: heroku create medmind-adherence-api"
        echo "4. Deploy: git push heroku main"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md Section 'Option 3' for details"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
read -p "Press Enter when deployment is complete..."
echo ""

echo "Step 4: Test Deployed API"
echo "----------------------------------------------------------------------"
read -p "Enter your deployed API URL: " api_url

if [ -z "$api_url" ]; then
    echo -e "${YELLOW}⚠️  No URL provided. Skipping tests.${NC}"
else
    echo "Testing API at: $api_url"
    python test_deployed_api.py "$api_url"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ All API tests passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Some tests failed. Review the output above.${NC}"
    fi
fi
echo ""

echo "Step 5: Document Public URL"
echo "----------------------------------------------------------------------"
echo "Update the following files with your API URL:"
echo "  - summative/API/README.md"
echo "  - summative/README.md"
echo ""
echo "Replace '[TO BE ADDED AFTER DEPLOYMENT]' with: $api_url"
echo ""
read -p "Press Enter when you've updated the README files..."
echo ""

echo "======================================================================"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "======================================================================"
echo ""
echo "Your API is now live at: $api_url"
echo "Swagger UI: $api_url/docs"
echo ""
echo "Next Steps:"
echo "1. ✅ API is deployed and tested"
echo "2. ⏭️  Update Flutter app with API URL (Task 17-19)"
echo "3. ⏭️  Create video demonstration (Task 23)"
echo ""
echo "======================================================================"
