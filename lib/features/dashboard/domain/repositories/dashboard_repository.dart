import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../../../medication/domain/entities/medication_entity.dart';
import '../entities/adherence_entity.dart';

abstract class DashboardRepository {
  /// Get today's medications for the specified user
  Future<Either<Failure, List<MedicationEntity>>> getTodayMedications(
    String userId,
  );

  /// Get adherence statistics for the specified user
  Future<Either<Failure, AdherenceEntity>> getAdherenceStats(
    String userId, {
    DateTime? startDate,
    DateTime? endDate,
  });

  /// Watch adherence stats in real-time for the specified user
  Stream<Either<Failure, AdherenceEntity>> watchAdherenceStats(String userId);
}
