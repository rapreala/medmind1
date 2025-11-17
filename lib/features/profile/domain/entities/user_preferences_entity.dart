import 'package:equatable/equatable.dart';

enum ThemeMode { light, dark, system }
enum Language { english, spanish, french }

class UserPreferencesEntity extends Equatable {
  final ThemeMode themeMode;
  final bool notificationsEnabled;
  final int reminderSnoozeDuration; // in minutes
  final Language language;
  final bool biometricAuthEnabled;
  final bool dataBackupEnabled;
  final DateTime? lastBackup;

  const UserPreferencesEntity({
    this.themeMode = ThemeMode.system,
    this.notificationsEnabled = true,
    this.reminderSnoozeDuration = 5,
    this.language = Language.english,
    this.biometricAuthEnabled = false,
    this.dataBackupEnabled = true,
    this.lastBackup,
  });

  @override
  List<Object?> get props => [
    themeMode,
    notificationsEnabled,
    reminderSnoozeDuration,
    language,
    biometricAuthEnabled,
    dataBackupEnabled,
    lastBackup,
  ];

  UserPreferencesEntity copyWith({
    ThemeMode? themeMode,
    bool? notificationsEnabled,
    int? reminderSnoozeDuration,
    Language? language,
    bool? biometricAuthEnabled,
    bool? dataBackupEnabled,
    DateTime? lastBackup,
  }) {
    return UserPreferencesEntity(
      themeMode: themeMode ?? this.themeMode,
      notificationsEnabled: notificationsEnabled ?? this.notificationsEnabled,
      reminderSnoozeDuration: reminderSnoozeDuration ?? this.reminderSnoozeDuration,
      language: language ?? this.language,
      biometricAuthEnabled: biometricAuthEnabled ?? this.biometricAuthEnabled,
      dataBackupEnabled: dataBackupEnabled ?? this.dataBackupEnabled,
      lastBackup: lastBackup ?? this.lastBackup,
    );
  }

  static const defaultPreferences = UserPreferencesEntity();
}
