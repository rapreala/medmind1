# Video Demonstration Guide - MedMind Adherence Prediction

## 📹 Recording Requirements

**Duration:** Maximum 5 minutes  
**Camera:** Presenter must be visible throughout  
**Platform:** YouTube (Public or Unlisted)  
**Quality:** 720p minimum recommended

---

## 🎬 Video Script (5 Minutes)

### Introduction (30 seconds)
**[Show your face on camera]**

"Hi, I'm [Your Name], and this is my MedMind Adherence Prediction System. This project uses machine learning to predict patient medication adherence rates, helping healthcare providers identify at-risk patients before adherence deteriorates."

---

### Part 1: Mobile App Demonstration (1 minute)

**[Screen record Flutter app]**

1. **Launch the app**
   - "Here's the MedMind mobile application"
   - Navigate to Dashboard
   - Tap "Adherence Prediction"

2. **Test Case 1: High-risk patient**
   ```
   Age: 72
   Medications: 8
   Complexity: 4.5
   Days Since Start: 365
   Missed Doses: 5
   Snooze Frequency: 0.8
   Chronic Conditions: 4
   Previous Adherence: 45.0
   ```
   - "Let me enter data for a high-risk patient"
   - Tap "Predict"
   - "The model predicts low adherence around 35-40%"

3. **Test Case 2: Low-risk patient**
   ```
   Age: 35
   Medications: 2
   Complexity: 1.5
   Days Since Start: 30
   Missed Doses: 0
   Snooze Frequency: 0.1
   Chronic Conditions: 1
   Previous Adherence: 95.0
   ```
   - "Now a low-risk patient with good adherence history"
   - Tap "Predict"
   - "The model predicts high adherence around 85-90%"

---

### Part 2: Swagger UI Testing (1.5 minutes)

