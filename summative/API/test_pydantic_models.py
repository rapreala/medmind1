"""
Test suite for Pydantic input validation models.

This module tests the PredictionInput and PredictionOutput models
to ensure proper validation and constraint enforcement.
"""

import pytest
from pydantic import ValidationError
from prediction import PredictionInput, PredictionOutput


class TestPredictionInput:
    """Test cases for PredictionInput model."""
    
    def test_valid_input_all_fields(self):
        """Test that valid input with all fields is accepted."""
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
        
        input_model = PredictionInput(**data)
        
        assert input_model.age == 45
        assert input_model.num_medications == 3
        assert input_model.medication_complexity == 2.5
        assert input_model.days_since_start == 120
        assert input_model.missed_doses_last_week == 1
        assert input_model.snooze_frequency == 0.2
        assert input_model.chronic_conditions == 2
        assert input_model.previous_adherence_rate == 85.5
    
    def test_age_boundary_values(self):
        """Test age field boundary values."""
        # Valid boundaries
        valid_data = {
            "age": 0,
            "num_medications": 1,
            "medication_complexity": 1.0,
            "days_since_start": 0,
            "missed_doses_last_week": 0,
            "snooze_frequency": 0.0,
            "chronic_conditions": 0,
            "previous_adherence_rate": 0.0
        }
        input_model = PredictionInput(**valid_data)
        assert input_model.age == 0
        
        valid_data["age"] = 120
        input_model = PredictionInput(**valid_data)
        assert input_model.age == 120
    
    def test_age_out_of_range_negative(self):
        """Test that negative age is rejected."""
        data = {
            "age": -1,
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('age',) for error in errors)
    
    def test_age_out_of_range_too_high(self):
        """Test that age > 120 is rejected."""
        data = {
            "age": 121,
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('age',) for error in errors)
    
    def test_num_medications_out_of_range(self):
        """Test that num_medications outside valid range is rejected."""
        data = {
            "age": 45,
            "num_medications": 0,  # Invalid: must be >= 1
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('num_medications',) for error in errors)
    
    def test_medication_complexity_out_of_range(self):
        """Test that medication_complexity outside valid range is rejected."""
        data = {
            "age": 45,
            "num_medications": 3,
            "medication_complexity": 5.5,  # Invalid: must be <= 5.0
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('medication_complexity',) for error in errors)
    
    def test_snooze_frequency_out_of_range(self):
        """Test that snooze_frequency outside valid range is rejected."""
        data = {
            "age": 45,
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 1.5,  # Invalid: must be <= 1.0
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('snooze_frequency',) for error in errors)
    
    def test_previous_adherence_rate_out_of_range(self):
        """Test that previous_adherence_rate outside valid range is rejected."""
        data = {
            "age": 45,
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 105.0  # Invalid: must be <= 100.0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('previous_adherence_rate',) for error in errors)
    
    def test_missing_required_field(self):
        """Test that missing required fields are rejected."""
        data = {
            "age": 45,
            "num_medications": 3,
            # Missing medication_complexity
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('medication_complexity',) for error in errors)
    
    def test_wrong_type_for_age(self):
        """Test that wrong type for age is rejected."""
        data = {
            "age": "forty-five",  # Invalid: should be int
            "num_medications": 3,
            "medication_complexity": 2.5,
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('age',) for error in errors)
    
    def test_wrong_type_for_medication_complexity(self):
        """Test that wrong type for medication_complexity is rejected."""
        data = {
            "age": 45,
            "num_medications": 3,
            "medication_complexity": "medium",  # Invalid: should be float
            "days_since_start": 120,
            "missed_doses_last_week": 1,
            "snooze_frequency": 0.2,
            "chronic_conditions": 2,
            "previous_adherence_rate": 85.5
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionInput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('medication_complexity',) for error in errors)


class TestPredictionOutput:
    """Test cases for PredictionOutput model."""
    
    def test_valid_output(self):
        """Test that valid output is accepted."""
        data = {
            "predicted_adherence_rate": 82.3,
            "confidence": "high",
            "message": "Prediction successful"
        }
        
        output_model = PredictionOutput(**data)
        
        assert output_model.predicted_adherence_rate == 82.3
        assert output_model.confidence == "high"
        assert output_model.message == "Prediction successful"
    
    def test_output_with_different_confidence_levels(self):
        """Test output with different confidence levels."""
        for confidence in ["high", "medium", "low"]:
            data = {
                "predicted_adherence_rate": 75.0,
                "confidence": confidence,
                "message": "Prediction successful"
            }
            
            output_model = PredictionOutput(**data)
            assert output_model.confidence == confidence
    
    def test_missing_required_field_in_output(self):
        """Test that missing required fields in output are rejected."""
        data = {
            "predicted_adherence_rate": 82.3,
            # Missing confidence
            "message": "Prediction successful"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PredictionOutput(**data)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('confidence',) for error in errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
