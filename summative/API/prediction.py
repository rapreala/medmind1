"""
FastAPI application for medication adherence prediction.

This module provides a RESTful API endpoint for predicting patient medication
adherence rates using a trained machine learning model.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MedMind Adherence Prediction API",
    description="API for predicting medication adherence rates using machine learning",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and scaler
model = None
scaler = None

# Model paths
MODEL_PATH = Path(__file__).parent / "models" / "best_model.pkl"
SCALER_PATH = Path(__file__).parent / "models" / "scaler.pkl"


class PredictionInput(BaseModel):
    """Input model for adherence prediction requests."""
    
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years"
    )
    num_medications: int = Field(
        ...,
        ge=1,
        le=20,
        description="Number of active medications"
    )
    medication_complexity: float = Field(
        ...,
        ge=1.0,
        le=5.0,
        description="Complexity score (1=simple, 5=complex)"
    )
    days_since_start: int = Field(
        ...,
        ge=0,
        description="Days since starting medication regimen"
    )
    missed_doses_last_week: int = Field(
        ...,
        ge=0,
        le=50,
        description="Number of missed doses in past 7 days"
    )
    snooze_frequency: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Proportion of reminders snoozed"
    )
    chronic_conditions: int = Field(
        ...,
        ge=0,
        le=10,
        description="Number of chronic health conditions"
    )
    previous_adherence_rate: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Historical adherence rate percentage"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "num_medications": 3,
                "medication_complexity": 2.5,
                "days_since_start": 120,
                "missed_doses_last_week": 1,
                "snooze_frequency": 0.2,
                "chronic_conditions": 2,
                "previous_adherence_rate": 85.5
            }
        }


class PredictionOutput(BaseModel):
    """Output model for adherence prediction responses."""
    
    predicted_adherence_rate: float = Field(
        ...,
        description="Predicted adherence rate percentage (0-100)"
    )
    confidence: str = Field(
        ...,
        description="Confidence level of prediction"
    )
    message: str = Field(
        ...,
        description="Status message"
    )


@app.on_event("startup")
async def load_model():
    """Load the trained model and scaler at startup."""
    global model, scaler
    
    try:
        logger.info(f"Loading model from {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully")
        
        logger.info(f"Loading scaler from {SCALER_PATH}")
        scaler = joblib.load(SCALER_PATH)
        logger.info("Scaler loaded successfully")
        
    except FileNotFoundError as e:
        logger.error(f"Model or scaler file not found: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Error loading model or scaler: {e}", exc_info=True)
        raise


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "MedMind Adherence Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_loaded = model is not None
    scaler_loaded = scaler is not None
    
    return {
        "status": "healthy" if (model_loaded and scaler_loaded) else "unhealthy",
        "model_loaded": model_loaded,
        "scaler_loaded": scaler_loaded
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict_adherence(input_data: PredictionInput):
    """
    Predict medication adherence rate based on patient features.
    
    Args:
        input_data: Patient features for prediction
        
    Returns:
        PredictionOutput: Predicted adherence rate and metadata
        
    Raises:
        HTTPException: If model is not loaded or prediction fails
    """
    # Check if model and scaler are loaded
    if model is None or scaler is None:
        logger.error("Model or scaler not loaded")
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Please contact support."
        )
    
    try:
        # Log the prediction request
        logger.info(f"Prediction request received: {input_data.dict()}")
        
        # Prepare features in the correct order
        features = np.array([[
            input_data.age,
            input_data.num_medications,
            input_data.medication_complexity,
            input_data.days_since_start,
            input_data.missed_doses_last_week,
            input_data.snooze_frequency,
            input_data.chronic_conditions,
            input_data.previous_adherence_rate
        ]])
        
        # Preprocess features using the scaler
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Ensure prediction is within valid range
        prediction = float(np.clip(prediction, 0.0, 100.0))
        
        # Determine confidence level based on prediction value
        if prediction >= 80:
            confidence = "high"
        elif prediction >= 60:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Log the prediction result
        logger.info(f"Prediction successful: {prediction:.2f}%")
        
        return PredictionOutput(
            predicted_adherence_rate=round(prediction, 2),
            confidence=confidence,
            message="Prediction successful"
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
