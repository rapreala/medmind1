# API Integration Guide for Prediction Function

## Overview

This guide provides instructions for integrating the `predict_adherence()` function into the FastAPI service (Tasks 9-13).

## Quick Start

### Import the Function

```python
from predict_adherence import predict_adherence, predict_adherence_batch
```

### Basic Usage in FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from predict_adherence import predict_adherence

app = FastAPI()

class PredictionInput(BaseModel):
    age: int = Field(..., ge=0, le=120)
    num_medications: int = Field(..., ge=1, le=20)
    medication_complexity: float = Field(..., ge=1.0, le=5.0)
    days_since_start: int = Field(..., ge=0)
    missed_doses_last_week: int = Field(..., ge=0, le=50)
    snooze_frequency: float = Field(..., ge=0.0, le=1.0)
    chronic_conditions: int = Field(..., ge=0, le=10)
    previous_adherence_rate: float = Field(..., ge=0.0, le=100.0)

class PredictionOutput(BaseModel):
    predicted_adherence_rate: float
    confidence: str
    message: str

@app.post("/predict", response_model=PredictionOutput)
async def predict_endpoint(input_data: PredictionInput):
    try:
        prediction = predict_adherence(
            age=input_data.age,
            num_medications=input_data.num_medications,
            medication_complexity=input_data.medication_complexity,
            days_since_start=input_data.days_since_start,
            missed_doses_last_week=input_data.missed_doses_last_week,
            snooze_frequency=input_data.snooze_frequency,
            chronic_conditions=input_data.chronic_conditions,
            previous_adherence_rate=input_data.previous_adherence_rate
        )
        
        # Determine confidence level based on prediction
        if prediction >= 80:
            confidence = "high"
        elif prediction >= 60:
            confidence = "medium"
        else:
            confidence = "low"
        
        return PredictionOutput(
            predicted_adherence_rate=round(prediction, 2),
            confidence=confidence,
            message="Prediction successful"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Function Specifications

### predict_adherence()

**Purpose**: Predict adherence rate for a single patient

**Parameters**:
- `age` (int/float): Patient age in years (0-150)
- `num_medications` (int/float): Number of active medications (0-50)
- `medication_complexity` (float): Complexity score (0.0-10.0)
- `days_since_start` (int/float): Days since starting regimen (≥0)
- `missed_doses_last_week` (int/float): Missed doses in past week (≥0)
- `snooze_frequency` (float): Proportion of reminders snoozed (0.0-1.0)
- `chronic_conditions` (int/float): Number of chronic conditions (≥0)
- `previous_adherence_rate` (float): Historical adherence rate (0.0-100.0)
- `model_path` (str, optional): Path to model file (default: 'models/best_model.pkl')
- `scaler_path` (str, optional): Path to scaler file (default: 'models/scaler.pkl')

**Returns**: `float` - Predicted adherence rate (0.0-100.0)

**Raises**:
- `FileNotFoundError`: If model or scaler files not found
- `ValueError`: If input values are invalid
- `RuntimeError`: If model loading fails

### predict_adherence_batch()

**Purpose**: Predict adherence rates for multiple patients efficiently

**Parameters**:
- `features_list` (List[List[float]]): List of feature arrays
- `model_path` (str, optional): Path to model file
- `scaler_path` (str, optional): Path to scaler file

**Returns**: `List[float]` - List of predicted adherence rates

## Error Handling

### Common Errors and Solutions

1. **FileNotFoundError: Model file not found**
   - Ensure `models/best_model.pkl` exists
   - Check working directory
   - Use absolute paths if needed

2. **ValueError: Input out of range**
   - Validate input before calling function
   - Use Pydantic models for automatic validation

3. **RuntimeError: Error loading model**
   - Check model file integrity
   - Verify scikit-learn version compatibility
   - Ensure joblib is installed

### Example Error Handling

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

@app.post("/predict")
async def predict_endpoint(input_data: PredictionInput):
    try:
        prediction = predict_adherence(**input_data.dict())
        return {"predicted_adherence_rate": prediction}
    
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise HTTPException(
            status_code=500,
            detail="Model file not found. Please contact support."
        )
    
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(
            status_code=422,
            detail=f"Invalid input: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Please try again."
        )
```

## Model Files Setup

### For Local Development

```bash
# Ensure model files are in the correct location
ls -lh models/
# Should show:
# best_model.pkl (trained Random Forest model)
# scaler.pkl (StandardScaler)
```

### For Deployment

1. **Copy model files to API directory**:
```bash
mkdir -p summative/API/models
cp summative/linear_regression/models/best_model.pkl summative/API/models/
cp summative/linear_regression/models/scaler.pkl summative/API/models/
```

2. **Update paths in API code**:
```python
# Option 1: Use relative paths
prediction = predict_adherence(
    ...,
    model_path='models/best_model.pkl',
    scaler_path='models/scaler.pkl'
)

# Option 2: Use absolute paths
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')
```

## Testing the Integration

### Test with curl

```bash
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
```

Expected response:
```json
{
  "predicted_adherence_rate": 55.18,
  "confidence": "low",
  "message": "Prediction successful"
}
```

### Test with Python requests

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "age": 45,
    "num_medications": 3,
    "medication_complexity": 2.5,
    "days_since_start": 120,
    "missed_doses_last_week": 1,
    "snooze_frequency": 0.2,
    "chronic_conditions": 2,
    "previous_adherence_rate": 85.5
}

response = requests.post(url, json=data)
print(response.json())
```

## Performance Considerations

### Single vs Batch Predictions

- **Single prediction**: ~10-50ms per request
- **Batch prediction**: ~5-10ms per patient (more efficient)

### Optimization Tips

1. **Load model once at startup**:
```python
import joblib

# Load at startup
model = joblib.load('models/best_model.pkl')
scaler = joblib.load('models/scaler.pkl')

@app.post("/predict")
async def predict_endpoint(input_data: PredictionInput):
    # Use pre-loaded model
    features = scaler.transform([[...]])
    prediction = model.predict(features)[0]
    return {"predicted_adherence_rate": prediction}
```

2. **Use batch endpoint for multiple predictions**:
```python
@app.post("/predict/batch")
async def predict_batch_endpoint(inputs: List[PredictionInput]):
    features_list = [[i.age, i.num_medications, ...] for i in inputs]
    predictions = predict_adherence_batch(features_list)
    return {"predictions": predictions}
```

## Validation Rules

### Input Constraints (from Design Document)

| Field | Type | Min | Max | Description |
|-------|------|-----|-----|-------------|
| age | int | 0 | 120 | Patient age in years |
| num_medications | int | 1 | 20 | Number of medications |
| medication_complexity | float | 1.0 | 5.0 | Complexity score |
| days_since_start | int | 0 | ∞ | Days since starting |
| missed_doses_last_week | int | 0 | 50 | Missed doses |
| snooze_frequency | float | 0.0 | 1.0 | Snooze proportion |
| chronic_conditions | int | 0 | 10 | Number of conditions |
| previous_adherence_rate | float | 0.0 | 100.0 | Historical rate |

### Pydantic Validation Example

```python
from pydantic import BaseModel, Field, validator

class PredictionInput(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    num_medications: int = Field(..., ge=1, le=20, description="Number of medications")
    medication_complexity: float = Field(..., ge=1.0, le=5.0, description="Complexity score")
    days_since_start: int = Field(..., ge=0, description="Days since starting regimen")
    missed_doses_last_week: int = Field(..., ge=0, le=50, description="Missed doses")
    snooze_frequency: float = Field(..., ge=0.0, le=1.0, description="Snooze proportion")
    chronic_conditions: int = Field(..., ge=0, le=10, description="Number of conditions")
    previous_adherence_rate: float = Field(..., ge=0.0, le=100.0, description="Historical rate")
    
    @validator('medication_complexity')
    def validate_complexity(cls, v):
        if not 1.0 <= v <= 5.0:
            raise ValueError('Medication complexity must be between 1.0 and 5.0')
        return v
```

## Next Steps

1. **Task 9**: Set up FastAPI project structure
   - Create `summative/API/` directory
   - Create `prediction.py` file
   - Copy model files to `summative/API/models/`

2. **Task 10**: Implement Pydantic models (see examples above)

3. **Task 11**: Implement FastAPI endpoint (see Quick Start)

4. **Task 12**: Add CORS and logging

5. **Task 13**: Deploy to Render/Railway

## Resources

- **Prediction Function**: `summative/linear_regression/predict_adherence.py`
- **Test Suite**: `summative/linear_regression/test_prediction_function.py`
- **Model Files**: `summative/linear_regression/models/`
- **Design Document**: `.kiro/specs/adherence-prediction-ml/design.md`

## Support

For issues or questions:
1. Check error logs
2. Verify model files exist
3. Validate input data
4. Review test cases in `test_prediction_function.py`

---

**Status**: ✅ Ready for FastAPI Integration (Tasks 9-13)
