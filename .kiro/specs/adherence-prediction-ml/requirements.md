# Requirements Document

## Introduction

MedMind is an intelligent medication adherence application that helps patients manage their medication schedules and track their adherence patterns. This feature extends MedMind's capabilities by implementing a machine learning-based prediction system that forecasts patient medication adherence rates. By analyzing historical adherence data, medication complexity, and patient behavior patterns, the system will predict future adherence rates, enabling proactive interventions and personalized support for patients at risk of non-adherence.

This predictive capability addresses a critical healthcare challenge: medication non-adherence affects approximately 50% of patients with chronic conditions globally and results in $100-$289 billion in avoidable healthcare costs annually. By predicting adherence rates, healthcare providers and patients can take preventive action before adherence deteriorates.

## Glossary

- **Adherence Rate**: The percentage of prescribed medication doses that a patient takes as scheduled over a specific time period
- **ML Model**: Machine Learning Model - a trained algorithm that makes predictions based on input features
- **Prediction API**: A RESTful web service endpoint that accepts patient data and returns predicted adherence rates
- **Training Dataset**: Historical patient adherence data used to train the machine learning model
- **Feature Engineering**: The process of selecting and transforming raw data into meaningful input variables for the ML model
- **Linear Regression**: A supervised learning algorithm that models the relationship between input features and a continuous output variable
- **Random Forest**: An ensemble learning method that constructs multiple decision trees for improved prediction accuracy
- **Decision Tree**: A tree-structured model that makes predictions by learning decision rules from data features
- **Loss Metric**: A quantitative measure of prediction error (e.g., Mean Squared Error, Mean Absolute Error)
- **FastAPI**: A modern Python web framework for building APIs with automatic documentation
- **Pydantic**: A Python library for data validation using type annotations
- **CORS**: Cross-Origin Resource Sharing - a security mechanism that allows web applications to make requests across different domains
- **Swagger UI**: An interactive API documentation interface for testing endpoints
- **Flutter App**: The MedMind mobile application built using the Flutter framework
- **Adherence Log**: A record of when a patient took, missed, or snoozed a medication dose

## Requirements

### Requirement 1: Dataset Acquisition and Preparation

**User Story:** As a data scientist, I want to acquire and prepare a rich medication adherence dataset, so that I can train accurate prediction models.

#### Acceptance Criteria

1. THE System SHALL obtain a medication adherence dataset from a public repository (Kaggle, Google Datasets, or data.gov) containing at least 1000 patient records
2. THE System SHALL include at least 8 distinct features in the dataset including patient demographics, medication characteristics, and adherence history
3. THE Dataset SHALL contain a continuous target variable representing adherence rate (percentage between 0-100)
4. THE System SHALL document the dataset source, description, and relevance to medication adherence in the project README
5. THE System SHALL NOT use generic house price prediction datasets or any datasets previously used in class examples

### Requirement 2: Exploratory Data Analysis and Visualization

**User Story:** As a data scientist, I want to visualize and analyze the dataset, so that I can understand feature relationships and inform model development.

#### Acceptance Criteria

1. THE System SHALL generate a correlation heatmap showing relationships between all numeric features and the target variable
2. THE System SHALL create at least 2 distribution visualizations (histograms or scatter plots) for key features that impact adherence prediction
3. THE System SHALL identify and document which features have the strongest correlation with adherence rates
4. THE System SHALL include interpretations of all visualizations in the Jupyter notebook with markdown cells
5. THE System SHALL save all visualization plots as image files in the project repository

### Requirement 3: Feature Engineering and Data Preprocessing

**User Story:** As a data scientist, I want to engineer and preprocess features, so that the models can learn effectively from clean, normalized data.

#### Acceptance Criteria

1. THE System SHALL identify and handle missing values in the dataset using appropriate imputation or removal strategies
2. THE System SHALL convert all categorical variables to numeric representations using encoding techniques (one-hot encoding or label encoding)
3. THE System SHALL standardize all numeric features using StandardScaler or similar normalization technique
4. THE System SHALL document which columns are dropped and provide justification based on correlation analysis or domain knowledge
5. THE System SHALL split the dataset into training (80%) and testing (20%) sets with random state for reproducibility

### Requirement 4: Linear Regression Model Implementation

**User Story:** As a data scientist, I want to implement a linear regression model, so that I can establish a baseline for adherence rate prediction.

#### Acceptance Criteria

1. THE System SHALL implement a linear regression model using scikit-learn's LinearRegression class
2. THE System SHALL train the linear regression model on the standardized training dataset
3. THE System SHALL evaluate the model using Mean Squared Error (MSE) and R-squared metrics on both training and test sets
4. THE System SHALL plot a loss curve showing training and test error across iterations (if using gradient descent) or residual plots
5. THE System SHALL create a scatter plot comparing actual vs predicted adherence rates with the regression line overlaid

### Requirement 5: Decision Tree Model Implementation

**User Story:** As a data scientist, I want to implement a decision tree model, so that I can capture non-linear relationships in adherence patterns.

#### Acceptance Criteria

1. THE System SHALL implement a decision tree regressor using scikit-learn's DecisionTreeRegressor class
2. THE System SHALL tune hyperparameters (max_depth, min_samples_split) using cross-validation or grid search
3. THE System SHALL evaluate the decision tree model using MSE and R-squared metrics on both training and test sets
4. THE System SHALL compare decision tree performance against the linear regression baseline
5. THE System SHALL visualize feature importance scores from the trained decision tree model

### Requirement 6: Random Forest Model Implementation

