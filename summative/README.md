# MedMind Adherence Prediction System

## Mission Statement

MedMind's ML-powered adherence prediction system forecasts patient medication-taking behavior using advanced regression algorithms. By analyzing patient demographics, medication complexity, and behavioral patterns, the system identifies at-risk patients before adherence deteriorates, enabling proactive healthcare interventions and personalized support. This predictive capability addresses the critical challenge of medication non-adherence, which affects 50% of chronic disease patients globally and costs healthcare systems $100-$289 billion annually.

## Dataset Description

**Dataset Name:** Medication Adherence Prediction Dataset

**Source:** Synthetic dataset generated based on realistic patient behavior patterns and clinical research on medication adherence factors

**Description:** This dataset contains 1,500 patient records with 8 distinct features that influence medication adherence rates. The data simulates real-world scenarios where patient demographics, medication characteristics, temporal factors, and behavioral indicators combine to predict adherence outcomes.

**Relevance to Medication Adherence:** The dataset captures key factors identified in clinical research as primary drivers of medication adherence:
- **Patient Demographics:** Age influences cognitive ability and health awareness
- **Medication Burden:** Number and complexity of medications affect adherence difficulty
- **Temporal Patterns:** Adherence typically decreases over time (medication fatigue)
- **Behavioral Indicators:** Recent missed doses and snooze patterns predict future behavior
- **Health Context:** Chronic conditions impact motivation and adherence patterns
- **Historical Performance:** Past adherence is the strongest predictor of future adherence

**Dataset Statistics:**
- Total Records: 1,500 patients
- Features: 8 input features + 1 target variable
- Target Variable: `adherence_rate` (continuous, 0-100%)
- Missing Values: ~2% in 3 columns (realistic scenario)
- Data Quality: Validated ranges, realistic distributions

**Features:**
1. `age` - Patient age in years (18-120)
2. `num_medications` - Number of active medications (1-20)
3. `medication_complexity` - Medication regimen complexity score (1.0-5.0)
4. `days_since_start` - Days since starting current regimen (0-3650)
5. `missed_doses_last_week` - Number of missed doses in past 7 days (0-50)
6. `snooze_frequency` - Proportion of medication reminders snoozed (0.0-1.0)
7. `chronic_conditions` - Number of chronic health conditions (0-10)
8. `previous_adherence_rate` - Historical adherence rate percentage (0.0-100.0)

## Project Structure

```
summative/
├── linear_regression/
│   ├── multivariate.ipynb          # Main ML pipeline notebook
│   ├── adherence_data.csv          # Dataset (1500 records)
│   ├── generate_dataset.py         # Dataset generation script
│   ├── models/                     # Trained models directory
│   └── plots/                      # Visualization outputs
│
├── API/
│   ├── prediction.py               # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── models/                     # Deployed models
│   └── tests/                      # API tests
│
└── FlutterApp/
    └── lib/features/adherence/     # Flutter integration
```

## API Endpoint

**🌐 Public URL:** `https://medmind-adherence-api.onrender.com`

**📚 Swagger UI:** `https://medmind-adherence-api.onrender.com/docs`

**✅ Status:** Live and operational (Deployed on Render)

