import 'package:dartz/dartz.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/errors/failures.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/medication_entity.dart';
import '../../domain/repositories/medication_repository.dart';
import '../datasources/medication_remote_data_source.dart';
import '../models/medication_model.dart';

class MedicationRepositoryImpl implements MedicationRepository {
  final MedicationRemoteDataSource remoteDataSource;
  final FirebaseAuth firebaseAuth;

  MedicationRepositoryImpl({
    required this.remoteDataSource,
    required this.firebaseAuth,
  });

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<Either<Failure, List<MedicationEntity>>> getMedications() async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final medications = await remoteDataSource.getMedications(_currentUserId);
      return Right(medications.map((model) => model.toEntity()).toList());
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on NotFoundException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
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
  Future<Either<Failure, MedicationEntity>> getMedicationById(String id) async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      final medication = await remoteDataSource.getMedicationById(id);
      return Right(medication.toEntity());
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on NotFoundException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
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
  Future<Either<Failure, MedicationEntity>> addMedication(
    MedicationEntity medication,
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

      final medicationModel = MedicationModel.fromEntity(medication);
      final addedMedication = await remoteDataSource.addMedication(
        medicationModel,
      );
      return Right(addedMedication.toEntity());
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
  Future<Either<Failure, MedicationEntity>> updateMedication(
    MedicationEntity medication,
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

      final medicationModel = MedicationModel.fromEntity(medication);
      await remoteDataSource.updateMedication(medicationModel);
      return Right(medication);
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on NotFoundException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
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
  Future<Either<Failure, void>> deleteMedication(String id) async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      await remoteDataSource.deleteMedication(id);
      return const Right(null);
    } on PermissionException catch (e) {
      return Left(PermissionFailure(message: e.message, code: e.code));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message, code: e.code));
    } on NotFoundException catch (e) {
      return Left(DataFailure(message: e.message, code: e.code));
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
  Future<Either<Failure, String>> scanBarcode() async {
    try {
      if (_currentUserId.isEmpty) {
        return const Left(
          AuthenticationFailure(
            message: 'User not authenticated',
            code: 'not_authenticated',
          ),
        );
      }

      // This should be handled by the barcode scanner widget
      // For now, return a placeholder
      return const Left(
        DataFailure(
          message: 'Barcode scanning not implemented in repository',
          code: 'not_implemented',
        ),
      );
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
  Stream<Either<Failure, List<MedicationEntity>>> watchMedications() {
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
          .watchMedications(_currentUserId)
          .map((medications) {
            return Right(medications.map((model) => model.toEntity()).toList())
                as Either<Failure, List<MedicationEntity>>;
          })
          .handleError((error) {
            if (error is PermissionException) {
              return Left(
                    PermissionFailure(message: error.message, code: error.code),
                  )
                  as Either<Failure, List<MedicationEntity>>;
            } else if (error is NetworkException) {
              return Left(
                    NetworkFailure(message: error.message, code: error.code),
                  )
                  as Either<Failure, List<MedicationEntity>>;
            } else if (error is FirestoreException) {
              return Left(DataFailure(message: error.message, code: error.code))
                  as Either<Failure, List<MedicationEntity>>;
            } else {
              return Left(
                    DataFailure(
                      message: 'Unexpected error: ${error.toString()}',
                      code: 'unexpected_error',
                    ),
                  )
                  as Either<Failure, List<MedicationEntity>>;
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
