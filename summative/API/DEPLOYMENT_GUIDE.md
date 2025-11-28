# API Deployment Guide

This guide provides step-by-step instructions for deploying the MedMind Adherence Prediction API to various hosting platforms.

## Prerequisites

Before deploying, ensure:
- ✅ API works locally (`uvicorn prediction:app --reload`)
- ✅ All tests pass
- ✅ Model files exist in `models/` directory
- ✅ `requirements.txt` is up to date
- ✅ Code is committed to a Git repository (GitHub recommended)

## Option 1: Deploy to Render (Recommended - Free Tier Available)

### Step 1: Create Render Account

1. Go to [https://render.com](https://render.com)
2. Click "Get Started" or "Sign Up"
3. Sign up with GitHub (recommended for easier deployment)

### Step 2: Create New Web Service

1. From Render Dashboard, click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository
   - If first time: Click "Connect GitHub" and authorize Render
   - Select your repository from the list
   - Click "Connect"

### Step 3: Configure Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `medmind-adherence-api` (or your preferred name)
- **Region**: Choose closest to your users (e.g., Oregon, Ohio)
- **Branch**: `main` (or your default branch)
- **Root Directory**: `summative/API`

**Build & Deploy Settings:**
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn prediction:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select **Free** tier (sufficient for testing and development)

### Step 4: Environment Variables (Optional)

If needed, add environment variables:
- Click "Advanced" → "Add Environment Variable"
- Add any custom variables (none required for basic setup)

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start the application
3. Wait for deployment to complete (usually 2-5 minutes)
4. Watch the logs for any errors

### Step 6: Verify Deployment

Once deployed, Render provides a public URL like:
```
https://medmind-adherence-api.onrender.com
```

Test the endpoints:

```bash
# Test health endpoint
curl https://medmind-adherence-api.onrender.com/health

# Test prediction endpoint
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

Access Swagger UI:
```
https://medmind-adherence-api.onrender.com/docs
```

### Step 7: Document Public URL

Add the public URL to your README files:
- `summative/API/README.md`
- `summative/README.md`

---

## Option 2: Deploy to Railway

### Step 1: Create Railway Account

1. Go to [https://railway.app](https://railway.app)
2. Click "Login" and sign in with GitHub

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will auto-detect it's a Python project

### Step 3: Configure Service

1. Click on the deployed service
2. Go to "Settings" tab
3. Configure:
   - **Root Directory**: `summative/API`
   - **Start Command**: `uvicorn prediction:app --host 0.0.0.0 --port $PORT`
   - **Build Command**: `pip install -r requirements.txt`

### Step 4: Deploy

1. Railway automatically deploys on push
2. Wait for build to complete
3. Railway provides a public URL

### Step 5: Verify Deployment

Test using the Railway-provided URL (similar to Render steps above)

---

## Option 3: Deploy to Heroku

### Step 1: Create Heroku Account

1. Go to [https://heroku.com](https://heroku.com)
2. Sign up for free account

### Step 2: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 3: Login and Create App

```bash
# Login to Heroku
heroku login

# Navigate to API directory
cd summative/API

# Create new Heroku app
heroku create medmind-adherence-api

# Or use auto-generated name
heroku create
```

### Step 4: Deploy

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Add Heroku remote
heroku git:remote -a medmind-adherence-api

# Deploy
git push heroku main
```

### Step 5: Verify Deployment

```bash
# Open app in browser
heroku open

# View logs
heroku logs --tail

# Test health endpoint
curl https://medmind-adherence-api.herokuapp.com/health
```

---

## Troubleshooting

### Issue: Build Fails - Dependencies Not Installing

**Solution:**
- Verify `requirements.txt` is in the root directory being deployed
- Check Python version compatibility
- Review build logs for specific error messages

### Issue: App Crashes on Startup

**Solution:**
- Check that model files are included in repository
- Verify start command is correct: `uvicorn prediction:app --host 0.0.0.0 --port $PORT`
- Review application logs for errors

### Issue: Model Files Not Found

**Solution:**
- Ensure `models/best_model.pkl` and `models/scaler.pkl` are committed to git
- Check `.gitignore` doesn't exclude `.pkl` files
- Verify file paths in `prediction.py` are correct

### Issue: CORS Errors from Flutter App

**Solution:**
- Verify CORS middleware is configured in `prediction.py`
- Check that `allow_origins=["*"]` is set for development
- For production, add specific Flutter app domain

### Issue: Slow Response Times

**Solution:**
- Free tier services may have cold starts (first request slow)
- Consider upgrading to paid tier for production
- Implement caching if needed

### Issue: 422 Validation Errors

**Solution:**
- Check input data matches Pydantic model constraints
- Review Swagger UI docs for correct field types and ranges
- Test with example request from README

---

## Post-Deployment Checklist

- [ ] API is accessible at public URL
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] Swagger UI is accessible at `/docs`
- [ ] Prediction endpoint accepts valid requests
- [ ] Prediction endpoint rejects invalid requests with 422
- [ ] CORS is configured for Flutter app
- [ ] Public URL is documented in README files
- [ ] API response time is acceptable (< 5 seconds)
- [ ] Logs are accessible for debugging

