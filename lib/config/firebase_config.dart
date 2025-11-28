import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

class FirebaseConfig {
  static Future<void> initialize() async {
    // Check if Firebase is already initialized
    try {
      if (Firebase.apps.isNotEmpty) {
        if (kDebugMode) {
          print('🔥 Firebase already initialized, skipping...');
        }
        return;
      }
    } catch (e) {
      // Firebase not initialized yet, continue
    }

    final firebaseOptions = _getFirebaseOptions();
    _logFirebaseOptions(firebaseOptions);

    try {
      await Firebase.initializeApp(options: firebaseOptions);

      if (kDebugMode) {
        print('🔥 Firebase initialized successfully');
      }
    } catch (e) {
      if (kDebugMode) {
        print('❌ Firebase initialization error: $e');
      }
      rethrow;
    }
  }

  static FirebaseOptions _getFirebaseOptions() {
    // Platform-specific Firebase configuration
    if (kIsWeb) {
      return const FirebaseOptions(
        apiKey: 'AIzaSyBxGDxjBp_-Ar1_WHeivlwAkv97K_P8u3I',
        appId: '1:1018558923142:web:7fa35f0c4a8bdb034b2c07',
        messagingSenderId: '1018558923142',
        projectId: 'medmind-c6af2',
        authDomain: 'medmind-c6af2.firebaseapp.com',
        storageBucket: 'medmind-c6af2.firebasestorage.app',
      );
    }

    // ANDROID CONFIG (Updated from google-services.json)
    if (defaultTargetPlatform == TargetPlatform.android) {
      return const FirebaseOptions(
        apiKey: 'AIzaSyDzQIjstsnhiW7xZlP4dI71pComnWzEuFE',
        appId: '1:301697188256:android:dbc6ddc49d4d1c5ee624c5',
        messagingSenderId: '301697188256',
        projectId: 'medmind1-da4fa',
        storageBucket: 'medmind1-da4fa.firebasestorage.app',
      );
    }

    // iOS CONFIG (Fill later if needed)
    if (defaultTargetPlatform == TargetPlatform.iOS) {
      return const FirebaseOptions(
        apiKey: 'YOUR_IOS_API_KEY',
        appId: 'YOUR_IOS_APP_ID',
        messagingSenderId: 'YOUR_MESSAGING_SENDER_ID',
        projectId: 'medmind-c6af2',
        storageBucket: 'medmind-c6af2.firebasestorage.app',
        iosBundleId: 'com.example.medmind',
      );
    }

    throw UnsupportedError(
      'Platform ${defaultTargetPlatform.name} is not supported by FirebaseConfig',
    );
  }

  static void _logFirebaseOptions(FirebaseOptions options) {
    if (!kDebugMode) {
      return;
    }

    print('🔍 Firebase configuration in use:');
    print('  • Project ID: ${options.projectId}');
    print('  • App ID: ${options.appId}');
    print('  • API Key: ${options.apiKey}');
    print('  • Auth Domain: ${options.authDomain ?? 'N/A'}');
    print('  • Storage Bucket: ${options.storageBucket ?? 'N/A'}');
    print('  • Messaging Sender ID: ${options.messagingSenderId ?? 'N/A'}');
  }
}
