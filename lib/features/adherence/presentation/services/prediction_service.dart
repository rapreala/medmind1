import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

/// Service for making adherence prediction API calls
///
/// This service communicates with the deployed FastAPI prediction endpoint
/// to generate medication adherence rate predictions based on patient data.
class AdherencePredictionService {
  // Deployed API base URL
  static const String _baseUrl = 'https://medmind-adherence-api.onrender.com';

  // API endpoint for predictions
  static const String _predictEndpoint = '/predict';

  // Request timeout duration (increased for cold starts on free tier)
  static const Duration _timeout = Duration(seconds: 90);

  /// Predicts medication adherence rate based on patient features
  ///
  /// Parameters:
  /// - [age]: Patient age in years (18-120)
  /// - [numMedications]: Number of active medications (1-20)
  /// - [medicationComplexity]: Complexity score (1.0-5.0)
  /// - [daysSinceStart]: Days since starting regimen (0+)
  /// - [missedDosesLastWeek]: Missed doses in past 7 days (0-50)
  /// - [snoozeFrequency]: Proportion of reminders snoozed (0.0-1.0)
  /// - [chronicConditions]: Number of chronic conditions (0-10)
  /// - [previousAdherenceRate]: Historical adherence rate (0.0-100.0)
  ///
  /// Returns: Predicted adherence rate as a percentage (0.0-100.0)
  ///
  /// Throws:
  /// - [TimeoutException] if request exceeds 10 seconds
  /// - [SocketException] if no internet connection
  /// - [HttpException] for HTTP errors (4xx, 5xx)
  /// - [FormatException] if response parsing fails
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
    try {
      // Construct the full URL
      final url = Uri.parse('$_baseUrl$_predictEndpoint');

      // Create JSON request body with all 8 features
      final requestBody = {
        'age': age,
        'num_medications': numMedications,
        'medication_complexity': medicationComplexity,
        'days_since_start': daysSinceStart,
        'missed_doses_last_week': missedDosesLastWeek,
        'snooze_frequency': snoozeFrequency,
        'chronic_conditions': chronicConditions,
        'previous_adherence_rate': previousAdherenceRate,
      };

      // Make POST request with timeout
      final response = await http
          .post(
            url,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(requestBody),
          )
          .timeout(_timeout);

      // Handle HTTP status codes
      if (response.statusCode == 200) {
        // Success - parse response
        final data = jsonDecode(response.body) as Map<String, dynamic>;

        // Extract predicted adherence rate
        final predictedRate = data['predicted_adherence_rate'];

        if (predictedRate is num) {
          return predictedRate.toDouble();
        } else {
          throw FormatException(
            'Invalid response format: predicted_adherence_rate is not a number',
          );
        }
      } else if (response.statusCode == 422) {
        // Validation error - extract error details
        final errorData = jsonDecode(response.body) as Map<String, dynamic>;
        final details = errorData['detail'] as List<dynamic>?;

        if (details != null && details.isNotEmpty) {
          final firstError = details[0] as Map<String, dynamic>;
          final field =
              (firstError['loc'] as List<dynamic>?)?.last ?? 'unknown';
          final message = firstError['msg'] ?? 'Validation error';
          throw HttpException(
            'Validation error for $field: $message',
            uri: url,
          );
        } else {
          throw HttpException(
            'Invalid input data. Please check all fields.',
            uri: url,
          );
        }
      } else if (response.statusCode >= 500) {
        // Server error
        throw HttpException(
          'Server error (${response.statusCode}). Please try again later.',
          uri: url,
        );
      } else if (response.statusCode >= 400) {
        // Client error
        throw HttpException(
          'Request error (${response.statusCode}). Please check your input.',
          uri: url,
        );
      } else {
        // Unexpected status code
        throw HttpException(
          'Unexpected response (${response.statusCode})',
          uri: url,
        );
      }
    } on TimeoutException {
      // Request timed out
      throw TimeoutException(
        'Request timed out after ${_timeout.inSeconds} seconds. The API may be starting up (cold start). Please wait a moment and try again.',
      );
    } on SocketException {
      // No internet connection
      throw SocketException(
        'No internet connection. Please check your network and try again.',
      );
    } on FormatException catch (e) {
      // JSON parsing error
      throw FormatException('Failed to parse server response: ${e.message}');
    } on HttpException {
      // Re-throw HTTP exceptions
      rethrow;
    } catch (e) {
      // Unexpected error
      throw Exception('Unexpected error: $e');
    }
  }

  /// Tests the API connection by checking the health endpoint
  ///
  /// Returns: true if API is healthy and models are loaded
  ///
  /// Throws: Exception if health check fails
  Future<bool> checkHealth() async {
    try {
      final url = Uri.parse('$_baseUrl/health');

      final response = await http.get(url).timeout(_timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        final status = data['status'] as String?;
        final modelLoaded = data['model_loaded'] as bool?;
        final scalerLoaded = data['scaler_loaded'] as bool?;

        return status == 'healthy' &&
            modelLoaded == true &&
            scalerLoaded == true;
      } else {
        return false;
      }
    } catch (e) {
      throw Exception('Health check failed: $e');
    }
  }
}
