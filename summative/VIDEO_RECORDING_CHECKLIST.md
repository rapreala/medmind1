# Video Recording Checklist

## Before Recording

### Technical Setup
- [ ] Flutter app running on emulator/device
- [ ] API accessible at: https://medmind-adherence-api.onrender.com
- [ ] Swagger UI open at: https://medmind-adherence-api.onrender.com/docs
- [ ] Jupyter notebook open: `summative/linear_regression/multivariate.ipynb`
- [ ] VS Code/Editor open with:
  - [ ] `summative/API/prediction.py`
  - [ ] `lib/features/adherence/presentation/pages/adherence_prediction_page.dart`
  - [ ] `lib/features/adherence/presentation/services/prediction_service.dart`

### Recording Setup
- [ ] Screen recording software ready (OBS, QuickTime, etc.)
- [ ] Camera positioned and visible
- [ ] Good lighting on face
- [ ] Microphone tested (clear audio)
- [ ] Close unnecessary applications
- [ ] Disable notifications
- [ ] Set screen resolution to 1080p or higher

### Preparation
- [ ] Read through VIDEO_DEMONSTRATION_GUIDE.md
- [ ] Practice the demonstration once
- [ ] Prepare test data (see guide for sample inputs)
- [ ] Time yourself (must be ≤ 5 minutes)

---

## During Recording

### ✅ Required Content (Must Include All)

#### 1. Introduction (30 seconds)
- [ ] Camera visible showing your face
- [ ] Introduce yourself by name
- [ ] Briefly explain the project

#### 2. Mobile App Demo (1 minute)
- [ ] Show navigation to prediction page
- [ ] Enter valid patient data in all 8 fields
- [ ] Click "Predict" button
- [ ] Show loading indicator
- [ ] Display prediction result
- [ ] Test with different input values

#### 3. Swagger UI Testing (1.5 minutes)
- [ ] Show Swagger UI interface
- [ ] Test 1: Valid input → 200 response
- [ ] Test 2: Wrong data type (e.g., string for age) → 422 error
- [ ] Test 3: Out of range value (e.g., age=150) → 422 error
- [ ] Test 4: Missing required fields → 422 error
- [ ] Highlight error messages for each validation failure

#### 4. Jupyter Notebook (1.5 minutes)
- [ ] Show dataset overview (1000+ records, 8+ features)
- [ ] Show Linear Regression results (MSE, R²)
- [ ] Show Decision Tree results (MSE, R²)
- [ ] Show Random Forest results (MSE, R²)
- [ ] Show model comparison visualization
- [ ] Show feature importance plot
- [ ] Explain why Random Forest was selected

#### 5. Code Walkthrough (30 seconds)
- [ ] Show API code (prediction.py):
  - [ ] Pydantic model with validation
  - [ ] POST /predict endpoint
  - [ ] Model loading and prediction logic
- [ ] Show Flutter code (prediction_service.dart):
  - [ ] HTTP POST request
  - [ ] JSON encoding
  - [ ] Error handling

#### 6. Conclusion (10 seconds)
- [ ] Camera visible showing your face
- [ ] Brief summary statement
- [ ] Thank viewers

---

## Quality Checks

### Technical Quality
- [ ] Video duration ≤ 5 minutes
- [ ] Camera visible throughout entire video
- [ ] Audio is clear and understandable
- [ ] Screen content is readable (text not too small)
- [ ] No long pauses or dead air
- [ ] Smooth transitions between sections

### Content Completeness
- [ ] All 8 required sections covered
- [ ] All validation tests demonstrated
- [ ] All three models discussed
- [ ] Loss metrics (MSE, R²) explained
- [ ] Model selection justified
- [ ] Code shown for both API and Flutter

---

## After Recording

### Video Processing
- [ ] Review entire video
- [ ] Trim any unnecessary parts
- [ ] Ensure total length ≤ 5 minutes
- [ ] Check audio levels are consistent
- [ ] Verify all text on screen is readable

### YouTube Upload
- [ ] Create YouTube account (if needed)
- [ ] Upload video to YouTube
- [ ] Set title: "MedMind Medication Adherence Prediction - ML System Demonstration"
- [ ] Add description with project overview
- [ ] Set visibility: Public or Unlisted (as required)
- [ ] Add tags: machine learning, healthcare, flutter, fastapi, medication adherence
- [ ] Wait for processing to complete
- [ ] Test video plays correctly

### Documentation Update
- [ ] Copy YouTube video URL
- [ ] Open `summative/README.md`
- [ ] Replace `YOUR_YOUTUBE_URL_HERE` with actual URL
- [ ] Save and commit changes
- [ ] Verify link works when clicked

---

## Final Verification

Before submitting, verify:
- [ ] Video is accessible (not private)
- [ ] Video length is ≤ 5 minutes
- [ ] Camera is visible throughout
- [ ] All required demonstrations are included
- [ ] YouTube link in README works
- [ ] Video quality is good (1080p recommended)
- [ ] Audio is clear

---

## Sample Test Data (Copy-Paste Ready)

### Valid Input 1 (Good Adherence):
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

### Valid Input 2 (Poor Adherence):
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

### Invalid - Wrong Type:
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

### Invalid - Out of Range:
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

### Invalid - Missing Fields:
```json
{
  "age": 45,
  "num_medications": 3
}
```

---

## Time Budget

- Introduction: 0:00 - 0:30 (30s)
- Mobile App: 0:30 - 1:30 (60s)
- Swagger UI: 1:30 - 3:00 (90s)
- Jupyter Notebook: 3:00 - 4:30 (90s)
- Code Walkthrough: 4:30 - 5:00 (30s)

**Total: 5:00 minutes**

---

## Troubleshooting

**Problem: Video is too long**
- Solution: Speak faster, reduce pauses, skip less important details

**Problem: API is slow (cold start)**
- Solution: Make a test request 1-2 minutes before recording to "wake up" the API

**Problem: Screen text is too small**
- Solution: Increase zoom level in browser/editor, use larger font sizes

**Problem: Camera not visible**
- Solution: Use picture-in-picture mode or split screen with camera feed

**Problem: Audio quality poor**
- Solution: Use external microphone, record in quiet room, speak clearly

---

## Resources

- Detailed Script: `summative/VIDEO_DEMONSTRATION_GUIDE.md`
- API Documentation: `summative/API/README.md`
- Model Performance: `summative/linear_regression/MODEL_COMPARISON_SUMMARY.md`
- Deployed API: https://medmind-adherence-api.onrender.com/docs

---

## Contact

If you have questions about the video requirements, refer to:
- Requirements Document: `.kiro/specs/adherence-prediction-ml/requirements.md`
- Task List: `.kiro/specs/adherence-prediction-ml/tasks.md`
- Requirement 14.2, 14.3, 14.4, 14.5
