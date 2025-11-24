import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/adherence_log_entity.dart';

abstract class AdherenceRepository {
  /// Get adherence logs for a date range
  Future<Either<Failure, List<AdherenceLogEntity>>> getAdherenceLogs({
    DateTime? startDate,
    DateTime? endDate,
  });

  /// Log that a medication was taken
  Future<Either<Failure, AdherenceLogEntity>> logMedicationTaken(AdherenceLogEntity log);

  /// Get adherence summary/statistics for a date range
  Future<Either<Failure, Map<String, dynamic>>> getAdherenceSummary({
    required DateTime startDate,
    required DateTime endDate,
  });

  /// Export adherence data (for data export feature)
  Future<Either<Failure, String>> exportAdherenceData({
    DateTime? startDate,
    DateTime? endDate,
  });

  /// Watch adherence logs in real-time
  Stream<Either<Failure, List<AdherenceLogEntity>>> watchAdherenceLogs();
}

