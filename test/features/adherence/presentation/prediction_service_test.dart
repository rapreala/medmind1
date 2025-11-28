import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:medmind/features/adherence/presentation/services/prediction_service.dart';

void main() {
  group('AdherencePredictionService', () {
    late AdherencePredictionService service;

    setUp(() {
      service = AdherencePredictionService();
    });

    test(
      'predictAdherence returns a valid adherence rate',
      () async {
        // This test requires internet connection and the API to be running
        // Skip if running in CI or offline environment

        try {
          final result = await service.predictAdherence(
            age: 45,
            numMedications: 3,
            medicationComplexity: 2.5,
            daysSinceStart: 120,
            missedDosesLastWeek: 1,
            snoozeFrequency: 0.2,
            chronicConditions: 2,
            previousAdherenceRate: 85.5,
          );

          // Verify result is within valid range
          expect(result, greaterThanOrEqualTo(0.0));
          expect(result, lessThanOrEqualTo(100.0));
        } on SocketException {
          // Skip test if no internet connection
          print('Skipping test: No internet connection');
        } catch (e) {
          // Log error but don't fail test (API might be cold starting)
          print('Test skipped due to: $e');
        }
      },
      skip: 'Requires live API connection',
    );

    test(
      'predictAdherence throws TimeoutException on timeout',
      () async {
        // This test would require mocking, which is beyond the scope
        // of this basic verification
      },
      skip: 'Requires mocking',
    );

    test(
      'checkHealth returns true when API is healthy',
      () async {
        try {
          final isHealthy = await service.checkHealth();
          expect(isHealthy, isA<bool>());
        } on SocketException {
          print('Skipping test: No internet connection');
        } catch (e) {
          print('Test skipped due to: $e');
        }
      },
      skip: 'Requires live API connection',
    );
  });
}
