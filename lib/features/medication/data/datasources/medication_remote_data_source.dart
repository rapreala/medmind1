import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../../../core/constants/firebase_constants.dart';
import '../../../../core/errors/exceptions.dart';
import '../models/medication_model.dart';

abstract class MedicationRemoteDataSource {
  Future<List<MedicationModel>> getMedications(String userId);
  Future<MedicationModel> getMedicationById(String id);
  Future<MedicationModel> addMedication(MedicationModel medication);
  Future<void> updateMedication(MedicationModel medication);
  Future<void> deleteMedication(String id);
  Future<MedicationModel?> lookupBarcode(String barcodeData);
  Stream<List<MedicationModel>> watchMedications(String userId);
}

class MedicationRemoteDataSourceImpl implements MedicationRemoteDataSource {
  final FirebaseFirestore firestore;
  final FirebaseAuth firebaseAuth;

  MedicationRemoteDataSourceImpl({
    required this.firestore,
    required this.firebaseAuth,
  });

  CollectionReference get _medicationsCollection =>
      firestore.collection(FirebaseConstants.medicationsPath);

  String get _currentUserId => firebaseAuth.currentUser?.uid ?? '';

  @override
  Future<List<MedicationModel>> getMedications(String userId) async {
    try {
      final querySnapshot = await _medicationsCollection
          .where(FirebaseConstants.userIdField, isEqualTo: userId)
          .where(FirebaseConstants.isActiveField, isEqualTo: true)
          .orderBy(FirebaseConstants.createdAtField, descending: true)
          .get();

      return querySnapshot.docs
          .map((doc) => MedicationModel.fromDocument(doc))
          .toList();
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to get medications: ${e.toString()}',
        code: 'get_medications_error',
      );
    }
  }

  @override
  Future<MedicationModel> getMedicationById(String id) async {
    try {
      final doc = await _medicationsCollection.doc(id).get();

      if (!doc.exists) {
        throw NotFoundException(
          message: 'Medication not found',
          code: 'medication_not_found',
        );
      }

      final medication = MedicationModel.fromDocument(doc);

      // Verify ownership
      if (medication.userId != _currentUserId) {
        throw PermissionException(
          message: 'You do not have permission to access this medication',
          code: 'permission_denied',
        );
      }

      return medication;
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } on AppException {
      rethrow;
    } catch (e) {
      throw DataException(
        message: 'Failed to get medication: ${e.toString()}',
        code: 'get_medication_error',
      );
    }
  }

  @override
  Future<MedicationModel> addMedication(MedicationModel medication) async {
    try {
      // Verify ownership
      if (medication.userId != _currentUserId) {
        throw PermissionException(
          message: 'You can only add medications for yourself',
          code: 'permission_denied',
        );
      }

      final docRef = _medicationsCollection.doc();
      final now = DateTime.now();

      final medicationWithId = MedicationModel(
        id: docRef.id,
        userId: medication.userId,
        name: medication.name,
        dosage: medication.dosage,
        form: medication.form,
        frequency: medication.frequency,
        times: medication.times,
        days: medication.days,
        startDate: medication.startDate,
        isActive: medication.isActive,
        barcodeData: medication.barcodeData,
        refillReminder: medication.refillReminder,
        instructions: medication.instructions,
        createdAt: now,
        updatedAt: now,
      );

      await docRef.set(medicationWithId.toDocument());
      return medicationWithId;
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } on AppException {
      rethrow;
    } catch (e) {
      throw DataException(
        message: 'Failed to add medication: ${e.toString()}',
        code: 'add_medication_error',
      );
    }
  }

  @override
  Future<void> updateMedication(MedicationModel medication) async {
    try {
      // Verify ownership
      if (medication.userId != _currentUserId) {
        throw PermissionException(
          message: 'You can only update your own medications',
          code: 'permission_denied',
        );
      }

      final docRef = _medicationsCollection.doc(medication.id);
      final doc = await docRef.get();

      if (!doc.exists) {
        throw NotFoundException(
          message: 'Medication not found',
          code: 'medication_not_found',
        );
      }

      final updatedMedication = MedicationModel(
        id: medication.id,
        userId: medication.userId,
        name: medication.name,
        dosage: medication.dosage,
        form: medication.form,
        frequency: medication.frequency,
        times: medication.times,
        days: medication.days,
        startDate: medication.startDate,
        isActive: medication.isActive,
        barcodeData: medication.barcodeData,
        refillReminder: medication.refillReminder,
        instructions: medication.instructions,
        createdAt: medication.createdAt,
        updatedAt: DateTime.now(),
      );

      await docRef.update(updatedMedication.toDocument());
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } on AppException {
      rethrow;
    } catch (e) {
      throw DataException(
        message: 'Failed to update medication: ${e.toString()}',
        code: 'update_medication_error',
      );
    }
  }

  @override
  Future<void> deleteMedication(String id) async {
    try {
      final docRef = _medicationsCollection.doc(id);
      final doc = await docRef.get();

      if (!doc.exists) {
        throw NotFoundException(
          message: 'Medication not found',
          code: 'medication_not_found',
        );
      }

      final medication = MedicationModel.fromDocument(doc);

      // Verify ownership
      if (medication.userId != _currentUserId) {
        throw PermissionException(
          message: 'You can only delete your own medications',
          code: 'permission_denied',
        );
      }

      // Soft delete by setting isActive = false
      await docRef.update({
        FirebaseConstants.isActiveField: false,
        FirebaseConstants.updatedAtField: FieldValue.serverTimestamp(),
      });
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } on AppException {
      rethrow;
    } catch (e) {
      throw DataException(
        message: 'Failed to delete medication: ${e.toString()}',
        code: 'delete_medication_error',
      );
    }
  }

  @override
  Future<MedicationModel?> lookupBarcode(String barcodeData) async {
    try {
      final querySnapshot = await _medicationsCollection
          .where('barcodeData', isEqualTo: barcodeData)
          .where(FirebaseConstants.userIdField, isEqualTo: _currentUserId)
          .where(FirebaseConstants.isActiveField, isEqualTo: true)
          .limit(1)
          .get();

      if (querySnapshot.docs.isEmpty) {
        return null;
      }

      return MedicationModel.fromDocument(querySnapshot.docs.first);
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to lookup barcode: ${e.toString()}',
        code: 'barcode_lookup_error',
      );
    }
  }

  @override
  Stream<List<MedicationModel>> watchMedications(String userId) {
    try {
      return _medicationsCollection
          .where(FirebaseConstants.userIdField, isEqualTo: userId)
          .where(FirebaseConstants.isActiveField, isEqualTo: true)
          .orderBy(FirebaseConstants.createdAtField, descending: true)
          .snapshots()
          .map(
            (snapshot) => snapshot.docs
                .map((doc) => MedicationModel.fromDocument(doc))
                .toList(),
          );
    } on FirebaseException catch (e) {
      throw _handleFirebaseException(e);
    } catch (e) {
      throw DataException(
        message: 'Failed to watch medications: ${e.toString()}',
        code: 'watch_medications_error',
      );
    }
  }

  AppException _handleFirebaseException(FirebaseException e) {
    switch (e.code) {
      case 'permission-denied':
        return PermissionException(
          message: 'Permission denied: ${e.message}',
          code: e.code,
        );
      case 'unavailable':
      case 'deadline-exceeded':
        return NetworkException(
          message: 'Network error: ${e.message}',
          code: e.code,
        );
      case 'not-found':
        return NotFoundException(
          message: 'Resource not found: ${e.message}',
          code: e.code,
        );
      default:
        return FirestoreException(
          message: e.message ?? 'Firestore error occurred',
          code: e.code,
          originalCode: e.code,
        );
    }
  }
}
