# MedMind Adherence Prediction System

## Mission Statement

MedMind's ML-powered adherence prediction system forecasts patient medication-taking behavior using advanced regression algorithms. By analyzing patient demographics, medication complexity, and behavioral patterns, the system identifies at-risk patients before adherence deteriorates, enabling proactive healthcare interventions. This predictive capability addresses the critical challenge of medication non-adherence, which affects 50% of chronic disease patients and costs healthcare systems billions annually.

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

**Public URL:** [To be added after deployment]

**Example Request:**
```bash
curl -X POST "https://your-api-url.com/predict" \
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

1. Navigate to the Flutter app directory:
   ```bash
   cd summative/FlutterApp
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Run the app:
   ```bash
   flutter run
   ```

4. Navigate to the "Adherence Prediction" page and enter patient data to get predictions.

## Video Demonstration

**YouTube Link:** [To be added]

## Dependencies

### Python (ML & API)
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- fastapi >= 0.100.0
- uvicorn >= 0.23.0
- pydantic >= 2.0.0
- joblib >= 1.3.0

### Flutter
- http >= 1.1.0
- flutter_bloc >= 8.1.0

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r summative/API/requirements.txt
   ```
3. Install Flutter dependencies:
   ```bash
   cd summative/FlutterApp && flutter pub get
   ```

## Development

### Training Models
Open and run `summative/linear_regression/multivariate.ipynb` in Jupyter Notebook or JupyterLab.

### Running API Locally
```bash
cd summative/API
uvicorn prediction:app --reload
```

Access Swagger UI at: http://localhost:8000/docs

## License

This project is part of the MedMind application for educational purposes.
