import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/user_preferences_entity.dart';
import '../entities/user_profile_entity.dart';

abstract class ProfileRepository {
  // User Profile Methods
  Future<Either<Failure, UserProfileEntity>> getUserProfile();
  Future<Either<Failure, UserProfileEntity>> updateUserProfile(UserProfileEntity profile);
  Future<Either<Failure, void>> updateDisplayName(String displayName);
  Future<Either<Failure, void>> updatePhotoURL(String photoURL);
  Future<Either<Failure, void>> updateEmergencyContact(EmergencyContact contact);
  Future<Either<Failure, void>> updateHealthInfo({
    List<String>? healthConditions,
    List<String>? allergies,
    DateTime? dateOfBirth,
    String? gender,
  });

  // User Preferences Methods
  Future<Either<Failure, UserPreferencesEntity>> getPreferences();
  Future<Either<Failure, void>> savePreferences(UserPreferencesEntity preferences);
  Future<Either<Failure, UserPreferencesEntity>> updateThemeMode(ThemeMode themeMode);
  Future<Either<Failure, UserPreferencesEntity>> updateNotifications(bool enabled);
  Future<Either<Failure, void>> clearAllData();
  
  // Account Management
  Future<Either<Failure, void>> deleteAccount();
  Future<Either<Failure, void>> exportUserData();
}
