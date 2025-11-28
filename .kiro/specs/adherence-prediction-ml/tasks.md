# Implementation Plan

- [x] 1. Set up project structure and acquire dataset
  - Create directory structure: `summative/linear_regression/`, `summative/API/`, `summative/FlutterApp/`
  - Search and download medication adherence dataset from Kaggle, Google Datasets, or data.gov
  - Verify dataset has at least 1000 records and 8+ features
  - Create Jupyter notebook: `summative/linear_regression/multivariate.ipynb`
  - Load dataset and perform initial exploration (shape, columns, dtypes)
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Perform exploratory data analysis and visualization
  - Generate correlation heatmap showing relationships between features and target variable
  - Create at least 2 distribution visualizations (histograms or scatter plots) for key features
  - Identify features with strongest correlation to adherence rate
  - Add markdown cells with interpretations of all visualizations
  - Save all plots as PNG files in `summative/linear_regression/plots/`
  - _Requirements: 2.1, 2.2, 2.3, 2.5_

- [ ]* 2.1 Write property test for correlation calculation
  - **Property 1: Feature Correlation Calculation Consistency**
  - **Validates: Requirements 2.3**

- [x] 3. Implement data preprocessing pipeline
  - Identify and handle missing values (document strategy used)
  - Convert categorical variables to numeric using encoding techniques
  - Implement StandardScaler for feature normalization
  - Document which columns are dropped and why
  - Split dataset into 80% training and 20% testing sets with random_state=42
  - Save scaler object for later use in predictions
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 3.1 Write property test for missing value handling
  - **Property 2: Missing Value Handling Completeness**
  - **Validates: Requirements 3.1**

- [ ]* 3.2 Write property test for categorical encoding
  - **Property 3: Categorical Encoding Transformation**
  - **Validates: Requirements 3.2**

- [ ]* 3.3 Write property test for feature standardization
  - **Property 4: Feature Standardization Properties**
  - **Validates: Requirements 3.3**

- [ ]* 3.4 Write property test for train-test split proportions
  - **Property 5: Train-Test Split Proportions**
  - **Validates: Requirements 3.5**

- [x] 4. Implement and train Linear Regression model
  - Import LinearRegression from scikit-learn
  - Train model on standardized training data
  - Make predictions on test set
  - Calculate MSE and R-squared metrics for both train and test sets
  - Create scatter plot of actual vs predicted values with regression line
  - Plot residuals or loss curve
  - Document model performance in notebook
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5. Implement and train Decision Tree model
  - Import DecisionTreeRegressor from scikit-learn
  - Implement hyperparameter tuning using GridSearchCV (max_depth, min_samples_split)
  - Train model on standardized training data
  - Make predictions on test set
  - Calculate MSE and R-squared metrics for both train and test sets
  - Visualize feature importance scores
  - Compare performance against Linear Regression baseline
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 6. Implement and train Random Forest model
  - Import RandomForestRegressor from scikit-learn
  - Configure with at least 100 estimators
  - Implement hyperparameter tuning (n_estimators, max_depth, min_samples_split)
  - Train model on standardized training data
  - Make predictions on test set
  - Calculate MSE and R-squared metrics for both train and test sets
  - Visualize feature importance scores
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 7. Compare models and select best performer
  - Create comparison table with MSE, R-squared, and training time for all three models
  - Identify model with lowest test set MSE
  - Save best-performing model using joblib to `summative/linear_regression/models/best_model.pkl`
  - Save scaler to `summative/linear_regression/models/scaler.pkl`
  - Document model selection rationale based on metrics and dataset characteristics
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ]* 7.1 Write property test for model selection logic
  - **Property 6: Model Selection by Minimum Loss**
  - **Validates: Requirements 7.2**

- [ ]* 7.2 Write property test for model persistence round-trip
  - **Property 7: Model Persistence Round-Trip**
  - **Validates: Requirements 7.3, 7.5**

- [x] 8. Implement prediction function
  - Create `predict_adherence()` function that accepts 8 feature values as parameters
  - Load saved model and scaler from disk
  - Preprocess input features using loaded scaler
  - Generate prediction using loaded model
  - Return predicted adherence rate as float between 0-100
  - Test function on at least one sample data point from test set
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 7.5_

