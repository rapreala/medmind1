import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:medmind/core/services/pending_dose_tracker.dart';

/// Debug script to manually test pending dose functionality
/// Run with: flutter test test/debug_pending_doses.dart
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('Debug: Add and retrieve pending doses', () async {
    // Initialize SharedPreferences for testing
    SharedPreferences.setMockInitialValues({});

    print('\n=== PENDING DOSES DEBUG TEST ===\n');

    // Clear any existing doses
    await PendingDoseTracker.clearAllPendingDoses();
    print('✅ Cleared all pending doses');

    // Check initial count
    var count = await PendingDoseTracker.getPendingDoseCount();
    print('📊 Initial count: $count');
    assert(count == 0, 'Initial count should be 0');

    // Add a missed dose
    final now = DateTime.now();
    final missedTime = DateTime(
      now.year,
      now.month,
      now.day,
      1,
      0,
    ); // 1:00 AM today

    print('\n📋 Adding missed dose...');
    print('   Medication: Test Med');
    print('   Scheduled: ${missedTime.toString()}');
    print('   Current time: ${now.toString()}');

    await PendingDoseTracker.addPendingDose(
      medicationId: 'test-med-1',
      medicationName: 'Test Med',
      scheduledTime: missedTime,
    );

    // Check count after adding
    count = await PendingDoseTracker.getPendingDoseCount();
    print('\n📊 Count after adding: $count');
    assert(count == 1, 'Count should be 1 after adding one dose');

    // Retrieve all doses
    final doses = await PendingDoseTracker.getPendingDoses();
    print('\n📋 All pending doses:');
    for (final entry in doses.entries) {
      print('   ID: ${entry.key}');
      print('   Medication: ${entry.value['medicationName']}');
      print('   Scheduled: ${entry.value['scheduledTime']}');
      print('   ---');
    }

    // Add more doses
    print('\n📋 Adding 2 more doses...');
    await PendingDoseTracker.addPendingDose(
      medicationId: 'test-med-2',
      medicationName: 'Test Med 2',
      scheduledTime: DateTime(now.year, now.month, now.day, 2, 0),
    );

    await PendingDoseTracker.addPendingDose(
      medicationId: 'test-med-3',
      medicationName: 'Test Med 3',
      scheduledTime: DateTime(now.year, now.month, now.day, 3, 0),
    );

    count = await PendingDoseTracker.getPendingDoseCount();
    print('📊 Final count: $count');
    assert(count == 3, 'Count should be 3 after adding three doses');

    print('\n✅ All tests passed!');
    print('=== END DEBUG TEST ===\n');
  });
}
