# MEDMIND VIDEO WALKTHROUGH SCRIPT
## Exemplary Demo Recording Guide

**Duration:** 8-10 minutes  
**Format:** Single continuous recording, no cuts  
**Quality:** ≥1080p video, crisp audio, steady camera  
**Team:** All 4 members speak briefly

---

## PRE-RECORDING CHECKLIST

### Equipment Setup
- [ ] Physical Android phone (not emulator)
- [ ] Phone charged to 100%
- [ ] Screen brightness at maximum
- [ ] Do Not Disturb mode enabled
- [ ] Camera/tripod positioned to capture phone clearly
- [ ] Laptop with Firebase Console visible
- [ ] Good lighting (no glare on phone screen)
- [ ] Quiet environment (no background noise)
- [ ] Test audio levels before recording

### App Preparation
- [ ] Build release APK: `flutter build apk --release`
- [ ] Install APK on physical phone
- [ ] Clear all app data before recording
- [ ] Ensure stable internet connection
- [ ] Firebase Console open and logged in
- [ ] Firestore database visible in browser
- [ ] Test all features work before recording

### Team Coordination
- [ ] Assign features to each team member
- [ ] Practice hand-offs between speakers
- [ ] Rehearse timing (8-10 minutes total)
- [ ] Prepare what each person will say
- [ ] No introductions - jump straight to demo

---

## VIDEO SCRIPT

### SECTION 1: UI NAVIGATION & RESPONSIVE DESIGN (0:00 - 2:00)
**Speaker: Mahad Kakooza (Frontend Developer 1)**

**[Camera shows phone on home screen, Firebase Console visible on laptop]**

**Mahad:** "Welcome to MedMind. I'll demonstrate our responsive UI and navigation system, starting with a cold launch."

**[Action: Tap MedMind app icon]**
**[Show: Splash screen with MedMind logo and loading indicator]**
**[Screen: App loads to login page]**

**Mahad:** "The app initializes and shows the login screen. Since we'll register shortly, let me first show you all the main screens and responsive design."

**[Action: Tap "Don't have an account? Sign Up"]**
**[Screen: Registration page]**

**Mahad:** "This is our registration screen with form validation. Let me quickly register so we can explore the full app."

**[Action: Fill registration form quickly]**
- Email: demo@medmind.app
- Password: Demo123!
- Display Name: Demo User

**[Action: Tap "Create Account"]**
**[Screen: Dashboard appears]**

**Mahad:** "Now I'll demonstrate navigation and responsive design across all screens. We're on the Dashboard."

