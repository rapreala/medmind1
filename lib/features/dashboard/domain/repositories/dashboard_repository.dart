import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../../../medication/domain/entities/medication_entity.dart';
import '../entities/adherence_entity.dart';

abstract class DashboardRepository {
  /// Get today's medications for the current user
  Future<Either<Failure, List<MedicationEntity>>> getTodayMedications();

  /// Get adherence statistics
  Future<Either<Failure, AdherenceEntity>> getAdherenceStats({
    DateTime? startDate,
    DateTime? endDate,
  });

  /// Watch adherence stats in real-time
  Stream<Either<Failure, AdherenceEntity>> watchAdherenceStats();
}