---

## Monitoring and Maintenance

### View Logs

**Render:**
- Dashboard → Your Service → Logs tab

**Railway:**
- Project → Service → Deployments → View Logs

**Heroku:**
```bash
heroku logs --tail -a medmind-adherence-api
```

### Update Deployment

**Render/Railway:**
- Push changes to GitHub
- Automatic deployment triggered

**Heroku:**
```bash
git push heroku main
```

### Scale Service (Paid Plans)

**Render:**
- Dashboard → Service → Settings → Instance Type

**Railway:**
- Automatically scales based on usage

**Heroku:**
```bash
heroku ps:scale web=1
```

---

## Security Considerations for Production

1. **Restrict CORS Origins:**
   ```python
   allow_origins=["https://your-flutter-app.com"]
   ```

2. **Add Rate Limiting:**
   - Use middleware like `slowapi`
   - Prevent abuse and DoS attacks

3. **Enable HTTPS:**
   - All platforms provide free SSL certificates
   - Ensure all requests use HTTPS

4. **Add Authentication (if needed):**
   - API keys
   - OAuth tokens
   - JWT authentication

5. **Monitor Usage:**
   - Set up alerts for errors
   - Track API usage metrics
   - Monitor response times

---

## Cost Considerations

### Free Tier Limitations

**Render:**
- Free tier available
- Services spin down after 15 minutes of inactivity
- 750 hours/month free

**Railway:**
- $5 free credit per month
- Pay-as-you-go after credit exhausted

**Heroku:**
- Free tier discontinued (as of Nov 2022)
- Minimum $7/month for Eco dynos

### Recommendation

For this project (development/testing):
- **Render** is recommended for free tier with good performance
- **Railway** is good alternative with generous free credit

For production:
- Consider paid tiers for better performance and uptime
- Render Starter: $7/month
- Railway: Pay-as-you-go based on usage

---

## Next Steps

1. ✅ Deploy API to chosen platform
2. ✅ Test all endpoints with public URL
3. ✅ Document public URL in README
4. ✅ Update Flutter app to use deployed API URL
5. ✅ Create video demonstration showing deployed API
6. ✅ Monitor logs and performance

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Heroku Docs**: https://devcenter.heroku.com
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

## Example: Complete Render Deployment

Here's a complete example of deploying to Render:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare API for deployment"
   git push origin main
   ```

2. **Create Render account** at https://render.com

3. **Create Web Service**
   - New + → Web Service
   - Connect GitHub repo
   - Select repository

4. **Configure**
   - Name: `medmind-adherence-api`
   - Root Directory: `summative/API`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn prediction:app --host 0.0.0.0 --port $PORT`
   - Instance: Free

5. **Deploy** - Click "Create Web Service"

6. **Test**
   ```bash
   curl https://medmind-adherence-api.onrender.com/health
   ```

7. **Document URL** in README files

Done! 🎉
