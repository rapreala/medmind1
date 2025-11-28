# MedMind API - Quick Reference Card

## 🌐 Base URL
```
https://medmind-adherence-api.onrender.com
```

## 📚 Swagger UI
```
https://medmind-adherence-api.onrender.com/docs
```

---

## 🔗 Endpoints

### GET /
**Description:** API information  
**URL:** `https://medmind-adherence-api.onrender.com/`

### GET /health
**Description:** Health check  
**URL:** `https://medmind-adherence-api.onrender.com/health`

### POST /predict
**Description:** Predict adherence rate  
**URL:** `https://medmind-adherence-api.onrender.com/predict`

---

## 📥 Request Format

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

## 📤 Response Format

```json
{
  "predicted_adherence_rate": 55.18,
  "confidence": "low",
  "message": "Prediction successful"
}
```

---

## 🔢 Input Constraints

| Field | Type | Min | Max |
|-------|------|-----|-----|
| age | int | 0 | 120 |
| num_medications | int | 1 | 20 |
| medication_complexity | float | 1.0 | 5.0 |
| days_since_start | int | 0 | ∞ |
| missed_doses_last_week | int | 0 | 50 |
| snooze_frequency | float | 0.0 | 1.0 |
| chronic_conditions | int | 0 | 10 |
| previous_adherence_rate | float | 0.0 | 100.0 |

---

## 💻 cURL Examples

### Health Check
```bash
curl https://medmind-adherence-api.onrender.com/health
```

### Prediction
```bash
curl -X POST https://medmind-adherence-api.onrender.com/predict \
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

---

## 📱 Flutter/Dart Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

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
    Uri.parse('https://medmind-adherence-api.onrender.com/predict'),
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
```

---

## 🐍 Python Example

```python
import requests

url = "https://medmind-adherence-api.onrender.com/predict"

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
result = response.json()

print(f"Predicted Adherence: {result['predicted_adherence_rate']}%")
print(f"Confidence: {result['confidence']}")
```

---

## 🟢 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 422 | Validation Error (invalid input) |
| 500 | Server Error |

---

## ⚠️ Common Errors

### 422 - Validation Error
**Cause:** Input values out of range or wrong type  
**Solution:** Check input constraints above

### 500 - Server Error
**Cause:** Model loading or prediction failure  
**Solution:** Check API logs or contact support

### Timeout
**Cause:** Cold start (free tier spins down after 15 min)  
**Solution:** Wait 30-60 seconds for first request

---

## 🧪 Test Command

```bash
python test_deployed_api.py https://medmind-adherence-api.onrender.com
```

---

## 📊 Performance

- **Response Time:** ~2 seconds (warm)
- **Cold Start:** ~30-60 seconds (first request after idle)
- **Uptime:** 24/7 (free tier)

---

## 🔗 Links

- **API:** https://medmind-adherence-api.onrender.com
- **Docs:** https://medmind-adherence-api.onrender.com/docs
- **Health:** https://medmind-adherence-api.onrender.com/health
- **Dashboard:** https://dashboard.render.com

---

**Last Updated:** November 28, 2025  
**Status:** ✅ Operational
