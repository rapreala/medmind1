# Video Demonstration Guide - MedMind Adherence Prediction ML

## Overview
This guide provides a detailed script for creating the 5-minute video demonstration required for the adherence prediction ML feature.

**Requirements:**
- Maximum duration: 5 minutes
- Presenter camera visible throughout
- Cover all components: Mobile App, API (Swagger UI), Jupyter Notebook, Code walkthrough

---

## Pre-Recording Checklist

### Setup Required:
- [ ] Flutter app running on emulator/device
- [ ] API deployed and accessible at: https://medmind-adherence-api.onrender.com
- [ ] Swagger UI accessible at: https://medmind-adherence-api.onrender.com/docs
- [ ] Jupyter notebook open: `summative/linear_regression/multivariate.ipynb`
- [ ] Code editor open with:
  - `summative/API/prediction.py`
  - `lib/features/adherence/presentation/pages/adherence_prediction_page.dart`
  - `lib/features/adherence/presentation/services/prediction_service.dart`
- [ ] Screen recording software ready
- [ ] Camera positioned and visible
- [ ] Good lighting and audio

---

## Video Script (5 Minutes)

### Segment 1: Introduction (30 seconds)

**[Camera visible, show your face]**

"Hello! I'm [Your Name], and today I'll demonstrate the Medication Adherence Prediction system I built for MedMind. This system uses machine learning to predict patient medication adherence rates based on multiple factors. I'll show you the mobile app, the API, the machine learning models, and walk through the code."

---

### Segment 2: Mobile App Demonstration (1 minute)

**[Screen: Flutter app on emulator/device, camera still visible in corner]**

"Let's start with the mobile app. Here's the Adherence Prediction page in the MedMind Flutter application."

**Actions:**
1. Navigate to the prediction page from the dashboard
2. Show the 8 input fields:
   - Age: 45
   - Number of Medications: 3
   - Medication Complexity: 2.5
   - Days Since Start: 120
   - Missed Doses Last Week: 1
   - Snooze Frequency: 0.2
   - Chronic Conditions: 2
   - Previous Adherence Rate: 85.5

3. Click "Predict" button
4. Show loading indicator
5. Display prediction result (e.g., "Predicted Adherence Rate: 82.3%")

**Narration:**
"I'll enter valid patient data and request a prediction. The app sends this data to our FastAPI backend, which uses the trained machine learning model to generate a prediction. As you can see, the predicted adherence rate is 82.3%."

**Test another scenario:**
6. Enter different values (e.g., higher missed doses, lower previous adherence)
7. Show how prediction changes

---

### Segment 3: API Testing with Swagger UI (1.5 minutes)

**[Screen: Swagger UI at /docs endpoint]**

"Now let's test the API directly using Swagger UI, which provides interactive API documentation."

#### Test 1: Valid Input
**Actions:**
1. Open POST /predict endpoint
2. Click "Try it out"
3. Enter valid JSON:
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
4. Click "Execute"
5. Show 200 response with prediction

**Narration:**
"With valid input, the API returns a 200 status code and the predicted adherence rate."

#### Test 2: Data Type Validation (Wrong Types)
**Actions:**
1. Modify JSON to have wrong type:
```json
{
  "age": "forty-five",
  "num_medications": 3,
  ...
}
```
2. Click "Execute"
3. Show 422 Unprocessable Entity response
4. Highlight validation error message

**Narration:**
"When I send a string instead of an integer for age, the API correctly rejects it with a 422 status and provides a detailed error message explaining the validation failure."

#### Test 3: Range Validation (Out of Range Values)
**Actions:**
1. Modify JSON to have out-of-range value:
```json
{
  "age": 150,
  "num_medications": 3,
  ...
}
```
2. Click "Execute"
3. Show 422 response
4. Highlight range validation error

**Narration:**
"Similarly, when I provide an age of 150, which exceeds our maximum of 120, the API rejects it with a clear error message about the constraint violation."

#### Test 4: Missing Required Fields
**Actions:**
1. Remove a required field:
```json
{
  "age": 45,
  "num_medications": 3
}
```
2. Click "Execute"
3. Show 422 response listing missing fields

**Narration:**
"And when required fields are missing, the API tells us exactly which fields are required."

---

### Segment 4: Jupyter Notebook - Model Training (1.5 minutes)

**[Screen: Jupyter notebook]**

"Now let's look at the machine learning pipeline where I trained and compared three different models."

#### Show Key Sections:

**1. Dataset Overview (10 seconds)**
- Scroll to dataset loading cell
- Show dataset shape (1000+ records, 8+ features)
- Show first few rows

**Narration:**
"I used a medication adherence dataset with over 1000 patient records and 8 features including age, medication complexity, and historical adherence patterns."

