import 'package:dartz/dartz.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/errors/failures.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../medication/domain/entities/medication_entity.dart';
import '../../domain/entities/adherence_entity.dart';
import '../../domain/repositories/dashboard_repository.dart';
import '../datasources/dashboard_remote_data_source.dart';
import '../../../medication/data/models/medication_model.dart';

class DashboardRepositoryImpl implements DashboardRepository {
  final DashboardRemoteDataSource remoteDataSource;
  final FirebaseAuth firebaseAuth;

  DashboardRepositoryImpl({
    required this.remoteDataSource,
    required this.firebaseAuth,
  });

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<Either<Failure, List<MedicationEntity>>> getTodayMedications() async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final medications = await remoteDataSource.getTodayMedications(
        _currentUserId,
      );
      return Right(medications.map((model) => model.toEntity()).toList());
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
  Future<Either<Failure, AdherenceEntity>> getAdherenceStats({
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

      final adherenceModel = await remoteDataSource.getAdherenceStats(
        _currentUserId,
        startDate: startDate,
        endDate: endDate,
      );
      return Right(adherenceModel.toEntity());
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
  Stream<Either<Failure, AdherenceEntity>> watchAdherenceStats() {
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
          .watchAdherenceStats(_currentUserId)
          .map((adherence) {
            return Right(adherence.toEntity())
                as Either<Failure, AdherenceEntity>;
          })
          .handleError((error) {
            if (error is PermissionException) {
              return Left(
                    PermissionFailure(message: error.message, code: error.code),
                  )
                  as Either<Failure, AdherenceEntity>;
            } else if (error is NetworkException) {
              return Left(
                    NetworkFailure(message: error.message, code: error.code),
                  )
                  as Either<Failure, AdherenceEntity>;
            } else if (error is FirestoreException) {
              return Left(DataFailure(message: error.message, code: error.code))
                  as Either<Failure, AdherenceEntity>;
            } else {
              return Left(
                    DataFailure(
                      message: 'Unexpected error: ${error.toString()}',
                      code: 'unexpected_error',
                    ),
                  )
                  as Either<Failure, AdherenceEntity>;
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
