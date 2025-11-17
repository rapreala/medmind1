import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/user_preferences_entity.dart';
import '../repositories/profile_repository.dart';

class SaveUserPreferences implements UseCase<void, SaveUserPreferencesParams> {
  final ProfileRepository repository;

  SaveUserPreferences(this.repository);

  @override
  Future<Either<Failure, void>> call(SaveUserPreferencesParams params) async {
    return await repository.savePreferences(params.preferences);
  }
}

class SaveUserPreferencesParams {
  final UserPreferencesEntity preferences;

  SaveUserPreferencesParams({required this.preferences});
}
