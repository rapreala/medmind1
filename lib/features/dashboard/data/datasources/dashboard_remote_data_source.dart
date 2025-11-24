import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/constants/firebase_constants.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../medication/data/models/medication_model.dart';
import '../../../medication/domain/entities/medication_entity.dart';
import '../models/adherence_model.dart';
import '../../domain/entities/adherence_entity.dart';
import '../../../adherence/data/datasources/adherence_remote_data_source.dart';
import '../../../adherence/data/models/adherence_log_model.dart';
import '../../../adherence/domain/entities/adherence_log_entity.dart';

abstract class DashboardRemoteDataSource {
  Future<List<MedicationModel>> getTodayMedications(String userId);
  Future<AdherenceModel> getAdherenceStats(
    String userId, {
    DateTime? startDate,
    DateTime? endDate,
  });
  Stream<AdherenceModel> watchAdherenceStats(String userId);
}

class DashboardRemoteDataSourceImpl implements DashboardRemoteDataSource {
  final FirebaseFirestore firestore;
  final FirebaseAuth firebaseAuth;
  final AdherenceRemoteDataSource adherenceDataSource;

  DashboardRemoteDataSourceImpl({
    required this.firestore,
    required this.firebaseAuth,
    required this.adherenceDataSource,
  });

  CollectionReference get _medicationsCollection =>
      firestore.collection(FirebaseConstants.medicationsPath);

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<List<MedicationModel>> getTodayMedications(String userId) async {
    try {
      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);

      // Get all active medications for the user
      final querySnapshot = await _medicationsCollection
          .where(FirebaseConstants.userIdField, isEqualTo: userId)
          .where(FirebaseConstants.isActiveField, isEqualTo: true)
          .get();

      final allMedications = querySnapshot.docs
          .map((doc) => MedicationModel.fromDocument(doc))
          .toList();

      // Filter medications that should be taken today
      final todayMedications = <MedicationModel>[];

      for (final medication in allMedications) {
        if (_shouldTakeToday(medication, today)) {
          todayMedications.add(medication);
        }
      }

      // Sort by first scheduled time
      todayMedications.sort((a, b) {
        if (a.times.isEmpty) return 1;
        if (b.times.isEmpty) return -1;
        final aTime = a.times.first;
        final bTime = b.times.first;
        final aMinutes = aTime.hour * 60 + aTime.minute;
        final bMinutes = bTime.hour * 60 + bTime.minute;
        return aMinutes.compareTo(bMinutes);
      });

      return todayMedications;
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to get today medications: ${e.toString()}',
        code: 'get_today_medications_error',
      );
    }
  }

  bool _shouldTakeToday(MedicationModel medication, DateTime today) {
    // Check if medication has started
    if (medication.startDate.isAfter(today)) {
      return false;
    }

    switch (medication.frequency) {
      case MedicationFrequency.daily:
        return true;
      case MedicationFrequency.weekly:
        final dayOfWeek = today.weekday % 7; // 0 = Sunday, 1 = Monday, etc.
        return medication.days.contains(dayOfWeek);
      case MedicationFrequency.custom:
        // For custom, check if today matches any of the specified days
        final dayOfWeek = today.weekday % 7;
        return medication.days.contains(dayOfWeek);
      default:
        return false;
    }
  }

  @override
  Future<AdherenceModel> getAdherenceStats(
    String userId, {
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      final now = DateTime.now();
      final defaultStartDate =
          startDate ?? now.subtract(const Duration(days: 30));
      final defaultEndDate = endDate ?? now;

      // Get adherence summary
      final summary = await adherenceDataSource.getAdherenceSummary(
        userId,
        defaultStartDate,
        defaultEndDate,
      );

      // Get all logs for weekly/monthly breakdown
      final logs = await adherenceDataSource.getAdherenceLogs(
        userId,
        startDate: defaultStartDate,
        endDate: defaultEndDate,
      );

      // Calculate weekly stats
      final weeklyStats = _calculateWeeklyStats(
        logs,
        defaultStartDate,
        defaultEndDate,
      );

      // Calculate monthly stats
      final monthlyStats = _calculateMonthlyStats(
        logs,
        defaultStartDate,
        defaultEndDate,
      );

      // Get total active medications
      final medicationsSnapshot = await _medicationsCollection
          .where(FirebaseConstants.userIdField, isEqualTo: userId)
          .where(FirebaseConstants.isActiveField, isEqualTo: true)
          .get();

      final totalMedications = medicationsSnapshot.docs.length;

      return AdherenceModel(
        adherenceRate: summary['adherenceRate'] as double,
        totalMedications: totalMedications,
        takenCount: summary['takenCount'] as int,
        missedCount: summary['missedCount'] as int,
        weeklyStats: weeklyStats,
        monthlyStats: monthlyStats,
        streakDays: summary['streakDays'] as int,
      );
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to get adherence stats: ${e.toString()}',
        code: 'get_adherence_stats_error',
      );
    }
  }

  List<WeeklyStats> _calculateWeeklyStats(
    List<AdherenceLogModel> logs,
    DateTime startDate,
    DateTime endDate,
  ) {
    final weeklyStats = <WeeklyStats>[];
    final weekMap = <int, List<AdherenceLogModel>>{};

    // Group logs by week
    for (final log in logs) {
      final logDate = log.scheduledTime;
      final weekNumber = _getWeekNumber(logDate, startDate);
      weekMap.putIfAbsent(weekNumber, () => []).add(log);
    }

    // Calculate stats for each week
    for (final entry in weekMap.entries) {
      final weekLogs = entry.value;
      final taken = weekLogs
          .where((log) => log.status == AdherenceStatus.taken)
          .length;
      final missed = weekLogs
          .where((log) => log.status == AdherenceStatus.missed)
          .length;
      final total = weekLogs.length;
      final rate = total > 0 ? taken / total : 0.0;

      weeklyStats.add(
        WeeklyStats(
          weekNumber: entry.key,
          adherenceRate: rate,
          takenCount: taken,
          missedCount: missed,
        ),
      );
    }

    return weeklyStats;
  }

  List<MonthlyStats> _calculateMonthlyStats(
    List<AdherenceLogModel> logs,
    DateTime startDate,
    DateTime endDate,
  ) {
    final monthlyStats = <MonthlyStats>[];
    final monthMap = <String, List<AdherenceLogModel>>{};

    // Group logs by month
    for (final log in logs) {
      final logDate = log.scheduledTime;
      final key = '${logDate.year}-${logDate.month}';
      monthMap.putIfAbsent(key, () => []).add(log);
    }

    // Calculate stats for each month
    for (final entry in monthMap.entries) {
      final parts = entry.key.split('-');
      final year = int.parse(parts[0]);
      final month = int.parse(parts[1]);
      final monthLogs = entry.value;
      final taken = monthLogs
          .where((log) => log.status == AdherenceStatus.taken)
          .length;
      final missed = monthLogs
          .where((log) => log.status == AdherenceStatus.missed)
          .length;
      final total = monthLogs.length;
      final rate = total > 0 ? taken / total : 0.0;

      monthlyStats.add(
        MonthlyStats(
          month: month,
          year: year,
          adherenceRate: rate,
          takenCount: taken,
          missedCount: missed,
        ),
      );
    }

    return monthlyStats;
  }

  int _getWeekNumber(DateTime date, DateTime startDate) {
    final difference = date.difference(startDate).inDays;
    return (difference / 7).floor();
  }

  @override
  Stream<AdherenceModel> watchAdherenceStats(String userId) {
    // For real-time stats, we'll need to combine streams from medications and logs
    // This is a simplified version - in production, you might want to debounce or combine streams
    return Stream.periodic(const Duration(seconds: 30), (_) {
      return getAdherenceStats(userId);
    }).asyncMap((future) => future);
  }

  AppException _handleFirebaseException(FirebaseException e) {
    switch (e.code) {
      case 'permission-denied':
        return PermissionException(
          message: 'Permission denied: ${e.message}',
          code: e.code,
        );
      case 'unavailable':
      case 'deadline-exceeded':
        return NetworkException(
          message: 'Network error: ${e.message}',
          code: e.code,
        );
      case 'not-found':
        return NotFoundException(
          message: 'Resource not found: ${e.message}',
          code: e.code,
        );
      default:
        return FirestoreException(
          message: e.message ?? 'Firestore error occurred',
          code: e.code,
          originalCode: e.code,
        );
    }
  }
}