**Example Request:**
```bash
curl -X POST "https://medmind-adherence-api.onrender.com/predict" \
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

**Example Response:**
```json
{
  "predicted_adherence_rate": 82.3,
  "confidence": "high",
  "message": "Prediction successful"
}
```

## Running the Flutter App

### Prerequisites
- Flutter SDK 3.24.0 or higher
- Dart SDK 3.8.0 or higher
- Android Studio / Xcode (for mobile development)
- A physical device or emulator

### Installation Steps

1. **Navigate to the project root directory:**
   ```bash
   cd /path/to/medmind
   ```

2. **Install Flutter dependencies:**
   ```bash
   flutter pub get
   ```

3. **Verify Flutter installation:**
   ```bash
   flutter doctor
   ```

4. **Run the application:**
   ```bash
   flutter run
   ```
   
   Or for a specific device:
   ```bash
   flutter run -d <device_id>
   ```

5. **Access the Adherence Prediction feature:**
   - Launch the MedMind app
   - Navigate to the Dashboard
   - Tap on "Adherence Prediction" in the menu
   - Enter patient data (age, medications, etc.)
   - Tap "Predict" to get the adherence forecast

### Testing the Prediction Feature

Use these sample inputs to test the prediction:
```
Age: 45
Number of Medications: 3
Medication Complexity: 2.5
Days Since Start: 120
Missed Doses Last Week: 1
Snooze Frequency: 0.2
Chronic Conditions: 2
Previous Adherence Rate: 85.5
```

Expected prediction: ~55% adherence rate

## Video Demonstration

**📹 YouTube Link:** [Click here to watch the 5-minute demonstration](YOUR_YOUTUBE_URL_HERE)

**Video Contents:**
- ✅ Mobile app demonstration with various prediction inputs
- ✅ Swagger UI testing (valid inputs, type validation, range validation)
- ✅ Jupyter notebook walkthrough with model training code
- ✅ Model performance comparison (Linear Regression, Decision Trees, Random Forest)
- ✅ Loss metrics discussion (MSE, R-squared)
- ✅ Model selection justification
- ✅ API code walkthrough (prediction endpoint implementation)
- ✅ Flutter code walkthrough (API integration)

**Instructions to Record:**
See `summative/VIDEO_DEMONSTRATION_GUIDE.md` for a detailed script and recording guide.

**After Recording:**
1. Upload video to YouTube (Public or Unlisted)
2. Replace `YOUR_YOUTUBE_URL_HERE` above with your actual YouTube URL
3. Ensure video is accessible and meets all requirements

## Dependencies and Versions

### Python Dependencies (ML Pipeline & API)

**Core ML Libraries:**
- `scikit-learn >= 1.3.0, < 2.0.0` - Machine learning algorithms (Random Forest, Decision Tree, Linear Regression)
- `numpy >= 1.24.0, < 2.0.0` - Numerical computing and array operations
- `pandas >= 2.0.0` - Data manipulation and analysis
- `joblib >= 1.3.0, < 2.0.0` - Model serialization and persistence

**Visualization:**
- `matplotlib >= 3.7.0` - Plotting and visualization
- `seaborn >= 0.12.0` - Statistical data visualization

**API Framework:**
- `fastapi >= 0.104.0, < 0.116.0` - Modern web framework for building APIs
- `uvicorn[standard] >= 0.24.0, < 0.33.0` - ASGI server for running FastAPI
- `pydantic >= 2.5.0, < 3.0.0` - Data validation using type annotations
- `python-multipart >= 0.0.6` - Form data parsing support

### Flutter Dependencies

**Core Framework:**
- `flutter: sdk: flutter` - Flutter SDK (>= 3.24.0)
- `dart: sdk: ^3.8.0` - Dart SDK

**State Management:**
- `flutter_bloc: ^8.1.6` - BLoC pattern implementation for state management
- `equatable: ^2.0.5` - Value equality for Dart objects

**Dependency Injection:**
- `get_it: ^7.7.0` - Service locator for dependency injection
- `injectable: ^2.4.4` - Code generation for dependency injection

**Backend Integration:**
- `firebase_core: ^3.6.0` - Firebase core functionality
- `firebase_auth: ^5.3.1` - Firebase authentication
- `cloud_firestore: ^5.4.4` - Cloud Firestore database
- `firebase_storage: ^12.3.4` - Firebase cloud storage
- `google_sign_in: ^6.2.2` - Google Sign-In authentication

**Network & HTTP:**
- `http: ^1.2.2` - HTTP client for API requests (used for ML predictions)

**Local Storage:**
- `shared_preferences: ^2.3.2` - Key-value storage for local data

**Notifications:**
- `flutter_local_notifications: ^17.2.3` - Local notification support
- `timezone: ^0.9.4` - Timezone data for scheduled notifications

**UI & Visualization:**
- `fl_chart: ^0.69.0` - Beautiful charts and graphs
- `cupertino_icons: ^1.0.8` - iOS-style icons

**Utilities:**
- `intl: ^0.19.0` - Internationalization and date formatting
- `dartz: ^0.10.1` - Functional programming utilities
- `permission_handler: ^11.3.1` - Runtime permission handling
- `mobile_scanner: ^5.2.3` - Barcode and QR code scanning

**Development Dependencies:**
- `flutter_test: sdk: flutter` - Flutter testing framework
- `flutter_lints: ^5.0.0` - Recommended lints for Flutter
- `build_runner: ^2.4.0` - Code generation tool
- `injectable_generator: ^2.6.2` - Injectable code generator
- `mockito: ^5.4.4` - Mocking framework for tests
- `bloc_test: ^9.1.7` - Testing utilities for BLoC

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd medmind
```

### 2. Python Environment Setup (ML Pipeline & API)

**Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Install Python dependencies:**
```bash
pip install -r summative/API/requirements.txt
```

**Verify installation:**
```bash
cd summative/API
python test_setup.py
```

### 3. Flutter Environment Setup

**Install Flutter dependencies:**
```bash
flutter pub get
```

**Verify Flutter installation:**
```bash
flutter doctor
```

**Run code generation (if needed):**
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### 4. Firebase Configuration (Optional)

