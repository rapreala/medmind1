# Manual Notification Testing Guide

This guide will help you verify that the notification system is working correctly, including the badge count on the notification icon and the pending doses page.

## Prerequisites
- App must be running on a physical device or emulator
- Notifications permissions must be granted
- You must be logged in

## Test 1: Missed Dose Detection (Immediate)

### Purpose
Verify that when you create a medication with times that have already passed today, those doses immediately appear as pending.

### Steps
1. **Hot restart** the app (important!)
2. Note the current time (e.g., 2:30 PM)
3. Navigate to "Add Medication"
4. Fill in medication details:
   - Name: "Test Med 1"
   - Dosage: "10mg"
   - Enable reminders: ON
   - Times: Add 3 times that have already passed today:
     - 1:00 AM
     - 2:00 AM  
     - 3:00 AM
5. Save the medication
6. Return to dashboard

### Expected Results
✅ **Notification icon badge should show "3"**
✅ **Notification summary card should show "3 doses need to be taken"**
✅ **Tap notification icon → should see 3 pending doses listed**
✅ **Each dose should show the medication name and scheduled time**

### If It Fails
- Check console logs for "📋 Added missed dose to pending" messages
- Verify hot restart was done (not just hot reload)
- Check that reminders are enabled for the medication

---

## Test 2: Future Notification Scheduling

### Purpose
Verify that notifications fire at their scheduled time and add to pending doses.

### Steps
1. Note the current time (e.g., 2:30 PM)
2. Navigate to "Add Medication"
3. Fill in medication details:
   - Name: "Test Med 2"
   - Dosage: "5mg"
   - Enable reminders: ON
   - Times: Add 1 time that's 2 minutes in the future:
     - If current time is 2:30 PM, set time to 2:32 PM
4. Save the medication
5. Return to dashboard
6. **Wait 2 minutes** (keep app open or in background)

### Expected Results
✅ **After 2 minutes, notification should appear on device**
✅ **Notification should show "Time to take Test Med 2 - 5mg"**
✅ **Badge count should increase by 1**
✅ **Pending doses page should show the new dose**

### If It Fails
- Check Android notification permissions (Settings → Apps → MedMind → Notifications)
- For Android 13+, ensure exact alarm permission is granted
- Check console logs for "✅ Scheduled daily reminder" messages
- Try long-pressing the notification icon to access the test page

---

## Test 3: Notification Test Page (Quick Test)

### Purpose
Verify notifications work using the built-in test page.

### Steps
1. On dashboard, **long-press** the notification bell icon (top right)
2. This opens the Notification Test Page
3. Tap "Schedule Notification (30s)"
4. Wait 30 seconds

### Expected Results
✅ **After 30 seconds, notification should appear**
✅ **Notification should say "Test Reminder"**
✅ **Badge count should increase by 1**
✅ **Pending doses should show the test medication**

### Alternative Test Delays
- "Schedule Notification (10s)" - Quick test
- "Schedule Notification (1m)" - Longer test
- "Show Instant Notification" - Immediate test (no pending dose added)

---

## Test 4: Badge Count Updates

### Purpose
Verify that the badge count updates correctly when doses are marked as taken.

### Steps
1. Ensure you have pending doses (from Test 1 or 2)
2. Note the current badge count (e.g., "3")
3. Tap the notification icon to open Pending Doses page
4. Tap "Mark as Taken" on one of the doses
5. Return to dashboard

### Expected Results
✅ **Badge count should decrease by 1** (e.g., from "3" to "2")
✅ **Notification summary card should update** (e.g., "2 doses need to be taken")
✅ **Pending doses page should show one less dose**

---

## Test 5: Multiple Medications

### Purpose
Verify the system handles multiple medications correctly.

### Steps
1. Create 3 medications, each with 2 past times:
   - Med A: 1:00 AM, 2:00 AM
   - Med B: 3:00 AM, 4:00 AM
   - Med C: 5:00 AM, 6:00 AM
2. Return to dashboard

### Expected Results
✅ **Badge count should show "6"** (2 doses × 3 medications)
✅ **Pending doses page should list all 6 doses**
✅ **Doses should be sorted by time** (oldest first)
✅ **Each dose should show correct medication name**

---

## Test 6: Daily Recurring Notifications

### Purpose
Verify that notifications repeat daily.

### Steps
1. Create a medication with a time that's already passed today
2. Note that it appears in pending doses immediately
3. **The next day**, at the same time, a notification should fire
4. This will continue daily

### Expected Results
✅ **Notification fires at the same time every day**
✅ **Each day's dose is added to pending doses**
✅ **Badge count accumulates if doses aren't marked as taken**

### Note
This test requires waiting until the next day. You can verify the notification is scheduled by checking console logs for "✅ Scheduled daily reminder" messages.

---

## Test 7: Clear All Pending Doses

### Purpose
Verify you can clear pending doses.

### Steps
1. Ensure you have multiple pending doses
2. Navigate to Pending Doses page
3. Mark each dose as taken one by one
4. Return to dashboard

### Expected Results
✅ **Badge count decreases with each dose marked as taken**
✅ **When all doses are marked, badge disappears**
✅ **Notification summary shows "All caught up!"**

---

## Troubleshooting

### Notifications Not Appearing
1. **Check permissions**: Settings → Apps → MedMind → Notifications → Allow
2. **For Android 13+**: Settings → Apps → MedMind → Alarms & reminders → Allow
3. **Check Do Not Disturb**: Ensure DND is off or MedMind is allowed
4. **Hot restart**: Always hot restart after code changes, not just hot reload

### Badge Count Not Updating
1. **Pull down to refresh** on dashboard
2. **Navigate away and back** to dashboard
3. **Check console logs** for error messages
4. **Clear app data** and try again

### Pending Doses Not Showing
1. **Check SharedPreferences**: Pending doses are stored locally
2. **Check console logs** for "📋 Added missed dose" messages
3. **Verify medication has reminders enabled**
4. **Verify times are in the past**

### Console Log Messages to Look For
- `📍 Using timezone: [timezone]` - Timezone configured
- `✅ Scheduled daily reminder for [med] at [time]` - Notification scheduled
- `📋 Added missed dose to pending: [med] at [time]` - Missed dose detected
- `✅ Notification shown successfully` - Notification displayed

---

## Success Criteria

All tests should pass with these results:
- ✅ Missed doses appear immediately when medication is created
- ✅ Badge count updates correctly
- ✅ Pending doses page shows all pending doses
- ✅ Notifications fire at scheduled times
- ✅ Marking doses as taken updates the UI
- ✅ Multiple medications work correctly
- ✅ Daily recurring notifications work

If any test fails, check the troubleshooting section and console logs for error messages.
