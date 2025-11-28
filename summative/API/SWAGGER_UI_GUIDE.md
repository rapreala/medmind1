# Swagger UI Testing Guide

## How to Access and Test the API with Swagger UI

### Step 1: Start the API Server

Open a terminal and run:

```bash
cd summative/API
uvicorn prediction:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Open Swagger UI

Open your web browser and navigate to:

```
http://localhost:8000/docs
```

You should see the interactive Swagger UI documentation page.

### Step 3: Test the `/predict` Endpoint

#### Testing with Valid Input:

1. Click on the **POST /predict** endpoint to expand it
2. Click the **"Try it out"** button
3. You'll see an editable JSON request body with example values:

```json
{
  "age": 45,
  "num_medications": 3,
  "medication_complexity": 2.5,
  "days_since_start": 120,
  "missed_doses_last_week": 1,
  "snooze_frequency": 0.2,
  "chronic_conditions": 2,
  "previous_adherence_rate": 85.5
}
```

4. Click **"Execute"**
5. Scroll down to see the response:
   - **Response Code**: 200
   - **Response Body**: Contains predicted adherence rate

#### Testing with Invalid Input (Out of Range):

1. Modify the JSON to have an invalid age:

```json
{
  "age": 150,
  "num_medications": 3,
  "medication_complexity": 2.5,
  "days_since_start": 120,
  "missed_doses_last_week": 1,
  "snooze_frequency": 0.2,
  "chronic_conditions": 2,
  "previous_adherence_rate": 85.5
}
```

2. Click **"Execute"**
3. You should see:
   - **Response Code**: 422
   - **Error Message**: "Input should be less than or equal to 120"

#### Testing with Wrong Type:

1. Modify the JSON to have a string instead of a number:

```json
{
  "age": "forty-five",
  "num_medications": 3,
  "medication_complexity": 2.5,
  "days_since_start": 120,
  "missed_doses_last_week": 1,
  "snooze_frequency": 0.2,
  "chronic_conditions": 2,
  "previous_adherence_rate": 85.5
}
```

2. Click **"Execute"**
3. You should see:
   - **Response Code**: 422
   - **Error Message**: "Input should be a valid integer"

#### Testing with Missing Fields:

1. Remove some required fields:

```json
{
  "age": 45,
  "num_medications": 3
}
```

2. Click **"Execute"**
3. You should see:
   - **Response Code**: 422
   - **Multiple Error Messages**: One for each missing field

### Step 4: Explore Other Endpoints

#### Health Check Endpoint:

1. Click on **GET /health**
2. Click **"Try it out"**
3. Click **"Execute"**
4. You should see:
   - **Response Code**: 200
   - **Response Body**: 
     ```json
     {
       "status": "healthy",
       "model_loaded": true,
       "scaler_loaded": true
     }
     ```

#### Root Endpoint:

1. Click on **GET /**
2. Click **"Try it out"**
3. Click **"Execute"**
4. You should see API information

### Step 5: View Schema Documentation

Scroll down in Swagger UI to see the **Schemas** section:

- **PredictionInput**: Shows all input fields with their types, constraints, and descriptions
- **PredictionOutput**: Shows the response structure

### Alternative: Using ReDoc

For a different documentation style, visit:

```
http://localhost:8000/redoc
```

ReDoc provides a cleaner, more readable documentation format.

### Alternative: Using curl

You can also test the API from the command line:

```bash
# Valid request
curl -X POST "http://localhost:8000/predict" \
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

# Invalid request (age out of range)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 150,
    "num_medications": 3,
    "medication_complexity": 2.5,
    "days_since_start": 120,
    "missed_doses_last_week": 1,
    "snooze_frequency": 0.2,
    "chronic_conditions": 2,
    "previous_adherence_rate": 85.5
  }'
```

### Troubleshooting

#### API Not Starting:
- Check if port 8000 is already in use
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify model files exist in `models/` directory

#### 500 Internal Server Error:
- Check the terminal logs for error messages
- Ensure model and scaler files are present and valid
- Verify Python version compatibility (3.8+)

#### Cannot Access Swagger UI:
- Ensure you're using `http://localhost:8000/docs` (not `https`)
- Try `http://127.0.0.1:8000/docs` instead
- Check if your firewall is blocking the connection

---

## Summary

Swagger UI provides an excellent way to:
- ✅ Test API endpoints interactively
- ✅ View detailed documentation
- ✅ See request/response examples
- ✅ Validate input constraints
- ✅ Debug error responses

All tests can be performed directly in the browser without writing any code!
