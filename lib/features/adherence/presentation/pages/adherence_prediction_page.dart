import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import '../../../../core/widgets/custom_text_field.dart';
import '../../../../core/widgets/custom_button.dart';
import '../services/prediction_service.dart';

class AdherencePredictionPage extends StatefulWidget {
  const AdherencePredictionPage({super.key});

  @override
  State<AdherencePredictionPage> createState() =>
      _AdherencePredictionPageState();
}

class _AdherencePredictionPageState extends State<AdherencePredictionPage> {
  final _formKey = GlobalKey<FormState>();
  final _ageController = TextEditingController();
  final _numMedicationsController = TextEditingController();
  final _medicationComplexityController = TextEditingController();
  final _daysSinceStartController = TextEditingController();
  final _missedDosesController = TextEditingController();
  final _snoozeFrequencyController = TextEditingController();
  final _chronicConditionsController = TextEditingController();
  final _previousAdherenceController = TextEditingController();

  // Inject prediction service
  final _predictionService = AdherencePredictionService();

  bool _isLoading = false;
  double? _predictedAdherence;
  String? _errorMessage;

  @override
  void dispose() {
    _ageController.dispose();
    _numMedicationsController.dispose();
    _medicationComplexityController.dispose();
    _daysSinceStartController.dispose();
    _missedDosesController.dispose();
    _snoozeFrequencyController.dispose();
    _chronicConditionsController.dispose();
    _previousAdherenceController.dispose();
    super.dispose();
  }

  String? _validateInteger(String? value, String fieldName, int min, int max) {
    if (value == null || value.isEmpty) {
      return '$fieldName is required';
    }
    final intValue = int.tryParse(value);
    if (intValue == null) {
      return '$fieldName must be a valid number';
    }
    if (intValue < min || intValue > max) {
      return '$fieldName must be between $min and $max';
    }
    return null;
  }

  String? _validateDouble(
    String? value,
    String fieldName,
    double min,
    double max,
  ) {
    if (value == null || value.isEmpty) {
      return '$fieldName is required';
    }
    final doubleValue = double.tryParse(value);
    if (doubleValue == null) {
      return '$fieldName must be a valid number';
    }
    if (doubleValue < min || doubleValue > max) {
      return '$fieldName must be between $min and $max';
    }
    return null;
  }