**[Open browser to https://medmind-adherence-api.onrender.com/docs]**

1. **Valid Input Test**
   - "Here's the Swagger UI for our API"
   - Click "POST /predict"
   - Click "Try it out"
   - Use example JSON:
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
   - Click "Execute"
   - "We get a 200 response with predicted adherence rate"

2. **Type Validation Test**
   - "Let's test type validation"
   - Change `"age": "not a number"`
   - Click "Execute"
   - "The API returns 422 with validation error"

3. **Range Validation Test**
   - "Now let's test range validation"
   - Change `"age": 150` (invalid)
   - Click "Execute"
   - "Again, 422 error - age must be ≤ 120"

4. **Missing Field Test**
   - "What if we remove a required field?"
   - Delete the `num_medications` field
   - Click "Execute"
   - "422 error - field required"

---

### Part 3: Jupyter Notebook Walkthrough (1.5 minutes)

**[Open multivariate.ipynb]**

1. **Dataset Overview**
   - Scroll to dataset loading cell
   - "We have 1,500 patient records with 8 features"
   - Show correlation heatmap
   - "Missed doses and previous adherence are strongest predictors"

2. **Model Training**
   - Scroll to Linear Regression section
   - "First, Linear Regression: MSE 95.74, R² 0.66"
   
   - Scroll to Decision Tree section
   - "Decision Tree: MSE 72.81, R² 0.74 - better"
   
   - Scroll to Random Forest section
   - "Random Forest: MSE 31.56, R² 0.89 - best performance"

3. **Model Comparison**
   - Show comparison table/plot
   - "Random Forest has 67% lower error than Linear Regression"
   - "It explains 88.7% of variance in adherence rates"

4. **Model Selection Justification**
   - "I selected Random Forest because:"
   - "1. Lowest MSE - most accurate predictions"
   - "2. Highest R² - best fit to data"
   - "3. Robust to outliers and non-linear relationships"
   - "4. This dataset has complex interactions between features"
   - "5. Random Forest handles these better than linear models"

---

### Part 4: API Code Walkthrough (30 seconds)

**[Open summative/API/prediction.py]**

- Scroll to `/predict` endpoint
- "Here's the prediction endpoint"
- "It uses Pydantic for validation"
- "Loads the Random Forest model"
- "Preprocesses input with StandardScaler"
- "Returns prediction as JSON"

---

### Part 5: Flutter Code Walkthrough (30 seconds)

**[Open lib/features/adherence/presentation/services/prediction_service.dart]**

- "Here's the Flutter service"
- "It makes HTTP POST to our API"
- "Handles errors gracefully"
- "Returns the predicted adherence rate"

**[Open adherence_prediction_page.dart]**

- "And here's the UI"
- "8 input fields with validation"
- "Calls the service when user taps Predict"
- "Displays result in a card"

---

### Conclusion (10 seconds)

**[Show your face on camera]**

"That's the complete system - from data to model to API to mobile app. The Random Forest model achieves 88.7% accuracy in predicting medication adherence. Thank you!"

---

## 📝 Recording Tips

1. **Preparation**
   - Test all demos before recording
   - Have all tabs/apps open and ready
   - Close unnecessary applications
   - Ensure good lighting for camera
   - Use a quiet environment

2. **Screen Recording**
   - Use OBS Studio, QuickTime, or similar
   - Record at 1920x1080 or 1280x720
   - Show cursor movements clearly
   - Keep camera feed in corner (picture-in-picture)

3. **Pacing**
   - Speak clearly and at moderate pace
   - Don't rush through demonstrations
   - Pause briefly between sections
   - Stay within 5-minute limit

4. **Editing**
   - Trim any dead air at start/end
   - Add title card if desired (optional)
   - Ensure audio is clear
   - Verify camera is visible throughout

---

## 🎥 Recording Checklist

Before recording:
- [ ] Flutter app running and tested
- [ ] API URL accessible
- [ ] Swagger UI loaded
- [ ] Jupyter notebook open
- [ ] Code files open in editor
- [ ] Camera positioned and tested
- [ ] Microphone tested
- [ ] Screen recording software ready
- [ ] Timer/stopwatch ready

During recording:
- [ ] Camera visible throughout
- [ ] Demonstrate mobile app (2 test cases)
- [ ] Test Swagger UI (valid + 3 invalid tests)
- [ ] Show Jupyter notebook
- [ ] Explain model comparison
- [ ] Justify model selection
- [ ] Show API code
- [ ] Show Flutter code
- [ ] Stay under 5 minutes

After recording:
- [ ] Review video for quality
- [ ] Check audio clarity
- [ ] Verify camera visibility
- [ ] Confirm all requirements covered
- [ ] Upload to YouTube
- [ ] Set to Public or Unlisted
- [ ] Copy YouTube URL
- [ ] Update README.md

---

## 📤 Upload Instructions

1. **Go to YouTube Studio**
   - https://studio.youtube.com

2. **Upload Video**
   - Click "Create" → "Upload videos"
   - Select your video file
   - Title: "MedMind Adherence Prediction System - ML Demo"
   - Description: "Machine learning system for predicting medication adherence rates using Random Forest regression. Part of MedMind application."

3. **Settings**
   - Visibility: Public or Unlisted (your choice)
   - Category: Science & Technology
   - Tags: machine learning, healthcare, medication adherence, flutter, fastapi

4. **Get URL**
   - After upload completes, copy the video URL
   - Format: `https://www.youtube.com/watch?v=XXXXXXXXXXX`

5. **Update README**
   - Open `summative/README.md`
   - Find line with `YOUR_YOUTUBE_URL_HERE`
   - Replace with your actual YouTube URL
   - Save and commit

---

## ✅ Verification

After uploading:
- [ ] Video is accessible (not private)
- [ ] Video plays correctly
- [ ] Audio is clear
- [ ] Camera is visible throughout
- [ ] All demonstrations are shown
- [ ] Duration is ≤ 5 minutes
- [ ] README.md updated with URL
- [ ] Changes committed to repository

---

**Good luck with your recording! 🎬**
