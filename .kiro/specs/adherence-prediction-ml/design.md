# Design Document: Medication Adherence Rate Prediction System

## Overview

This design document outlines the architecture and implementation strategy for a machine learning-based medication adherence prediction system integrated into the MedMind application. The system will predict patient adherence rates using three regression algorithms (Linear Regression, Decision Trees, and Random Forest), expose predictions through a RESTful API, and integrate with the existing Flutter mobile application.

The prediction system addresses a critical healthcare challenge: by forecasting which patients are at risk of poor medication adherence, healthcare providers and patients can take proactive interventions. The system analyzes multiple factors including medication complexity, patient demographics, historical adherence patterns, and behavioral indicators to generate accurate predictions.

**Key Components:**
1. Machine Learning Pipeline (Jupyter Notebook)
2. Prediction API (FastAPI)
3. Mobile App Integration (Flutter)
4. Model Persistence and Deployment

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MedMind Flutter App                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Adherence Prediction Page                           │  │
│  │  - Input Fields (Age, Medications, etc.)             │  │
│  │  - Predict Button                                    │  │
│  │  - Result Display                                    │  │
│  └────────────────┬─────────────────────────────────────┘  │
└───────────────────┼─────────────────────────────────────────┘
                    │ HTTP POST /predict
                    │ JSON Request/Response
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Prediction Service                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORS Middleware                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Pydantic Input Validation                           │  │
│  │  - Type checking                                     │  │
│  │  - Range constraints                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Prediction Engine                                   │  │
│  │  - Load trained model                                │  │
│  │  - Preprocess input                                  │  │
│  │  - Generate prediction                               │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              Trained ML Model (Pickle/Joblib)                │
│  - Best performing model (LR/DT/RF)                         │
│  - Scaler for feature normalization                         │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Training Phase:**
   ```
   Raw Dataset → EDA & Visualization → Feature Engineering → 
   Train/Test Split → Model Training (LR, DT, RF) → 
   Model Evaluation → Best Model Selection → Model Serialization
   ```

2. **Prediction Phase:**
   ```
   User Input (Flutter) → API Request → Input Validation → 
   Feature Preprocessing → Model Prediction → 
   JSON Response → Display Result
   ```

## Components and Interfaces

### 1. Machine Learning Pipeline (Jupyter Notebook)

**Location:** `summative/linear_regression/multivariate.ipynb`

**Responsibilities:**
- Load and explore medication adherence dataset
- Perform exploratory data analysis with visualizations
- Engineer features and preprocess data
- Train three regression models
- Compare model performance
- Save the best-performing model

**Key Functions:**
```python
def load_dataset(filepath: str) -> pd.DataFrame
def visualize_correlations(df: pd.DataFrame) -> None
def preprocess_features(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]
def train_linear_regression(X_train, y_train) -> LinearRegression
def train_decision_tree(X_train, y_train) -> DecisionTreeRegressor
def train_random_forest(X_train, y_train) -> RandomForestRegressor
def evaluate_model(model, X_test, y_test) -> Dict[str, float]
def save_best_model(model, scaler, filepath: str) -> None
def predict_adherence(model, scaler, features: List[float]) -> float
```

### 2. FastAPI Prediction Service

**Location:** `summative/API/prediction.py`

**Responsibilities:**
- Expose RESTful API endpoint for predictions
- Validate input data with Pydantic models
- Load trained model and make predictions
- Handle errors gracefully
- Enable CORS for Flutter app

**API Endpoints:**

