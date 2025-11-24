import 'package:dartz/dartz.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/errors/failures.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/adherence_log_entity.dart';
import '../../domain/repositories/adherence_repository.dart';
import '../datasources/adherence_remote_data_source.dart';
import '../models/adherence_log_model.dart';
import 'dart:convert';

class AdherenceRepositoryImpl implements AdherenceRepository {
  final AdherenceRemoteDataSource remoteDataSource;
  final FirebaseAuth firebaseAuth;

  AdherenceRepositoryImpl({
    required this.remoteDataSource,
    required this.firebaseAuth,
  });

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<Either<Failure, List<AdherenceLogEntity>>> getAdherenceLogs({
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final logs = await remoteDataSource.getAdherenceLogs(
        _currentUserId,
        startDate: startDate,
        endDate: endDate,
      );
      return Right(logs.map((model) => model.toEntity()).toList());
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on FirestoreException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } on DataException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } catch (e) {
      return Left(
        DataFailure(
          message: 'Unexpected error: ${e.toString()}',
          code: 'unexpected_error',
        ),
      );
    }
  }

  @override
  Future<Either<Failure, AdherenceLogEntity>> logMedicationTaken(
    AdherenceLogEntity log,
  ) async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final logModel = AdherenceLogModel.fromEntity(log);
      final logged = await remoteDataSource.logMedicationTaken(logModel);
      return Right(logged.toEntity());
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on FirestoreException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } on DataException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } catch (e) {
      return Left(
        DataFailure(
          message: 'Unexpected error: ${e.toString()}',
          code: 'unexpected_error',
        ),
      );
    }
  }

  @override
  Future<Either<Failure, Map<String, dynamic>>> getAdherenceSummary({
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final summary = await remoteDataSource.getAdherenceSummary(
        _currentUserId,
        startDate,
        endDate,
      );
      return Right(summary);
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on FirestoreException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } on DataException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } catch (e) {
      return Left(
        DataFailure(
          message: 'Unexpected error: ${e.toString()}',
          code: 'unexpected_error',
        ),
      );
    }
  }

  @override
  Future<Either<Failure, String>> exportAdherenceData({
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final logs = await remoteDataSource.getAdherenceLogs(
        _currentUserId,
        startDate: startDate,
        endDate: endDate,
      );

      // Convert to JSON
      final jsonData = {
        'exportDate': DateTime.now().toIso8601String(),
        'userId': _currentUserId,
        'startDate': startDate?.toIso8601String(),
        'endDate': endDate?.toIso8601String(),
        'logs': logs.map((log) => log.toJson()).toList(),
      };

      return Right(jsonEncode(jsonData));
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on FirestoreException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } on DataException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
    } catch (e) {
      return Left(
        DataFailure(
          message: 'Unexpected error: ${e.toString()}',
          code: 'unexpected_error',
        ),
      );
    }
  }

  @override
  Stream<Either<Failure, List<AdherenceLogEntity>>> watchAdherenceLogs() {
    try {
      if (_currentUserId.isEmpty) {
        return Stream.value(
          const Left(
            AuthenticationFailure(
              message: 'User not authenticated',
              code: 'not_authenticated',
            ),
          ),
        );
      }

      return remoteDataSource
          .watchAdherenceLogs(_currentUserId)
          .map((logs) {
            return Right(logs.map((model) => model.toEntity()).toList())
                as Either<Failure, List<AdherenceLogEntity>>;
          })
          .handleError((error) {
            if (error is PermissionException) {
              return Left(
                    PermissionFailure(message: error.message, code: error.code),
                  )
                  as Either<Failure, List<AdherenceLogEntity>>;
            } else if (error is NetworkException) {
              return Left(
                    NetworkFailure(message: error.message, code: error.code),
                  )
                  as Either<Failure, List<AdherenceLogEntity>>;
            } else if (error is FirestoreException) {
              return Left(DataFailure(message: error.message, code: error.code))
                  as Either<Failure, List<AdherenceLogEntity>>;
            } else {
              return Left(
                    DataFailure(
                      message: 'Unexpected error: ${error.toString()}',
                      code: 'unexpected_error',
                    ),
                  )
                  as Either<Failure, List<AdherenceLogEntity>>;
            }
          });
    } catch (e) {
      return Stream.value(
        Left(
          DataFailure(
            message: 'Unexpected error: ${e.toString()}',
            code: 'unexpected_error',
          ),
        ),
      );
    }
  }
}
