import 'package:dartz/dartz.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../../core/errors/failures.dart';
import '../../../medication/domain/entities/medication_entity.dart';
import '../../domain/entities/adherence_entity.dart';
import '../../domain/repositories/dashboard_repository.dart';
import '../datasources/dashboard_remote_data_source.dart';

class DashboardRepositoryImpl implements DashboardRepository {
  final DashboardRemoteDataSource remoteDataSource;
  final FirebaseAuth firebaseAuth;

  DashboardRepositoryImpl({
    required this.remoteDataSource,
    required this.firebaseAuth,
  });

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<Either<Failure, List<MedicationEntity>>> getTodayMedications(
    String userId,
  ) async {
    try {
      if (_currentUserId.isEmpty) {
        return Left(AuthenticationFailure(message: 'User not authenticated'));
      }

      // Verify user can only access their own medications
      if (userId != _currentUserId) {
        return Left(PermissionFailure(message: 'Access denied to medications'));
      }

      final medications = await remoteDataSource.getTodayMedications(userId);
      return Right(medications.cast<MedicationEntity>());
    } on AppException catch (e) {
      return Left(_mapExceptionToFailure(e));
    } catch (e) {
      return Left(DataFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, AdherenceEntity>> getAdherenceStats(
    String userId, {
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      if (_currentUserId.isEmpty) {
        return Left(AuthenticationFailure(message: 'User not authenticated'));
      }

      // Verify user can only access their own stats
      if (userId != _currentUserId) {
        return Left(
          PermissionFailure(message: 'Access denied to adherence stats'),
        );
      }

      // Validate date range if provided
      if (startDate != null && endDate != null && startDate.isAfter(endDate)) {
        return Left(
          ValidationFailure(message: 'Start date must be before end date'),
        );
      }

      final adherenceStats = await remoteDataSource.getAdherenceStats(
        userId,
        startDate: startDate,
        endDate: endDate,
      );

      return Right(adherenceStats);
    } on AppException catch (e) {
      return Left(_mapExceptionToFailure(e));
    } catch (e) {
      return Left(DataFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Stream<Either<Failure, AdherenceEntity>> watchAdherenceStats(String userId) {
    try {
      if (_currentUserId.isEmpty) {
        return Stream.value(
          Left(AuthenticationFailure(message: 'User not authenticated')),
        );
      }

      // Verify user can only watch their own stats
      if (userId != _currentUserId) {
        return Stream.value(
          Left(PermissionFailure(message: 'Access denied to adherence stats')),
        );
      }

      return remoteDataSource
          .watchAdherenceStats(userId)
          .map<Either<Failure, AdherenceEntity>>(
            (adherenceStats) => Right(adherenceStats),
          )
          .handleError((error) {
            if (error is AppException) {
              return Left(_mapExceptionToFailure(error));
            }
            return Left(
              DataFailure(message: 'Stream error: ${error.toString()}'),
            );
          });
    } catch (e) {
      return Stream.value(
        Left(DataFailure(message: 'Failed to setup stream: ${e.toString()}')),
      );
    }
  }

  /// Map exceptions to failures
  Failure _mapExceptionToFailure(AppException exception) {
    switch (exception.runtimeType) {
      case NetworkException:
        return NetworkFailure(message: exception.message);
      case ServerException:
        return ServerFailure(message: exception.message);
      case AuthenticationException:
        return AuthenticationFailure(message: exception.message);
      case PermissionException:
        return PermissionFailure(message: exception.message);
      case NotFoundException:
        return DataFailure(message: exception.message);
      case ValidationException:
        return ValidationFailure(message: exception.message);
      case FirestoreException:
        return DataFailure(message: exception.message);
      case DataException:
        return DataFailure(message: exception.message);
      default:
        return DataFailure(message: exception.message);
    }
  }
}
