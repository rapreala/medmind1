# Firebase Setup Guide for MedMind

## Step-by-Step Instructions to Create a New Firebase Project

### Step 1: Go to Firebase Console

1. Open your web browser
2. Go to: **https://console.firebase.google.com**
3. Sign in with your Google account

### Step 2: Create a New Project

1. Click the **"Add project"** button (or **"Create a project"**)
2. Enter project name: **`medmind-demo`** (or any name you prefer)
3. Click **"Continue"**

### Step 3: Google Analytics (Optional)

1. You'll be asked: "Enable Google Analytics for this project?"
2. **Toggle it OFF** (not needed for this demo)
3. Click **"Create project"**
4. Wait for project creation (takes ~30 seconds)
5. Click **"Continue"** when ready

### Step 4: Add Android App to Firebase

1. On the Firebase Console home page, click the **Android icon** (robot icon)
2. You'll see "Add Firebase to your Android app"

### Step 5: Register Your Android App

Fill in the following information:

**Android package name:** (REQUIRED)
```
com.example.medmind
```

**App nickname:** (Optional but recommended)
```
MedMind Android
```

**Debug signing certificate SHA-1:** (Optional - skip for now)
- Leave blank
- Click **"Register app"**

### Step 6: Download google-services.json

1. You'll see a button: **"Download google-services.json"**
2. Click it to download the file
3. The file will download to your Downloads folder

### Step 7: Add google-services.json to Your Project

**Option A: Using Finder (Mac)**
1. Open Finder
2. Navigate to your Downloads folder
3. Find `google-services.json`
4. Drag and drop it into your project at: `android/app/`
5. Replace the existing file when prompted

**Option B: Using Terminal**
```bash
# Navigate to your project root
cd /Users/ASUS/medmind1

# Copy the file from Downloads
cp ~/Downloads/google-services.json android/app/

# Verify it's there
ls -la android/app/google-services.json
```

### Step 8: Skip the SDK Setup Steps

Firebase will show you SDK setup instructions. You can **skip these** because your project is already configured:

1. Click **"Next"** (skip "Add Firebase SDK")
2. Click **"Next"** (skip "Add initialization code")
3. Click **"Continue to console"**

### Step 9: Enable Authentication (Required for MedMind)

1. In the Firebase Console, click **"Authentication"** in the left sidebar
2. Click **"Get started"**
3. Click on the **"Sign-in method"** tab
4. Enable **"Email/Password"**:
   - Click on "Email/Password"
   - Toggle **"Enable"** to ON
   - Click **"Save"**
5. Enable **"Google"** (optional but recommended):
   - Click on "Google"
   - Toggle **"Enable"** to ON
   - Select your support email
   - Click **"Save"**

### Step 10: Set Up Firestore Database (Required for MedMind)

1. In the Firebase Console, click **"Firestore Database"** in the left sidebar
2. Click **"Create database"**
3. Choose **"Start in test mode"** (for development)
4. Click **"Next"**
5. Select location: **"us-central"** (or closest to you)
6. Click **"Enable"**
7. Wait for database creation (~30 seconds)

### Step 11: Set Up Storage (Required for MedMind)

1. In the Firebase Console, click **"Storage"** in the left sidebar
2. Click **"Get started"**
3. Click **"Next"** (accept default security rules)
4. Select location: **"us-central"** (same as Firestore)
5. Click **"Done"**

### Step 12: Update Firebase Config in Your Code

Now you need to update the Firebase configuration in your Flutter app with the new project details.

1. In Firebase Console, click the **gear icon** (⚙️) next to "Project Overview"
2. Click **"Project settings"**
3. Scroll down to "Your apps" section
4. You'll see your Android app listed
5. Note down these values:
   - **Project ID**
   - **App ID**
   - **API Key**
   - **Storage Bucket**

### Step 13: Update firebase_config.dart

Open `lib/config/firebase_config.dart` and update the Android section with your new values:

```dart
// ANDROID CONFIG (Update with your new values)
if (defaultTargetPlatform == TargetPlatform.android) {
  return const FirebaseOptions(
    apiKey: 'YOUR_NEW_API_KEY',              // From Firebase Console
    appId: 'YOUR_NEW_APP_ID',                // From Firebase Console
    messagingSenderId: 'YOUR_SENDER_ID',     // From Firebase Console
    projectId: 'medmind-demo',               // Your new project ID
    storageBucket: 'medmind-demo.firebasestorage.app',  // Your new bucket
  );
}
```

### Step 14: Clean and Rebuild

```bash
# Clean the project
flutter clean

# Get dependencies
flutter pub get

# Run the app
flutter run
```

---

## Quick Reference: What You Need

From Firebase Console → Project Settings → Your Android App:

| Field | Where to Find | Example |
|-------|---------------|---------|
| **apiKey** | Project Settings → Your apps → Android app | `AIzaSyABC123...` |
| **appId** | Project Settings → Your apps → Android app | `1:123456:android:abc123` |
| **messagingSenderId** | Project Settings → General → Project number | `123456789` |
| **projectId** | Project Settings → General → Project ID | `medmind-demo` |
| **storageBucket** | Project Settings → General → Storage bucket | `medmind-demo.firebasestorage.app` |

---

## Troubleshooting

### Problem: "Package name already exists"
**Solution:** Use a different package name like `com.example.medmind2` or `com.yourname.medmind`

### Problem: Can't find google-services.json
**Solution:** Check your Downloads folder, or re-download from Firebase Console → Project Settings → Your apps → Download

### Problem: Still getting duplicate app error
**Solution:** 
1. Uninstall the app from emulator: `flutter clean`
2. Delete app data on emulator
3. Restart emulator
4. Run `flutter run` again

### Problem: Firebase initialization fails
**Solution:** Make sure you:
1. Enabled Authentication
2. Created Firestore database
3. Set up Storage
4. Updated firebase_config.dart with correct values

---

## After Setup is Complete

Once you've completed all steps:

1. ✅ google-services.json is in `android/app/`
2. ✅ firebase_config.dart is updated with new values
3. ✅ Authentication is enabled
4. ✅ Firestore database is created
5. ✅ Storage is set up

Run your app:
```bash
flutter run
```

You should see:
```
🔥 Firebase initialized successfully
```

No more duplicate app errors! 🎉

---

## For Video Demo

Once Firebase is working, you can:
1. Navigate to Adherence Prediction page
2. Test predictions (doesn't require Firebase)
3. Record your video demonstration

The adherence prediction feature works independently of Firebase since it only calls your deployed API.

---

## Need Help?

If you encounter issues:
1. Check Firebase Console for any error messages
2. Verify all services (Auth, Firestore, Storage) are enabled
3. Confirm google-services.json package name matches `com.example.medmind`
4. Try `flutter clean` and rebuild

Good luck! 🚀