```python
POST /predict
Request Body:
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

Response (Success):
{
  "predicted_adherence_rate": 82.3,
  "confidence": "high",
  "message": "Prediction successful"
}

Response (Error):
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

**Pydantic Models:**

```python
class PredictionInput(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    num_medications: int = Field(..., ge=1, le=20, description="Number of active medications")
    medication_complexity: float = Field(..., ge=1.0, le=5.0, description="Complexity score (1=simple, 5=complex)")
    days_since_start: int = Field(..., ge=0, description="Days since starting medication regimen")
    missed_doses_last_week: int = Field(..., ge=0, le=50, description="Number of missed doses in past 7 days")
    snooze_frequency: float = Field(..., ge=0.0, le=1.0, description="Proportion of reminders snoozed")
    chronic_conditions: int = Field(..., ge=0, le=10, description="Number of chronic health conditions")
    previous_adherence_rate: float = Field(..., ge=0.0, le=100.0, description="Historical adherence rate percentage")

class PredictionOutput(BaseModel):
    predicted_adherence_rate: float
    confidence: str
    message: str
```

### 3. Flutter Mobile App Integration

**Location:** `summative/FlutterApp/`

**New Page:** `lib/features/adherence/presentation/pages/adherence_prediction_page.dart`

**Responsibilities:**
- Provide input form for prediction features
- Make HTTP POST requests to API
- Display prediction results
- Handle loading states and errors

**UI Components:**
- 8 TextFormField widgets (one per feature)
- ElevatedButton for "Predict" action
- Card widget for displaying results
- CircularProgressIndicator for loading state
- SnackBar for error messages

**HTTP Service:**
```dart
class AdherencePredictionService {
  final String baseUrl = 'https://your-api.render.com';
  
  Future<double> predictAdherence({
    required int age,
    required int numMedications,
    required double medicationComplexity,
    required int daysSinceStart,
    required int missedDosesLastWeek,
    required double snoozeFrequency,
    required int chronicConditions,
    required double previousAdherenceRate,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/predict'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'age': age,
        'num_medications': numMedications,
        'medication_complexity': medicationComplexity,
        'days_since_start': daysSinceStart,
        'missed_doses_last_week': missedDosesLastWeek,
        'snooze_frequency': snoozeFrequency,
        'chronic_conditions': chronicConditions,
        'previous_adherence_rate': previousAdherenceRate,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['predicted_adherence_rate'];
    } else {
      throw Exception('Failed to get prediction');
    }
  }
}
```

## Data Models

### Dataset Features

The medication adherence dataset will contain the following features:

| Feature Name | Type | Description | Range/Values |
|-------------|------|-------------|--------------|
| age | Integer | Patient age in years | 18-120 |
| num_medications | Integer | Number of active medications | 1-20 |
| medication_complexity | Float | Complexity score based on frequency and timing | 1.0-5.0 |
| days_since_start | Integer | Days since starting current regimen | 0-3650 |
| missed_doses_last_week | Integer | Number of missed doses in past 7 days | 0-50 |
| snooze_frequency | Float | Proportion of reminders snoozed (0-1) | 0.0-1.0 |
| chronic_conditions | Integer | Number of chronic health conditions | 0-10 |
| previous_adherence_rate | Float | Historical adherence rate percentage | 0.0-100.0 |
| **adherence_rate** | **Float** | **Target: Current adherence rate percentage** | **0.0-100.0** |

### Feature Engineering Rationale

1. **age**: Older patients may have different adherence patterns due to cognitive factors or experience
2. **num_medications**: Polypharmacy increases complexity and potential for non-adherence
3. **medication_complexity**: Captures the difficulty of the medication regimen (multiple times per day, with/without food, etc.)
4. **days_since_start**: Adherence often decreases over time as initial motivation wanes
5. **missed_doses_last_week**: Recent behavior is a strong predictor of future behavior
6. **snooze_frequency**: Indicates procrastination or difficulty with timing
7. **chronic_conditions**: More conditions may correlate with better or worse adherence depending on health awareness
8. **previous_adherence_rate**: Historical performance is typically the strongest predictor

### Data Preprocessing Pipeline

```python
# 1. Handle missing values
df = df.dropna()  # or use imputation if appropriate

# 2. Encode categorical variables (if any)
# (This dataset is primarily numeric)

# 3. Feature scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Feature Correlation Calculation Consistency
*For any* numeric dataset with features and a target variable, calculating feature correlations should produce values between -1 and 1, and the correlation of a feature with itself should equal 1.
**Validates: Requirements 2.3**

### Property 2: Missing Value Handling Completeness
*For any* dataset containing missing values, after preprocessing, the resulting dataset should contain zero missing values (either through imputation or removal).
**Validates: Requirements 3.1**

### Property 3: Categorical Encoding Transformation
*For any* dataset containing categorical columns, after encoding, all columns should be numeric (integer or float types only).
**Validates: Requirements 3.2**

### Property 4: Feature Standardization Properties
*For any* numeric feature after standardization using StandardScaler, the mean should be approximately 0 (within ±0.01) and the standard deviation should be approximately 1 (within ±0.01).
**Validates: Requirements 3.3**

### Property 5: Train-Test Split Proportions
*For any* dataset split with test_size=0.2, the test set should contain 20% (±1%) of the total samples and the train set should contain 80% (±1%) of the total samples.
**Validates: Requirements 3.5**

### Property 6: Model Selection by Minimum Loss
*For any* set of trained models with different MSE values, the model selected as "best" should be the one with the lowest test set MSE.
**Validates: Requirements 7.2**

### Property 7: Model Persistence Round-Trip
*For any* trained model, after saving to disk and loading back, making predictions on the same input should produce identical results (within floating-point precision).
**Validates: Requirements 7.3, 7.5**

### Property 8: Prediction Preprocessing Consistency
*For any* input data, the preprocessing applied during prediction should use the same scaler parameters (mean and std) as were fit during training, ensuring consistent feature scaling.
**Validates: Requirements 8.3**

### Property 9: Prediction Output Range Constraint
*For any* valid input features, the predicted adherence rate should be a float value between 0.0 and 100.0 (inclusive).
**Validates: Requirements 8.4**

### Property 10: API Input Validation Rejection
*For any* API request with input values that violate Pydantic constraints (wrong type or out of range), the API should return a 422 status code with validation error details.
**Validates: Requirements 9.4, 10.1, 10.2, 10.3**

### Property 11: Required Field Validation
*For any* API request missing one or more required fields, the API should return a 422 status code indicating which fields are missing.
**Validates: Requirements 10.4**

### Property 12: API Response Time Performance
*For any* valid prediction request to the deployed API, the response should be received within 5 seconds.
**Validates: Requirements 11.4**

### Property 13: Flutter Error Display on API Failure
*For any* API error response (4xx or 5xx status codes), the Flutter app should display a user-friendly error message rather than crashing or showing raw error data.
**Validates: Requirements 12.4**

### Property 14: Out-of-Range Validation Error Response
*For any* API request with numeric values outside defined ranges (e.g., age > 120), the API should return a 422 status with specific field-level error messages.
**Validates: Requirements 13.1**

### Property 15: Network Failure Error Handling
*For any* network request failure in the Flutter app (connection timeout, no internet), the app should display a connection error message to the user.
**Validates: Requirements 13.3**

### Property 16: Request Logging Completeness
*For any* prediction request received by the API (successful or failed), a log entry should be created containing the request timestamp, input data, and outcome.
**Validates: Requirements 13.5**

## Error Handling

### API Error Handling Strategy

1. **Validation Errors (422):**
   - Pydantic automatically validates input data
   - Returns detailed field-level error messages
   - Example: `{"detail": [{"loc": ["body", "age"], "msg": "ensure this value is less than or equal to 120"}]}`

2. **Model Loading Errors (500):**
   ```python
   try:
       model = joblib.load('best_model.pkl')
   except FileNotFoundError:
       raise HTTPException(status_code=500, detail="Model file not found. Please contact support.")
   ```

3. **Prediction Errors (500):**
   ```python
   try:
       prediction = model.predict(features)
   except Exception as e:
       logger.error(f"Prediction failed: {str(e)}")
       raise HTTPException(status_code=500, detail="Prediction failed. Please try again.")
   ```

4. **CORS Errors:**
   - Middleware configured to allow all origins during development
   - Production should restrict to specific Flutter app domains

### Flutter Error Handling Strategy

1. **Network Errors:**
   ```dart
   try {
     final response = await http.post(...).timeout(Duration(seconds: 10));
   } on TimeoutException {
     _showError('Request timed out. Please check your connection.');
   } on SocketException {
     _showError('No internet connection. Please try again.');
   }
   ```

2. **API Errors:**
   ```dart
   if (response.statusCode == 422) {
     final errors = jsonDecode(response.body)['detail'];
     _showError('Invalid input: ${errors[0]['msg']}');
   } else if (response.statusCode >= 500) {
     _showError('Server error. Please try again later.');
   }
   ```

3. **Input Validation:**
   ```dart
   if (_formKey.currentState!.validate()) {
     // Proceed with API call
   } else {
     _showError('Please fill all fields correctly.');
   }
   ```

### Model Training Error Handling

1. **Dataset Loading Errors:**
   - Verify file exists and is readable
   - Check for correct format (CSV, JSON, etc.)
   - Validate required columns are present

2. **Training Errors:**
   - Handle insufficient data (< 100 samples)
   - Catch convergence warnings
   - Validate model parameters are reasonable

3. **Evaluation Errors:**
   - Ensure test set is not empty
   - Handle edge cases (all predictions identical)
   - Validate metrics are computable (no division by zero)

## Testing Strategy

### Unit Testing

Unit tests will verify specific components and edge cases:

**Machine Learning Pipeline Tests:**
```python
def test_load_dataset_returns_dataframe():
    """Verify dataset loading returns a pandas DataFrame"""
    df = load_dataset('adherence_data.csv')
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_standardization_produces_zero_mean():
    """Verify StandardScaler produces mean ≈ 0"""
    X = np.array([[1, 2], [3, 4], [5, 6]])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    assert np.abs(X_scaled.mean()) < 0.01

def test_train_test_split_proportions():
    """Verify 80/20 split is correct"""
    X = np.random.rand(100, 5)
    y = np.random.rand(100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    assert len(X_test) == 20
    assert len(X_train) == 80
```

**API Tests:**
```python
def test_predict_endpoint_returns_200_for_valid_input():
    """Verify API returns 200 for valid input"""
    response = client.post('/predict', json={
        'age': 45,
        'num_medications': 3,
        'medication_complexity': 2.5,
        'days_since_start': 120,
        'missed_doses_last_week': 1,
        'snooze_frequency': 0.2,
        'chronic_conditions': 2,
        'previous_adherence_rate': 85.5
    })
    assert response.status_code == 200
    assert 'predicted_adherence_rate' in response.json()

def test_predict_endpoint_returns_422_for_invalid_age():
    """Verify API rejects age > 120"""
    response = client.post('/predict', json={
        'age': 150,  # Invalid
        'num_medications': 3,
        # ... other fields
    })
    assert response.status_code == 422

def test_predict_endpoint_returns_422_for_missing_field():
    """Verify API rejects requests with missing required fields"""
    response = client.post('/predict', json={
        'age': 45,
        # Missing other required fields
    })
    assert response.status_code == 422
```

**Flutter Widget Tests:**
```dart
testWidgets('Prediction page displays 8 input fields', (WidgetTester tester) async {
  await tester.pumpWidget(MaterialApp(home: AdherencePredictionPage()));
  
  expect(find.byType(TextFormField), findsNWidgets(8));
});

testWidgets('Predict button triggers API call', (WidgetTester tester) async {
  await tester.pumpWidget(MaterialApp(home: AdherencePredictionPage()));
  
  await tester.tap(find.text('Predict'));
  await tester.pump();
  
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});

testWidgets('Error message displayed on API failure', (WidgetTester tester) async {
  // Mock API to return error
  await tester.pumpWidget(MaterialApp(home: AdherencePredictionPage()));
  
  await tester.tap(find.text('Predict'));
  await tester.pumpAndSettle();
  
  expect(find.text('Failed to get prediction'), findsOneWidget);
});
```

### Property-Based Testing

Property-based tests will verify universal properties across many random inputs using a testing framework. For Python, we'll use `hypothesis`:

**Installation:**
```bash
pip install hypothesis
```

**Property Tests:**

```python
from hypothesis import given, strategies as st
import hypothesis.extra.numpy as npst

@given(npst.arrays(dtype=np.float64, shape=(100, 5)))
def test_property_standardization_zero_mean(X):
    """Property: Standardization should produce mean ≈ 0 for any numeric array"""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    assert np.abs(X_scaled.mean()) < 0.01

@given(st.integers(min_value=1, max_value=1000))
def test_property_train_test_split_proportions(n_samples):
    """Property: 80/20 split should hold for any dataset size"""
    X = np.random.rand(n_samples, 5)
    y = np.random.rand(n_samples)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    expected_test_size = int(n_samples * 0.2)
    assert abs(len(X_test) - expected_test_size) <= 1  # Allow ±1 for rounding

@given(
    st.integers(min_value=18, max_value=120),
    st.integers(min_value=1, max_value=20),
    st.floats(min_value=1.0, max_value=5.0),
    st.integers(min_value=0, max_value=3650),
    st.integers(min_value=0, max_value=50),
    st.floats(min_value=0.0, max_value=1.0),
    st.integers(min_value=0, max_value=10),
    st.floats(min_value=0.0, max_value=100.0)
)
def test_property_prediction_output_range(age, num_meds, complexity, days, missed, snooze, conditions, prev_rate):
    """Property: Predictions should always be between 0-100 for any valid input"""
    features = [age, num_meds, complexity, days, missed, snooze, conditions, prev_rate]
    prediction = predict_adherence(model, scaler, features)
    
    assert 0.0 <= prediction <= 100.0

@given(
    st.integers(min_value=121, max_value=200),  # Invalid age
    st.integers(min_value=1, max_value=20),
    st.floats(min_value=1.0, max_value=5.0),
    st.integers(min_value=0, max_value=3650),
    st.integers(min_value=0, max_value=50),
    st.floats(min_value=0.0, max_value=1.0),
    st.integers(min_value=0, max_value=10),
    st.floats(min_value=0.0, max_value=100.0)
)
def test_property_api_rejects_invalid_age(age, num_meds, complexity, days, missed, snooze, conditions, prev_rate):
    """Property: API should reject any age > 120"""
    response = client.post('/predict', json={
        'age': age,
        'num_medications': num_meds,
        'medication_complexity': complexity,
        'days_since_start': days,
        'missed_doses_last_week': missed,
        'snooze_frequency': snooze,
        'chronic_conditions': conditions,
        'previous_adherence_rate': prev_rate
    })
    assert response.status_code == 422

@given(st.data())
def test_property_model_persistence_round_trip(data):
    """Property: Save/load should preserve predictions for any input"""
    # Generate random valid input
    features = [
        data.draw(st.integers(min_value=18, max_value=120)),
        data.draw(st.integers(min_value=1, max_value=20)),
        data.draw(st.floats(min_value=1.0, max_value=5.0)),
        data.draw(st.integers(min_value=0, max_value=3650)),
        data.draw(st.integers(min_value=0, max_value=50)),
        data.draw(st.floats(min_value=0.0, max_value=1.0)),
        data.draw(st.integers(min_value=0, max_value=10)),
        data.draw(st.floats(min_value=0.0, max_value=100.0))
    ]
    
    # Predict with original model
    prediction_before = model.predict([features])[0]
    
    # Save and load model
    joblib.dump(model, 'temp_model.pkl')
    loaded_model = joblib.load('temp_model.pkl')
    
    # Predict with loaded model
    prediction_after = loaded_model.predict([features])[0]
    
    # Should be identical (within floating-point precision)
    assert np.abs(prediction_before - prediction_after) < 1e-10
```

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Full Prediction Pipeline:**
   - Load dataset → Preprocess → Train models → Select best → Save → Load → Predict
   - Verify entire pipeline executes without errors
   - Validate final prediction is reasonable

2. **API Integration:**
   - Start FastAPI server
   - Send prediction requests from test client
   - Verify responses match expected format
   - Test error scenarios (invalid input, missing model)

3. **Flutter-API Integration:**
   - Mock API responses in Flutter tests
   - Verify UI updates correctly based on responses
   - Test error handling flows

### Test Execution

**Python Tests:**
```bash
# Run unit tests
pytest tests/test_ml_pipeline.py -v

# Run property-based tests (100 iterations per property)
pytest tests/test_properties.py -v --hypothesis-show-statistics

# Run API tests
pytest tests/test_api.py -v

# Run all tests with coverage
pytest --cov=summative --cov-report=html
```

**Flutter Tests:**
```bash
# Run widget tests
flutter test

# Run with coverage
flutter test --coverage
```

### Testing Configuration

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

**hypothesis settings:**
```python
from hypothesis import settings, Verbosity

settings.register_profile("dev", max_examples=10, verbosity=Verbosity.verbose)
settings.register_profile("ci", max_examples=100, deadline=None)
settings.load_profile("dev")  # Use "ci" for continuous integration
```

## Implementation Plan

### Phase 1: Dataset Acquisition and EDA (Estimated: 2-3 hours)

1. Search for medication adherence datasets on Kaggle, Google Datasets, or data.gov
2. Download and load dataset into Jupyter notebook
3. Perform initial data exploration (shape, dtypes, missing values)
4. Create correlation heatmap
5. Generate distribution plots for key features
6. Document findings in markdown cells

### Phase 2: Data Preprocessing (Estimated: 1-2 hours)

1. Handle missing values (imputation or removal)
2. Encode categorical variables if present
3. Standardize numeric features using StandardScaler
4. Split data into train/test sets (80/20)
5. Save preprocessed data and scaler for later use

### Phase 3: Model Training and Evaluation (Estimated: 3-4 hours)

1. Implement Linear Regression model
   - Train on training set
   - Evaluate on test set
   - Plot actual vs predicted scatter plot
   - Calculate MSE and R-squared

2. Implement Decision Tree model
   - Train with hyperparameter tuning
   - Evaluate on test set
   - Visualize feature importance
   - Calculate MSE and R-squared

3. Implement Random Forest model
   - Train with 100+ estimators
   - Tune hyperparameters
   - Evaluate on test set
   - Visualize feature importance
   - Calculate MSE and R-squared

4. Compare all three models
   - Create comparison table
   - Select best model based on test MSE
   - Save best model and scaler to disk

### Phase 4: Prediction Function (Estimated: 1 hour)

1. Implement `predict_adherence()` function
2. Load saved model and scaler
3. Preprocess input features
4. Return prediction
5. Test on sample data points

### Phase 5: FastAPI Development (Estimated: 2-3 hours)

1. Set up FastAPI project structure
2. Create Pydantic models for input/output
3. Implement `/predict` POST endpoint
4. Add CORS middleware
5. Implement error handling
6. Add logging
7. Test locally with Swagger UI

### Phase 6: API Deployment (Estimated: 1-2 hours)

1. Create requirements.txt
2. Set up Render account (or alternative)
3. Configure deployment settings
4. Deploy API
5. Test public endpoint
6. Document public URL

### Phase 7: Flutter Integration (Estimated: 3-4 hours)

1. Create new prediction page in MedMind app
2. Design UI with 8 input fields
3. Implement HTTP service for API calls
4. Add form validation
5. Implement loading states
6. Add error handling
7. Test with deployed API

### Phase 8: Testing and Documentation (Estimated: 2-3 hours)

1. Write unit tests for ML pipeline
2. Write API tests
3. Write Flutter widget tests
4. Update README with:
   - Mission statement (4 lines max)
   - Dataset description and source
   - Public API URL
   - Instructions to run Flutter app
5. Create video demonstration (5 minutes max)

### Total Estimated Time: 15-22 hours

## Deployment Architecture

### API Hosting (Render)

```yaml
# render.yaml
services:
  - type: web
    name: medmind-adherence-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn prediction:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

### Environment Variables

```bash
# .env (not committed to git)
MODEL_PATH=./models/best_model.pkl
SCALER_PATH=./models/scaler.pkl
LOG_LEVEL=INFO
```

### File Structure

```
summative/
├── linear_regression/
│   ├── multivariate.ipynb          # Main notebook
│   ├── adherence_data.csv          # Dataset
│   ├── models/
│   │   ├── best_model.pkl          # Saved model
│   │   └── scaler.pkl              # Saved scaler
│   └── plots/
│       ├── correlation_heatmap.png
│       ├── feature_distributions.png
│       ├── actual_vs_predicted.png
│       └── feature_importance.png
│
├── API/
│   ├── prediction.py               # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── models/
│   │   ├── best_model.pkl          # Copy of trained model
│   │   └── scaler.pkl              # Copy of scaler
│   └── tests/
│       ├── test_api.py
│       └── test_properties.py
│
└── FlutterApp/
    └── lib/
        └── features/
            └── adherence/
                └── presentation/
                    ├── pages/
                    │   └── adherence_prediction_page.dart
                    └── services/
                        └── prediction_service.dart
```

## Security Considerations

1. **API Security:**
   - Input validation prevents injection attacks
   - Rate limiting should be added for production
   - HTTPS enforced by hosting platform
   - No sensitive data stored in API

2. **Model Security:**
   - Model file integrity checks
   - Version control for model updates
   - Monitoring for prediction anomalies

3. **Flutter App Security:**
   - API key not required (public endpoint)
   - Input sanitization before API calls
   - Secure HTTP connections only

## Performance Optimization

1. **Model Loading:**
   - Load model once at startup, not per request
   - Use global variable or dependency injection

2. **Prediction Speed:**
   - Preprocessing should be < 1ms
   - Model inference should be < 10ms
   - Total API response < 100ms (excluding network)

3. **API Optimization:**
   - Use async/await for non-blocking operations
   - Implement caching for repeated predictions
   - Monitor response times with logging

## Monitoring and Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.post("/predict")
async def predict(input_data: PredictionInput):
    logger.info(f"Prediction request received: {input_data.dict()}")
    try:
        prediction = make_prediction(input_data)
        logger.info(f"Prediction successful: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

## Future Enhancements

1. **Model Improvements:**
   - Implement deep learning models (Neural Networks)
   - Add ensemble methods (Gradient Boosting, XGBoost)
   - Incorporate time-series analysis for temporal patterns

2. **Feature Enhancements:**
   - Real-time adherence tracking integration
   - Personalized intervention recommendations
   - Multi-user prediction batching

3. **API Enhancements:**
   - Authentication and authorization
   - Rate limiting and quotas
   - Prediction confidence intervals
   - Model versioning and A/B testing

4. **Mobile App Enhancements:**
   - Save prediction history
   - Visualize adherence trends
   - Push notifications for low predicted adherence
   - Integration with existing MedMind features

## Conclusion

This design provides a comprehensive blueprint for implementing a medication adherence prediction system that seamlessly integrates with the MedMind application. By following Clean Architecture principles and implementing robust testing strategies, the system will be maintainable, scalable, and reliable. The use of industry-standard tools (scikit-learn, FastAPI, Flutter) ensures compatibility and ease of deployment.