**User Story:** As a data scientist, I want to implement a random forest model, so that I can leverage ensemble learning for improved prediction accuracy.

#### Acceptance Criteria

1. THE System SHALL implement a random forest regressor using scikit-learn's RandomForestRegressor class
2. THE System SHALL configure the random forest with at least 100 estimators (trees)
3. THE System SHALL tune hyperparameters (n_estimators, max_depth, min_samples_split) for optimal performance
4. THE System SHALL evaluate the random forest model using MSE and R-squared metrics on both training and test sets
5. THE System SHALL visualize feature importance scores from the trained random forest model

### Requirement 7: Model Comparison and Selection

**User Story:** As a data scientist, I want to compare all three models, so that I can select the best-performing model for deployment.

#### Acceptance Criteria

1. THE System SHALL create a comparison table showing MSE, R-squared, and training time for all three models
2. THE System SHALL identify the model with the lowest test set MSE as the best-performing model
3. THE System SHALL save the best-performing model to disk using joblib or pickle serialization
4. THE System SHALL document the model selection rationale based on performance metrics and dataset characteristics
5. THE System SHALL create a function that loads the saved model and makes predictions on new data points

### Requirement 8: Prediction Function Implementation

**User Story:** As a developer, I want a reusable prediction function, so that I can integrate the model into the API and mobile app.

#### Acceptance Criteria

1. THE System SHALL implement a Python function that accepts feature values as input parameters
2. THE Function SHALL load the saved best-performing model from disk
3. THE Function SHALL preprocess input data using the same standardization applied during training
4. THE Function SHALL return a predicted adherence rate as a float value between 0 and 100
5. THE System SHALL demonstrate the prediction function on at least one test data point in the notebook

### Requirement 9: FastAPI Endpoint Development

**User Story:** As a mobile app developer, I want a RESTful API endpoint, so that the Flutter app can request adherence predictions.

#### Acceptance Criteria

1. THE System SHALL implement a FastAPI application with a POST endpoint at `/predict`
2. THE Endpoint SHALL accept JSON input containing all required feature values for prediction
3. THE System SHALL implement CORS middleware to allow cross-origin requests from the Flutter mobile app
4. THE System SHALL validate input data types and ranges using Pydantic BaseModel with appropriate constraints
5. THE System SHALL return predictions as JSON responses with the predicted adherence rate and HTTP status codes

### Requirement 10: Input Validation and Constraints

**User Story:** As an API consumer, I want input validation, so that I receive clear error messages for invalid data.

#### Acceptance Criteria

1. THE System SHALL enforce data types for each input field (integer, float, string) using Pydantic type annotations
2. THE System SHALL define realistic range constraints for numeric inputs (e.g., age between 0-120, adherence rate 0-100)
3. WHEN invalid data is submitted THEN the API SHALL return a 422 Unprocessable Entity status with detailed validation errors
4. THE System SHALL validate that all required fields are present in the request body
5. THE System SHALL document all input constraints in the Pydantic model docstrings

### Requirement 11: API Deployment and Documentation

**User Story:** As a project stakeholder, I want a publicly accessible API, so that the system can be tested and integrated with the mobile app.

#### Acceptance Criteria

1. THE System SHALL deploy the FastAPI application to a free hosting platform (Render, Railway, or similar)
2. THE System SHALL provide a publicly accessible URL that routes to the Swagger UI documentation at `/docs`
3. THE System SHALL include a requirements.txt file listing all Python dependencies with version numbers
4. THE System SHALL ensure the deployed API responds to prediction requests within 5 seconds
5. THE System SHALL document the public API URL in the project README with example curl commands

### Requirement 12: Flutter Mobile App Integration

**User Story:** As a MedMind user, I want to see my predicted adherence rate in the mobile app, so that I can understand my medication-taking behavior.

#### Acceptance Criteria

1. THE Flutter App SHALL create a new page with text input fields matching the number of prediction features
2. THE Flutter App SHALL implement HTTP POST requests to the deployed API endpoint using the http or dio package
3. THE Flutter App SHALL display the predicted adherence rate in a dedicated output area after successful API response
4. WHEN API errors occur THEN the Flutter App SHALL display user-friendly error messages
5. THE Flutter App SHALL organize UI elements without overlapping and maintain a clean, presentable layout

### Requirement 13: Error Handling and Edge Cases

**User Story:** As a system user, I want robust error handling, so that the system gracefully handles unexpected inputs and failures.

#### Acceptance Criteria

1. WHEN the API receives out-of-range values THEN the System SHALL return a 422 status with specific field errors
2. WHEN the model file is missing THEN the API SHALL return a 500 status with an appropriate error message
3. WHEN network requests fail in the Flutter app THEN the System SHALL display a connection error message
4. WHEN the API is unreachable THEN the Flutter App SHALL timeout after 10 seconds and notify the user
5. THE System SHALL log all prediction requests and errors for debugging and monitoring purposes

### Requirement 14: Documentation and Demonstration

**User Story:** As a project evaluator, I want comprehensive documentation and demonstration, so that I can assess the system's functionality and quality.

#### Acceptance Criteria

1. THE Project SHALL include a README with mission statement (4 lines maximum), dataset description, and API endpoint URL
2. THE Project SHALL provide a YouTube video demonstration of maximum 5 minutes duration
3. THE Video SHALL demonstrate the mobile app making predictions and Swagger UI testing with presenter camera visible
4. THE Video SHALL explain model performance comparison (Linear Regression, Random Forest, Decision Trees) using loss metrics
5. THE Video SHALL show the Jupyter notebook with model training code and justify model selection based on dataset characteristics