If using Firebase features:
1. Create a Firebase project at https://console.firebase.google.com
2. Download `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
3. Place configuration files in appropriate directories
4. Update Firebase configuration in `lib/config/firebase_config.dart`

## Development Guide

### Machine Learning Pipeline

**1. Generate Dataset:**
```bash
cd summative/linear_regression
python generate_dataset.py
```

**2. Run Jupyter Notebook:**
```bash
jupyter notebook multivariate.ipynb
```

Or run individual pipeline steps:
```bash
python run_eda.py                    # Exploratory Data Analysis
python run_linear_regression.py     # Train Linear Regression
python run_decision_tree.py         # Train Decision Tree
python run_random_forest.py         # Train Random Forest
python compare_and_select_model.py  # Compare and select best model
```

**3. Test Prediction Function:**
```bash
python test_prediction_function.py
```

### API Development

**Run API locally:**
```bash
cd summative/API
uvicorn prediction:app --reload
```

**Access API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

**Run API tests:**
```bash
python test_api_endpoint.py
python test_pydantic_models.py
python test_cors_logging.py
```

**Test deployed API:**
```bash
python test_deployed_api.py https://medmind-adherence-api.onrender.com
```

### Flutter Development

**Run in debug mode:**
```bash
flutter run
```

**Run tests:**
```bash
flutter test
```

**Run specific test file:**
```bash
flutter test test/features/adherence/presentation/prediction_service_test.dart
```

**Build for production:**
```bash
flutter build apk          # Android
flutter build ios          # iOS
flutter build web          # Web
```

## Model Performance Summary

### Models Compared

Three regression algorithms were trained and evaluated:

| Model | Test MSE | Test R² | Test RMSE | Training Time |
|-------|----------|---------|-----------|---------------|
| Linear Regression | 95.74 | 0.6571 | 9.78 | 0.001s |
| Decision Tree | 72.81 | 0.7392 | 8.53 | 5.77s |
| **Random Forest** | **31.56** | **0.8869** | **5.62** | **102.14s** |

### Selected Model: Random Forest

**Why Random Forest?**
- ✅ **Lowest prediction error**: Test MSE of 31.56 (67% better than Linear Regression)
- ✅ **Highest accuracy**: Explains 88.7% of variance in adherence rates (R² = 0.8869)
- ✅ **Best generalization**: Predictions are off by only ~5.6 percentage points on average
- ✅ **Robust ensemble**: Combines 300 decision trees to reduce overfitting
- ✅ **Feature insights**: Identifies key factors affecting adherence

**Top Features by Importance:**
1. Missed doses last week (57.61%)
2. Previous adherence rate (16.49%)
3. Number of medications (9.72%)
4. Medication complexity (8.10%)

**Model Details:**
- Algorithm: Random Forest Regressor with 300 estimators
- Training samples: 1,431 patient records
- Features: 8 input variables
- Preprocessing: StandardScaler (mean=0, std=1)
- Saved model size: 13.97 MB

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MedMind Flutter App                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Adherence Prediction Page                           │  │
│  │  - 8 Input Fields (Age, Medications, etc.)           │  │
│  │  - Predict Button                                    │  │
│  │  - Result Display Card                               │  │
│  └────────────────┬─────────────────────────────────────┘  │
└───────────────────┼─────────────────────────────────────────┘
                    │ HTTP POST /predict
                    │ JSON Request/Response
                    ▼
┌─────────────────────────────────────────────────────────────┐
│         FastAPI Prediction Service (Render)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORS Middleware + Input Validation (Pydantic)       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Prediction Engine                                   │  │
│  │  - Load Random Forest model (13.97 MB)              │  │
│  │  - Preprocess with StandardScaler                   │  │
│  │  - Generate prediction (0-100%)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Testing

### Python Tests
```bash
cd summative/linear_regression
python test_preprocessing.py
python test_prediction_function.py
python test_best_model.py

cd ../API
python test_api_endpoint.py
python test_pydantic_models.py
python test_deployed_api.py https://medmind-adherence-api.onrender.com
```

### Flutter Tests
```bash
flutter test test/features/adherence/presentation/prediction_service_test.dart
flutter test test/features/adherence/presentation/adherence_prediction_navigation_test.dart
```

## Troubleshooting

### API Issues

**Problem: API returns 500 error**
- Check that model files exist in `summative/API/models/`
- Verify model and scaler load correctly: `python test_setup.py`

**Problem: API returns 422 validation error**
- Verify all 8 required fields are present in request
- Check that values are within valid ranges (see Input Validation table)

**Problem: Slow API response (cold start)**
- Free tier services spin down after 15 minutes of inactivity
- First request may take 30-60 seconds
- Subsequent requests are fast (2-3 seconds)

### Flutter Issues

**Problem: Network error when calling API**
- Verify internet connection
- Check API URL is correct: `https://medmind-adherence-api.onrender.com`
- Test API directly with curl to confirm it's accessible

**Problem: Build errors**
- Run `flutter clean`
- Run `flutter pub get`
- Run `flutter pub run build_runner build --delete-conflicting-outputs`

## Contributing

This project is part of the MedMind application for educational purposes. For questions or issues, please refer to the project documentation.

## License

Educational project - MedMind Medication Adherence Application
