import 'package:cloud_firestore/cloud_firestore.dart';
import '../../domain/entities/adherence_log_entity.dart';

class AdherenceLogModel extends AdherenceLogEntity {
  const AdherenceLogModel({
    required super.id,
    required super.userId,
    required super.medicationId,
    required super.scheduledTime,
    super.takenTime,
    required super.status,
    super.snoozeDuration,
    required super.createdAt,
    super.deviceInfo,
  });

  /// Convert entity to model
  factory AdherenceLogModel.fromEntity(AdherenceLogEntity entity) {
    return AdherenceLogModel(
      id: entity.id,
      userId: entity.userId,
      medicationId: entity.medicationId,
      scheduledTime: entity.scheduledTime,
      takenTime: entity.takenTime,
      status: entity.status,
      snoozeDuration: entity.snoozeDuration,
      createdAt: entity.createdAt,
      deviceInfo: entity.deviceInfo,
    );
  }

  /// Convert from Firestore document
  factory AdherenceLogModel.fromDocument(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return AdherenceLogModel(
      id: doc.id,
      userId: data['userId'] as String,
      medicationId: data['medicationId'] as String,
      scheduledTime: (data['scheduledTime'] as Timestamp).toDate(),
      takenTime: data['takenTime'] != null
          ? (data['takenTime'] as Timestamp).toDate()
          : null,
      status: AdherenceStatus.values.firstWhere(
        (e) => e.name == data['status'],
        orElse: () => AdherenceStatus.missed,
      ),
      snoozeDuration: data['snoozeDuration'] as int?,
      createdAt: (data['createdAt'] as Timestamp).toDate(),
      deviceInfo: data['deviceInfo'] != null
          ? Map<String, dynamic>.from(data['deviceInfo'] as Map)
          : null,
    );
  }

  /// Convert to Firestore document map
  Map<String, dynamic> toDocument() {
    return {
      'userId': userId,
      'medicationId': medicationId,
      'scheduledTime': Timestamp.fromDate(scheduledTime),
      if (takenTime != null) 'takenTime': Timestamp.fromDate(takenTime!),
      'status': status.name,
      if (snoozeDuration != null) 'snoozeDuration': snoozeDuration,
      'createdAt': Timestamp.fromDate(createdAt),
      if (deviceInfo != null) 'deviceInfo': deviceInfo,
    };
  }

  /// Convert to JSON (for local storage/caching)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'medicationId': medicationId,
      'scheduledTime': scheduledTime.toIso8601String(),
      'takenTime': takenTime?.toIso8601String(),
      'status': status.name,
      'snoozeDuration': snoozeDuration,
      'createdAt': createdAt.toIso8601String(),
      'deviceInfo': deviceInfo,
    };
  }

  /// Convert from JSON
  factory AdherenceLogModel.fromJson(Map<String, dynamic> json) {
    return AdherenceLogModel(
      id: json['id'] as String,
      userId: json['userId'] as String,
      medicationId: json['medicationId'] as String,
      scheduledTime: DateTime.parse(json['scheduledTime'] as String),
      takenTime: json['takenTime'] != null
          ? DateTime.parse(json['takenTime'] as String)
          : null,
      status: AdherenceStatus.values.firstWhere(
        (e) => e.name == json['status'],
        orElse: () => AdherenceStatus.missed,
      ),
      snoozeDuration: json['snoozeDuration'] as int?,
      createdAt: DateTime.parse(json['createdAt'] as String),
      deviceInfo: json['deviceInfo'] != null
          ? Map<String, dynamic>.from(json['deviceInfo'] as Map)
          : null,
    );
  }

  /// Convert entity to model
  AdherenceLogEntity toEntity() {
    return AdherenceLogEntity(
      id: id,
      userId: userId,
      medicationId: medicationId,
      scheduledTime: scheduledTime,
      takenTime: takenTime,
      status: status,
      snoozeDuration: snoozeDuration,
      createdAt: createdAt,
      deviceInfo: deviceInfo,
    );
  }
}

