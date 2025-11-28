import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/timezone.dart' as tz;
import '../services/pending_dose_tracker.dart';

class NotificationUtils {
  static final FlutterLocalNotificationsPlugin _notificationsPlugin =
      FlutterLocalNotificationsPlugin();

  static bool _isInitialized = false;

  static Future<void> initialize() async {
    try {
      const AndroidInitializationSettings androidSettings =
          AndroidInitializationSettings('@mipmap/ic_launcher');

      const DarwinInitializationSettings iosSettings =
          DarwinInitializationSettings(
            requestAlertPermission: true,
            requestBadgePermission: true,
            requestSoundPermission: true,
          );

      const InitializationSettings settings = InitializationSettings(
        android: androidSettings,
        iOS: iosSettings,
      );

      // Set up notification tap handler and background handler
      await _notificationsPlugin.initialize(
        settings,
        onDidReceiveNotificationResponse: _onNotificationTapped,
        onDidReceiveBackgroundNotificationResponse: _onNotificationTapped,
      );

      _isInitialized = true;
      print('Notification system initialized successfully');
    } catch (e) {
      print('Failed to initialize notifications: $e');
      _isInitialized = false;
    }
  }

  static Future<void> _onNotificationTapped(
    NotificationResponse response,
  ) async {
    // Handle notification tap
    // Payload contains medication ID and name in format: "id|name"
    print('Notification tapped: ${response.payload}');

    if (response.payload != null && response.payload!.isNotEmpty) {
      final parts = response.payload!.split('|');
      if (parts.length >= 2) {
        final medicationId = parts[0];
        final medicationName = parts[1];

        // Add to pending doses when notification is tapped
        await _addToPendingDoses(medicationId, medicationName);
      }
    }
    // TODO: Navigate to medication detail or pending doses page
  }

  /// Add a dose to pending doses tracker when notification fires
  static Future<void> _addToPendingDoses(
    String medicationId,
    String medicationName,
  ) async {
    try {
      await PendingDoseTracker.addPendingDose(
        medicationId: medicationId,
        medicationName: medicationName,
        scheduledTime: DateTime.now(),
      );
      print('✅ Added pending dose for $medicationName');
    } catch (e) {
      print('❌ Failed to add pending dose: $e');
    }
  }

  static Future<void> scheduleMedicationReminder({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledTime,
    required String payload,
    bool recurring = true,
  }) async {
    if (!_isInitialized) {
      print('Notifications not initialized - skipping schedule');
      return;
    }

    try {
      final tzScheduledTime = _scheduleTime(scheduledTime);

      await _notificationsPlugin.zonedSchedule(
        id,
        title,
        body,
        tzScheduledTime,
        NotificationDetails(
          android: AndroidNotificationDetails(
            'medication_reminder',
            'Medication Reminders',
            channelDescription: 'Notifications for medication reminders',
            importance: Importance.high,
            priority: Priority.high,
            // Show notification even when app is in foreground
            playSound: true,
            enableVibration: true,
          ),
          iOS: const DarwinNotificationDetails(
            sound: 'default',
            presentAlert: true,
            presentBadge: true,
            presentSound: true,
          ),
        ),
        uiLocalNotificationDateInterpretation:
            UILocalNotificationDateInterpretation.absoluteTime,
        matchDateTimeComponents: recurring ? DateTimeComponents.time : null,
        payload: payload,
        androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      );

      print(
        '✅ Scheduled notification for ${scheduledTime.hour}:${scheduledTime.minute.toString().padLeft(2, '0')}',
      );
    } catch (e) {
      print('Failed to schedule reminder: $e');
    }
  }

  static tz.TZDateTime _scheduleTime(DateTime scheduledTime) {
    final now = DateTime.now();
    final scheduled = DateTime(
      now.year,
      now.month,
      now.day,
      scheduledTime.hour,
      scheduledTime.minute,
    );

    if (scheduled.isBefore(now)) {
      return tz.TZDateTime.from(
        scheduled.add(const Duration(days: 1)),
        tz.local,
      );
    }

    return tz.TZDateTime.from(scheduled, tz.local);
  }

  static Future<void> cancelReminder(int id) async {
    if (!_isInitialized) return;

    try {
      await _notificationsPlugin.cancel(id);
    } catch (e) {
      print('Failed to cancel reminder: $e');
    }
  }

  static Future<void> cancelAllReminders() async {
    if (!_isInitialized) return;

    try {
      await _notificationsPlugin.cancelAll();
    } catch (e) {
      print('Failed to cancel all reminders: $e');
    }
  }

  static Future<void> showInstantNotification({
    required String title,
    required String body,
    String? payload,
  }) async {
    print('🔔 showInstantNotification called: $title');
    print('🔔 Initialized: $_isInitialized');

    if (!_isInitialized) {
      print('❌ Notifications not initialized - showing fallback');
      print('NOTIFICATION: $title - $body');
      return;
    }

    try {
      print('📤 Attempting to show notification...');
      await _notificationsPlugin.show(
        DateTime.now().millisecondsSinceEpoch.remainder(100000),
        title,
        body,
        const NotificationDetails(
          android: AndroidNotificationDetails(
            'instant_notifications',
            'Instant Notifications',
            channelDescription: 'Instant notification channel',
            importance: Importance.high,
            priority: Priority.high,
            playSound: true,
            enableVibration: true,
          ),
          iOS: DarwinNotificationDetails(),
        ),
        payload: payload,
      );
      print('✅ Notification shown successfully');
    } catch (e) {
      print('❌ Failed to show notification: $e');
      print('NOTIFICATION FALLBACK: $title - $body');
    }
  }

  static Future<void> requestPermissions() async {
    if (!_isInitialized) return;

    try {
      await _notificationsPlugin
          .resolvePlatformSpecificImplementation<
            IOSFlutterLocalNotificationsPlugin
          >()
          ?.requestPermissions(alert: true, badge: true, sound: true);
    } catch (e) {
      print('Failed to request permissions: $e');
    }
  }

  static Future<List<PendingNotificationRequest>>
  getPendingNotifications() async {
    if (!_isInitialized) return [];

    try {
      return await _notificationsPlugin.pendingNotificationRequests();
    } catch (e) {
      print('Failed to get pending notifications: $e');
      return [];
    }
  }

  /// Schedule a one-time notification for testing (fires in X seconds)
  static Future<void> scheduleTestNotification({
    required String medicationId,
    required String medicationName,
    required int delaySeconds,
  }) async {
    if (!_isInitialized) {
      print('Notifications not initialized');
      return;
    }

    final scheduledTime = DateTime.now().add(Duration(seconds: delaySeconds));

    await scheduleMedicationReminder(
      id: medicationId.hashCode,
      title: 'Test Reminder',
      body: 'Time to take $medicationName (Test notification)',
      scheduledTime: scheduledTime,
      payload: '$medicationId|$medicationName',
      recurring: false, // One-time notification for testing
    );

    print(
      '✅ Scheduled test notification for $medicationName in $delaySeconds seconds',
    );
  }
}