**2. Model Training Results (30 seconds)**
- Scroll to Linear Regression results
- Show MSE and R-squared metrics
- Scroll to Decision Tree results
- Show MSE and R-squared metrics
- Scroll to Random Forest results
- Show MSE and R-squared metrics

**Narration:**
"I trained three models: Linear Regression achieved an MSE of [X] and R-squared of [Y]. Decision Trees performed with MSE of [X] and R-squared of [Y]. Random Forest, our best performer, achieved MSE of [X] and R-squared of [Y]."

**3. Model Comparison Visualization (20 seconds)**
- Show model comparison bar chart
- Show feature importance plot

**Narration:**
"This comparison chart clearly shows Random Forest had the lowest test error. The feature importance analysis reveals that previous adherence rate and missed doses are the strongest predictors."

**4. Model Selection Justification (20 seconds)**
- Scroll to model selection cell with rationale

**Narration:**
"I selected Random Forest as the best model because it had the lowest test MSE, handles non-linear relationships well, and is robust to outliers - all important characteristics for this healthcare dataset where patient behaviors can be complex and varied."

---

### Segment 5: Code Walkthrough (30 seconds)

**[Screen: Split view or quick switches between files]**

#### API Code (15 seconds)
**[Show: summative/API/prediction.py]**

"Here's the FastAPI prediction endpoint. It uses Pydantic models for input validation, loads the trained Random Forest model, preprocesses the input using the same scaler from training, and returns the prediction."

**Highlight:**
- Pydantic model with Field constraints
- POST /predict endpoint
- Model loading
- Prediction logic

#### Flutter Code (15 seconds)
**[Show: lib/features/adherence/presentation/services/prediction_service.dart]**

"And here's the Flutter service that makes the API call. It constructs the JSON request body, sends a POST request to our deployed API, handles the response, and manages errors like timeouts and network failures."

**Highlight:**
- predictAdherence method
- HTTP POST request
- JSON encoding
- Error handling

---

### Segment 6: Conclusion (10 seconds)

**[Camera visible, show your face]**

"This system demonstrates end-to-end machine learning integration: from data analysis and model training in Python, to a production API with validation, to a mobile app that provides predictions to users. Thank you for watching!"

---

## Recording Tips

1. **Practice first**: Do a dry run to ensure smooth transitions
2. **Keep it concise**: Stay within 5 minutes
3. **Clear audio**: Speak clearly and at a moderate pace
4. **Camera position**: Keep camera visible but not obstructive (corner of screen)
5. **Screen resolution**: Use 1080p or higher for clarity
6. **Zoom appropriately**: Make sure text is readable
7. **Smooth transitions**: Use keyboard shortcuts to switch between apps quickly

---

## Post-Recording Steps

1. **Review the video**: Ensure all requirements are covered
2. **Edit if needed**: Trim any dead space, add transitions
3. **Upload to YouTube**:
   - Title: "MedMind Medication Adherence Prediction - ML System Demonstration"
   - Description: Include project overview and GitHub link
   - Visibility: Public or Unlisted (as required)
4. **Copy YouTube URL**
5. **Update README**: Add YouTube link to summative/README.md

---

## Checklist - Ensure Video Includes:

- [ ] Presenter camera visible throughout (5 minutes)
- [ ] Mobile app demonstration with various inputs
- [ ] Swagger UI testing with valid inputs
- [ ] Data type validation test (wrong types)
- [ ] Range validation test (out of range values)
- [ ] Missing field validation test
- [ ] Jupyter notebook with model training code
- [ ] Model performance comparison (LR, DT, RF)
- [ ] Loss metrics discussion (MSE, R-squared)
- [ ] Model selection justification
- [ ] API code showing prediction endpoint
- [ ] Flutter code showing API call
- [ ] Video uploaded to YouTube
- [ ] YouTube link added to README

---

## Sample Test Data for Demonstrations

### Valid Test Case 1 (Good Adherence):
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

### Valid Test Case 2 (Poor Adherence):
```json
{
  "age": 72,
  "num_medications": 8,
  "medication_complexity": 4.5,
  "days_since_start": 365,
  "missed_doses_last_week": 5,
  "snooze_frequency": 0.7,
  "chronic_conditions": 4,
  "previous_adherence_rate": 45.0
}
```

### Invalid Test Case 1 (Wrong Type):
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

### Invalid Test Case 2 (Out of Range):
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

### Invalid Test Case 3 (Missing Fields):
```json
{
  "age": 45,
  "num_medications": 3
}
```

---

## Time Management

- Introduction: 0:00 - 0:30
- Mobile App: 0:30 - 1:30
- Swagger UI: 1:30 - 3:00
- Jupyter Notebook: 3:00 - 4:30
- Code Walkthrough: 4:30 - 5:00

**Total: 5:00 minutes**
