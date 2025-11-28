# MedMind Adherence Prediction API

FastAPI-based REST API for predicting medication adherence rates using machine learning.

## Project Structure

```
summative/API/
├── prediction.py          # Main FastAPI application
├── requirements.txt       # Python dependencies
├── test_setup.py         # Setup verification script
├── models/
│   ├── best_model.pkl    # Trained ML model (Random Forest)
│   └── scaler.pkl        # Feature scaler (StandardScaler)
└── README.md             # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Setup

```bash
python test_setup.py
```

This will verify:
- All required packages are installed
- Model and scaler files exist
- Model and scaler can be loaded
- Prediction module is properly configured

## Running the API

### Local Development

```bash
uvicorn prediction:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc

### Production

```bash
uvicorn prediction:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### GET /

Root endpoint providing API information.

**Response:**
```json
{
  "message": "MedMind Adherence Prediction API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

### GET /health

Health check endpoint to verify model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true
}
```

### POST /predict

Predict medication adherence rate based on patient features.

**Request Body:**
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

**Response (Success - 200):**
```json
{
  "predicted_adherence_rate": 82.3,
  "confidence": "high",
  "message": "Prediction successful"
}
```

**Response (Validation Error - 422):**
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is less than or equal to 120",
      "type": "value_error.number.not_le"
    }
  ]
}
```

## Input Validation

All input fields are validated with the following constraints:

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| age | int | 0-120 | Patient age in years |
| num_medications | int | 1-20 | Number of active medications |
| medication_complexity | float | 1.0-5.0 | Complexity score (1=simple, 5=complex) |
| days_since_start | int | ≥0 | Days since starting medication regimen |
| missed_doses_last_week | int | 0-50 | Number of missed doses in past 7 days |
| snooze_frequency | float | 0.0-1.0 | Proportion of reminders snoozed |
| chronic_conditions | int | 0-10 | Number of chronic health conditions |
| previous_adherence_rate | float | 0.0-100.0 | Historical adherence rate percentage |

## Testing with cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
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

## Dependencies

- **fastapi==0.104.1** - Modern web framework for building APIs
- **uvicorn==0.24.0** - ASGI server for running FastAPI
- **pydantic==2.5.0** - Data validation using Python type annotations
- **scikit-learn==1.7.2** - Machine learning library
- **numpy==2.3.5** - Numerical computing library
- **joblib==1.5.2** - Model serialization
- **python-multipart==0.0.6** - Form data parsing

## CORS Configuration

The API is configured to allow all origins for development. For production deployment, update the CORS middleware in `prediction.py` to restrict origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-flutter-app-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Logging

The API logs all prediction requests and errors. Logs include:
- Request timestamp
- Input data
- Prediction results
- Error messages and stack traces

## Error Handling

The API handles the following error scenarios:

1. **Validation Errors (422)**: Invalid input data (wrong type, out of range, missing fields)
2. **Model Loading Errors (500)**: Model or scaler files not found
3. **Prediction Errors (500)**: Unexpected errors during prediction

## Deployment

See the main project README for deployment instructions to Render, Railway, or other hosting platforms.

## Model Information

- **Algorithm**: Random Forest Regressor
- **Training Data**: Medication adherence dataset with 8 features
- **Performance**: See `summative/linear_regression/MODEL_COMPARISON_SUMMARY.md`
- **Feature Scaling**: StandardScaler (mean=0, std=1)

## Next Steps

1. Test the API locally using Swagger UI at http://localhost:8000/docs
2. Deploy to a hosting platform (Render, Railway, Heroku)
3. Integrate with Flutter mobile app
4. Monitor logs and performance in production