  Future<void> _handlePredict() async {
    // Show immediate feedback
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Making prediction...'),
        duration: Duration(seconds: 1),
      ),
    );

    if (!_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please fill in all fields correctly'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    // Clear previous results when new prediction is requested
    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _predictedAdherence = null;
    });

    try {
      // Make API call with all 8 features
      final prediction = await _predictionService.predictAdherence(
        age: int.parse(_ageController.text),
        numMedications: int.parse(_numMedicationsController.text),
        medicationComplexity: double.parse(
          _medicationComplexityController.text,
        ),
        daysSinceStart: int.parse(_daysSinceStartController.text),
        missedDosesLastWeek: int.parse(_missedDosesController.text),
        snoozeFrequency: double.parse(_snoozeFrequencyController.text),
        chronicConditions: int.parse(_chronicConditionsController.text),
        previousAdherenceRate: double.parse(_previousAdherenceController.text),
      );

      // Display predicted adherence rate on successful response
      setState(() {
        _isLoading = false;
        _predictedAdherence = prediction;
      });

      // Show success message
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Prediction complete: ${prediction.toStringAsFixed(1)}%',
            ),
            backgroundColor: Colors.green,
          ),
        );
      }
    } on TimeoutException catch (e) {
      // Display connection error messages on network failures
      final errorMsg =
          e.message ??
          'Request timed out. Please check your connection and try again.';
      setState(() {
        _isLoading = false;
        _errorMessage = errorMsg;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
        );
      }
    } on SocketException catch (e) {
      // Display connection error messages on network failures
      final errorMsg = e.message.isNotEmpty
          ? e.message
          : 'No internet connection. Please check your network and try again.';
      setState(() {
        _isLoading = false;
        _errorMessage = errorMsg;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
        );
      }
    } on HttpException catch (e) {
      // Display user-friendly error messages on API errors
      setState(() {
        _isLoading = false;
        _errorMessage = e.message;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message), backgroundColor: Colors.red),
        );
      }
    } on FormatException {
      // Display user-friendly error messages on API errors
      const errorMsg = 'Failed to parse server response. Please try again.';
      setState(() {
        _isLoading = false;
        _errorMessage = errorMsg;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
        );
      }
    } catch (e) {
      // Display user-friendly error messages on API errors
      final errorMsg = 'An unexpected error occurred: $e';
      setState(() {
        _isLoading = false;
        _errorMessage = errorMsg;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Adherence Prediction')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Information card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.info_outline,
                            color: Theme.of(context).colorScheme.primary,
                            size: 20,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            'Predict Your Adherence Rate',
                            style: Theme.of(context).textTheme.titleMedium
                                ?.copyWith(fontWeight: FontWeight.w600),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Enter your information below to get a prediction of your medication adherence rate.',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Theme.of(
                            context,
                          ).colorScheme.onSurface.withValues(alpha: 0.7),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Input fields
              CustomTextField(
                label: 'Age',
                hintText: 'Enter your age (18-120)',
                controller: _ageController,
                keyboardType: TextInputType.number,
                validator: (value) => _validateInteger(value, 'Age', 18, 120),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Number of Medications',
                hintText: 'Enter number of medications (1-20)',
                controller: _numMedicationsController,
                keyboardType: TextInputType.number,
                validator: (value) =>
                    _validateInteger(value, 'Number of medications', 1, 20),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Medication Complexity',
                hintText: 'Enter complexity score (1.0-5.0)',
                controller: _medicationComplexityController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                validator: (value) =>
                    _validateDouble(value, 'Medication complexity', 1.0, 5.0),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Days Since Start',
                hintText: 'Days since starting regimen (0+)',
                controller: _daysSinceStartController,
                keyboardType: TextInputType.number,
                validator: (value) =>
                    _validateInteger(value, 'Days since start', 0, 10000),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Missed Doses Last Week',
                hintText: 'Number of missed doses (0-50)',
                controller: _missedDosesController,
                keyboardType: TextInputType.number,
                validator: (value) =>
                    _validateInteger(value, 'Missed doses', 0, 50),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Snooze Frequency',
                hintText: 'Proportion of reminders snoozed (0.0-1.0)',
                controller: _snoozeFrequencyController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                validator: (value) =>
                    _validateDouble(value, 'Snooze frequency', 0.0, 1.0),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Chronic Conditions',
                hintText: 'Number of chronic conditions (0-10)',
                controller: _chronicConditionsController,
                keyboardType: TextInputType.number,
                validator: (value) =>
                    _validateInteger(value, 'Chronic conditions', 0, 10),
              ),
              const SizedBox(height: 16),

              CustomTextField(
                label: 'Previous Adherence Rate',
                hintText: 'Historical adherence rate % (0.0-100.0)',
                controller: _previousAdherenceController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                validator: (value) => _validateDouble(
                  value,
                  'Previous adherence rate',
                  0.0,
                  100.0,
                ),
              ),
              const SizedBox(height: 24),

              // Predict button
              PrimaryButton(
                text: 'Predict Adherence',
                onPressed: _handlePredict,
                isLoading: _isLoading,
                fullWidth: true,
                icon: Icons.analytics,
              ),
              const SizedBox(height: 24),

              // Result card
              if (_predictedAdherence != null || _errorMessage != null)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(
                              _errorMessage != null
                                  ? Icons.error_outline
                                  : Icons.check_circle_outline,
                              color: _errorMessage != null
                                  ? Theme.of(context).colorScheme.error
                                  : Colors.green,
                              size: 24,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              _errorMessage != null
                                  ? 'Error'
                                  : 'Prediction Result',
                              style: Theme.of(context).textTheme.titleMedium
                                  ?.copyWith(fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        if (_errorMessage != null)
                          Text(
                            _errorMessage!,
                            style: Theme.of(context).textTheme.bodyMedium
                                ?.copyWith(
                                  color: Theme.of(context).colorScheme.error,
                                ),
                          )
                        else if (_predictedAdherence != null)
                          Column(
                            children: [
                              Text(
                                '${_predictedAdherence!.toStringAsFixed(1)}%',
                                style: Theme.of(context).textTheme.displayMedium
                                    ?.copyWith(
                                      fontWeight: FontWeight.bold,
                                      color: Theme.of(
                                        context,
                                      ).colorScheme.primary,
                                    ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Predicted Adherence Rate',
                                style: Theme.of(context).textTheme.bodyLarge,
                              ),
                              const SizedBox(height: 16),
                              LinearProgressIndicator(
                                value: _predictedAdherence! / 100,
                                backgroundColor: Theme.of(
                                  context,
                                ).colorScheme.surfaceContainerHighest,
                                valueColor: AlwaysStoppedAnimation<Color>(
                                  _getAdherenceColor(_predictedAdherence!),
                                ),
                                minHeight: 8,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                _getAdherenceMessage(_predictedAdherence!),
                                style: Theme.of(context).textTheme.bodyMedium
                                    ?.copyWith(
                                      color: Theme.of(context)
                                          .colorScheme
                                          .onSurface
                                          .withValues(alpha: 0.7),
                                    ),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getAdherenceColor(double adherence) {
    if (adherence >= 80) {
      return Colors.green;
    } else if (adherence >= 60) {
      return Colors.orange;
    } else {
      return Colors.red;
    }
  }

  String _getAdherenceMessage(double adherence) {
    if (adherence >= 80) {
      return 'Excellent! You\'re maintaining good medication adherence.';
    } else if (adherence >= 60) {
      return 'Good progress, but there\'s room for improvement.';
    } else {
      return 'Your adherence could be better. Consider setting more reminders.';
    }
  }
}