- [ ]* 8.1 Write property test for preprocessing consistency
  - **Property 8: Prediction Preprocessing Consistency**
  - **Validates: Requirements 8.3**

- [ ]* 8.2 Write property test for prediction output range
  - **Property 9: Prediction Output Range Constraint**
  - **Validates: Requirements 8.4**

- [x] 9. Checkpoint - Verify ML pipeline is complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Set up FastAPI project structure
  - Create `summative/API/` directory
  - Create `prediction.py` file for FastAPI application
  - Copy trained model and scaler to `summative/API/models/`
  - Install FastAPI, Pydantic, Uvicorn, and other dependencies
  - Create requirements.txt with all dependencies and versions
  - _Requirements: 9.1, 11.3_

- [ ] 11. Implement Pydantic input validation models
  - Create `PredictionInput` BaseModel with 8 fields
  - Add type annotations for each field (int, float)
  - Define Field constraints with ge/le for range validation
  - Add descriptions for each field
  - Create `PredictionOutput` BaseModel for response structure
  - _Requirements: 9.4, 10.1, 10.2, 10.5_

- [ ]* 11.1 Write property test for input type validation
  - **Property 10: API Input Validation Rejection**
  - **Validates: Requirements 9.4, 10.1, 10.2, 10.3**

- [ ]* 11.2 Write property test for required field validation
  - **Property 11: Required Field Validation**
  - **Validates: Requirements 10.4**

- [ ]* 11.3 Write property test for out-of-range validation
  - **Property 14: Out-of-Range Validation Error Response**
  - **Validates: Requirements 13.1**

- [ ] 12. Implement FastAPI prediction endpoint
  - Create FastAPI app instance
  - Implement POST endpoint at `/predict`
  - Load model and scaler at startup (not per request)
  - Accept PredictionInput in request body
  - Preprocess input using scaler
  - Generate prediction using model
  - Return PredictionOutput with predicted adherence rate
  - Add error handling for model loading failures
  - Add error handling for prediction failures
  - _Requirements: 9.1, 9.2, 9.5_

- [ ] 13. Add CORS middleware and logging
  - Import and configure CORSMiddleware
  - Allow all origins for development (restrict in production)
  - Set up Python logging with INFO level
  - Log all prediction requests with input data
  - Log all prediction results
  - Log all errors with stack traces
  - _Requirements: 9.3, 13.5_

- [ ]* 13.1 Write property test for request logging
  - **Property 16: Request Logging Completeness**
  - **Validates: Requirements 13.5**

- [ ] 14. Test API locally with Swagger UI
  - Run API locally using `uvicorn prediction:app --reload`
  - Access Swagger UI at `http://localhost:8000/docs`
  - Test `/predict` endpoint with valid input
  - Test with invalid inputs (out of range, wrong types, missing fields)
  - Verify 200 responses for valid input
  - Verify 422 responses for invalid input with detailed error messages
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 10.3, 10.4_

- [ ]* 14.1 Write unit tests for API endpoints
  - Test predict endpoint returns 200 for valid input
  - Test predict endpoint returns 422 for invalid age
  - Test predict endpoint returns 422 for missing fields
  - Test CORS headers are present in responses

- [ ] 15. Deploy API to hosting platform
  - Create account on Render (or Railway/Heroku)
  - Create new Web Service
  - Connect to GitHub repository
  - Configure build command: `pip install -r requirements.txt`
  - Configure start command: `uvicorn prediction:app --host 0.0.0.0 --port $PORT`
  - Set environment variables if needed
  - Deploy and wait for build to complete
  - Test deployed API endpoint
  - Document public URL in README
  - _Requirements: 11.1, 11.2, 11.4_

- [ ]* 15.1 Write property test for API response time
  - **Property 12: API Response Time Performance**
  - **Validates: Requirements 11.4**

