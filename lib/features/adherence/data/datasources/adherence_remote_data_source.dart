import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/constants/firebase_constants.dart';
import '../../../../core/errors/exceptions.dart';
import '../models/adherence_log_model.dart';
import '../../domain/entities/adherence_log_entity.dart';

abstract class AdherenceRemoteDataSource {
  Future<List<AdherenceLogModel>> getAdherenceLogs(
    String userId, {
    DateTime? startDate,
    DateTime? endDate,
  });
  Future<AdherenceLogModel> logMedicationTaken(AdherenceLogModel log);
  Future<void> updateAdherenceLog(AdherenceLogModel log);
  Future<Map<String, dynamic>> getAdherenceSummary(
    String userId,
    DateTime startDate,
    DateTime endDate,
  );
  Stream<List<AdherenceLogModel>> watchAdherenceLogs(String userId);
}

class AdherenceRemoteDataSourceImpl implements AdherenceRemoteDataSource {
  final FirebaseFirestore firestore;
  final FirebaseAuth firebaseAuth;

  AdherenceRemoteDataSourceImpl({
    required this.firestore,
    required this.firebaseAuth,
  });

  CollectionReference get _adherenceLogsCollection =>
      firestore.collection(FirebaseConstants.adherenceLogsPath);

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<List<AdherenceLogModel>> getAdherenceLogs(
    String userId, {
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      Query query = _adherenceLogsCollection.where(
        FirebaseConstants.userIdField,
        isEqualTo: userId,
      );

      if (startDate != null) {
        query = query.where(
          'scheduledTime',
          isGreaterThanOrEqualTo: Timestamp.fromDate(startDate),
        );
      }

      if (endDate != null) {
        query = query.where(
          'scheduledTime',
          isLessThanOrEqualTo: Timestamp.fromDate(endDate),
        );
      }

      final querySnapshot = await query
          .orderBy('scheduledTime', descending: true)
          .get();

      return querySnapshot.docs
          .map((doc) => AdherenceLogModel.fromDocument(doc))
          .toList();
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to get adherence logs: ${e.toString()}',
        code: 'get_adherence_logs_error',
      );
    }
  }

  @override
  Future<AdherenceLogModel> logMedicationTaken(AdherenceLogModel log) async {
    try {
      // Verify ownership
      if (log.userId != _currentUserId) {
        throw PermissionException(
          message: 'You can only log medications for yourself',
          code: 'permission_denied',
        );
      }

      final docRef = _adherenceLogsCollection.doc();
      final now = DateTime.now();

      final logWithId = AdherenceLogModel(
        id: docRef.id,
        userId: log.userId,
        medicationId: log.medicationId,
        scheduledTime: log.scheduledTime,
        takenTime: log.takenTime ?? now,
        status: log.status,
        snoozeDuration: log.snoozeDuration,
        createdAt: now,
        deviceInfo: log.deviceInfo,
      );

      await docRef.set(logWithId.toDocument());
      return logWithId;
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } on AppException {
      rethrow;
    } catch (e) {
      throw DataException(
        message: 'Failed to log medication: ${e.toString()}',
        code: 'log_medication_error',
      );
    }
  }

  @override
  Future<void> updateAdherenceLog(AdherenceLogModel log) async {
    try {
      // Verify ownership
      if (log.userId != _currentUserId) {
        throw PermissionException(
          message: 'You can only update your own adherence logs',
          code: 'permission_denied',
        );
      }

      final docRef = _adherenceLogsCollection.doc(log.id);
      final doc = await docRef.get();

      if (!doc.exists) {
        throw NotFoundException(
          message: 'Adherence log not found',
          code: 'adherence_log_not_found',
        );
      }

      await docRef.update(log.toDocument());
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } on AppException {
      rethrow;
    } catch (e) {
      throw DataException(
        message: 'Failed to update adherence log: ${e.toString()}',
        code: 'update_adherence_log_error',
      );
    }
  }

  @override
  Future<Map<String, dynamic>> getAdherenceSummary(
    String userId,
    DateTime startDate,
    DateTime endDate,
  ) async {
    try {
      final logs = await getAdherenceLogs(
        userId,
        startDate: startDate,
        endDate: endDate,
      );

      final totalScheduled = logs.length;
      final takenCount = logs
          .where((log) => log.status == AdherenceStatus.taken)
          .length;
      final missedCount = logs
          .where((log) => log.status == AdherenceStatus.missed)
          .length;
      final snoozedCount = logs
          .where((log) => log.status == AdherenceStatus.snoozed)
          .length;

      final adherenceRate = totalScheduled > 0
          ? takenCount / totalScheduled
          : 0.0;

      // Calculate streak (consecutive days with taken status)
      int streakDays = 0;
      if (logs.isNotEmpty) {
        final sortedLogs = List<AdherenceLogModel>.from(logs)
          ..sort((a, b) => b.scheduledTime.compareTo(a.scheduledTime));

        for (final log in sortedLogs) {
          if (log.status == AdherenceStatus.taken) {
            streakDays++;
          } else {
            break;
          }
        }
      }

      return {
        'adherenceRate': adherenceRate,
        'totalScheduled': totalScheduled,
        'takenCount': takenCount,
        'missedCount': missedCount,
        'snoozedCount': snoozedCount,
        'streakDays': streakDays,
        'startDate': startDate.toIso8601String(),
        'endDate': endDate.toIso8601String(),
      };
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to get adherence summary: ${e.toString()}',
        code: 'get_adherence_summary_error',
      );
    }
  }

  @override
  Stream<List<AdherenceLogModel>> watchAdherenceLogs(String userId) {
    try {
      return _adherenceLogsCollection
          .where(FirebaseConstants.userIdField, isEqualTo: userId)
          .orderBy('scheduledTime', descending: true)
          .snapshots()
          .map(
            (snapshot) => snapshot.docs
                .map((doc) => AdherenceLogModel.fromDocument(doc))
                .toList(),
          );
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to watch adherence logs: ${e.toString()}',
        code: 'watch_adherence_logs_error',
      );
    }
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