**[Screen: Dashboard showing welcome message, adherence stats, today's medications]**

**Mahad:** "The dashboard displays today's medication schedule, adherence statistics, and quick actions."

**[Action: Rotate phone to landscape]**
**[Show: UI adapts to landscape orientation]**
**[Action: Rotate back to portrait]**

**Mahad:** "Notice how the layout adapts smoothly to orientation changes. Let's visit all screens."

**[Action: Tap "Medications" in bottom navigation]**
**[Screen: Medication List page]**

**Mahad:** "Medication list with search and filter capabilities."

**[Action: Tap "Adherence" in bottom navigation]**
**[Screen: Adherence History page with calendar]**
**[Action: Rotate to landscape]**
**[Show: Calendar adapts to landscape]**
**[Action: Rotate back to portrait]**

**Mahad:** "Adherence calendar with responsive design."

**[Action: Tap "Profile" in bottom navigation]**
**[Screen: Profile page]**

**Mahad:** "Profile page with user settings. All screens maintain state and adapt to orientation changes. Now Kenneth will demonstrate our form validation."

---

### SECTION 2: FORMS & VALIDATION (2:00 - 4:00)
**Speaker: Kenneth Chirchir (Frontend Developer 2)**

**[Hand-off: Mahad passes phone to Kenneth]**

**Kenneth:** "I'll demonstrate our form validation and error handling. Let's add a medication."

**[Action: Navigate to Medications screen]**
**[Action: Tap FAB (+ button)]**
**[Screen: Add Medication form]**

**Kenneth:** "First, let me show validation by trying to save without filling required fields."

**[Action: Leave form empty]**
**[Action: Tap "Save"]**

**[Show: Validation errors appear]**
**[Text: "Please enter medication name", "Please enter dosage"]**

**Kenneth:** "The form validates all required fields. Now let's try invalid data."

**[Action: Enter name: "Test Med"]**
**[Action: Enter dosage: "abc"]**
**[Action: Tap "Save"]**

**[Show: Validation error]**
**[Text: "Please enter a valid dosage"]**

**Kenneth:** "Now I'll fill the form correctly."

**[Action: Fill form properly]**
- Name: Aspirin
- Dosage: 100mg
- Frequency: Daily
- Schedule: 08:00 AM

**[Action: Tap "Save"]**
**[Show: Success message]**

**Kenneth:** "Medication saved successfully. Now let me test network error handling."

**[Action: Enable airplane mode]**
**[Action: Try to add another medication]**
**[Show: Error message: "Unable to save. Please check your internet connection."]**

**[Action: Disable airplane mode]**

**Kenneth:** "All errors display polite, actionable messages. Now Lenny will demonstrate Firebase integration."

---

### SECTION 3: FIREBASE CRUD & REAL-TIME SYNC (4:00 - 7:00)
**Speaker: Lenny Ihirwe (Backend Developer 1)**

**[Hand-off: Kenneth passes phone to Lenny]**

**Lenny:** "I'll demonstrate our Firebase integration with Create, Read, Update, and Delete operations. Watch both the app and Firebase Console."

**[Position: Phone and Firebase Console both visible]**
**[Firebase Console: Navigate to Firestore Database, medications collection]**

#### CREATE
**Lenny:** "First, let's create a medication and watch it sync to Firestore in real-time."

**[Action: Navigate to Medications screen]**
**[Action: Tap FAB (+ button)]**
**[Screen: Add Medication form]**

**[Action: Fill form]**
- Name: Vitamin D
- Dosage: 1000 IU
- Frequency: Daily
- Schedule: 09:00 AM
- Notes: Take with breakfast

**[Action: Tap "Save"]**
**[Point to Firebase Console]**

**Lenny:** "Watch the Firestore console - the document appears instantly with all fields."

**[Firebase Console: New document appears in medications collection with auto-generated ID]**
**[Screen: Returns to medication list showing new medication]**

#### READ
**Lenny:** "The medication list automatically updates, demonstrating real-time read operations from Firestore."

**[Action: Tap on the Vitamin D medication card]**
**[Screen: Medication detail page]**

**Lenny:** "All data is retrieved from Firestore and displayed. Notice the document ID matches what's in the console."

#### UPDATE
**[Action: Tap "Edit" button]**
**[Screen: Edit medication form with pre-filled data]**

**Lenny:** "Now I'll update the dosage."

**[Action: Change dosage to 2000 IU]**
**[Action: Tap "Save"]**

**[Point to Firebase Console]**

**Lenny:** "Watch the Firebase Console update in real-time."

**[Firebase Console: Document updates with new dosage value]**
**[Screen: Detail page shows updated information]**

#### DELETE
**Lenny:** "Finally, let's delete this medication."

**[Action: Tap "Delete" button]**
**[Show: Confirmation dialog]**

**Lenny:** "Confirmation prevents accidental deletions."

**[Action: Confirm delete]**
**[Point to Firebase Console]**

**Lenny:** "The document is removed from Firestore immediately."

**[Firebase Console: Document disappears or isActive set to false]**
**[Screen: Returns to medication list]**

**Lenny:** "All CRUD operations sync instantly with Firebase. Now Ryan will demonstrate authentication and state management."

---

### SECTION 4: AUTHENTICATION & STATE MANAGEMENT (7:00 - 10:00)
**Speaker: Ryan Apreala (Backend Developer 2)**

**[Hand-off: Lenny passes phone to Ryan]**

**Ryan:** "I'll demonstrate our authentication system, BLoC state management, and data persistence. First, let's test the full authentication flow."

#### AUTHENTICATION FLOW
**[Action: Navigate to Profile]**
**[Action: Tap "Logout"]**
**[Show: Confirmation dialog]**
**[Action: Confirm]**
**[Screen: Returns to login page]**

**Ryan:** "User logged out. Now let's log back in."

**[Action: Enter credentials]**
- Email: demo@medmind.app
- Password: Demo123!

**[Action: Tap "Sign In"]**
**[Point to Firebase Console Authentication tab]**

**Ryan:** "Firebase Authentication verifies credentials and creates a session token."

**[Screen: Dashboard appears]**

#### STATE MANAGEMENT
**Ryan:** "Now I'll demonstrate BLoC state management with multiple widgets updating from one state change."

**[Action: Add a new medication quickly]**
**[Action: Navigate to Medications, tap FAB]**
**[Action: Fill form]**
- Name: Aspirin
- Dosage: 100mg
- Frequency: Daily
- Schedule: 08:00 AM

**[Action: Save]**

**Ryan:** "Watch how multiple widgets update from one state change."

**[Action: Navigate to Dashboard]**
**[Screen: Dashboard shows "Today's Medications" with Aspirin]**

**Ryan:** "The dashboard's medication list widget updated. Now watch two widgets update simultaneously."

**[Action: Tap "Mark as Taken" on Aspirin]**
**[Show: Checkmark animation on medication card]**
**[Point to adherence stats card]**

**Ryan:** "Notice two widgets updated: the medication card shows 'taken' status, and the adherence statistics card shows updated percentage. Both widgets respond to the same BLoC state change - this is our state management in action."

#### SHARED PREFERENCES PERSISTENCE
**Ryan:** "Now I'll demonstrate data persistence using SharedPreferences."

**[Action: Navigate to Profile]**
**[Action: Tap "Settings"]**
**[Screen: Settings page]**

**Ryan:** "I'll enable dark mode."

**[Action: Toggle "Dark Mode" switch]**
**[Show: App theme changes to dark mode immediately]**

**Ryan:** "Theme changed instantly. Now let's verify it persists after app restart."

**[Action: Press home button]**
**[Action: Open recent apps, swipe away MedMind]**

**Ryan:** "App completely closed. Now I'll relaunch."

**[Action: Tap MedMind icon]**
**[Show: Splash screen]**
**[Screen: App opens in dark mode, directly to dashboard]**

**Ryan:** "The app reopened in dark mode - SharedPreferences persisted the setting. The user session also persisted, so no login required."

#### CLOSING
**Ryan:** "We've demonstrated MedMind's complete functionality organized by our team roles:"

**[Screen: Show dashboard]**

**Ryan:** "Frontend team showed responsive UI navigation and form validation. Backend team demonstrated Firebase CRUD operations, authentication, BLoC state management, and data persistence. MedMind is built with Clean Architecture, 85% test coverage across 15,000 lines of code, and is production-ready."

**[Screen: Fade to MedMind logo]**

**[END RECORDING]**

---

## POST-RECORDING CHECKLIST

### Video Quality Check
- [ ] Video is ≥1080p resolution
- [ ] Phone screen is clearly legible throughout
- [ ] Firebase Console is clearly legible when shown
- [ ] No cuts or speed-ups in the recording
- [ ] Camera remained steady throughout
- [ ] Lighting is consistent

### Audio Quality Check
- [ ] All speakers are clearly audible
- [ ] No background noise or echo
- [ ] No humming or buzzing sounds
- [ ] Audio levels are consistent
- [ ] No clipping or distortion

### Content Verification
- [ ] Cold-start launch shown
- [ ] Register → Logout → Login demonstrated
- [ ] Every screen visited with one rotation
- [ ] CRUD operations shown with Firebase Console visible
- [ ] State update affecting two widgets demonstrated
- [ ] SharedPreferences persistence verified with app restart
- [ ] Validation error with polite message shown
- [ ] All 4 team members spoke
- [ ] Hand-offs were smooth
- [ ] No team member introductions
- [ ] Total duration 8-10 minutes

### Technical Verification
- [ ] All features worked correctly
- [ ] No crashes or freezes
- [ ] Firebase sync was visible
- [ ] UI was responsive
- [ ] Animations were smooth
- [ ] Error messages were appropriate

---

## TEAM MEMBER ASSIGNMENTS (BY ROLE)

| Team Member | Role | Section | Features to Demonstrate | Time |
|-------------|------|---------|------------------------|------|
| **Mahad Kakooza** | Frontend Dev 1 | UI Navigation & Responsive Design | Screen navigation, rotation, responsive layouts | 0:00 - 2:00 |
| **Kenneth Chirchir** | Frontend Dev 2 | Forms & Validation | Add medication form, validation, error messages | 2:00 - 4:00 |
| **Lenny Ihirwe** | Backend Dev 1 | Firebase CRUD & Real-time Sync | Create, Read, Update, Delete with Firestore Console | 4:00 - 7:00 |
| **Ryan Apreala** | Backend Dev 2 | Authentication & State Management | Register, login, logout, BLoC state, SharedPreferences | 7:00 - 10:00 |

---

## SPEAKING TIPS

### Do's:
✅ Speak clearly and at moderate pace  
✅ Point to specific UI elements as you describe them  
✅ Mention what you're about to do before doing it  
✅ Highlight Firebase Console changes  
✅ Keep explanations concise and technical  
✅ Maintain professional tone  
✅ Practice hand-offs beforehand  

### Don'ts:
❌ Don't introduce team members  
❌ Don't use filler words (um, uh, like)  
❌ Don't apologize for anything  
❌ Don't mention what you "would" do - just do it  
❌ Don't rush through demonstrations  
❌ Don't make jokes or casual comments  
❌ Don't explain obvious things  

---

## FIREBASE CONSOLE SETUP

### Before Recording:
1. Open Firebase Console in Chrome
2. Navigate to your project (medmind-c6af2)
3. Open Firestore Database in one tab
4. Open Authentication in another tab
5. Arrange windows so both phone and console are visible
6. Zoom in on console text for readability
7. Clear any existing test data

### During Recording:
- Keep Firestore Database view open showing medications collection
- Switch to Authentication tab when creating/logging in users
- Ensure document IDs and data are visible
- Highlight real-time updates as they happen

---

## TROUBLESHOOTING

### If App Crashes:
- Stop recording immediately
- Fix the issue
- Clear app data
- Start recording from beginning

### If Firebase Doesn't Sync:
- Check internet connection
- Verify Firebase configuration
- Check security rules
- Restart recording if necessary

### If Audio Has Issues:
- Stop and restart recording
- Check microphone placement
- Reduce background noise
- Test audio levels again

### If Video Quality Is Poor:
- Improve lighting
- Clean phone screen
- Adjust camera position
- Increase phone brightness

---

## FINAL NOTES

**Remember:** This is a single, continuous recording with no cuts. Practice the entire flow multiple times before recording. Each team member should know exactly what they'll say and do. Smooth hand-offs are crucial. The goal is to demonstrate technical excellence and professional presentation.

**Duration Target:** 8-10 minutes total  
**Quality Standard:** Exemplary (highest grade)  
**Key Success Factor:** Smooth, professional, technically accurate demonstration

Good luck with your recording! 🎥