- [ ] 16. Checkpoint - Verify API is deployed and functional
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 17. Create Flutter prediction page UI
  - Create new file: `lib/features/adherence/presentation/pages/adherence_prediction_page.dart`
  - Design page layout with Scaffold and AppBar
  - Add 8 TextFormField widgets for input (age, num_medications, etc.)
  - Add labels and hints for each field
  - Add input validation for each field (numeric, required)
  - Add "Predict" ElevatedButton
  - Add Card widget for displaying prediction result
  - Add CircularProgressIndicator for loading state
  - Ensure UI elements don't overlap and layout is clean
  - _Requirements: 12.1, 12.5_

- [ ] 18. Implement HTTP service for API calls
  - Create `lib/features/adherence/presentation/services/prediction_service.dart`
  - Add http package to pubspec.yaml
  - Implement `predictAdherence()` method
  - Configure API base URL (use deployed URL)
  - Create JSON request body with all 8 features
  - Make POST request to `/predict` endpoint
  - Set timeout to 10 seconds
  - Parse JSON response and extract predicted adherence rate
  - Handle HTTP errors (4xx, 5xx status codes)
  - Handle network errors (timeout, no connection)
  - _Requirements: 12.2, 13.3, 13.4_

- [ ] 19. Integrate API service with prediction page
  - Inject prediction service into page
  - Implement form submission handler
  - Show loading indicator while waiting for API response
  - Display predicted adherence rate on successful response
  - Display user-friendly error messages on API errors
  - Display connection error messages on network failures
  - Clear previous results when new prediction is requested
  - _Requirements: 12.3, 12.4, 13.3_

- [ ]* 19.1 Write property test for Flutter error handling
  - **Property 13: Flutter Error Display on API Failure**
  - **Validates: Requirements 12.4**

- [ ]* 19.2 Write property test for network failure handling
  - **Property 15: Network Failure Error Handling**
  - **Validates: Requirements 13.3**

- [ ]* 19.3 Write Flutter widget tests
  - Test prediction page displays 8 input fields
  - Test predict button triggers API call
  - Test error message displayed on API failure
  - Test loading indicator shown during API call

- [ ] 20. Add navigation to prediction page
  - Add route for prediction page in router configuration
  - Add navigation button/menu item in appropriate location (dashboard or adherence section)
  - Test navigation flow
  - _Requirements: 12.1_

- [ ] 21. Checkpoint - Verify Flutter integration is complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 22. Create comprehensive README documentation
  - Add mission statement (maximum 4 lines) describing MedMind and adherence prediction
  - Document dataset source, description, and relevance to medication adherence
  - Provide public API endpoint URL with example curl command
  - Add instructions to run Flutter app (flutter pub get, flutter run)
  - Include link to YouTube video demonstration
  - Add project structure overview
  - Document all dependencies and versions
  - _Requirements: 1.4, 11.5, 14.1_

- [ ] 23. Create video demonstration
  - Record 5-minute maximum video demonstration
  - Ensure presenter camera is visible throughout
  - Demonstrate mobile app making predictions with various inputs
  - Show Swagger UI testing with valid and invalid inputs
  - Test data type validation (wrong types)
  - Test range validation (out of range values)
  - Show Jupyter notebook with model training code
  - Explain model performance comparison (Linear Regression, Decision Trees, Random Forest)
  - Discuss loss metrics (MSE, R-squared) for each model
  - Justify model selection based on dataset characteristics and performance
  - Show API code where prediction endpoint is implemented
  - Show Flutter code where API call is made
  - Upload video to YouTube
  - Add YouTube link to README
  - _Requirements: 14.2, 14.3, 14.4, 14.5_

- [ ] 24. Final testing and quality assurance
  - Run all unit tests and verify they pass
  - Run all property-based tests with 100 iterations
  - Test complete end-to-end flow: Flutter app → API → Model → Response
  - Verify all visualizations are saved and documented
  - Verify all code is properly commented
  - Check that requirements.txt is complete and accurate
  - Verify deployed API is accessible and responsive
  - Test Flutter app on physical device or emulator
  - Review all documentation for completeness
  - _Requirements: All_

- [ ] 25. Prepare submission
  - Organize all files in correct directory structure
  - Verify GitHub repository is up to date
  - Double-check README has all required information
  - Verify YouTube video is public and accessible
  - Test public API URL one final time
  - Create submission package
  - _Requirements: All_
