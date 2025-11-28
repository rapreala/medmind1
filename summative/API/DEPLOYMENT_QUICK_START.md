# Quick Start: Deploy to Render

This is a condensed guide for deploying the MedMind API to Render. For detailed instructions, see `DEPLOYMENT_GUIDE.md`.

## Prerequisites

✅ API works locally  
✅ All tests pass  
✅ Code committed to GitHub  

## Steps

### 1. Verify Deployment Readiness

```bash
cd summative/API
python verify_deployment_ready.py
```

### 2. Commit and Push to GitHub

```bash
git add .
git commit -m "Prepare API for deployment"
git push origin main
```

### 3. Create Render Account

Go to https://render.com and sign up with GitHub

### 4. Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository

### 5. Configure Service

**Name:** `medmind-adherence-api`

**Root Directory:** `summative/API`

**Build Command:** `pip install -r requirements.txt`

**Start Command:** `uvicorn prediction:app --host 0.0.0.0 --port $PORT`

**Instance Type:** Free

### 6. Deploy

Click "Create Web Service" and wait 2-5 minutes

### 7. Test Deployment

```bash
# Replace with your actual URL
python test_deployed_api.py https://medmind-adherence-api.onrender.com
```

### 8. Document URL

Update these files with your public URL:
- `summative/API/README.md`
- `summative/README.md`

Replace `[TO BE ADDED AFTER DEPLOYMENT]` with your actual URL.

## Your Deployed URLs

After deployment, you'll have:

**API Base URL:**
```
https://medmind-adherence-api.onrender.com
```

**Swagger UI:**
```
https://medmind-adherence-api.onrender.com/docs
```

**Health Check:**
```
https://medmind-adherence-api.onrender.com/health
```

## Test Commands

```bash
# Health check
curl https://medmind-adherence-api.onrender.com/health

# Prediction
curl -X POST https://medmind-adherence-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "num_medications": 3,
    "medication_complexity": 2.5,
    "days_since_start": 120,
    "missed_doses_last_week": 1,
    "snooze_frequency": 0.2,
    "chronic_conditions": 2,
    "previous_adherence_rate": 85.5
  }'
```

## Troubleshooting

**Build fails?**
- Check `requirements.txt` exists
- Review build logs in Render dashboard

**App crashes?**
- Verify model files are in repository
- Check logs in Render dashboard

**422 errors?**
- Verify input data matches constraints
- Check Swagger UI for field requirements

## Next Steps

1. ✅ Test all endpoints
2. ✅ Document public URL in README files
3. ✅ Update Flutter app with API URL
4. ✅ Create video demonstration

## Support

- Render Docs: https://render.com/docs
- Full Guide: See `DEPLOYMENT_GUIDE.md`
- API Tests: Run `python test_deployed_api.py <URL>`
